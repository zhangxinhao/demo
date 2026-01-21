# -*- coding: utf-8 -*-
"""
上传笔记到 HackMD

遍历本地 md 文件目录，获取文件内容并上传到 HackMD
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

from common import get_logger
from common.client.hackmd_client import HackMDClient
from common.models.hackmd import CreateNoteRequest
from common.utils.path_manager import get_path_manager, PathType

logger = get_logger("upload_notes")


@dataclass
class MdFile:
    """Markdown 文件信息"""
    path: Path  # 文件路径
    content: str  # 文件内容


@dataclass
class UploadResult:
    """上传结果信息"""
    filename: str  # 文件名（不含扩展名）
    title: str  # 笔记标题
    url: str  # 笔记 URL
    directory: Path  # 所属目录


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

            md_files.append(MdFile(
                path=md_path,
                content=content
            ))
            logger.debug(f"Found: {md_path.name}")

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


def get_sort_key(filename: str) -> tuple:
    """
    获取文件名的排序键
    
    排序规则：
    1. 纯数字文件名按数字从小到大排序，放在最前面
    2. 非数字文件名按字符串从小到大排序，放在后面
    
    Args:
        filename: 文件名（不含扩展名）
        
    Returns:
        排序键元组 (是否为非数字, 排序值)
    """
    # 检查是否为纯数字
    if filename.isdigit():
        return (0, int(filename), "")
    else:
        return (1, 0, filename)


def generate_yaml_list(results: List[UploadResult]) -> str:
    """
    生成 YAML 格式的无序列表
    
    Args:
        results: 上传结果列表
        
    Returns:
        YAML 格式的字符串
    """
    if not results:
        return ""

    # 按目录分组
    grouped: Dict[Path, List[UploadResult]] = {}
    for result in results:
        if result.directory not in grouped:
            grouped[result.directory] = []
        grouped[result.directory].append(result)

    output_lines = []

    # 遍历每个目录
    for directory, dir_results in grouped.items():
        # 对结果按文件名排序
        sorted_results = sorted(dir_results, key=lambda r: get_sort_key(r.filename))

        # 添加目录标题
        output_lines.append(f"\n# {directory.name}")

        # 生成无序列表
        for result in sorted_results:
            output_lines.append(f"- [{result.title}]({result.url})")

    return "\n".join(output_lines)


def upload_notes(directories: List[Path]) -> None:
    """
    上传笔记主函数
    
    Args:
        directories: 要扫描的目录列表
    """
    logger.info(f"Directories to scan: {[str(d) for d in directories]}")

    # 扫描 md 文件
    md_files = scan_md_files(directories)
    logger.info(f"Found {len(md_files)} valid md files")

    if not md_files:
        logger.info("No files to upload")
        return

    # 初始化路径管理器和客户端
    pm = get_path_manager()
    pm.ensure_dir_exists(PathType.HACKMD_NOTES)
    client = HackMDClient.from_settings()

    # 收集上传结果
    upload_results: List[UploadResult] = []

    # 上传每个文件
    for md_file in md_files:
        try:
            logger.info(f"Uploading: {md_file.path.name}")

            # 调用 create_note，只传 content
            request = CreateNoteRequest(content=md_file.content)
            note = client.create_note(request)

            # 获取返回信息
            short_id = note.short_id
            title = note.title
            note_id = note.id
            url = f"https://hackmd.io/{note_id}"

            # 打印结果
            logger.info(f"  shortId: {short_id}")
            logger.info(f"  title: {title}")
            logger.info(f"  URL: {url}")
            logger.info(f"  Link: [{title}]({url})")

            # 保存到本地 JSON 文件
            output_path = pm.get_path(PathType.HACKMD_NOTES) / f"{short_id}.json"

            # 构建保存数据（使用 Note 对象的属性）
            note_data = {
                "id": note.id,
                "title": note.title,
                "tags": note.tags,
                "createdAt": note.created_at,
                "titleUpdatedAt": note.title_updated_at,
                "tagsUpdatedAt": note.tags_updated_at,
                "publishType": note.publish_type,
                "publishedAt": note.published_at,
                "permalink": note.permalink,
                "publishLink": note.publish_link,
                "shortId": note.short_id,
                "content": note.content,
                "lastChangedAt": note.last_changed_at,
                "lastChangeUser": {
                    "name": note.last_change_user.name,
                    "userPath": note.last_change_user.user_path,
                    "photo": note.last_change_user.photo,
                    "biography": note.last_change_user.biography,
                } if note.last_change_user else None,
                "userPath": note.user_path,
                "teamPath": note.team_path,
                "readPermission": note.read_permission,
                "writePermission": note.write_permission,
            }

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(note_data, f, ensure_ascii=False, indent=2)

            logger.info(f"  Saved to: {output_path}")

            # 收集上传结果
            upload_results.append(UploadResult(
                filename=md_file.path.stem,  # 文件名不含扩展名
                title=title,
                url=url,
                directory=md_file.path.parent
            ))

        except Exception as e:
            logger.error(f"Failed to upload {md_file.path.name}: {e}")

    # 输出 YAML 格式列表
    if upload_results:
        yaml_list = generate_yaml_list(upload_results)
        logger.info(f"\n{'=' * 50}\nYAML List:{yaml_list}\n{'=' * 50}")


if __name__ == "__main__":
    pm = get_path_manager()

    # 书籍名称列表
    book_names = [
        # "正念-卡巴金",
    ]

    # 构建目录列表：PathType.ARTICLE_MD + book 目录
    directories = [
        pm.get_path(PathType.ARTICLE_MD),
        *get_book_directories(book_names)
    ]

    # 扫描并上传
    upload_notes(directories)
