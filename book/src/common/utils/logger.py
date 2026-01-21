# -*- coding: utf-8 -*-
"""
日志管理模块

提供统一的日志配置和管理
"""

import logging
import logging.handlers
import os
import sys
from typing import Optional

from common.utils.path_manager import get_path_manager, PathType


def setup_logger(
        name: str = "app",
        level: int = logging.INFO,
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        enable_file: bool = True
) -> logging.Logger:
    """
    设置并返回 logger

    Args:
        name: logger 名称
        level: logger 基础级别
        console_level: 控制台输出级别
        file_level: 文件输出级别
        enable_file: 是否启用文件输出

    Returns:
        配置好的 logger
    """
    app_logger = logging.getLogger(name)

    # 避免重复添加 handler
    if app_logger.handlers:
        return app_logger

    app_logger.setLevel(level)

    # 创建格式器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - "%(filename)s:%(lineno)d" - %(message)s'
    )

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    app_logger.addHandler(console_handler)

    # 文件处理器（可选）
    if enable_file:
        path_manager = get_path_manager()
        logs_dir = path_manager.get_dir(PathType.LOGS)
        path_manager.ensure_dir_exists(PathType.LOGS)

        # 普通日志文件
        log_file_path = os.path.join(logs_dir, f'{name}.log')
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)

        # 错误日志文件
        error_file_path = os.path.join(logs_dir, f'{name}_error.log')
        error_handler = logging.FileHandler(error_file_path, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        app_logger.addHandler(error_handler)

    return app_logger


def get_logger(name: str = "app") -> logging.Logger:
    """
    获取已配置的 logger，如果不存在则创建

    Args:
        name: logger 名称

    Returns:
        logger 实例
    """
    app_logger = logging.getLogger(name)
    if not app_logger.handlers:
        return setup_logger(name)
    return app_logger


# 默认 logger 实例
_default_logger: Optional[logging.Logger] = None


def logger() -> logging.Logger:
    """获取默认 logger 实例"""
    global _default_logger
    if _default_logger is None:
        _default_logger = setup_logger("app", enable_file=False)
    return _default_logger
