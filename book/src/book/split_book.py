"""
根据目录文件切分书籍 MD 文件，生成多个 TXT 文件
"""

import os
import re
from pathlib import Path


def get_book_files(book_dir: Path) -> list[Path]:
    """获取 book 目录下所有的 md 文件"""
    return list(book_dir.glob("*.md"))


def get_catalog_file(catalog_dir: Path, book_name: str) -> Path | None:
    """获取对应书名的目录文件"""
    catalog_file = catalog_dir / f"{book_name}.txt"
    if catalog_file.exists():
        return catalog_file
    return None


def read_catalog(catalog_file: Path) -> list[str]:
    """读取目录文件，返回章节标题列表"""
    with open(catalog_file, "r", encoding="utf-8") as f:
        # 读取每一行，去除空行
        lines = [line.strip() for line in f.readlines()]
        return [line for line in lines if line]


def read_book_content(book_file: Path) -> str:
    """读取书籍内容"""
    with open(book_file, "r", encoding="utf-8") as f:
        return f.read()


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
    positions = []
    
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
            print(f"Warning: Catalog title not found in book: {title}")
            positions.append(-1)
    
    # 过滤掉未找到的标题
    valid_positions = [(i, pos) for i, pos in enumerate(positions) if pos >= 0]
    
    if not valid_positions:
        return []
    
    # 按位置排序
    valid_positions.sort(key=lambda x: x[1])
    
    # 切分内容
    chapters = []
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


def ensure_output_dir(output_dir: Path) -> None:
    """确保输出目录存在"""
    output_dir.mkdir(parents=True, exist_ok=True)


def save_chapters(output_dir: Path, chapters: list[str]) -> None:
    """保存章节到文件"""
    for i, chapter in enumerate(chapters, start=1):
        output_file = output_dir / f"{i}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(chapter)
        print(f"Saved: {output_file}")


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
    print(f"\nProcessing book: {book_name}")
    
    # 获取目录文件
    catalog_file = get_catalog_file(catalog_dir, book_name)
    if not catalog_file:
        print(f"Warning: Catalog file not found for {book_name}")
        return False
    
    # 读取目录
    catalog = read_catalog(catalog_file)
    if not catalog:
        print(f"Warning: Catalog is empty for {book_name}")
        return False
    
    print(f"Found {len(catalog)} catalog entries")
    
    # 读取书籍内容
    content = read_book_content(book_file)
    
    # 切分书籍
    chapters = split_book_by_catalog(content, catalog)
    
    if len(chapters) != len(catalog):
        print(f"Warning: Expected {len(catalog)} chapters, got {len(chapters)}")
    
    # 创建输出目录
    output_dir = output_base_dir / book_name
    ensure_output_dir(output_dir)
    
    # 保存章节
    save_chapters(output_dir, chapters)
    
    print(f"Successfully processed {book_name}: {len(chapters)} chapters")
    return True


def main():
    """主函数"""
    # 获取项目根目录（假设脚本在 src/book 目录下）
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    
    # 定义路径
    book_dir = project_root / "data" / "book"
    catalog_dir = project_root / "data" / "catalog"
    output_dir = project_root / "data" / "txt"
    
    print(f"Book directory: {book_dir}")
    print(f"Catalog directory: {catalog_dir}")
    print(f"Output directory: {output_dir}")
    
    # 检查目录是否存在
    if not book_dir.exists():
        print(f"Error: Book directory not found: {book_dir}")
        return
    
    if not catalog_dir.exists():
        print(f"Error: Catalog directory not found: {catalog_dir}")
        return
    
    # 获取所有书籍文件
    book_files = get_book_files(book_dir)
    
    if not book_files:
        print("No book files found")
        return
    
    print(f"Found {len(book_files)} book(s)")
    
    # 处理每本书
    success_count = 0
    for book_file in book_files:
        if process_book(book_file, catalog_dir, output_dir):
            success_count += 1
    
    print(f"\n=== Summary ===")
    print(f"Total books: {len(book_files)}")
    print(f"Successfully processed: {success_count}")


if __name__ == "__main__":
    main()

