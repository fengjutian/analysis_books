from fastapi import APIRouter
from pydantic import BaseModel
from app.db import driver

router = APIRouter(
    prefix="/book2author",       # 路由前缀
    tags=["book2author"],        # 文档分类标签
)

# 请求体模型
class BookAuthor(BaseModel):
    book_title: str
    author_name: str


@router.post("/create")
def create_book_author_relation(data: BookAuthor):
    """创建 书籍-作者 关系"""
    cypher = """
    MERGE (b:Book {title: $book_title})
    MERGE (a:Author {name: $author_name})
    MERGE (b)-[:WRITTEN_BY]->(a)
    RETURN b.title AS book, a.name AS author
    """
    with driver.session() as session:
        result = session.run(cypher, book_title=data.book_title, author_name=data.author_name)
        record = result.single()
    return {"book": record["book"], "author": record["author"]}


@router.get("/author/{author_name}")
def get_books_by_author(author_name: str):
    """查询某作者的所有书籍"""
    cypher = """
    MATCH (a:Author {name: $author_name})<-[:WRITTEN_BY]-(b:Book)
    RETURN a.name AS author, collect(b.title) AS books
    """
    with driver.session() as session:
        result = session.run(cypher, author_name=author_name)
        record = result.single()
    if record:
        return {"author": record["author"], "books": record["books"]}
    return {"author": author_name, "books": []}
