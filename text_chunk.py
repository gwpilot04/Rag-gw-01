from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from document_loader import document_loader
from langchain.chains import retrieval_qa
from embeding import add_text_to_qdrant
import re

def get_title_from_text(texts_chunk:str):
    titles = []
    for text in texts_chunk.split("\n"):
        if (re.findall(r"(?m)^\d+(\.\d+)+\s(?!\)).*", text)):
            titles.append(text)
    return titles

def text_splitter(docs:list[Document]):
    try:

        # Step 2: Split
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,        # ปรับตามขนาด context ที่ต้องการ
            chunk_overlap=200,      # ช่วยให้ context เชื่อมกัน
            add_start_index=True,   # ถ้าต้องการติดตามตำแหน่งในเอกสารดั้งเดิม
            separators=[r"^\d+(\.\d+)+\s(?!\)).*","\n", " ", ""]
        )
 
        # ถ้าไฟล์ภาษาไทย (หรือไฟล์ที่ copy จาก PDF/เว็บข่าว) มี zero-width space แฝงอยู่ → ต้องเพิ่ม "\u200b" ลงใน separators ของ RecursiveCharacterTextSplitter 
        # เพื่อให้ split ได้ตรงย่อหน้าหรือคำจริง
        doc_texts = text_splitter.create_documents([doc.page_content for doc in docs], [doc.metadata for doc in docs])
        # set metadata
        index = 0
        pattern =  r"(?m)^\d+(\.\d+)+\s(?!\)).*"
        titles_befor = []
        for text in doc_texts:
            if re.findall(pattern, text.page_content):
                title_paragraph_chunk = get_title_from_text(text.page_content)
                titles_befor = title_paragraph_chunk
                doc_texts[index].metadata.update({"title_paragraph": title_paragraph_chunk})
            elif len(titles_befor) > 0:
                doc_texts[index].metadata.update({"title_paragraph" : [titles_befor[len(titles_befor) -1]]})
            index += 1
        return doc_texts

    except Exception as e:
        print(f"Error during text splitting: {e}")
        return []

texts = document_loader()
texts = text_splitter(texts)
add_text_to_qdrant(texts)