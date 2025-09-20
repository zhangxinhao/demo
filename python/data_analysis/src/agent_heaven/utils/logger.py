# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os


def setup_logger():
    """设置应用日志器"""
    # 创建logger
    app_logger = logging.getLogger('app')
    app_logger.setLevel(logging.DEBUG)

    # 创建格式器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - "%(filename)s:%(lineno)d" - %(message)s'
    )

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 确保日志目录存在
    logs_dir = "D:\code\zxh\demo\python\data_analysis\data\log"

    # 文件处理器
    log_file_path = os.path.join(logs_dir, 'app.log')
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 错误文件处理器
    error_file_path = os.path.join(logs_dir, 'error.log')
    error_handler = logging.FileHandler(error_file_path, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # 添加处理器到logger
    app_logger.addHandler(console_handler)
    app_logger.addHandler(file_handler)
    app_logger.addHandler(error_handler)

    return app_logger


# 使用
logger = setup_logger()
