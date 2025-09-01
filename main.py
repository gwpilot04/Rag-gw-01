import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_openai import AzureChatOpenAI
import getpass
from embeding import search_documents

load_dotenv()

if not os.environ.get("AZURE_OPENAI_API_KEY"):
  os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass("Enter API key for Azure: ")

llm_azure = AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    )

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        คุณคือผู้บริหารระดับสูงด้านกำกับดูแล (Executive Compliance Reviewer)
        มีหน้าที่ตรวจสอบความถูกต้องของข้อมูล นโยบาย กระบวนการ และเอกสาร
        โดยอ้างอิงจากข้อมูลใน Context เท่านั้น

        ข้อกำหนดสำคัญ:
        - ตอบโดยยึดเฉพาะข้อมูลใน Context; ห้ามใช้ความรู้ภายนอกหรือ suy đoán
        - ถ้าคำถาม/ประเด็นอยู่นอกเหนือ Context ให้ตอบว่า "ไม่มีข้อมูลนี้ในฐานความรู้"
        - ถ้า Context พูดถึงคนละเรื่องกับคำถาม ให้ตอบว่า "ไม่มีข้อมูลนี้ในฐานความรู้"
        - เลือกตอบเฉพาะส่วนใน Context ที่เกี่ยวข้องกับคำถาม
        - ชี้ให้เห็นความไม่สอดคล้อง/ขัดแย้งกันภายใน Context หากมี

        งานของคุณ:
        1) ตรวจสอบ “ความสอดคล้อง” กับกรอบบริหารและกฎหมายจาก Context (เช่น Governance, Strategy, HR, Finance, IT/Data, Risk & Audit, ESG, Stakeholder)
        2) ระบุ “ประเด็นเสี่ยง” และ “ช่องว่าง” (gaps) ที่พบ พร้อมอ้างอิงบรรทัด/หัวข้อจาก Context
        3) ให้ “คำวินิจฉัย” แบบสั้น (ผ่าน/ผ่านแบบมีเงื่อนไข/ไม่ผ่าน)
        4) ให้ “คะแนนความสอดคล้อง” 0–100 และ “ความเชื่อมั่น” ต่ำ/กลาง/สูง
        5) ถ้าไม่มีหลักฐานใน Context ให้ตอบสั้น ๆ ว่า "ไม่มีข้อมูลนี้ในฐานความรู้"

        รูปแบบคำตอบ (บังคับ):
        - สรุปย่อ: <1–3 บรรทัด>
        - การอ้างอิง: <บทย่อ/หัวข้อใน Context ที่คุณใช้ตรวจสอบ>
        - ประเด็นสอดคล้อง: <bullet สั้น>
        - ช่องว่าง/ความเสี่ยง: <bullet สั้น>
        - คำวินิจฉัย: <ผ่าน | ผ่านแบบมีเงื่อนไข | ไม่ผ่าน>
        - คะแนนความสอดคล้อง: <0–100>
        - ความเชื่อมั่น: <ต่ำ | กลาง | สูง>

    Context:
    {context}
        """),
        ("human", "{question}")
    ])

def Agent_help():

    chain = prompt | llm_azure 

    def Agent_think(question):
        try:
            print("🔍 กำลังค้นหาเอกสารที่เกี่ยวข้อง...")

            found_docs = search_documents(question)
            if not found_docs:
                return "❌ ไม่พบเอกสารที่เกี่ยวข้อง"
            
            # รวมเอกสารเป็น context

            context = "\n\n".join([
                f"เอกสารที่ {i+1}:\n{doc.page_content}" 
                for i, doc in enumerate(found_docs)
            ])

            print("🤖 กำลังวิเคราะห์และประเมิน...")
            
            response = chain.invoke({
                "context": context,
                "question": question
            })
            
            return response.content
        except Exception as e:
            return f"❌ เกิดข้อผิดพลาด: {e}"
    
    return Agent_think

my_agent = Agent_help()

if __name__ == "__main__":
   
    print("\n=== ถูกต้องของข้อมูล นโยบาย กระบวนการ และเอกสาร ===")
    print("พิมพ์ 'q' เพื่อออก\n")
    
    question_score_full = """องค์กรได้กำหนดวิสัยทัศน์และพันธกิจที่ชัดเจน  
        มีการวางแผนเชิงกลยุทธ์โดยใช้ตัวชี้วัดหลายมิติ ทั้งด้านการเงิน ลูกค้า และกระบวนการภายใน  
        นอกจากนี้ยังมีการกำหนดเป้าหมายและผลลัพธ์ที่วัดได้เป็นรอบ ๆ เพื่อขับเคลื่อนองค์กร  
        ด้านเทคโนโลยีได้วางแผนปรับตัวสู่ดิจิทัลอย่างเป็นระบบ  
        ส่วนเรื่องสิ่งแวดล้อมและความยั่งยืน องค์กรมีนโยบายที่ชัดเจน รวมทั้งรายงานรอยเท้าคาร์บอนเป็นประจำ  
        ในด้านบุคลากร มีการจัดอบรมพัฒนาอย่างต่อเนื่อง และมีการเตรียมคนสืบทอดตำแหน่งสำคัญ  
        """
    question_score_middle = """แผนกลยุทธ์ขององค์กรนี้คือจะเน้นขยายตลาดออนไลน์  
        แต่ไม่ได้กล่าวถึง Balanced Scorecard หรือ OKR  
        และไม่มีแผน ESG หรือเรื่องความยั่งยืน  
        แต่มีการพูดถึงการจ้างงานและการฝึกอบรมพนักงาน  
        """

    question_score_low = """องค์กรจะเน้นขายสินค้าแฟชั่นออนไลน์  
        โดยมุ่งหวังกำไรสูงสุด  
        ไม่ได้อ้างอิงแผนกลยุทธ์ใด ๆ  
        ไม่พูดถึงการบริหารบุคคล กฎหมาย หรือ ESG  
        """
    for question in [question_score_full, question_score_middle, question_score_low]:
        print(f"🤔 ถามเกี่ยวกับถูกต้องของข้อมูล นโยบาย กระบวนการ และเอกสาร:\n{question}\n")
                
        if question.strip():
            answer = my_agent(question)
            print(f"\n📋 **การประเมินผล:**\n{answer}\n")
            print("-" * 80)
        else:
            print("❗ กรุณาใส่คำถาม\n")

            
    # while True:
    #     question = input("🤔 ถามเกี่ยวกับถูกต้องของข้อมูล นโยบาย กระบวนการ และเอกสาร: ")

    #     if question_score_full.lower() == 'q':
    #         print("👋 ลาก่อน!")
    #         break
            
    #     if question_score_full.strip():
    #         # ใช้ agent เพื่อตอบคำถาม
    #         answer = my_agent(question_score_full)
    #         print(f"\n📋 **การประเมินผล:**\n{answer}\n")
    #         print("-" * 80)
    #     else:
    #         print("❗ กรุณาใส่คำถาม\n")

        