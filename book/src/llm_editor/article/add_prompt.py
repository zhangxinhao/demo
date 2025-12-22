"""
文章提示词添加模块

遍历 data/article/txt 目录下的 txt 文件，
在文件末尾添加提示词后保存到 data/article/prompt_txt 目录
"""

import re
from pathlib import Path


def is_chinese_document(text: str, threshold: float = 0.3) -> bool:
    """
    判断文档是否为中文文档
    
    通过计算中文字符占总字符的比例来判断
    
    Args:
        text: 文本内容
        threshold: 中文字符比例阈值，超过此值视为中文文档
    
    Returns:
        True 表示中文文档，False 表示英文文档
    """
    if not text:
        return False
    
    # 匹配中文字符（包括中文标点）
    chinese_pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
    chinese_chars = chinese_pattern.findall(text)
    
    # 计算中文字符比例
    total_chars = len(text.replace(' ', '').replace('\n', ''))
    if total_chars == 0:
        return False
    
    chinese_ratio = len(chinese_chars) / total_chars
    return chinese_ratio >= threshold


def count_words(text: str) -> int:
    """
    统计英文文档的单词数
    
    Args:
        text: 文本内容
    
    Returns:
        单词数量
    """
    # 使用正则匹配单词（字母数字组成的序列）
    words = re.findall(r'\b[a-zA-Z0-9]+\b', text)
    return len(words)


def count_chars(text: str) -> int:
    """
    统计中文文档的字符数（不含空白字符）
    
    Args:
        text: 文本内容
    
    Returns:
        字符数量
    """
    # 移除空白字符后计算长度
    return len(text.replace(' ', '').replace('\n', '').replace('\t', ''))


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
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent.parent
    
    # 定义路径
    input_dir = project_root / "data" / "article" / "txt"
    output_dir = project_root / "data" / "article" / "prompt_txt"
    prompt_dir = project_root / "data" / "prompt"
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 选择提示词文件
    prompt_file = prompt_dir / ("link.txt" if use_link_prompt else "nolink.txt")
    prompt_type = "link（保留链接）" if use_link_prompt else "nolink（删除链接）"
    
    # 读取提示词
    if not prompt_file.exists():
        print(f"错误：提示词文件不存在 - {prompt_file}")
        return
    
    prompt_content = prompt_file.read_text(encoding="utf-8")
    
    print(f"使用提示词模板: {prompt_type}")
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print("-" * 50)
    
    # 遍历输入目录下的所有 txt 文件
    txt_files = list(input_dir.glob("*.txt"))
    
    if not txt_files:
        print("未找到任何 txt 文件")
        return
    
    for txt_file in txt_files:
        # 读取原始内容
        content = txt_file.read_text(encoding="utf-8")
        
        # 判断文档语言并统计
        is_chinese = is_chinese_document(content)
        
        if is_chinese:
            char_count = count_chars(content)
            lang_info = f"中文文档，字符数: {char_count}"
        else:
            word_count = count_words(content)
            lang_info = f"英文文档，单词数: {word_count}"
        
        print(f"处理文件: {txt_file.name} - {lang_info}")
        
        # 在末尾添加提示词
        new_content = content + prompt_content
        
        # 保存到输出目录
        output_file = output_dir / txt_file.name
        output_file.write_text(new_content, encoding="utf-8")
        print(f"  -> 已保存到: {output_file.name}")
    
    print("-" * 50)
    print(f"处理完成，共处理 {len(txt_files)} 个文件")


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

