# -*- coding: utf-8 -*-
"""
路径管理模块

提供项目路径的统一管理，支持枚举类型定义常用路径
"""

import os
from enum import Enum
from pathlib import Path
from typing import Union, Optional


class PathType(Enum):
    """路径类型枚举"""
    # 通用目录
    DATA = "data"
    LOGS = "data/logs"
    PROMPT = "data/prompt"

    # Book 模块相关目录
    BOOK_BASE = "data/book"
    BOOK_TXT = "data/book/txt"
    BOOK_BOOK = "data/book/book"
    BOOK_CATALOG = "data/book/catalog"
    BOOK_MD = "data/book/md"

    # Article 模块相关目录
    ARTICLE_BASE = "data/article"
    ARTICLE_TXT = "data/article/txt"
    ARTICLE_PROMPT_TXT = "data/article/prompt_txt"
    ARTICLE_MD = "data/article/md"

    # Subtitle 模块相关目录
    SUBTITLE_BASE = "data/subtitle"
    SUBTITLE_SRT = "data/subtitle/srt"
    SUBTITLE_TXT = "data/subtitle/txt"

    # HackMD 模块相关目录
    HACKMD_BASE = "data/hackmd"
    HACKMD_NOTES = "data/hackmd/notes"


class PathManager:
    """路径管理器"""

    def __init__(self):
        self._project_root: Optional[str] = None

    @property
    def project_root(self) -> str:
        """获取项目根目录"""
        if self._project_root is None:
            self._project_root = self._find_project_root()
        return self._project_root

    def _find_project_root(self) -> str:
        """
        查找项目根目录
        从 src/common/utils/path_manager.py 向上 4 层到项目根目录
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # utils -> common -> src -> project_root
        return os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

    def get_absolute_path(self, path: Union[str, Path]) -> str:
        """
        将相对路径转换为绝对路径

        Args:
            path: 相对或绝对路径

        Returns:
            绝对路径字符串
        """
        path_str = str(path)
        if os.path.isabs(path_str):
            return path_str
        return os.path.join(self.project_root, path_str)

    def get_path(self, path: Union[Path, PathType]) -> Path:
        """
        将路径转换为 Path 对象

        Args:
            path: Path 对象或路径类型枚举

        Returns:
            Path 对象
        """
        if isinstance(path, PathType):
            return Path(self.get_dir(path))
        return Path(self.get_absolute_path(path))

    def get_dir(self, path_type: PathType) -> str:
        """
        获取指定类型的目录绝对路径

        Args:
            path_type: 路径类型枚举

        Returns:
            绝对路径字符串
        """
        return self.get_absolute_path(path_type.value)

    def get_dir_path(self, path_type: PathType) -> Path:
        """
        获取指定类型的目录 Path 对象

        Args:
            path_type: 路径类型枚举

        Returns:
            Path 对象
        """
        return Path(self.get_dir(path_type))

    def ensure_dir_exists(self, path: Union[str, Path, PathType]) -> bool:
        """
        确保目录存在，不存在则创建

        Args:
            path: 目录路径或路径类型枚举

        Returns:
            True 表示成功，False 表示失败
        """
        try:
            if isinstance(path, PathType):
                abs_path = self.get_dir(path)
            else:
                abs_path = self.get_absolute_path(path)
            os.makedirs(abs_path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Failed to create directory: {path}, error: {str(e)}")
            return False


# 全局单例
_path_manager_instance: Optional[PathManager] = None


def get_path_manager() -> PathManager:
    """获取全局路径管理器实例"""
    global _path_manager_instance
    if _path_manager_instance is None:
        _path_manager_instance = PathManager()
    return _path_manager_instance
