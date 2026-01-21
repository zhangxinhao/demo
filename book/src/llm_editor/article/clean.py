"""
文章数据清洗模块

清洗 article 相关目录的数据：
1. 清空 data/article/txt 目录下所有 txt 文件的内容
2. 删除 data/article/prompt_txt 目录下所有的 txt 文件
3. 删除 data/article/md 目录下所有的 md 文件
"""

from common import get_logger, PathType, get_path_manager
from llm_editor.utils import (
    write_file,
)

# 初始化 logger
logger = get_logger("article_clean")


def clear_txt_contents() -> int:
    """
    清空 data/article/txt 目录下所有 txt 文件的内容
    
    Returns:
        处理的文件数量
    """
    txt_dir = get_path_manager().get_dir_path(PathType.ARTICLE_TXT)

    if not txt_dir.exists():
        logger.warning(f"Directory not found: {txt_dir}")
        return 0

    txt_files = list(txt_dir.glob("*.txt"))

    if not txt_files:
        logger.info("No txt files to clear in txt directory")
        return 0

    cleared_count = 0
    for txt_file in txt_files:
        # 清空文件内容（写入空字符串）
        write_file(txt_file, "")
        logger.info(f"Cleared content: {txt_file.name}")
        cleared_count += 1

    return cleared_count


def delete_prompt_txt_files() -> int:
    """
    删除 data/article/prompt_txt 目录下所有的 txt 文件
    
    Returns:
        删除的文件数量
    """
    prompt_txt_dir = get_path_manager().get_dir_path(PathType.ARTICLE_PROMPT_TXT)

    if not prompt_txt_dir.exists():
        logger.warning(f"Directory not found: {prompt_txt_dir}")
        return 0

    txt_files = list(prompt_txt_dir.glob("*.txt"))

    if not txt_files:
        logger.info("No txt files to delete in prompt_txt directory")
        return 0

    deleted_count = 0
    for txt_file in txt_files:
        txt_file.unlink()
        logger.info(f"Deleted file: {txt_file.name}")
        deleted_count += 1

    return deleted_count


def delete_md_files() -> int:
    """
    删除 data/article/md 目录下所有的 md 文件
    
    Returns:
        删除的文件数量
    """
    md_dir = get_path_manager().get_dir_path(PathType.ARTICLE_MD)

    if not md_dir.exists():
        logger.warning(f"Directory not found: {md_dir}")
        return 0

    md_files = list(md_dir.glob("*.md"))

    if not md_files:
        logger.info("No md files to delete in md directory")
        return 0

    deleted_count = 0
    for md_file in md_files:
        md_file.unlink()
        logger.info(f"Deleted file: {md_file.name}")
        deleted_count += 1

    return deleted_count


def clean_all() -> None:
    """
    执行完整的清洗流程
    
    1. 清空 txt 目录下所有 txt 文件的内容
    2. 删除 prompt_txt 目录下所有 txt 文件
    3. 删除 md 目录下所有 md 文件
    """
    logger.info("=" * 50)
    logger.info("Starting article data cleaning...")
    logger.info("=" * 50)

    # 1. 清空 txt 文件内容
    logger.info("[Step 1] Clearing txt file contents...")
    cleared_count = clear_txt_contents()
    logger.info(f"Cleared {cleared_count} txt file(s) content")
    logger.info("-" * 50)

    # 2. 删除 prompt_txt 文件
    logger.info("[Step 2] Deleting prompt_txt files...")
    prompt_deleted_count = delete_prompt_txt_files()
    logger.info(f"Deleted {prompt_deleted_count} prompt_txt file(s)")
    logger.info("-" * 50)

    # 3. 删除 md 文件
    logger.info("[Step 3] Deleting md files...")
    md_deleted_count = delete_md_files()
    logger.info(f"Deleted {md_deleted_count} md file(s)")
    logger.info("-" * 50)

    # 汇总
    logger.info("=" * 50)
    logger.info("Cleaning complete!")
    logger.info(f"  - Cleared txt content: {cleared_count} file(s)")
    logger.info(f"  - Deleted prompt_txt: {prompt_deleted_count} file(s)")
    logger.info(f"  - Deleted md: {md_deleted_count} file(s)")
    logger.info("=" * 50)


def main() -> None:
    """主函数"""
    clean_all()


if __name__ == "__main__":
    main()
