"""
从 srt/txt 字幕文件中提取纯文本
遍历 data/subtitle/srt 目录下的 srt 和 txt 文件
在 data/subtitle/txt 目录下生成对应名称的 txt 文件
"""

import re
from pathlib import Path

from common import get_logger, PathType, get_path_manager
from llm_editor.utils import (
    ensure_dir,
    write_file,
)

logger = get_logger("subtitle_extract")


# ==================== SRT 格式处理 ====================

def is_srt_time_line(line: str) -> bool:
    """判断是否为 SRT 时间行，格式如: 0:0:18,24 --> 0:0:19,74"""
    time_pattern = r'^\d+:\d+:\d+[,\.]\d+\s*-->\s*\d+:\d+:\d+[,\.]\d+$'
    return bool(re.match(time_pattern, line.strip()))


def is_sequence_number(line: str) -> bool:
    """判断是否为序号行，纯数字行"""
    return line.strip().isdigit()


def extract_text_from_srt(srt_path: Path) -> list[str]:
    """
    从 srt 文件中提取字幕文本
    
    Args:
        srt_path: srt 文件路径
        
    Returns:
        字幕文本列表
    """
    subtitles = []

    with open(srt_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行、序号行、时间行
            if not line:
                continue
            if is_sequence_number(line):
                continue
            if is_srt_time_line(line):
                continue
            # 剩下的是字幕文本
            subtitles.append(line)

    return subtitles


# ==================== TXT 格式处理 ====================

def is_speaker_line(line: str) -> bool:
    """
    判断是否为发言人时间行，格式如: 发言人1   00:17
    
    Args:
        line: 待检测的行
        
    Returns:
        是否为发言人行
    """
    # 匹配 "发言人X   时间戳" 格式
    speaker_pattern = r'^发言人\d+\s+\d+:\d+'
    return bool(re.match(speaker_pattern, line.strip()))


def is_metadata_line(line: str, line_number: int) -> bool:
    """
    判断是否为元数据行（标题行、日期行等）
    
    Args:
        line: 待检测的行
        line_number: 行号（从1开始）
        
    Returns:
        是否为元数据行
    """
    # 前两行通常是标题和日期
    if line_number <= 2:
        return True

    # 日期格式判断: 如 "2026年01月04日 20:20"
    date_pattern = r'^\d{4}年\d{2}月\d{2}日\s+\d+:\d+'
    if re.match(date_pattern, line.strip()):
        return True

    return False


def extract_text_from_txt_subtitle(txt_path: Path) -> list[str]:
    """
    从 txt 字幕文件中提取纯文本
    
    txt 字幕文件格式:
    - 第一行: 标题信息
    - 第二行: 日期
    - 后续: "发言人X   时间戳" 行 + 字幕文本
    
    Args:
        txt_path: txt 字幕文件路径
        
    Returns:
        字幕文本列表
    """
    subtitles = []

    with open(txt_path, 'r', encoding='utf-8') as f:
        line_number = 0
        for line in f:
            line_number += 1
            line = line.strip()

            # 跳过空行
            if not line:
                continue

            # 跳过元数据行（标题、日期）
            if is_metadata_line(line, line_number):
                continue

            # 跳过发言人时间行
            if is_speaker_line(line):
                continue

            # 剩下的是字幕文本
            subtitles.append(line)

    return subtitles


# ==================== 通用处理逻辑 ====================

def process_subtitle_files(src_dir: Path, txt_dir: Path) -> None:
    """
    处理字幕目录下的所有 srt 和 txt 文件，生成对应的纯文本文件
    
    Args:
        src_dir: 字幕源文件目录
        txt_dir: txt 输出目录
    """
    # 确保输出目录存在
    ensure_dir(txt_dir)

    # 遍历所有 srt 文件
    srt_files = list(src_dir.glob('*.srt'))
    # 遍历所有 txt 字幕文件
    txt_subtitle_files = list(src_dir.glob('*.txt'))

    total_files = len(srt_files) + len(txt_subtitle_files)
    if total_files == 0:
        logger.warning(f"No subtitle files found in {src_dir}")
        return

    logger.info(f"Found {len(srt_files)} SRT files and {len(txt_subtitle_files)} TXT files")

    # 处理 srt 文件
    for srt_file in srt_files:
        logger.info(f"Processing SRT: {srt_file.name}")

        # 提取字幕文本
        subtitles = extract_text_from_srt(srt_file)

        # 生成对应的 txt 文件名
        output_file = txt_dir / f"{srt_file.stem}.txt"

        # 写入 txt 文件
        content = '\n'.join(subtitles) + '\n'
        write_file(output_file, content)

        logger.info(f"  -> Generated: {output_file.name} ({len(subtitles)} lines)")

    # 处理 txt 字幕文件
    for txt_file in txt_subtitle_files:
        logger.info(f"Processing TXT: {txt_file.name}")

        # 提取字幕文本
        subtitles = extract_text_from_txt_subtitle(txt_file)

        # 生成对应的 txt 文件名（保持同名，但输出到不同目录）
        output_file = txt_dir / txt_file.name

        # 写入 txt 文件
        content = '\n'.join(subtitles) + '\n'
        write_file(output_file, content)

        logger.info(f"  -> Generated: {output_file.name} ({len(subtitles)} lines)")


def main() -> None:
    """主函数"""
    # 使用统一的路径管理
    pm = get_path_manager()
    src_dir = pm.get_dir_path(PathType.SUBTITLE_SRT)
    txt_dir = pm.get_dir_path(PathType.SUBTITLE_TXT)

    logger.info(f"Source directory: {src_dir}")
    logger.info(f"Output directory: {txt_dir}")
    logger.info("-" * 50)

    process_subtitle_files(src_dir, txt_dir)

    logger.info("-" * 50)
    logger.info("Done!")


if __name__ == '__main__':
    main()
