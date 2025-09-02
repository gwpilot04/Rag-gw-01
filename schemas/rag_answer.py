from typing import List
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class RagAnswer(BaseModel):
    summary: str = Field(..., description="สรุปย่อ 1-3 บรรทัด")
    references: str = Field(..., description="การอ้างอิง: บทย่อ/หัวข้อใน Context ที่คุณใช้ตรวจสอบ")
    compliance_points: List[str] = Field(..., description="ประเด็นสอดคล้อง: bullet สั้น")
    gaps_risks: List[str] = Field(..., description="ช่องว่าง/ความเสี่ยง: bullet สั้น")
    verdict: str = Field(..., description="คำวินิจฉัย: ผ่าน | ผ่านแบบมีเงื่อนไข | ไม่ผ่าน")
    compliance_score: int = Field(..., ge=0, le=100, description="คะแนนความสอดคล้อง 0-100")
    confidence_level: str = Field(..., description="ความเชื่อมั่น: ต่ำ | กลาง | สูง")

StrOutputParserCustom = PydanticOutputParser(pydantic_object=RagAnswer)
format_instructions = StrOutputParserCustom.get_format_instructions()