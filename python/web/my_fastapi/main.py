import hashlib
from datetime import datetime
from typing import List

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status

from models import User
from models import UserCreate
from models import UserResponse
from models import UserUpdate

app = FastAPI(
    title="用户管理API",
    description="基于FastAPI和Pydantic的用户CRUD操作演示",
    version="1.0.0"
)

# 内存存储（演示用）
users_db: List[User] = []
next_id = 1


def hash_password(password: str) -> str:
    """简单的密码哈希（仅演示用）"""
    return hashlib.sha256(password.encode()).hexdigest()


def find_user_by_id(user_id: int) -> User:
    """根据ID查找用户"""
    for user in users_db:
        if user.id == user_id:
            return user
    return None


def find_user_by_email(email: str) -> User:
    """根据邮箱查找用户"""
    for user in users_db:
        if user.email == email:
            return user
    return None


@app.get("/", summary="根路径")
async def root():
    """API根路径信息"""
    return {
        "message": "用户管理API",
        "version": "1.0.0",
        "endpoints": ["/users", "/users/{user_id}"]
    }


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="创建用户")
async def create_user(user_data: UserCreate):
    """创建新用户"""
    global next_id
    
    # 检查邮箱是否已存在
    if find_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已存在"
        )
    
    # 创建新用户
    now = datetime.now()
    new_user = User(
        id=next_id,
        name=user_data.name,
        email=user_data.email,
        age=user_data.age,
        password_hash=hash_password(user_data.password),
        created_at=now,
        updated_at=now
    )
    
    users_db.append(new_user)
    next_id += 1
    
    # 返回用户响应
    return UserResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        age=new_user.age,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at
    )


@app.get("/users", response_model=List[UserResponse], summary="获取所有用户")
async def get_users():
    """获取所有用户列表"""
    return [
        UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            age=user.age,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        for user in users_db
    ]


@app.get("/users/{user_id}", response_model=UserResponse, summary="获取指定用户")
async def get_user(user_id: int):
    """根据ID获取用户信息"""
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        age=user.age,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@app.put("/users/{user_id}", response_model=UserResponse, summary="更新用户")
async def update_user(user_id: int, user_data: UserUpdate):
    """更新用户信息"""
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 检查邮箱是否被其他用户占用
    if user_data.email:
        existing_user = find_user_by_email(user_data.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被其他用户使用"
            )
    
    # 更新用户信息
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.age is not None:
        user.age = user_data.age
    
    user.updated_at = datetime.now()
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        age=user.age,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@app.delete("/users/{user_id}", summary="删除用户")
async def delete_user(user_id: int):
    """删除指定用户"""
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    users_db.remove(user)
    return {"message": f"用户 {user.name} 已删除"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
