# -*- coding: utf-8 -*-
"""
上传笔记到 HackMD

遍历本地 md 文件目录，获取文件标题和内容
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from common import get_logger
from common.utils.path_manager import get_path_manager, PathType

logger = get_logger("upload_notes")


@dataclass
class MdFile:
    """Markdown 文件信息"""
    path: Path  # 文件路径
    title: str  # 文章标题（从第一行提取）
    content: str  # 文件内容


def get_title_from_content(content: str) -> Optional[str]:
    """
    从内容中提取标题
    
    获取第一行，去除 # 符号和前后空白符
    
    Args:
        content: md 文件内容
        
    Returns:
        标题字符串，如果无法提取则返回 None
    """
    if not content:
        return None

    # 获取第一行
    first_line = content.split('\n')[0]

    # 去除 # 符号和前后空白符
    title = first_line.lstrip('#').strip()

    return title if title else None


def scan_md_files(directories: List[Path]) -> List[MdFile]:
    """
    扫描指定目录下的 md 文件
    
    Args:
        directories: 目录列表
        
    Returns:
        MdFile 列表
    """
    md_files: List[MdFile] = []

    for directory in directories:
        if not directory.exists():
            logger.warning(f"Directory not found: {directory}")
            continue

        logger.info(f"Scanning directory: {directory}")

        # 遍历目录下的 md 文件
        for md_path in directory.glob("*.md"):
            # 读取文件内容
            try:
                content = md_path.read_text(encoding="utf-8")
            except Exception as e:
                logger.error(f"Failed to read file {md_path}: {e}")
                continue

            # 过滤空文件
            if not content.strip():
                logger.debug(f"Skipping empty file: {md_path}")
                continue

            # 提取标题
            title = get_title_from_content(content)
            if not title:
                logger.warning(f"No title found in file: {md_path}")
                continue

            md_files.append(MdFile(
                path=md_path,
                title=title,
                content=content
            ))
            logger.debug(f"Found: {title} ({md_path.name})")

    return md_files


def get_book_directories(book_names: List[str]) -> List[Path]:
    """
    根据书籍名称列表生成对应的目录路径
    
    Args:
        book_names: 书籍名称列表
        
    Returns:
        目录 Path 列表
    """
    pm = get_path_manager()
    book_md_base = pm.get_path(PathType.BOOK_MD)
    return [book_md_base / book_name for book_name in book_names]


def upload_notes(directories: List[Path]) -> List[MdFile]:
    """
    上传笔记主函数
    
    Args:
        directories: 要扫描的目录列表
        
    Returns:
        扫描到的 MdFile 列表
    """
    logger.info(f"Directories to scan: {[str(d) for d in directories]}")

    # 扫描 md 文件
    md_files = scan_md_files(directories)
    logger.info(f"Found {len(md_files)} valid md files")

    # 打印文件信息
    for md_file in md_files:
        logger.info(f"  - {md_file.title} ({md_file.path.name})")

    return md_files


if __name__ == "__main__":
    pm = get_path_manager()

    # 书籍名称列表
    book_names = [
        # "正念的奇迹",
    ]

    # 构建目录列表：PathType.ARTICLE_MD + book 目录
    directories = [
        pm.get_path(PathType.ARTICLE_MD),
        *get_book_directories(book_names)
    ]

    # 扫描并上传
    files = upload_notes(directories)
