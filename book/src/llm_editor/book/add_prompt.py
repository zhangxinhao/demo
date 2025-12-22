"""
为书籍文本文件添加提示词
遍历data/txt下的目录，根据config.yaml配置为每个txt文件添加对应的提示词
"""

from pathlib import Path

from llm_editor.utils import (
    get_txt_dir,
    get_prompt_dir,
    load_config,
    save_config,
    read_file,
    append_file,
    get_logger,
    AppConfig,
)

# 初始化 logger
logger = get_logger("add_prompt")


def append_prompt_to_file(file_path: Path, prompt: str) -> int:
    """
    在文件末尾追加提示词
    
    Args:
        file_path: 文件路径
        prompt: 提示词内容
    
    Returns:
        添加提示词后文件的字符数量
    """
    append_file(file_path, prompt)
    # 读取文件内容并计算字符数
    content = read_file(file_path)
    char_count = len(content)
    logger.info(f"Added prompt to: {file_path}, character count: {char_count}")
    return char_count


def process_book(book_dir: Path, prompt: str) -> tuple[int, dict[str, int]]:
    """
    处理单本书的所有txt文件
    
    Args:
        book_dir: 书籍目录
        prompt: 提示词内容
    
    Returns:
        (处理的文件数量, 文件字符数统计字典)
    """
    processed_count = 0
    char_counts: dict[str, int] = {}
    # 遍历书籍目录下的所有txt文件
    for txt_file in sorted(book_dir.glob("*.txt")):
        char_count = append_prompt_to_file(txt_file, prompt)
        char_counts[txt_file.name] = char_count
        processed_count += 1
    return processed_count, char_counts


def main() -> None:
    """主函数"""
    # 路径配置
    txt_base_dir = get_txt_dir()
    prompt_dir = get_prompt_dir()
    link_prompt_path = prompt_dir / "link.txt"
    nolink_prompt_path = prompt_dir / "nolink.txt"

    # 加载配置
    config: AppConfig = load_config()
    books_config = config.get("books", {})

    # 加载提示词
    link_prompt = read_file(link_prompt_path)
    nolink_prompt = read_file(nolink_prompt_path)

    # 遍历txt目录下的书籍目录
    if not txt_base_dir.exists():
        logger.error(f"Directory not found: {txt_base_dir}")
        return

    books_processed: list[str] = []

    for book_dir in txt_base_dir.iterdir():
        if not book_dir.is_dir():
            continue

        book_name = book_dir.name
        book_config = books_config.get(book_name, {})

        # 检查是否已完成
        if book_config.get("add_prompt", False):
            logger.info(f"Skipping add_prompt book: {book_name}")
            continue

        # 检查书籍是否在配置中
        if book_name not in books_config:
            logger.warning(f"Book '{book_name}' not in config, skipping")
            continue

        # 根据配置选择提示词类型
        need_link = book_config.get("need_link", False)
        prompt = link_prompt if need_link else nolink_prompt

        logger.info(f"Processing book: {book_name} (need_link: {need_link})")

        # 处理书籍
        count, char_counts = process_book(book_dir, prompt)
        logger.info(f"Processed {count} files for book: {book_name}")
        
        # 打印每个文件的字符数量
        logger.info(f"Character counts for book '{book_name}':")
        for filename, char_count in char_counts.items():
            logger.info(f"  {filename}: {char_count} characters")

        # 记录已处理的书籍
        books_processed.append(book_name)

    # 更新配置，标记已完成的书籍
    for book_name in books_processed:
        if book_name in config["books"]:
            config["books"][book_name]["add_prompt"] = True

    # 保存配置
    save_config(config)
    logger.info(f"Config updated. Marked {len(books_processed)} books as add_prompt.")


if __name__ == "__main__":
    main()
