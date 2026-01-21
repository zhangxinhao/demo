"""
大模型处理模块（书籍版）
读取配置文件，遍历书籍的txt文件，调用大模型进行处理
"""

from pathlib import Path

from common import get_logger
from llm_editor.base import LLMClient, BatchFileProcessor, ProcessResult
from llm_editor.utils import (
    get_txt_dir,
    get_md_output_dir,
    load_config,
    save_config,
    read_file,
    write_file,
    AppConfig,
    BookConfig,
)

# 初始化 logger
logger = get_logger("book_llm_process")


def get_books_to_process(books_config: dict[str, BookConfig]) -> list[str]:
    """
    获取需要处理的书籍列表
    筛选条件：add_prompt=true 且 llm_process=false
    
    Args:
        books_config: 书籍配置字典
    
    Returns:
        需要处理的书籍名称列表
    """
    books_to_process: list[str] = []
    for book_name, book_info in books_config.items():
        add_prompt = book_info.get("add_prompt", False)
        llm_processed = book_info.get("llm_process", False)

        if add_prompt and not llm_processed:
            books_to_process.append(book_name)

    return books_to_process


class BookLLMProcessor(BatchFileProcessor):
    """
    书籍 LLM 处理器
    
    继承 BatchFileProcessor，实现书籍章节的批量 LLM 处理逻辑
    """
    
    def __init__(
        self,
        llm_client: LLMClient,
        input_dir: Path,
        output_dir: Path,
        num_threads: int = 2
    ):
        """
        初始化书籍处理器
        
        Args:
            llm_client: LLM 客户端
            input_dir: 输入目录
            output_dir: 输出目录
            num_threads: 并发线程数
        """
        super().__init__(input_dir, output_dir, num_threads, file_pattern="*.txt")
        self.llm_client = llm_client
    
    def process_file(self, input_file: Path) -> ProcessResult:
        """
        处理单个书籍章节文件
        
        Args:
            input_file: 输入文件路径
        
        Returns:
            ProcessResult 处理结果
        """
        file_name = input_file.name
        try:
            # 读取文件内容作为提示词
            prompt = read_file(input_file)
            
            logger.info(f"Processing file: {file_name}")
            
            # 调用大模型
            response = self.llm_client.call(prompt, file_name)
            
            # 保存结果到 md 文件
            output_file = self.output_dir / f"{input_file.stem}.md"
            write_file(output_file, response.content)
            
            logger.info(f"Completed: {file_name} -> {output_file.name} (took {response.elapsed_time:.2f}s)")
            
            return ProcessResult(
                file_name=file_name,
                success=True,
                elapsed_time=response.elapsed_time,
                prompt_tokens=response.prompt_tokens,
                completion_tokens=response.completion_tokens
            )
        except Exception as e:
            logger.error(f"Failed to process {file_name}: {e}")
            return ProcessResult(
                file_name=file_name,
                success=False,
                error_message=str(e)
            )


def process_book(
    llm_client: LLMClient,
    book_name: str,
    txt_dir: Path,
    output_base_dir: Path,
    num_threads: int
) -> bool:
    """
    处理单本书籍的所有章节
    
    Args:
        llm_client: LLM 客户端
        book_name: 书籍名称
        txt_dir: txt 文件基础目录
        output_base_dir: 输出基础目录
        num_threads: 并发线程数
    
    Returns:
        是否全部处理成功
    """
    book_txt_dir = txt_dir / book_name
    output_dir = output_base_dir / book_name
    
    if not book_txt_dir.exists():
        logger.warning(f"Directory not found for book '{book_name}': {book_txt_dir}")
        return False
    
    logger.info(f"Processing book: {book_name}")
    
    # 创建处理器并执行
    processor = BookLLMProcessor(
        llm_client=llm_client,
        input_dir=book_txt_dir,
        output_dir=output_dir,
        num_threads=num_threads
    )
    
    result = processor.run()
    result.log_summary(f"Book '{book_name}'")
    
    return result.all_success


def main() -> None:
    """主函数"""
    # 路径配置
    txt_dir = get_txt_dir()
    output_dir = get_md_output_dir()

    # 创建 LLM 客户端
    logger.info("Initializing LLM client...")
    llm_client = LLMClient.from_env()

    # 加载配置
    logger.info("Loading config...")
    config: AppConfig = load_config()
    num_threads = config.get("num_threads", 2)
    books_config = config.get("books", {})

    # 获取需要处理的书籍
    books_to_process = get_books_to_process(books_config)

    if not books_to_process:
        logger.info("No books to process (requires add_prompt=true and llm_process=false)")
        return

    logger.info(f"Found {len(books_to_process)} books to process: {books_to_process}")

    # 处理每本书
    processed_books: list[str] = []
    for book_name in books_to_process:
        success = process_book(
            llm_client=llm_client,
            book_name=book_name,
            txt_dir=txt_dir,
            output_base_dir=output_dir,
            num_threads=num_threads
        )

        if success:
            processed_books.append(book_name)

    # 更新配置，标记已处理的书籍
    for book_name in processed_books:
        if book_name in config["books"]:
            config["books"][book_name]["llm_process"] = True

    # 保存配置
    save_config(config)
    logger.info(f"Config updated. Marked {len(processed_books)} books as llm_process=true")


if __name__ == "__main__":
    main()
