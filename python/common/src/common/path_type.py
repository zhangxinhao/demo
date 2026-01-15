from enum import Enum

# 数据根目录
_DATA_ROOT = "data"


class PathType(Enum):
    """路径类型枚举"""
    # 通用目录
    DATA = _DATA_ROOT
    LOGS = f"{_DATA_ROOT}/logs"

    # 环境配置文件
    ENV_FILE = f"{_DATA_ROOT}/.env"
    ENV_EXAMPLE_FILE = f"{_DATA_ROOT}/.env.example"

    # SFTP
    SFTP = f"{_DATA_ROOT}/sftp"
