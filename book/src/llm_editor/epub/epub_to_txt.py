"""
EPUB 转 TXT 模块
将 data/epub/book 目录下的 epub 文件转换为 txt 格式
"""

import re
from pathlib import Path

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

from llm_editor.utils import (
    get_data_dir,
    ensure_dir,
    write_file,
    get_logger,
)

logger = get_logger(__name__)


def get_epub_book_dir() -> Path:
    """获取 epub 书籍目录"""
    return get_data_dir() / "epub" / "book"


def get_epub_txt_dir() -> Path:
    """获取 epub 转换后的 txt 输出目录"""
    return get_data_dir() / "epub" / "txt"


def extract_text_from_html(html_content: bytes) -> str:
    """
    从 HTML 内容中提取纯文本
    
    Args:
        html_content: HTML 字节内容
    
    Returns:
        提取的纯文本
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 移除脚本和样式标签
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    
    # 获取文本
    text = soup.get_text(separator='\n')
    
    # 清理多余的空白行
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            cleaned_lines.append(stripped)
    
    return '\n'.join(cleaned_lines)


def epub_to_txt(epub_path: Path) -> str:
    """
    将 epub 文件转换为纯文本
    
    Args:
        epub_path: epub 文件路径
    
    Returns:
        提取的纯文本内容
    """
    book = epub.read_epub(str(epub_path))
    
    all_text = []
    
    # 遍历所有文档项
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_content()
            text = extract_text_from_html(content)
            if text.strip():
                all_text.append(text)
    
    return '\n\n'.join(all_text)


def convert_epub_to_txt(epub_path: Path, txt_path: Path) -> bool:
    """
    将单个 epub 文件转换为 txt 文件
    
    Args:
        epub_path: epub 文件路径
        txt_path: 输出的 txt 文件路径
    
    Returns:
        是否转换成功
    """
    try:
        logger.info(f"Converting: {epub_path.name} -> {txt_path.name}")
        text_content = epub_to_txt(epub_path)
        write_file(txt_path, text_content)
        logger.info(f"Successfully converted: {epub_path.name}")
        return True
    except Exception as e:
        logger.error(f"Failed to convert {epub_path.name}: {e}")
        return False


def process_all_epub_files() -> dict[str, bool]:
    """
    处理所有 epub 文件，将其转换为 txt 格式
    
    如果目标 txt 文件已存在则跳过
    
    Returns:
        处理结果字典，key 为文件名，value 为是否成功
    """
    epub_dir = get_epub_book_dir()
    txt_dir = get_epub_txt_dir()
    
    # 确保输出目录存在
    ensure_dir(txt_dir)
    
    results = {}
    
    # 遍历所有 epub 文件
    epub_files = list(epub_dir.glob("*.epub"))
    
    if not epub_files:
        logger.info(f"No epub files found in {epub_dir}")
        return results
    
    logger.info(f"Found {len(epub_files)} epub file(s) in {epub_dir}")
    
    for epub_path in epub_files:
        # 生成对应的 txt 文件路径
        txt_filename = epub_path.stem + ".txt"
        txt_path = txt_dir / txt_filename
        
        # 检查是否已存在同名 txt 文件
        if txt_path.exists():
            logger.info(f"Skipping {epub_path.name}: {txt_filename} already exists")
            results[epub_path.name] = True  # 标记为已处理
            continue
        
        # 转换文件
        success = convert_epub_to_txt(epub_path, txt_path)
        results[epub_path.name] = success
    
    # 统计结果
    total = len(results)
    success_count = sum(1 for v in results.values() if v)
    logger.info(f"Processing complete: {success_count}/{total} files processed successfully")
    
    return results


if __name__ == "__main__":
    process_all_epub_files()
