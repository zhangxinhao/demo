from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class UserBase(BaseModel):
    """用户基础信息"""
    name: str = Field(..., description="用户姓名")
    email: str = Field(..., description="用户邮箱")
    age: Optional[int] = Field(None, description="用户年龄")


class UserCreate(UserBase):
    """创建用户时的数据结构"""
    password: str = Field(..., description="用户密码")


class UserUpdate(BaseModel):
    """更新用户时的数据结构"""
    name: Optional[str] = Field(None, description="用户姓名")
    email: Optional[str] = Field(None, description="用户邮箱")
    age: Optional[int] = Field(None, description="用户年龄")


class UserResponse(UserBase):
    """用户响应数据结构"""
    id: int = Field(..., description="用户ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class User(UserBase):
    """用户完整数据结构（内部使用）"""
    id: int
    password_hash: str
    created_at: datetime
    updated_at: datetime
