# -*- coding: utf-8 -*-
"""
同步 HackMD 笔记详情

根据指定的笔记 ID 列表，从 HackMD API 获取笔记详情并保存到本地 JSON 文件
"""

import json

from common import get_logger
from common.client.hackmd_client import HackMDClient
from common.utils.path_manager import get_path_manager, PathType

logger = get_logger("sync_note_detail")


def sync_note_details(note_ids: list[str]) -> None:
    """
    同步指定笔记的详情到本地文件
    
    Args:
        note_ids: 笔记 ID 列表
    """
    # 初始化路径管理器
    pm = get_path_manager()
    
    # 确保目录存在
    pm.ensure_dir_exists(PathType.HACKMD_NOTES)
    
    # 初始化 HackMD 客户端
    client = HackMDClient.from_settings()
    
    # 获取并保存每个笔记的详情
    for note_id in note_ids:
        try:
            logger.info(f"Fetching note detail: {note_id}")
            note = client.get_note_raw(note_id)
            
            # 使用 shortId 作为文件名
            short_id = note.get("shortId", note_id)
            output_path = pm.get_path(PathType.HACKMD_NOTES) / f"{short_id}.json"
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(note, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Note saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to fetch note {note_id}: {e}")


if __name__ == "__main__":
    # 需要同步的笔记 ID 列表
    NOTE_IDS = [
        "SkPQURprWe",
        "By-GUA6BWe",
    ]
    
    sync_note_details(NOTE_IDS)
