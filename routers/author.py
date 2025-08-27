from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services import author_services
from app.db import driver

router = APIRouter(
    prefix="/authors",       # 路由前缀
    tags=["authors"],        # 文档分类标签
)

class AuthorBase(BaseModel):
    name: str
    email: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True

fake_authors_db = [
    Author(id=1, name="Alice", email="alice@example.com"),
    Author(id=2, name="Bob", email="bob@example.com"),
]

@router.get("/", response_model=List[Author])
async def list_authors():
    """获取所有作者"""
    services = author_services.AuthorService(driver)
    authors = services.get_all_authors()
    # 转换用户数据为作者数据
    result = []
    for item in authors:
        result.append({
            "id": item["id"],
            "name": item["name"],
            "email": item["email"]
        })
    return result

@router.get("/{author_id}", response_model=Author)
async def get_author(author_id: int):
    """根据 ID 获取作者"""
    services = author_services.AuthorService(driver)
    author_node = services.get_author(str(author_id))  # 使用用户服务获取数据
    if not author_node:
        raise HTTPException(status_code=404, detail="Author not found")
    
    # Convert Neo4j node to Author model format
    author_dict = {
        "id": int(author_node["user_id"]),
        "name": author_node["name"],
        "email": f"{author_node['name'].lower()}@example.com"
    }
    return author_dict

@router.post("/", response_model=Author)
async def create_author(author: AuthorCreate):
    """创建新作者，author_id将自动生成"""
    services = author_services.AuthorService(driver)
    author_node = services.create_author(author.name, 30)  # 使用用户服务创建数据
    
    # Convert Neo4j node to Author model format
    author_dict = {
        "id": int(author_node["author_id"]),
        "name": author_node["name"],
        "email": author.email  # Keep the provided email
    }
    return author_dict

@router.delete("/{author_id}")
async def delete_author(author_id: int):
    """删除作者"""
    services = author_services.AuthorService(driver)
    deleted = services.delete_author(str(author_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"message": f"Author {author_id} deleted"}
