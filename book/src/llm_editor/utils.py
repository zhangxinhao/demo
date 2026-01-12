"""
公共工具模块
提供路径管理、配置管理、文件IO、日志等公共功能
"""

import logging
import sys
from pathlib import Path
from typing import TypedDict

import yaml


# ============ 类型定义 ============

class BookConfig(TypedDict, total=False):
    """书籍配置类型"""
    add_prompt: bool
    llm_process: bool
    need_link: bool


class AppConfig(TypedDict, total=False):
    """应用配置类型"""
    books: dict[str, BookConfig]
    num_threads: int


# ============ 路径管理 ============

def get_project_root() -> Path:
    """获取项目根目录"""
    # 从 src/book/utils.py 往上两级
    return Path(__file__).parent.parent.parent


def get_data_dir() -> Path:
    """获取 data 目录路径"""
    return get_project_root() / "data"


def get_book_base_dir() -> Path:
    """获取 book 模块的基础目录 (data/book)"""
    return get_data_dir() / "book"


def get_config_path() -> Path:
    """获取配置文件路径 (data/book/config.yaml)"""
    return get_book_base_dir() / "config.yaml"


def get_txt_dir() -> Path:
    """获取 txt 文件目录 (data/book/txt)"""
    return get_book_base_dir() / "txt"


def get_book_dir() -> Path:
    """获取书籍 MD 文件目录 (data/book/book)"""
    return get_book_base_dir() / "book"


def get_catalog_dir() -> Path:
    """获取目录文件目录 (data/book/catalog)"""
    return get_book_base_dir() / "catalog"


def get_prompt_dir() -> Path:
    """获取提示词目录 (data/prompt)"""
    return get_data_dir() / "prompt"


def get_md_output_dir() -> Path:
    """获取 MD 输出目录 (data/book/md)"""
    return get_book_base_dir() / "md"


def get_src_dir() -> Path:
    """获取 src 目录"""
    return get_project_root() / "src"


# ============ 配置管理 ============

def load_config(config_path: Path | None = None) -> AppConfig:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径，默认使用 data/book/config.yaml
    
    Returns:
        配置字典
    """
    if config_path is None:
        config_path = get_config_path()

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config(config: AppConfig, config_path: Path | None = None) -> None:
    """
    保存配置文件
    
    Args:
        config: 配置字典
        config_path: 配置文件路径，默认使用 data/book/config.yaml
    """
    if config_path is None:
        config_path = get_config_path()

    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)


# ============ 文件 IO ============

def read_file(file_path: Path) -> str:
    """
    读取文件内容
    
    Args:
        file_path: 文件路径
    
    Returns:
        文件内容
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(file_path: Path, content: str) -> None:
    """
    写入文件内容
    
    Args:
        file_path: 文件路径
        content: 文件内容
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def append_file(file_path: Path, content: str) -> None:
    """
    追加文件内容
    
    Args:
        file_path: 文件路径
        content: 追加的内容
    """
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(content)


def read_lines(file_path: Path) -> list[str]:
    """
    读取文件行（去除空行和空白）
    
    Args:
        file_path: 文件路径
    
    Returns:
        非空行列表
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
        return [line for line in lines if line]


def ensure_dir(dir_path: Path) -> None:
    """
    确保目录存在，不存在则创建
    
    Args:
        dir_path: 目录路径
    """
    dir_path.mkdir(parents=True, exist_ok=True)


# ============ 日志管理 ============

def setup_logger(
        name: str,
        level: int = logging.INFO,
        format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
) -> logging.Logger:
    """
    设置并返回 logger
    
    Args:
        name: logger 名称
        level: 日志级别
        format_str: 日志格式
    
    Returns:
        配置好的 logger
    """
    logger = logging.getLogger(name)

    # 避免重复添加 handler
    if not logger.handlers:
        logger.setLevel(level)

        # 控制台 handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # 设置格式
        formatter = logging.Formatter(format_str)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    获取已配置的 logger，如果不存在则创建
    
    Args:
        name: logger 名称
    
    Returns:
        logger 实例
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger
