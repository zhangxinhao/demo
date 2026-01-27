"""
根据 Markdown 标题切分书籍文件，生成多个 TXT 文件

功能：
1. 遍历未处理过的 md 文件
2. 识别中文还是英文文档
3. 输出字符数或词数
4. 识别 # 开头的标题，打印每个标题后的字符数量
5. 根据标题切分文档，保证每个文件少于 1w 字符
6. 输出到 txt 目录下同名目录
7. 被选中的切分标题汇总到 catalog 目录下的同名文件
"""

import re
from dataclasses import dataclass
from pathlib import Path

from common import get_logger, PathType, get_path_manager
from llm_editor.utils import (
    read_file,
    write_file,
    ensure_dir,
    is_chinese_document,
    count_words,
    count_chars,
)

# 初始化 logger
logger = get_logger("split_by_markdown")

# 中文文档每个切分文件的最大字符数
MAX_CHARS_PER_FILE_CN = 10000
# 英文文档每个切分文件的最大词数
MAX_WORDS_PER_FILE_EN = 5000


@dataclass
class Section:
    """标题段落"""
    title: str  # 标题文本（包含 # 前缀）
    level: int  # 标题级别（# 的数量）
    content: str  # 标题下的内容（不包含子标题）
    full_content: str  # 标题下的完整内容（包含子标题和其内容）
    char_count: int  # 字符数（中文使用）
    word_count: int  # 词数（英文使用）


def get_md_files(book_dir: Path) -> list[Path]:
    """获取 book 目录下所有的 md 文件"""
    return list(book_dir.glob("*.md"))


def get_unprocessed_files(book_dir: Path, output_dir: Path) -> list[Path]:
    """获取未处理过的 md 文件（输出目录不存在）"""
    md_files = get_md_files(book_dir)
    unprocessed = []
    for md_file in md_files:
        book_name = md_file.stem
        if not (output_dir / book_name).exists():
            unprocessed.append(md_file)
    return unprocessed


def parse_markdown_sections(content: str) -> list[Section]:
    """
    解析 Markdown 内容，提取所有标题及其内容
    
    Args:
        content: Markdown 文件内容
        
    Returns:
        Section 列表
    """
    # 匹配 markdown 标题（以 # 开头的行）
    # 需要匹配行首或换行后的 #
    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

    # 找到所有标题
    matches = list(header_pattern.finditer(content))

    if not matches:
        return []

    sections: list[Section] = []

    for i, match in enumerate(matches):
        level = len(match.group(1))  # # 的数量
        title_text = match.group(2).strip()
        title = f"{'#' * level} {title_text}"

        # 当前标题的起始位置
        start_pos = match.start()

        # 当前标题内容的起始位置（标题行之后）
        content_start = match.end()

        # 找到下一个同级或更高级标题的位置作为结束
        end_pos = len(content)
        for j in range(i + 1, len(matches)):
            next_match = matches[j]
            next_level = len(next_match.group(1))
            # 遇到同级或更高级标题时结束
            if next_level <= level:
                end_pos = next_match.start()
                break

        # 找到下一个标题位置（任意级别）作为直接内容的结束
        direct_content_end = len(content)
        if i + 1 < len(matches):
            direct_content_end = matches[i + 1].start()

        # 直接内容（不包含子标题）
        direct_content = content[content_start:direct_content_end].strip()

        # 完整内容（包含子标题及其内容）
        full_content = content[start_pos:end_pos].strip()

        # 计算字符数和词数
        char_count = count_chars(full_content)
        word_count = count_words(full_content)

        sections.append(Section(
            title=title,
            level=level,
            content=direct_content,
            full_content=full_content,
            char_count=char_count,
            word_count=word_count,
        ))

    return sections


def print_section_stats(sections: list[Section], is_chinese: bool) -> None:
    """打印每个标题的统计信息"""
    logger.info("=== Section Statistics ===")
    for section in sections:
        indent = "  " * (section.level - 1)
        if is_chinese:
            logger.info(f"{indent}{section.title}: {section.char_count} chars")
        else:
            logger.info(f"{indent}{section.title}: {section.word_count} words")


def split_by_limit(sections: list[Section], is_chinese: bool) -> list[tuple[list[str], str]]:
    """
    根据限制切分文档（中文按字符数，英文按词数）
    
    Args:
        sections: Section 列表
        is_chinese: 是否为中文文档
        
    Returns:
        切分结果列表，每个元素是 (切分标题列表, 合并内容)
    """
    if not sections:
        return []

    # 根据语言选择限制值
    max_limit = MAX_CHARS_PER_FILE_CN if is_chinese else MAX_WORDS_PER_FILE_EN

    # 获取所有一级标题（或最高级标题）
    min_level = min(s.level for s in sections)
    top_level_sections = [s for s in sections if s.level == min_level]

    if not top_level_sections:
        # 如果没有顶级标题，将所有内容作为一个文件
        all_content = "\n\n".join(s.full_content for s in sections)
        titles = [s.title for s in sections if s.level == min(s.level for s in sections)]
        return [(titles, all_content)]

    result: list[tuple[list[str], str]] = []
    current_titles: list[str] = []
    current_content: list[str] = []
    current_count = 0

    for section in top_level_sections:
        # 根据语言选择计数方式
        section_count = section.char_count if is_chinese else section.word_count

        # 如果单个 section 超过最大限制，需要特殊处理
        if section_count > max_limit:
            # 先保存当前累积的内容
            if current_content:
                result.append((current_titles.copy(), "\n\n".join(current_content)))
                current_titles.clear()
                current_content.clear()
                current_count = 0

            # 尝试进一步拆分这个大 section
            sub_sections = [s for s in sections
                            if s.full_content in section.full_content and s.level > section.level]

            # 使用子标题或段落进行拆分
            sub_result = _split_large_section(section, sub_sections, is_chinese)
            result.extend(sub_result)

        # 如果加上这个 section 会超过限制
        elif current_count + section_count > max_limit and current_content:
            # 保存当前内容，开始新的一组
            result.append((current_titles.copy(), "\n\n".join(current_content)))
            current_titles = [section.title]
            current_content = [section.full_content]
            current_count = section_count

        else:
            # 累加到当前组
            current_titles.append(section.title)
            current_content.append(section.full_content)
            current_count += section_count

    # 处理最后一组
    if current_content:
        result.append((current_titles.copy(), "\n\n".join(current_content)))

    return result


def _split_large_section(section: Section, sub_sections: list[Section], is_chinese: bool) -> list[tuple[list[str], str]]:
    """
    拆分过大的 section
    
    Args:
        section: 需要拆分的大 section
        sub_sections: 其子 section 列表
        is_chinese: 是否为中文文档
        
    Returns:
        拆分结果
    """
    result: list[tuple[list[str], str]] = []
    max_limit = MAX_CHARS_PER_FILE_CN if is_chinese else MAX_WORDS_PER_FILE_EN

    # 获取子 section 中的最高级别
    if not sub_sections:
        # 没有子标题，按段落拆分
        return _split_by_paragraphs(section, is_chinese)

    min_sub_level = min(s.level for s in sub_sections)
    top_sub_sections = [s for s in sub_sections if s.level == min_sub_level]

    current_titles: list[str] = []
    current_content: list[str] = []
    current_count = 0

    # 添加父标题的直接内容
    header_content = section.content
    if header_content:
        header_with_title = f"{section.title}\n\n{header_content}"
    else:
        header_with_title = section.title

    for sub_section in top_sub_sections:
        sub_count = sub_section.char_count if is_chinese else sub_section.word_count

        if current_count + sub_count > max_limit and current_content:
            # 保存当前内容
            full_content = header_with_title + "\n\n" + "\n\n".join(
                current_content) if current_content else header_with_title
            result.append(([section.title] + current_titles, full_content))
            current_titles = [sub_section.title]
            current_content = [sub_section.full_content]
            current_count = sub_count
        else:
            current_titles.append(sub_section.title)
            current_content.append(sub_section.full_content)
            current_count += sub_count

    # 处理最后一组
    if current_content:
        full_content = header_with_title + "\n\n" + "\n\n".join(current_content)
        result.append(([section.title] + current_titles, full_content))

    return result


def _split_by_paragraphs(section: Section, is_chinese: bool) -> list[tuple[list[str], str]]:
    """
    按段落拆分过大的 section（没有子标题时使用）
    
    Args:
        section: 需要拆分的 section
        is_chinese: 是否为中文文档
        
    Returns:
        拆分结果
    """
    result: list[tuple[list[str], str]] = []
    max_limit = MAX_CHARS_PER_FILE_CN if is_chinese else MAX_WORDS_PER_FILE_EN

    # 将内容按段落分割（双换行符分隔）
    paragraphs = re.split(r'\n\s*\n', section.full_content)

    if not paragraphs:
        return [([section.title], section.full_content)]

    current_content: list[str] = []
    current_count = 0
    part_num = 1

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # 根据语言选择计数方式
        para_count = count_chars(para) if is_chinese else count_words(para)

        # 如果单个段落超过限制，强制添加（无法进一步拆分）
        if para_count > max_limit:
            if current_content:
                # 先保存当前内容
                content = "\n\n".join(current_content)
                result.append(([f"{section.title} (Part {part_num})"], content))
                part_num += 1
                current_content = []
                current_count = 0
            # 添加超大段落
            result.append(([f"{section.title} (Part {part_num})"], para))
            part_num += 1
            continue

        # 如果加上当前段落会超过限制
        if current_count + para_count > max_limit and current_content:
            # 保存当前内容，开始新的一组
            content = "\n\n".join(current_content)
            result.append(([f"{section.title} (Part {part_num})"], content))
            part_num += 1
            current_content = [para]
            current_count = para_count
        else:
            current_content.append(para)
            current_count += para_count

    # 处理最后一组
    if current_content:
        content = "\n\n".join(current_content)
        # 如果只有一部分，不加 Part 后缀
        if part_num == 1:
            result.append(([section.title], content))
        else:
            result.append(([f"{section.title} (Part {part_num})"], content))

    logger.info(f"Split large section '{section.title}' into {len(result)} parts by paragraphs")
    return result


def save_split_files(output_dir: Path, splits: list[tuple[list[str], str]], is_chinese: bool) -> list[str]:
    """
    保存切分后的文件
    
    Args:
        output_dir: 输出目录
        splits: 切分结果列表
        is_chinese: 是否为中文文档
        
    Returns:
        所有切分标题的列表
    """
    all_titles: list[str] = []

    for i, (titles, content) in enumerate(splits, start=1):
        output_file = output_dir / f"{i}.txt"
        write_file(output_file, content)
        if is_chinese:
            logger.info(f"Saved: {output_file}, characters: {count_chars(content)}")
        else:
            logger.info(f"Saved: {output_file}, words: {count_words(content)}")

        # 记录第一个标题作为切分点
        if titles:
            all_titles.append(titles[0])

    return all_titles


def save_catalog(catalog_dir: Path, book_name: str, titles: list[str]) -> None:
    """保存目录文件"""
    catalog_file = catalog_dir / f"{book_name}.txt"
    content = "\n".join(titles)
    write_file(catalog_file, content)
    logger.info(f"Saved catalog: {catalog_file}")


def process_book(book_file: Path, output_base_dir: Path, catalog_dir: Path) -> bool:
    """
    处理单本书籍
    
    Args:
        book_file: 书籍 MD 文件路径
        output_base_dir: 输出基础目录
        catalog_dir: 目录文件输出目录
        
    Returns:
        是否处理成功
    """
    book_name = book_file.stem

    # 检查目标目录是否已存在
    output_dir = output_base_dir / book_name
    if output_dir.exists():
        logger.info(f"Skipping {book_name}: output directory already exists")
        return False

    logger.info(f"Processing book: {book_name}")

    # 读取书籍内容
    content = read_file(book_file)

    # 判断是中文还是英文
    is_chinese = is_chinese_document(content)
    lang = "Chinese" if is_chinese else "English"
    logger.info(f"Document language: {lang}")

    # 输出总字符数/词数
    if is_chinese:
        total_chars = count_chars(content)
        logger.info(f"Total characters: {total_chars}")
    else:
        total_words = count_words(content)
        logger.info(f"Total words: {total_words}")

    # 解析 Markdown 标题
    sections = parse_markdown_sections(content)

    if not sections:
        logger.warning(f"No markdown headers found in {book_name}")
        return False

    logger.info(f"Found {len(sections)} sections")

    # 打印每个标题的统计信息
    print_section_stats(sections, is_chinese)

    # 根据语言限制切分（中文按字符，英文按词数）
    splits = split_by_limit(sections, is_chinese)

    if not splits:
        logger.warning(f"Failed to split {book_name}")
        return False

    logger.info(f"Split into {len(splits)} files")

    # 创建输出目录
    ensure_dir(output_dir)

    # 保存切分文件
    all_titles = save_split_files(output_dir, splits, is_chinese)

    # 保存目录
    save_catalog(catalog_dir, book_name, all_titles)

    logger.info(f"Successfully processed {book_name}")
    return True


def main() -> None:
    """主函数"""
    # 使用路径管理器
    pm = get_path_manager()
    book_dir = pm.get_dir_path(PathType.BOOK_BOOK)
    output_dir = pm.get_dir_path(PathType.BOOK_TXT)
    catalog_dir = pm.get_dir_path(PathType.BOOK_CATALOG)

    logger.info(f"Book directory: {book_dir}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Catalog directory: {catalog_dir}")

    # 检查目录是否存在
    if not book_dir.exists():
        logger.error(f"Book directory not found: {book_dir}")
        return

    # 确保输出目录存在
    ensure_dir(output_dir)
    ensure_dir(catalog_dir)

    # 获取未处理的 md 文件
    unprocessed_files = get_unprocessed_files(book_dir, output_dir)

    if not unprocessed_files:
        logger.info("No unprocessed md files found")
        return

    logger.info(f"Found {len(unprocessed_files)} unprocessed md file(s)")

    # 处理每本书
    success_count = 0
    for book_file in unprocessed_files:
        if process_book(book_file, output_dir, catalog_dir):
            success_count += 1

    logger.info("=== Summary ===")
    logger.info(f"Total unprocessed: {len(unprocessed_files)}")
    logger.info(f"Successfully processed: {success_count}")


if __name__ == "__main__":
    main()
