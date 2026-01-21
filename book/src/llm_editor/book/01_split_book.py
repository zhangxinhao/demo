"""
根据目录文件切分书籍文件（支持 MD 和 TXT 格式），生成多个 TXT 文件
"""

import re
from pathlib import Path

from common import get_logger
from llm_editor.utils import (
    get_book_dir,
    get_catalog_dir,
    get_txt_dir,
    read_file,
    read_lines,
    write_file,
    ensure_dir,
)

# 初始化 logger
logger = get_logger("split_book")


def get_book_files(book_dir: Path) -> list[Path]:
    """获取 book 目录下所有的书籍文件（支持 md 和 txt 格式）"""
    md_files = list(book_dir.glob("*.md"))
    txt_files = list(book_dir.glob("*.txt"))
    return md_files + txt_files


def get_catalog_file(catalog_dir: Path, book_name: str) -> Path | None:
    """获取对应书名的目录文件"""
    catalog_file = catalog_dir / f"{book_name}.txt"
    if catalog_file.exists():
        return catalog_file
    return None


def split_book_by_catalog(content: str, catalog: list[str]) -> list[str]:
    """
    根据目录切分书籍内容
    
    Args:
        content: 书籍完整内容
        catalog: 目录标题列表
        
    Returns:
        切分后的内容列表，每个元素对应一个章节
    """
    if not catalog:
        return []

    # 存储每个章节的起始位置
    positions: list[int] = []

    for title in catalog:
        # 在内容中查找标题的位置
        # 标题可能在行首，需要匹配行首或换行后的位置
        pattern = rf"(^|\n)({re.escape(title)})(\n|$)"
        match = re.search(pattern, content)
        if match:
            # 记录标题开始的位置（不包括前面的换行符）
            start_pos = match.start(2)
            positions.append(start_pos)
        else:
            logger.warning(f"Catalog title not found in book: {title}")
            positions.append(-1)

    # 过滤掉未找到的标题
    valid_positions = [(i, pos) for i, pos in enumerate(positions) if pos >= 0]

    if not valid_positions:
        return []

    # 按位置排序
    valid_positions.sort(key=lambda x: x[1])

    # 切分内容
    chapters: list[tuple[int, str]] = []
    for idx, (catalog_idx, start_pos) in enumerate(valid_positions):
        if idx < len(valid_positions) - 1:
            # 取到下一个章节开始的位置
            end_pos = valid_positions[idx + 1][1]
            chapter_content = content[start_pos:end_pos].strip()
        else:
            # 最后一个章节，取到文件末尾
            chapter_content = content[start_pos:].strip()

        chapters.append((catalog_idx, chapter_content))

    # 按目录顺序排序
    chapters.sort(key=lambda x: x[0])

    return [ch[1] for ch in chapters]


def save_chapters(output_dir: Path, chapters: list[str]) -> None:
    """保存章节到文件"""
    for i, chapter in enumerate(chapters, start=1):
        output_file = output_dir / f"{i}.txt"
        write_file(output_file, chapter)
        logger.info(f"Saved: {output_file}, characters: {len(chapter)}")


def process_book(book_file: Path, catalog_dir: Path, output_base_dir: Path) -> bool:
    """
    处理单本书籍
    
    Args:
        book_file: 书籍 MD 文件路径
        catalog_dir: 目录文件所在目录
        output_base_dir: 输出基础目录
        
    Returns:
        是否处理成功
    """
    book_name = book_file.stem  # 获取文件名（不含扩展名）
    
    # 检查目标目录是否已存在，如果存在则跳过
    output_dir = output_base_dir / book_name
    if output_dir.exists():
        logger.info(f"Skipping {book_name}: output directory already exists")
        return False
    
    logger.info(f"Processing book: {book_name}")

    # 获取目录文件
    catalog_file = get_catalog_file(catalog_dir, book_name)
    if not catalog_file:
        logger.warning(f"Catalog file not found for {book_name}")
        return False

    # 读取目录
    catalog = read_lines(catalog_file)
    if not catalog:
        logger.warning(f"Catalog is empty for {book_name}")
        return False

    logger.info(f"Found {len(catalog)} catalog entries")

    # 读取书籍内容
    content = read_file(book_file)

    # 切分书籍
    chapters = split_book_by_catalog(content, catalog)

    if len(chapters) != len(catalog):
        logger.warning(f"Expected {len(catalog)} chapters, got {len(chapters)}")

    # 创建输出目录
    ensure_dir(output_dir)

    # 保存章节
    save_chapters(output_dir, chapters)

    logger.info(f"Successfully processed {book_name}: {len(chapters)} chapters")
    return True


def main() -> None:
    """主函数"""
    # 使用公共路径函数
    book_dir = get_book_dir()
    catalog_dir = get_catalog_dir()
    output_dir = get_txt_dir()

    logger.info(f"Book directory: {book_dir}")
    logger.info(f"Catalog directory: {catalog_dir}")
    logger.info(f"Output directory: {output_dir}")

    # 检查目录是否存在
    if not book_dir.exists():
        logger.error(f"Book directory not found: {book_dir}")
        return

    if not catalog_dir.exists():
        logger.error(f"Catalog directory not found: {catalog_dir}")
        return

    # 获取所有书籍文件
    book_files = get_book_files(book_dir)

    if not book_files:
        logger.info("No book files found")
        return

    logger.info(f"Found {len(book_files)} book(s)")

    # 处理每本书
    success_count = 0
    for book_file in book_files:
        if process_book(book_file, catalog_dir, output_dir):
            success_count += 1

    logger.info("=== Summary ===")
    logger.info(f"Total books: {len(book_files)}")
    logger.info(f"Successfully processed: {success_count}")


if __name__ == "__main__":
    main()
