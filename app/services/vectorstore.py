from ast import List
from app.core.config import get_settings
from langchain_core.documents import Document
from qdrant_client.http.models import Distance, VectorParams

settings = get_settings()

class VectorStore:

    def create_collection() -> bool:

        try:
            
            client = settings.client
            embeddings = settings.embeddings
            
            if client is None:
                return False
            
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

    def connect() -> bool:

        """ทดสอบการเชื่อมต่อ Qdrant"""
        try:

            # ทดสอบการเชื่อมต่อ
            collections = settings.client.get_collections()
            print(f"✅ Connected to Qdrant. Collections: {len(collections.collections)}")
            return True
        
        except Exception as e:
            print(f"❌ Cannot connect to Qdrant: {e}")
            return False

    def add_text_to_qdrant(texts:list[Document]):
        
        if settings.client is None:
            print("Cannot add texts: Qdrant client is not connected.")
    
        try:

            settings.qdrant_vector_store.add_texts(
                texts = [t.page_content for t in texts],   # list ของข้อความ
                metadatas = [t.metadata for t in texts]    # list ของ metadata
            )

            print(f"✅ เพิ่ม {len(texts)} chunks ลง collection เรียบร้อย")
            return True

        except Exception as e:
            print(f"❌ Failed to add texts to the collection: {e}")
            return False

    def search_documents(query : str) -> List[Document]:

        try:

            k = settings.DEFAULT_TOP_K

            if settings.client is None:
                return []
                
            found_docs = settings.vector_store.similarity_search(query, k=k)
        
            return found_docs

        except Exception as e:
            print(f"❌ Similarity search failed: {e}")
            return []