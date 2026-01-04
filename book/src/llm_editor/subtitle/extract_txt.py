"""
从 srt 字幕文件中提取纯文本
遍历 data/subtitle/srt 目录下的 srt 文件
在 data/subtitle/txt 目录下生成对应名称的 txt 文件
"""

import re
from pathlib import Path


def is_time_line(line: str) -> bool:
    """判断是否为时间行，格式如: 0:0:18,24 --> 0:0:19,74"""
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
            if is_time_line(line):
                continue
            # 剩下的是字幕文本
            subtitles.append(line)

    return subtitles


def process_srt_files(srt_dir: Path, txt_dir: Path) -> None:
    """
    处理 srt 目录下的所有文件，生成对应的 txt 文件
    
    Args:
        srt_dir: srt 文件目录
        txt_dir: txt 输出目录
    """
    # 确保输出目录存在
    txt_dir.mkdir(parents=True, exist_ok=True)

    # 遍历所有 srt 文件
    srt_files = list(srt_dir.glob('*.srt'))

    if not srt_files:
        print(f"No srt files found in {srt_dir}")
        return

    for srt_file in srt_files:
        print(f"Processing: {srt_file.name}")

        # 提取字幕文本
        subtitles = extract_text_from_srt(srt_file)

        # 生成对应的 txt 文件名
        txt_file = txt_dir / f"{srt_file.stem}.txt"

        # 写入 txt 文件
        with open(txt_file, 'w', encoding='utf-8') as f:
            for subtitle in subtitles:
                f.write(subtitle + '\n')

        print(f"  -> Generated: {txt_file.name} ({len(subtitles)} lines)")


def main():
    """主函数"""
    # 获取项目根目录 (src 的上级目录)
    project_root = Path(__file__).parent.parent.parent.parent

    srt_dir = project_root / 'data' / 'subtitle' / 'srt'
    txt_dir = project_root / 'data' / 'subtitle' / 'txt'

    print(f"SRT directory: {srt_dir}")
    print(f"TXT directory: {txt_dir}")
    print("-" * 50)

    process_srt_files(srt_dir, txt_dir)

    print("-" * 50)
    print("Done!")


if __name__ == '__main__':
    main()
