# -*- coding: utf-8 -*-
"""
HackMD API 数据模型定义
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ReadPermission(str, Enum):
    """读取权限"""
    OWNER = "owner"
    SIGNED_IN = "signed_in"
    GUEST = "guest"


class WritePermission(str, Enum):
    """写入权限"""
    OWNER = "owner"
    SIGNED_IN = "signed_in"
    GUEST = "guest"


class CommentPermission(str, Enum):
    """评论权限"""
    DISABLED = "disabled"
    FORBIDDEN = "forbidden"
    OWNERS = "owners"
    SIGNED_IN_USERS = "signed_in_users"
    EVERYONE = "everyone"


@dataclass
class Team:
    """团队信息"""
    id: str
    owner_id: str
    path: str
    name: str
    logo: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[str] = None
    created_at: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Team":
        """从字典创建Team对象"""
        return cls(
            id=data.get("id", ""),
            owner_id=data.get("ownerId", ""),
            path=data.get("path", ""),
            name=data.get("name", ""),
            logo=data.get("logo"),
            description=data.get("description"),
            visibility=data.get("visibility"),
            created_at=data.get("createdAt"),
        )


@dataclass
class User:
    """用户信息"""
    id: str
    name: str
    email: Optional[str] = None
    user_path: Optional[str] = None
    photo: Optional[str] = None
    teams: list[Team] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """从字典创建User对象"""
        teams = [Team.from_dict(t) for t in data.get("teams", [])]
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            user_path=data.get("userPath"),
            photo=data.get("photo"),
            teams=teams,
        )


@dataclass
class LastChangeUser:
    """最后修改用户信息"""
    name: str
    photo: Optional[str] = None
    biography: Optional[str] = None
    user_path: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "LastChangeUser":
        """从字典创建LastChangeUser对象"""
        return cls(
            name=data.get("name", ""),
            photo=data.get("photo"),
            biography=data.get("biography"),
            user_path=data.get("userPath"),
        )


@dataclass
class Note:
    """笔记信息"""
    id: str
    title: str
    tags: Optional[list[str]] = None
    created_at: Optional[int] = None
    publish_type: Optional[str] = None
    published_at: Optional[int] = None
    permalink: Optional[str] = None
    short_id: Optional[str] = None
    content: Optional[str] = None
    last_changed_at: Optional[int] = None
    last_change_user: Optional[LastChangeUser] = None
    user_path: Optional[str] = None
    team_path: Optional[str] = None
    read_permission: Optional[str] = None
    write_permission: Optional[str] = None
    publish_link: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        """从字典创建Note对象"""
        last_change_user = None
        if data.get("lastChangeUser"):
            last_change_user = LastChangeUser.from_dict(data["lastChangeUser"])

        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            tags=data.get("tags"),
            created_at=data.get("createdAt"),
            publish_type=data.get("publishType"),
            published_at=data.get("publishedAt"),
            permalink=data.get("permalink"),
            short_id=data.get("shortId"),
            content=data.get("content"),
            last_changed_at=data.get("lastChangedAt"),
            last_change_user=last_change_user,
            user_path=data.get("userPath"),
            team_path=data.get("teamPath"),
            read_permission=data.get("readPermission"),
            write_permission=data.get("writePermission"),
            publish_link=data.get("publishLink"),
        )


@dataclass
class CreateNoteRequest:
    """创建笔记请求"""
    title: Optional[str] = None
    content: Optional[str] = None
    read_permission: Optional[str] = None
    write_permission: Optional[str] = None
    comment_permission: Optional[str] = None
    permalink: Optional[str] = None

    def to_dict(self) -> dict:
        """转换为API请求字典"""
        data = {}
        if self.title is not None:
            data["title"] = self.title
        if self.content is not None:
            data["content"] = self.content
        if self.read_permission is not None:
            data["readPermission"] = self.read_permission
        if self.write_permission is not None:
            data["writePermission"] = self.write_permission
        if self.comment_permission is not None:
            data["commentPermission"] = self.comment_permission
        if self.permalink is not None:
            data["permalink"] = self.permalink
        return data


@dataclass
class UpdateNoteRequest:
    """更新笔记请求"""
    content: Optional[str] = None
    read_permission: Optional[str] = None
    write_permission: Optional[str] = None
    permalink: Optional[str] = None

    def to_dict(self) -> dict:
        """转换为API请求字典"""
        data = {}
        if self.content is not None:
            data["content"] = self.content
        if self.read_permission is not None:
            data["readPermission"] = self.read_permission
        if self.write_permission is not None:
            data["writePermission"] = self.write_permission
        if self.permalink is not None:
            data["permalink"] = self.permalink
        return data
