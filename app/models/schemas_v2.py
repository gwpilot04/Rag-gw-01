from typing import List
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class RagAnswer(BaseModel):
    summary: str = Field(..., description="สรุปย่อ 1-3 บรรทัด")
    # references: str = Field(..., description="การอ้างอิง: บทย่อ/หัวข้อใน Context ที่คุณใช้ตรวจสอบ")
    # compliance_points: List[str] = Field(..., description="ประเด็นสอดคล้อง: bullet สั้น")
    compliance_score: int = Field(..., ge=0, le=10, description="คะแนนความสอดคล้อง 0-10")

class ComplianceResponse(BaseModel):

    """Response model สำหรับ Executive Compliance Review API"""

    summary: str = Field(..., description="สรุปย่อ 1-3 บรรทัด", example="องค์กรมีการจัดทำ CSR Project เพื่อสังคมและชุมชนตามข้อ 76")
    #references: str = Field(..., description="การอ้างอิง: บทย่อ/หัวข้อใน Context", example="หมวดที่ 9: การสื่อสารและความสัมพันธ์กับผู้มีส่วนได้เสีย (ข้อ 76)")
    #compliance_points: List[str] = Field(..., description="ประเด็นสอดคล้อง", example=["มีการจัดทำ CSR Project", "ครอบคลุมด้านสังคมและชุมชน"])
    compliance_score: int = Field(..., ge=0, le=10, description="คะแนนความสอดคล้อง", example=10)

    class Config:
        json_schema_extra = {
            "example": {
                "summary": "องค์กรมีการจัดทำ CSR Project เพื่อสังคมและชุมชนตามข้อกำหนด",
                "references": "หมวดที่ 9: การสื่อสารและความสัมพันธ์กับผู้มีส่วนได้เสีย (ข้อ 76)",
                "compliance_points": [
                    "มีการจัดทำ CSR Project",
                    "ครอบคลุมด้านสังคมและชุมชน",
                    "มี Gender Equality Policy"
                ],
                "verdict": "ผ่านแบบมีเงื่อนไข",
                "compliance_score": 10,
            }
        }

class ComplianceRequest(BaseModel):
    """Request model สำหรับ Executive Compliance Review API"""
    
    query: str = Field(..., description="คำถามเกี่ยวกับการตรวจสอบการปฏิบัติตามกฎหมาย", 
                      example="องค์กรมีการจัดทำ CSR Project เพื่อสังคมและชุมชนหรือไม่")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "องค์กรมีการจัดทำ CSR Project เพื่อสังคมและชุมชนหรือไม่"
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    
    error: str = Field(..., description="รายละเอียดข้อผิดพลาด")
    message: str = Field(..., description="ข้อความแสดงข้อผิดพลาด")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "PROCESSING_ERROR",
                "message": "ไม่สามารถประมวลผลคำขอได้ กรุณาลองใหม่อีกครั้ง"
            }
        }


StrOutputParserCustom = PydanticOutputParser(pydantic_object=RagAnswer)
format_instructions = StrOutputParserCustom.get_format_instructions()
