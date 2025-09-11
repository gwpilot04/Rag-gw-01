import sys
from pathlib import Path
from langchain_core.documents import Document
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# เพิ่ม project root ลงใน Python path
project_root = Path(__file__).parent.parent.parent  
sys.path.insert(0, str(project_root))

from app.core.config import Settings
from app.models.schemas_v2 import RagAnswer,ComplianceResponse, StrOutputParserCustom, format_instructions 
from pprint import pprint
from scripts.prompt_v2 import prompt_product,query_product_excellent,query_product_good, query_product_fair, query_product_poor, query_product_very_poor,query_product_bad
load_dotenv()

settings = Settings()

if __name__ == "__main__":
    
    print(" Retrieving...")
    
    def format_docs(docs: list[Document]) -> str:
        return "\n\n".join(f"{d.page_content}\nSOURCE: {d.metadata.get('title','')}" for d in docs)
    

    retriever = settings.qdrant_vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 1, "fetch_k": 10, "lambda_mult": 0.5}
    )

    custom_prompt = ChatPromptTemplate.from_template(prompt_product)
   
    rag_chain = (
    {
        "question": lambda q: q['question'], 
        "answer": lambda q: q['answer'],
        "context": lambda q: format_docs(retriever.invoke(q['question'])), 
        "format_instructions": lambda _: format_instructions  
    }
    | custom_prompt             
    | settings.llm_azure
    | StrOutputParserCustom
    )

    def process_compliance_query(query_dict: dict) -> ComplianceResponse:
       
        try:

            result: RagAnswer = rag_chain.invoke(query_dict)
    
            return ComplianceResponse(
                summary=result.summary,
                # references=result.references,
                # compliance_points=result.compliance_points,
                compliance_score=result.compliance_score,
            )
            
        except Exception as e:

            return ComplianceResponse(
                summary="เกิดข้อผิดพลาดในการประมวลผล",
                # references="ไม่สามารถดึงข้อมูลได้",
                # compliance_points=[],
                compliance_score=0,
            )

    for query in [query_product_excellent,
                  query_product_good,
                  query_product_fair,
                  query_product_poor,
                  query_product_very_poor,
                  query_product_bad]:    
        response  = process_compliance_query(query)
        pprint(response.model_dump())

    # response  = process_compliance_query(query_product_v2)
    # pprint(response.model_dump())
    
