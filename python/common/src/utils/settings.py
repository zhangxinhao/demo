# -*- coding: utf-8 -*-
"""
Configuration settings module

Load configuration from .env file using python-dotenv
"""

import os
from typing import Optional, Union

from dotenv import load_dotenv

from common.env_var import EnvVar
from common.path_type import PathType
from utils.path_manager import get_path_manager


class Settings:
    """Application settings loaded from .env file"""

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
        """Load environment variables from .env file"""
        path_manager = get_path_manager()
        # .env file is located in data_v2/ directory
        env_path = path_manager.get_dir(PathType.ENV_FILE)

        if os.path.exists(env_path):
            # override=True 确保 .env 文件中的值会覆盖已存在的环境变量
            load_dotenv(env_path, override=True)
        else:
            # Try .env.example as fallback
            env_example_path = path_manager.get_dir(PathType.ENV_EXAMPLE_FILE)
            if os.path.exists(env_example_path):
                load_dotenv(env_example_path, override=True)

    def get(self, env_var: EnvVar) -> Union[str, int, float, None]:
        """Get environment variable value by EnvVar enum"""
        value = os.getenv(env_var.key, env_var.default)
        if value is None:
            return None
        return env_var.var_type(value)


# Global singleton instance
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """Get global settings instance"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
