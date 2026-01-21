# -*- coding: utf-8 -*-
"""
配置管理模块

从 .env 文件加载环境变量配置
"""

import os
from enum import Enum
from typing import Optional, Union

from dotenv import load_dotenv

from common.utils.path_manager import get_path_manager


class EnvVar(Enum):
    """
    环境变量定义
    格式: (key, default_value, type)
    """
    # API Keys
    GEMINI_API_KEY = ("GEMINI_API_KEY", None, str)
    DEEPSEEK_API_KEY = ("DEEPSEEK_API_KEY", None, str)
    OPENAI_API_KEY = ("OPENAI_API_KEY", None, str)
    OPENROUTER_API_KEY = ("OPENROUTER_API_KEY", None, str)

    # LLM 配置
    LLM_MODEL = ("LLM_MODEL", "gemini-2.0-flash", str)
    MODEL_NAME = ("MODEL_NAME", None, str)  # 兼容旧配置
    LLM_BASE_URL = ("LLM_BASE_URL", "https://openrouter.ai/api/v1", str)

    # 并发配置
    NUM_THREADS = ("NUM_THREADS", "4", int)

    @property
    def key(self) -> str:
        return self.value[0]

    @property
    def default(self) -> Optional[str]:
        return self.value[1]

    @property
    def var_type(self) -> type:
        return self.value[2]


class Settings:
    """应用配置管理器，从 .env 文件加载配置"""

    _instance: Optional["Settings"] = None
    _initialized: bool = False

    def __new__(cls) -> "Settings":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._load_env()
        self._initialized = True

    def _load_env(self) -> None:
        """加载 .env 文件中的环境变量"""
        path_manager = get_path_manager()
        # .env 文件位于 src/ 目录下
        env_path = path_manager.get_absolute_path("src/.env")

        if os.path.exists(env_path):
            load_dotenv(env_path)
        else:
            # 尝试 .env.example 作为备选
            env_example_path = path_manager.get_absolute_path("src/.env.example")
            if os.path.exists(env_example_path):
                load_dotenv(env_example_path)

    def get(self, env_var: EnvVar) -> Union[str, int, None]:
        """
        获取环境变量值

        Args:
            env_var: EnvVar 枚举

        Returns:
            环境变量值，已转换为对应类型
        """
        value = os.getenv(env_var.key, env_var.default)
        if value is None:
            return None
        return env_var.var_type(value)

    def get_api_key(self, provider: str = "gemini") -> Optional[str]:
        """
        获取指定 LLM 提供商的 API Key

        Args:
            provider: 提供商名称 (gemini, deepseek, openai)

        Returns:
            API Key 或 None
        """
        key_map = {
            "gemini": EnvVar.GEMINI_API_KEY,
            "deepseek": EnvVar.DEEPSEEK_API_KEY,
            "openai": EnvVar.OPENAI_API_KEY,
        }
        env_var = key_map.get(provider.lower())
        if env_var:
            return self.get(env_var)
        return None


# 全局单例
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """获取全局配置实例"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
