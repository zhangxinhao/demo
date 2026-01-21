# -*- coding: utf-8 -*-
"""
同步 HackMD 笔记列表

从 HackMD API 获取笔记列表并保存到本地 JSON 文件
"""

import json

from common import get_logger
from common.client.hackmd_client import HackMDClient
from common.utils.path_manager import get_path_manager, PathType

logger = get_logger("sync_notes")


def sync_notes() -> None:
    """
    同步笔记列表到本地文件
    
    从 HackMD API 获取所有笔记列表，保存到 data/hackmd/notes.json
    """
    # 初始化路径管理器
    pm = get_path_manager()
    
    # 确保目录存在
    pm.ensure_dir_exists(PathType.HACKMD_BASE)
    
    # 初始化 HackMD 客户端
    client = HackMDClient.from_settings()
    
    # 获取笔记列表（原始 JSON 格式）
    logger.info("Fetching notes list from HackMD API")
    notes = client.get_notes_raw()
    logger.info(f"Fetched {len(notes)} notes")
    
    # 保存到文件
    output_path = pm.get_path(PathType.HACKMD_BASE) / "notes.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Notes saved to {output_path}")


if __name__ == "__main__":
    sync_notes()
