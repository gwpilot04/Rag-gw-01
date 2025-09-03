import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import  AzureOpenAIEmbeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, SparseVectorParams, VectorParams

load_dotenv()

def document_loader():
    try:
        # loader = TextLoader("./documents/Executive_Governance_90.txt", encoding="utf-8")
        # Step 1: Load
        # ทำ .txt ไปก่อน pdf ค่อยว่ากัน
        loader = PyPDFLoader("./documents/กฎหมายลิทธิ์.pdf")
        docs = loader.load()
        return docs
        # print(f"Loaded {len(docs)} documents.")

        # print(docs[0].metadata)
        # print(docs[0].page_content[:1000])  # แสดงเนื้อหา

        # print(docs[0].page_content[:150])   # preview เนื้อหา
        # print(docs[0].metadata)            # ข้อมูลกำกับ เช่น path 
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return []