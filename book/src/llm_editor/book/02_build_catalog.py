"""
构建目录模块
根据 data/book/catalog 目录下的目录 txt 文件
在 data/book/md 目录下的同名目录中生成 catalog.md
"""

from common import get_logger
from llm_editor.utils import (
    ensure_dir,
    get_catalog_dir,
    get_md_output_dir,
    read_lines,
    write_file,
)

logger = get_logger(__name__)


def extract_title_from_line(line: str) -> str:
    """
    从目录行中提取标题
    
    Args:
        line: 目录行，格式为 "# 标题"
    
    Returns:
        标题文本
    """
    # 去掉开头的 # 和空格
    if line.startswith("#"):
        return line.lstrip("#").strip()
    return line.strip()


def build_catalog_for_book(book_name: str) -> bool:
    """
    为指定书籍构建目录
    
    Args:
        book_name: 书籍名称
    
    Returns:
        是否成功
    """
    catalog_file = get_catalog_dir() / f"{book_name}.txt"
    md_dir = get_md_output_dir() / book_name
    output_file = md_dir / "catalog.md"

    # 检查目录文件是否存在
    if not catalog_file.exists():
        logger.error(f"Catalog file not found: {catalog_file}")
        return False

    # 确保 md 目录存在
    ensure_dir(md_dir)

    # 读取目录条目
    catalog_lines = read_lines(catalog_file)
    if not catalog_lines:
        logger.warning(f"Catalog file is empty: {catalog_file}")
        return False

    # 构建目录内容
    content_lines = [
        f"# {book_name}",
        "",
        "目录:",
    ]

    for line in catalog_lines:
        title = extract_title_from_line(line)
        if not title:
            continue

        # 生成固定格式的链接
        link = f"- [{title}](XXX)"
        content_lines.append(link)

    # 写入目录文件
    content = "\n".join(content_lines) + "\n"
    write_file(output_file, content)
    logger.info(f"Catalog generated: {output_file}")

    return True


def build_all_catalogs() -> None:
    """
    为所有书籍构建目录
    """
    catalog_dir = get_catalog_dir()

    if not catalog_dir.exists():
        logger.error(f"Catalog directory not found: {catalog_dir}")
        return

    # 获取所有目录 txt 文件
    catalog_files = list(catalog_dir.glob("*.txt"))

    if not catalog_files:
        logger.warning(f"No catalog files found in: {catalog_dir}")
        return

    success_count = 0
    for catalog_file in catalog_files:
        book_name = catalog_file.stem  # 获取文件名（不含扩展名）
        logger.info(f"Building catalog for: {book_name}")

        if build_catalog_for_book(book_name):
            success_count += 1

    logger.info(f"Catalog build completed. Success: {success_count}/{len(catalog_files)}")


if __name__ == "__main__":
    build_all_catalogs()
