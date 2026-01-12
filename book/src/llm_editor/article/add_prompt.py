"""
文章提示词添加模块

遍历 data/article/txt 目录下的 txt 文件，
在文件末尾添加提示词后保存到 data/article/prompt_txt 目录
"""

from llm_editor.utils import (
    get_article_txt_dir,
    get_article_prompt_txt_dir,
    get_prompt_dir,
    read_file,
    write_file,
    ensure_dir,
    is_chinese_document,
    count_words,
    count_chars,
    get_logger,
)

# 初始化 logger
logger = get_logger("article_add_prompt")


def add_prompt_to_articles(use_link_prompt: bool = True) -> None:
    """
    为文章添加提示词
    
    遍历 data/article/txt 目录下的所有 txt 文件，
    在每个文件末尾添加指定的提示词，
    保存到 data/article/prompt_txt 目录
    
    Args:
        use_link_prompt: True 使用 link.txt 提示词（保留链接），
                        False 使用 nolink.txt 提示词（删除链接）
    """
    # 使用统一的路径管理
    input_dir = get_article_txt_dir()
    output_dir = get_article_prompt_txt_dir()
    prompt_dir = get_prompt_dir()
    
    # 确保输出目录存在
    ensure_dir(output_dir)
    
    # 选择提示词文件
    prompt_file = prompt_dir / ("link.txt" if use_link_prompt else "nolink.txt")
    prompt_type = "link（保留链接）" if use_link_prompt else "nolink（删除链接）"
    
    # 读取提示词
    if not prompt_file.exists():
        logger.error(f"Prompt file not found: {prompt_file}")
        return
    
    prompt_content = read_file(prompt_file)
    
    logger.info(f"Using prompt template: {prompt_type}")
    logger.info(f"Input directory: {input_dir}")
    logger.info(f"Output directory: {output_dir}")
    logger.info("-" * 50)
    
    # 遍历输入目录下的所有 txt 文件
    txt_files = list(input_dir.glob("*.txt"))
    
    if not txt_files:
        logger.warning("No txt files found")
        return
    
    processed_count = 0
    for txt_file in txt_files:
        # 读取原始内容
        content = read_file(txt_file)
        
        # 跳过空文件
        if not content.strip():
            logger.info(f"Skipping empty file: {txt_file.name}")
            continue
        
        # 判断文档语言并统计
        is_chinese = is_chinese_document(content)
        
        if is_chinese:
            char_count = count_chars(content)
            lang_info = f"Chinese document, chars: {char_count}"
        else:
            word_count = count_words(content)
            lang_info = f"English document, words: {word_count}"
        
        logger.info(f"Processing file: {txt_file.name} - {lang_info}")
        
        # 在末尾添加提示词
        new_content = content + prompt_content
        
        # 保存到输出目录
        output_file = output_dir / txt_file.name
        write_file(output_file, new_content)
        logger.info(f"  -> Saved to: {output_file.name}")
        processed_count += 1
    
    logger.info("-" * 50)
    logger.info(f"Processing complete, processed {processed_count} files")


def main(use_link: bool = True) -> None:
    """
    主函数
    
    Args:
        use_link: True 使用保留链接的提示词，False 使用删除链接的提示词
    """
    add_prompt_to_articles(use_link_prompt=use_link)


if __name__ == "__main__":
    # 控制使用哪种提示词
    # True: 使用 link.txt（保留链接）
    # False: 使用 nolink.txt（删除链接）
    USE_LINK_PROMPT = True
    
    main(use_link=USE_LINK_PROMPT)
