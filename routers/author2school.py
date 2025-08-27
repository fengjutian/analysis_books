from fastapi import APIRouter
from pydantic import BaseModel
from app.db import driver

router = APIRouter(
    prefix="/author2school",       # 路由前缀
    tags=["author2school"],        # 文档分类标签
)

# 请求体模型
class AuthorSchool(BaseModel):
    school_name: str
    author_name: str


@router.post("/create")
def create_author_school_relation(data: AuthorSchool):
    """创建 作者-学校 关系"""
    cypher = """
    MERGE (a:Author {name: $author_name})
    MERGE (s:School {name: $school_name})
    MERGE (a)-[:WRITTEN_BY]->(s)
    RETURN s.name AS school, a.name AS author  
    """
    with driver.session() as session:
        result = session.run(cypher, school_name=data.school_name, author_name=data.author_name)
        record = result.single()
    return {"school": record["school"], "author": record["author"]}


# @router.get("/author/{author_name}")
# def get_books_by_author(author_name: str):
#     """查询某作者的所有书籍"""
#     cypher = """
#     MATCH (a:Author {name: $author_name})<-[:WRITTEN_BY]-(b:Book)
#     RETURN a.name AS author, collect(b.title) AS books
#     """
#     with driver.session() as session:
#         result = session.run(cypher, author_name=author_name)
#         record = result.single()
#     if record:
#         return {"author": record["author"], "books": record["books"]}
#     return {"author": author_name, "books": []}
