from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def text_splitter(docs:list[Document]):
    try:

        # Step 2: Split
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=20,
            length_function=len,
            separators=["หมวดที่"]
            # is_separator_regex=True,
            # separators=["\n\n", "\n", " ", "\u200b", ""]
        )

        # ถ้าไฟล์ภาษาไทย (หรือไฟล์ที่ copy จาก PDF/เว็บข่าว) มี zero-width space แฝงอยู่ → ต้องเพิ่ม "\u200b" ลงใน separators ของ RecursiveCharacterTextSplitter 
        # เพื่อให้ split ได้ตรงย่อหน้าหรือคำจริง

        texts = text_splitter.create_documents([docs[0].page_content])
        # set metadata
        index = 0
        for text in texts:
            if ("หมวดที่" in text.page_content):
                line_metadata = text.page_content.split("\n")[0]
                line_metadata = line_metadata.replace(":", ",",1).split(",")
                texts[index].metadata = dict({
                    "section": line_metadata[0],
                    "category": line_metadata[1],
                })
            index += 1
        print(f"✅ Split into {len(texts)} chunks.")
        return texts
        # print("SSSSSSSSSSS ",texts[0])
        # print("AAAAAAAAAAAAA ",texts[1])
        # print("BBBBBBBBBBBBB ",texts[2])

    except Exception as e:
        print(f"Error during text splitting: {e}")
        return []

