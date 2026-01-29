# -*- coding: utf-8 -*-
"""
中文书籍处理模块

提供中文书籍的章节分割等功能
"""

from llm_editor.epub.chinese.split_chapters import (
    split_book_chapters,
    split_mingchao_book,
    extract_chapters,
    is_chapter_title,
)

__all__ = [
    "split_book_chapters",
    "split_mingchao_book",
    "extract_chapters",
    "is_chapter_title",
]
