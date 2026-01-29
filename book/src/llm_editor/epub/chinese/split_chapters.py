# -*- coding: utf-8 -*-
"""
中文书籍章节分割模块

将长文本书籍按章节分割成多个文件
"""

import re
from pathlib import Path
from typing import List, Tuple

from common import get_logger, PathType, get_path_manager
from llm_editor.utils import ensure_dir, write_file

logger = get_logger(__name__)


def is_chapter_title(line: str) -> bool:
    """
    判断是否为章节标题
    
    Args:
        line: 文本行
        
    Returns:
        是否为章节标题
    """
    line = line.strip()
    if not line:
        return False
    
    # 匹配"第X章"格式（支持中文数字）
    chapter_pattern = r'^第[一二三四五六七八九十百千万]+章\s+.*'
    if re.match(chapter_pattern, line):
        return True
    
    # 匹配特殊章节：引子、前言、后记
    special_chapters = ['引子', '前言', '后记']
    if line in special_chapters:
        return True
    
    return False


def extract_chapters(content: str) -> List[Tuple[str, str]]:
    """
    从文本中提取所有章节
    
    Args:
        content: 完整文本内容
        
    Returns:
        章节列表，每个元素为(章节标题, 章节内容)的元组
    """
    lines = content.split('\n')
    chapters = []
    current_chapter_title = None
    current_chapter_lines = []
    
    for line in lines:
        # 检查是否为章节标题
        if is_chapter_title(line):
            # 如果之前有章节，先保存
            if current_chapter_title is not None:
                chapter_content = '\n'.join(current_chapter_lines).strip()
                if chapter_content:  # 只保存非空章节
                    chapters.append((current_chapter_title, chapter_content))
            
            # 开始新章节
            current_chapter_title = line.strip()
            current_chapter_lines = []
        else:
            # 添加到当前章节内容（只有在遇到第一个章节标题后才开始收集）
            if current_chapter_title is not None:
                current_chapter_lines.append(line)
    
    # 保存最后一个章节
    if current_chapter_title is not None:
        chapter_content = '\n'.join(current_chapter_lines).strip()
        if chapter_content:
            chapters.append((current_chapter_title, chapter_content))
    
    return chapters


def sanitize_filename(title: str) -> str:
    """
    将章节标题转换为安全的文件名
    
    Args:
        title: 章节标题
        
    Returns:
        安全的文件名
    """
    # 移除或替换不安全的字符
    filename = title.strip()
    # 替换Windows不支持的字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 移除前后空格和点
    filename = filename.strip('. ')
    return filename


def split_book_chapters(
    input_file: Path,
    output_dir: Path,
    book_name: str = None
) -> dict[str, bool]:
    """
    将书籍文件按章节分割成多个文件
    
    Args:
        input_file: 输入的完整书籍文件路径
        output_dir: 输出目录路径
        book_name: 书籍名称（用于创建子目录），如果为None则使用输入文件名（不含扩展名）
        
    Returns:
        处理结果字典，key为章节标题，value为是否成功
    """
    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        return {}
    
    # 确定书籍名称和输出目录
    if book_name is None:
        book_name = input_file.stem
    
    book_output_dir = output_dir / book_name
    ensure_dir(book_output_dir)
    
    logger.info(f"Reading book file: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Failed to read file {input_file}: {e}")
        return {}
    
    # 提取章节
    logger.info("Extracting chapters...")
    chapters = extract_chapters(content)
    logger.info(f"Found {len(chapters)} chapters")
    
    results = {}
    
    # 保存每个章节
    for i, (title, chapter_content) in enumerate(chapters, 1):
        # 生成文件名
        safe_title = sanitize_filename(title)
        filename = f"{i:03d}_{safe_title}.txt"
        output_file = book_output_dir / filename
        
        try:
            write_file(output_file, chapter_content)
            logger.info(f"Saved chapter {i}: {title} -> {filename}")
            results[title] = True
        except Exception as e:
            logger.error(f"Failed to save chapter '{title}': {e}")
            results[title] = False
    
    # 统计结果
    success_count = sum(1 for v in results.values() if v)
    logger.info(f"Split complete: {success_count}/{len(results)} chapters saved successfully")
    
    return results


def split_mingchao_book() -> dict[str, bool]:
    """
    分割《明朝那些事儿》书籍
    
    Returns:
        处理结果字典
    """
    path_manager = get_path_manager()
    epub_txt_dir = path_manager.get_dir_path(PathType.DATA) / "epub" / "txt"
    
    input_file = epub_txt_dir / "明朝那些事儿.txt"
    output_dir = epub_txt_dir
    
    return split_book_chapters(input_file, output_dir, "明朝那些事儿")


if __name__ == "__main__":
    split_mingchao_book()
