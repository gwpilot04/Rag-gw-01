import os
from langchain_openai import AzureOpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from connect_db import connect_qdrant
from langchain_core.documents import Document



def add_text_to_qdrant(texts:list[Document]):
    client = connect_qdrant()
    
    if client is None:
        print("Cannot add texts: Qdrant client is not connected.")
        
    try:
        # STEP 3 Add texts to the  + Embeddings + VectorStore

        embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT_EMBEDDING"], 
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION_EMBEDDING"],
        )

        vector_store = QdrantVectorStore(
            client=client,
            collection_name="demo_collection",
            embedding=embeddings,
        )

        vector_store.add_texts(
            [t.page_content for t in texts],   # list ของข้อความ
            [t.metadata for t in texts]        # list ของ metadata
        )
        print(f"✅ เพิ่ม {len(texts)} chunks ลง collection เรียบร้อย")
        return True

    except Exception as e:
        print(f"❌ Failed to add texts to the collection: {e}")
        return False

def search_documents(query):
    try:
        client = connect_qdrant()
        if client is None:
            return []
            
        embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT_EMBEDDING"], 
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION_EMBEDDING"],
        )

        vector_store = QdrantVectorStore(
            client=client,
            collection_name="demo_collection",
            embedding=embeddings,
        )
            
        found_docs = vector_store.similarity_search(query, k=3)
        # print(f"✅ พบเอกสารที่เกี่ยวข้อง {len(found_docs)} ฉบับ")
        
        # # แสดงผลลัพธ์
        # for i, doc in enumerate(found_docs):
        #     print(f"\n--- เอกสารที่ {i+1} ---")
        #     print(doc.page_content[:200] + "...")
            
        return found_docs

    except Exception as e:
        print(f"❌ Similarity search failed: {e}")
        return []
