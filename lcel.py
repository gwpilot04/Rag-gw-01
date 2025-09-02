import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


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
    )

    # query = """องค์กรได้กำหนดวิสัยทัศน์และพันธกิจที่ชัดเจน  
    #      มีการวางแผนเชิงกลยุทธ์โดยใช้ตัวชี้วัดหลายมิติ ทั้งด้านการเงิน ลูกค้า และกระบวนการภายใน  
    #      นอกจากนี้ยังมีการกำหนดเป้าหมายและผลลัพธ์ที่วัดได้เป็นรอบ ๆ เพื่อขับเคลื่อนองค์กร  
    #      ด้านเทคโนโลยีได้วางแผนปรับตัวสู่ดิจิทัลอย่างเป็นระบบ  
    #      ส่วนเรื่องสิ่งแวดล้อมและความยั่งยืน องค์กรมีนโยบายที่ชัดเจน รวมทั้งรายงานรอยเท้าคาร์บอนเป็นประจำ  
    #      ในด้านบุคลากร มีการจัดอบรมพัฒนาอย่างต่อเนื่อง และมีการเตรียมคนสืบทอดตำแหน่งสำคัญ  
    #      """
    query = """แมวสีเทาแง่มๆ
         """
    chain = PromptTemplate.from_template(template=query) | llm_azure
    # result = chain.invoke(input={})
    # print(result.content)

    vector_store = QdrantVectorStore(
        client=client,
        collection_name="demo_collection",
        embedding=embeddings,
    )

    # retrieval QA chat prompt = สถาปัตยกรรม RAG
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    combine_docs_chain = create_stuff_documents_chain(llm_azure, retrieval_qa_chat_prompt)

    retrival_chain = create_retrieval_chain(
        retriever = vector_store.as_retriever(), combine_docs_chain=combine_docs_chain
    )

    result = retrival_chain.invoke(input={"input": query})

    print(result['answer'])
