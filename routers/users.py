# routers/users.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/users",       # 路由前缀
    tags=["users"],        # 文档分类标签
)

# ===== 数据模型 =====
class User(BaseModel):
    id: int
    name: str
    email: str

# 模拟数据库
fake_users_db = [
    User(id=1, name="Alice", email="alice@example.com"),
    User(id=2, name="Bob", email="bob@example.com"),
]

# ===== 路由接口 =====
@router.get("/", response_model=List[User])
async def list_users():
    """获取所有用户"""
    return fake_users_db

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """根据 ID 获取用户"""
    for user in fake_users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/", response_model=User)
async def create_user(user: User):
    """创建新用户"""
    fake_users_db.append(user)
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """删除用户"""
    global fake_users_db
    fake_users_db = [u for u in fake_users_db if u.id != user_id]
    return {"message": f"User {user_id} deleted"}
