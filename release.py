import os
from typing import List
from langchain_core.documents import Document
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from schemas.rag_answer import RagAnswer, StrOutputParserCustom, format_instructions
from schemas.response import ComplianceResponse
from pprint import pprint
from prompt import prompt, query_hight, query_mid, query_low, query_wtf

load_dotenv()

client = QdrantClient(host="localhost", port=6333)

if __name__ == "__main__":
    
    print(" Retrieving...")
    
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT_EMBEDDING"], 
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING"],
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION_EMBEDDING"],
    )

    llm_azure = AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        model_kwargs={"response_format": {"type": "json_object"}}  
    )

    vector_store = QdrantVectorStore(
        client=client,
        collection_name="demo_collection",
        embedding=embeddings,
    )

    def format_docs(docs: List[Document]) -> str:
        # return "\n\n".join(doc.page_content for doc in docs)
        
        # ถ้ามี metadata
        return "\n\n".join(f"{d.page_content}\nSOURCE: {d.metadata.get('source','')}" for d in docs)

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.5}
    )

    custom = ChatPromptTemplate.from_template(prompt)
   
    rag_chain = (
    {
        "context": retriever | RunnableLambda(format_docs),
        "input": RunnablePassthrough(), #  ใน chain คาดหวังให้ส่ง input เป็น string โดยตรง
        "format_instructions": lambda _: format_instructions  
    }
    | custom             
    | llm_azure
    | StrOutputParserCustom
    )

    def process_compliance_query(query: str) -> ComplianceResponse:
        """ฟังก์ชันสำหรับประมวลผล compliance query"""
        try:

            result: RagAnswer = rag_chain.invoke(query)
      
            # แปลง RagAnswer เป็น ComplianceResponse
            return ComplianceResponse(
                summary=result.summary,
                references=result.references,
                compliance_points=result.compliance_points,
                gaps_risks=result.gaps_risks,
                verdict=result.verdict,
                compliance_score=result.compliance_score,
                confidence_level=result.confidence_level
            )
            
        except Exception as e:
            # Return error response
            return ComplianceResponse(
                summary="เกิดข้อผิดพลาดในการประมวลผล",
                references="ไม่สามารถดึงข้อมูลได้",
                compliance_points=[],
                gaps_risks=["ระบบประมวลผลล้มเหลว"],
                verdict="ไม่สามารถประเมินได้",
                compliance_score=0,
                confidence_level="ต่ำ"
            )

    for query in [query_hight,query_mid,query_low,query_wtf]:
        print("\n\n========================\n")
        response = process_compliance_query(query)
        # print("Response Model:", response)
        pprint(response.model_dump()) 