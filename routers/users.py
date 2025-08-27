from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services import users_services
from app.db import driver

router = APIRouter(
    prefix="/users",       # 路由前缀
    tags=["users"],        # 文档分类标签
)

class User(BaseModel):
    id: int
    name: str
    email: str

fake_users_db = [
    User(id=1, name="Alice", email="alice@example.com"),
    User(id=2, name="Bob", email="bob@example.com"),
]

@router.get("/", response_model=List[User])
async def list_users():
    """获取所有用户"""
    services = users_services.UserService(driver)
    users = services.get_all_users()
    return users

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """根据 ID 获取用户"""
    services = users_services.UserService(driver)
    user_node = services.get_user(str(user_id))  # Convert to string for the service which expects string IDs
    if not user_node:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Convert Neo4j node to User model format
    user_dict = {
        "id": int(user_node["user_id"]),
        "name": user_node["name"],
        "email": f"{user_node['name'].lower()}@example.com"
    }
    return user_dict

@router.post("/", response_model=User)
async def create_user(user: User):
    """创建新用户"""
    services = users_services.UserService(driver)
    user_node = services.create_user(str(user.id), user.name, 30)
    
    # Convert Neo4j node to User model format
    user_dict = {
        "id": int(user_node["user_id"]),
        "name": user_node["name"],
        "email": user.email  # Keep the provided email
    }
    return user_dict

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """删除用户"""
    services = users_services.UserService(driver)
    deleted = services.delete_user(str(user_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {user_id} deleted"}
