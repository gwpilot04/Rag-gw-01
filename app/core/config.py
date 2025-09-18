from http import client
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import logging
from functools import lru_cache

load_dotenv()
logger = logging.getLogger(__name__)
class Settings:

        def __init__(self):
            #Validation
            self._validate_required_env_vars()

        def _validate_required_env_vars(self):
            """Validate required environment variables"""
            required_vars = [
                "QDRANT_HOST",
                "QDRANT_PORT",
                "DB_COLLECTION",
                "AZURE_OPENAI_API_KEY",
                "AZURE_OPENAI_ENDPOINT",
                "AZURE_OPENAI_DEPLOYMENT_NAME",
                "AZURE_OPENAI_API_VERSION",
                "AZURE_OPENAI_ENDPOINT_EMBEDDING",
                "AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING",
                "AZURE_OPENAI_API_VERSION_EMBEDDING"
            ]

            missing_vars = []

            # for var in required_vars:
            #     if not os.getenv(var):
            #         missing_vars.append(var)
                    
            # if missing_vars:
            #     raise ValueError(f"Missing required environment variables: {missing_vars}")

            missing_vars = [var for var in required_vars if not os.getenv(var)]
            if missing_vars:
                raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
        QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
        QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
        QDRANT_DOCKER : str = os.getenv("QDRANT_URL", "False")

        # Qdrant
        DB_COLLECTION: str = os.getenv("DB_COLLECTION", "demo_collection") 

        # Chat Azure OpenAI
        AZURE_OPENAI_API_KEY : str = os.getenv("AZURE_OPENAI_API_KEY")        
        AZURE_OPENAI_ENDPOINT : str = os.getenv("AZURE_OPENAI_ENDPOINT")
        AZURE_OPENAI_DEPLOYMENT_NAME : str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        AZURE_OPENAI_API_VERSION : str = os.getenv("AZURE_OPENAI_API_VERSION")

        # Embedding Azure OpenAI
        AZURE_OPENAI_ENDPOINT_EMBEDDING : str = os.getenv("AZURE_OPENAI_ENDPOINT_EMBEDDING")
        AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING : str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING")
        AZURE_OPENAI_API_VERSION_EMBEDDING : str = os.getenv("AZURE_OPENAI_API_VERSION_EMBEDDING")

        # Text Spliter
        CHUNK_SIZE : int = int(os.getenv("CHUNK_SIZE", "1000"))
        CHUNK_OVERLAP : int =  int(os.getenv("CHUNK_OVERLAP", "0"))

        # RETRIEVAL
        DEFAULT_TOP_K : int = int(os.getenv("DEFAULT_TOP_K", "4"))

        # Timeout settings
        REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
        MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))

        @property
        def client(self) -> QdrantClient:
            """Lazy loading สำหรับ Qdrant client"""
            if not hasattr(self, '_client'):
                try: 
                    if self.QDRANT_DOCKER:
                        self._client = QdrantClient(url = self.QDRANT_DOCKER)
                        logging.info("Connecting to Qdrant via Docker URL")
                    else:
                        self._client = QdrantClient(host=self.QDRANT_HOST, port=self.QDRANT_PORT)
                        logging.info(f"Connecting to Qdrant at {self.QDRANT_HOST}:{self.QDRANT_PORT}")
                        
                except Exception as e:
                    logging.error(f"Error connecting to Qdrant: {e}")
                    raise
            return self._client
        
        @property
        def llm_azure(self) -> AzureChatOpenAI:
            """Lazy loading สำหรับ LLM Azure"""
            if not hasattr(self, '_llm_azure'):
                try:
                    self._llm_azure = AzureChatOpenAI(
                        azure_endpoint=self.AZURE_OPENAI_ENDPOINT,
                        azure_deployment=self.AZURE_OPENAI_DEPLOYMENT_NAME,
                        openai_api_version=self.AZURE_OPENAI_API_VERSION,
                        model_kwargs={"response_format": {"type": "json_object"}}  
                    )
                    logging.info("AzureChatOpenAI initialized successfully")

                except Exception as e:
                    logging.error(f"Error initializing AzureChatOpenAI: {e}")
                    raise
            return self._llm_azure

        @property
        def embeddings(self) -> AzureOpenAIEmbeddings:
            """Lazy loading สำหรับ embeddings"""
            if not hasattr(self, '_embeddings'):
                try: 
                    self._embeddings = AzureOpenAIEmbeddings(
                        azure_endpoint=self.AZURE_OPENAI_ENDPOINT_EMBEDDING,
                        azure_deployment=self.AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING,
                        openai_api_version=self.AZURE_OPENAI_API_VERSION_EMBEDDING,
                    )
                    logging.info("AzureOpenAIEmbeddings initialized successfully")
                except Exception as e:
                    logging.error(f"Error initializing AzureOpenAIEmbeddings: {e}")
                    raise
            return self._embeddings
    
        @property
        def qdrant_vector_store(self) -> QdrantVectorStore:
            """Lazy loading สำหรับ vector store"""
            if not hasattr(self, '_vector_store'):
                try:

                    self._vector_store = QdrantVectorStore(
                        client=self.client,
                        collection_name=self.DB_COLLECTION,
                        embedding=self.embeddings,
                    )
                    logging.info("QdrantVectorStore initialized successfully")
                except Exception as e:
                    logging.error(f"Error initializing QdrantVectorStore: {e}")
                    raise
            return self._vector_store
        
        def health_check(self) -> dict:
            status = {}
            try:
                self.client.get_collections()
                status['qdrant'] = 'healthy'
            except Exception as e:
                status["qdrant"] = f'unhealthy: {e}'
            
            return status
        
@lru_cache()
def get_settings() -> Settings:
    return Settings()
