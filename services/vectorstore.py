import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, SparseVectorParams, VectorParams

load_dotenv()

def connect_qdrant():
    try:
        # use localhost .exe
        client = QdrantClient(host="localhost", port=6333)
        # if use docker run -p 6333:6333 -p 6334:6334
        # client = QdrantClient(url="http://localhost:6333")
        return client
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        return None

def create_collection():
    try:
        client = connect_qdrant()
        if client is None:
            return False
        
        embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT_EMBEDDING"], 
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION_EMBEDDING"],
        )
        vector_size = len(embeddings.embed_query("sample text"))
        print(f"Vector size: {vector_size}")

        client.create_collection(
            collection_name="demo_collection",
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            timeout=60
        )

        print("✅ สร้าง collection ใหม่แล้ว")
        return True

    except Exception as e:
        print(f"❌ ไม่สามารถสร้าง collection: {e}")
        return False
