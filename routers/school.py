from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services import school_services
from app.db import driver

router = APIRouter(
    prefix="/schools",       # 路由前缀
    tags=["schools"],        # 文档分类标签
)

class School(BaseModel):
    title: str
    author: str

class SchoolResponse(School):
    id: int
    
    class Config:
        from_attributes = True

class SchoolUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

# 创建一个全局的 SchoolService 实例，使用共享的neo4j驱动
school_service = school_services.SchoolService(driver)

@router.post("/", response_model=SchoolResponse)
async def create_school(school: School):
    """创建新学校，自动生成唯一ID"""
    result = school_service.create_school(school.title, school.author)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to create school")
    return result

@router.get("/", response_model=List[SchoolResponse])
async def get_all_schools():
    """获取所有学校"""
    return school_service.get_all_schools()

@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(school_id: int):
    """根据ID获取学校"""
    result = school_service.get_school(school_id)
    if result is None:
        raise HTTPException(status_code=404, detail="School not found")
    return result

@router.put("/{school_id}", response_model=SchoolResponse)
async def update_school(school_id: int, school: SchoolUpdate):
    """更新学校信息"""
    result = school_service.update_school(school_id, school.title, school.author)
    if result is None:
        raise HTTPException(status_code=404, detail="School not found")
    return result

@router.delete("/{school_id}")
async def delete_school(school_id: int):
    """删除学校"""
    result = school_service.delete_school(school_id)
    if not result:
        raise HTTPException(status_code=404, detail="School not found")
    return {"message": f"School {school_id} deleted"}