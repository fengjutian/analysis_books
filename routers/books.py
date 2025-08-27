from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services import books_services
from app.db import driver

router = APIRouter(
    prefix="/books",       # 路由前缀
    tags=["books"],        # 文档分类标签
)

class Book(BaseModel):
    id: int
    title: str
    author: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

# 创建一个全局的 BookService 实例，使用共享的neo4j驱动
book_service = books_services.BookService(driver)

@router.post("/", response_model=Book)
async def create_book(book: Book):
    """创建新书籍"""
    result = book_service.create_book(book.id, book.title, book.author)
    if result is None:
        raise HTTPException(status_code=400, detail="Book with this ID already exists")
    return result

@router.get("/", response_model=List[Book])
async def get_all_books():
    """获取所有书籍"""
    return book_service.get_all_books()

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int):
    """根据ID获取书籍"""
    result = book_service.get_book(book_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return result

@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: int, book: BookUpdate):
    """更新书籍信息"""
    result = book_service.update_book(book_id, book.title, book.author)
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return result

@router.delete("/{book_id}")
async def delete_book(book_id: int):
    """删除书籍"""
    result = book_service.delete_book(book_id)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"Book {book_id} deleted"}



