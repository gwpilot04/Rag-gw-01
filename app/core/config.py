from http import client
import os
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


class Settings:

        QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
        QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
        QDRANT_DOCKER : str = os.getenv("QDRANT_URL", "False")

        # Qdrant
        DB_COLLECTION: str = os.getenv("DB_COLLECTION", "demo_collection") 

        # Chat Azure OpenAI
        AZURE_OPENAI_API_KEY : str = os.environ["AZURE_OPENAI_API_KEY"]        
        AZURE_OPENAI_ENDPOINT : str = os.environ["AZURE_OPENAI_ENDPOINT"]
        AZURE_OPENAI_DEPLOYMENT_NAME : str = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
        AZURE_OPENAI_API_VERSION : str = os.environ["AZURE_OPENAI_API_VERSION"]

        # Embedding Azure OpenAI
        AZURE_OPENAI_ENDPOINT_EMBEDDING : str = os.environ["AZURE_OPENAI_ENDPOINT_EMBEDDING"]
        AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING : str = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING"]
        AZURE_OPENAI_API_VERSION_EMBEDDING : str = os.environ["AZURE_OPENAI_API_VERSION_EMBEDDING"]

        # Text Spliter
        CHUNK_SIZE : int = 1000
        CHUNK_OVERLAP : int = 0

        # RETRIEVAL
        DEFAULT_TOP_K : int = 4

        @property
        def client(self) -> QdrantClient:
            """Lazy loading สำหรับ Qdrant client"""
            if not hasattr(self, '_client'):
                self._client = QdrantClient(host=self.QDRANT_HOST, port=self.QDRANT_PORT)
                # self._client = QdrantClient(url= self.QDRANT_URL)  # ถ้าใช้ Docker
            return self._client
        
        @property
        def llm_azure(self) -> AzureChatOpenAI:
            """Lazy loading สำหรับ LLM Azure"""
            if not hasattr(self, '_llm_azure'):
                self._llm_azure = AzureChatOpenAI(
                    azure_endpoint=self.AZURE_OPENAI_ENDPOINT,
                    azure_deployment=self.AZURE_OPENAI_DEPLOYMENT_NAME,
                    openai_api_version=self.AZURE_OPENAI_API_VERSION,
                    model_kwargs={"response_format": {"type": "json_object"}}  
                )
            return self._llm_azure

        @property
        def embeddings(self) -> AzureOpenAIEmbeddings:
            """Lazy loading สำหรับ embeddings"""
            if not hasattr(self, '_embeddings'):
                self._embeddings = AzureOpenAIEmbeddings(
                    azure_endpoint=self.AZURE_OPENAI_ENDPOINT_EMBEDDING,
                    azure_deployment=self.AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING,
                    openai_api_version=self.AZURE_OPENAI_API_VERSION_EMBEDDING,
                )
            return self._embeddings
    
        @property
        def qdrant_vector_store(self) -> QdrantVectorStore:
            """Lazy loading สำหรับ vector store"""
            if not hasattr(self, '_vector_store'):
                self._vector_store = QdrantVectorStore(
                    client=self.client,
                    collection_name=self.DB_COLLECTION,
                    embedding=self.embeddings,
                )
            return self._vector_store
        

def get_settings() -> Settings:
    return Settings()
