from app.core.config import Settings
from app.services.chunk_text import ChunkText
from app.services.loader_document import DocumentLoader
from app.services.vectorstore import VectorStore


if __name__ == "__main__":
   
   # create collection if not exists
    settings = Settings()

    if not settings.client.get_collection(collection_name=settings.DB_COLLECTION):
        settings.client.recreate_collection(
            collection_name=settings.DB_COLLECTION,
            vectors_config={
                "size": 1536,  
                "distance": "Cosine"  
            }
        )
        print(f"Collection '{settings.DB_COLLECTION}' created.")

    file_path = "../documents/กฎหมายลิทธิ์.pdf"
    loader = DocumentLoader(file_path=file_path)
    docs = loader.load_pdf()
    print(f"Loaded {len(docs)} documents.")

    texts = ChunkText.text_splitter(docs)
    print(f"Split into {len(texts)} chunks.")

    texts = VectorStore.add_text_to_qdrant(texts)
    print("Ingestion complete.")