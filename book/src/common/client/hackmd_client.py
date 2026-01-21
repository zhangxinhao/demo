# -*- coding: utf-8 -*-
"""
HackMD API 客户端封装

提供 HackMD API 的统一调用接口
API文档参考: docs/hackmd/api.md
"""

from typing import Optional

import requests

from common import get_logger
from common.config import get_settings, EnvVar
from common.models.hackmd import (
    User,
    Note,
    CreateNoteRequest,
    UpdateNoteRequest,
)

logger = get_logger("hackmd_client")


class HackMDClient:
    """
    HackMD API 客户端
    
    封装 HackMD API 调用，支持笔记的增删改查操作
    """

    BASE_URL = "https://api.hackmd.io/v1"

    def __init__(self, api_token: str):
        """
        初始化 HackMD 客户端
        
        Args:
            api_token: HackMD API Token
        """
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        })

    @classmethod
    def from_settings(cls) -> "HackMDClient":
        """
        从配置文件创建客户端
        
        Returns:
            HackMDClient 实例
        
        Raises:
            ValueError: 缺少 HACKMD_API_TOKEN 配置
        """
        settings = get_settings()
        api_token = settings.get(EnvVar.HACKMD_API_TOKEN)

        if not api_token:
            raise ValueError("HACKMD_API_TOKEN not found in config")

        logger.info("HackMD client initialized")
        return cls(api_token=api_token)

    def _request(
            self,
            method: str,
            endpoint: str,
            data: Optional[dict] = None,
    ) -> Optional[dict | list]:
        """
        发送 HTTP 请求
        
        Args:
            method: HTTP 方法 (GET, POST, PATCH, DELETE)
            endpoint: API 端点
            data: 请求数据
        
        Returns:
            响应数据（JSON 解析后）
        
        Raises:
            requests.HTTPError: 请求失败
        """
        url = f"{self.BASE_URL}{endpoint}"
        logger.debug(f"Request: {method} {url}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
            )
            response.raise_for_status()

            # DELETE 请求返回 204 无内容
            if response.status_code == 204:
                return None
            # PATCH 请求可能返回 202 Accepted
            if response.status_code == 202:
                return None

            return response.json()
        except requests.HTTPError as e:
            logger.error(f"HTTP error: {e}, response: {e.response.text if e.response else 'N/A'}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise

    def get_me(self) -> User:
        """
        获取当前用户信息
        
        GET /me
        
        Returns:
            User 用户信息对象
        """
        logger.info("Getting user information")
        data = self._request("GET", "/me")
        return User.from_dict(data)

    def get_notes(self) -> list[Note]:
        """
        获取用户工作区的笔记列表
        
        GET /notes
        
        Returns:
            笔记列表
        """
        logger.info("Getting notes list")
        data = self._request("GET", "/notes")
        return [Note.from_dict(note) for note in data]

    def get_notes_raw(self) -> list[dict]:
        """
        获取用户工作区的笔记列表（原始 JSON 格式）
        
        GET /notes
        
        Returns:
            笔记列表的原始 dict 数据
        """
        logger.info("Getting notes list (raw)")
        data = self._request("GET", "/notes")
        return data

    def get_note(self, note_id: str) -> Note:
        """
        获取单个笔记详情
        
        GET /notes/:noteId
        
        Args:
            note_id: 笔记 ID
        
        Returns:
            Note 笔记对象（包含 content）
        """
        logger.info(f"Getting note: {note_id}")
        data = self._request("GET", f"/notes/{note_id}")
        return Note.from_dict(data)

    def get_note_raw(self, note_id: str) -> dict:
        """
        获取单个笔记详情（原始 JSON 格式）
        
        GET /notes/:noteId
        
        Args:
            note_id: 笔记 ID
        
        Returns:
            笔记的原始 dict 数据
        """
        logger.info(f"Getting note (raw): {note_id}")
        data = self._request("GET", f"/notes/{note_id}")
        return data

    def create_note(self, request: Optional[CreateNoteRequest] = None) -> Note:
        """
        创建新笔记
        
        POST /notes
        
        Args:
            request: 创建笔记请求参数，可选
        
        Returns:
            Note 创建的笔记对象
        
        Note:
            - 如果 content 中有 H1 标题，会作为笔记标题
            - 如果 content 中有 YAML metadata 的 title，会作为笔记标题
            - 如果没有 content，则使用 title 字段或默认 "Untitled"
            - readPermission 和 writePermission 需要同时提供
            - writePermission 必须比 readPermission 更严格
        """
        logger.info("Creating new note")
        data = request.to_dict() if request else {}
        response = self._request("POST", "/notes", data=data)
        return Note.from_dict(response)

    def update_note(self, note_id: str, request: UpdateNoteRequest) -> bool:
        """
        更新笔记
        
        PATCH /notes/:noteId
        
        Args:
            note_id: 笔记 ID
            request: 更新笔记请求参数
        
        Returns:
            True 表示更新成功
        
        Note:
            - readPermission 和 writePermission 需要同时提供
        """
        logger.info(f"Updating note: {note_id}")
        self._request("PATCH", f"/notes/{note_id}", data=request.to_dict())
        return True

    def delete_note(self, note_id: str) -> bool:
        """
        删除笔记
        
        DELETE /notes/:noteId
        
        Args:
            note_id: 笔记 ID
        
        Returns:
            True 表示删除成功
        """
        logger.info(f"Deleting note: {note_id}")
        self._request("DELETE", f"/notes/{note_id}")
        return True

    def get_history(self) -> list[Note]:
        """
        获取阅读历史
        
        GET /history
        
        Returns:
            阅读历史的笔记列表
        """
        logger.info("Getting reading history")
        data = self._request("GET", "/history")
        return [Note.from_dict(note) for note in data]
