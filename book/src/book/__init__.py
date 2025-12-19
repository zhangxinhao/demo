"""
Book 处理模块
提供书籍切分、提示词添加、LLM 处理等功能
"""

from book.add_prompt import (
    append_prompt_to_file,
    process_book as prompt_process_book,
)
from book.llm_process import (
    load_env,
    get_books_to_process,
    call_llm,
    process_single_file,
    process_book as llm_process_book,
)
from book.split_book import (
    get_book_files,
    get_catalog_file,
    split_book_by_catalog,
    save_chapters,
    process_book as split_process_book,
)
from book.utils import (
    # 路径管理
    get_project_root,
    get_data_dir,
    get_config_path,
    get_txt_dir,
    get_book_dir,
    get_catalog_dir,
    get_prompt_dir,
    get_md_output_dir,
    get_src_dir,
    # 配置管理
    load_config,
    save_config,
    # 文件 IO
    read_file,
    write_file,
    append_file,
    read_lines,
    ensure_dir,
    # 日志
    setup_logger,
    get_logger,
    # 类型
    BookConfig,
    AppConfig,
)

__all__ = [
    # utils - 路径管理
    "get_project_root",
    "get_data_dir",
    "get_config_path",
    "get_txt_dir",
    "get_book_dir",
    "get_catalog_dir",
    "get_prompt_dir",
    "get_md_output_dir",
    "get_src_dir",
    # utils - 配置管理
    "load_config",
    "save_config",
    # utils - 文件 IO
    "read_file",
    "write_file",
    "append_file",
    "read_lines",
    "ensure_dir",
    # utils - 日志
    "setup_logger",
    "get_logger",
    # utils - 类型
    "BookConfig",
    "AppConfig",
    # split_book
    "get_book_files",
    "get_catalog_file",
    "split_book_by_catalog",
    "save_chapters",
    "split_process_book",
    # add_prompt
    "append_prompt_to_file",
    "prompt_process_book",
    # llm_process
    "load_env",
    "get_books_to_process",
    "call_llm",
    "process_single_file",
    "llm_process_book",
]
