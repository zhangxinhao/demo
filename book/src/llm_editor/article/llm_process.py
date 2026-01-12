"""
大模型处理模块（文章版）
遍历 data/article/prompt_txt 目录下的 txt 文件，调用大模型进行处理
输出 md 文件到 data/article/md 目录
"""

from pathlib import Path

from llm_editor.base import LLMClient, BatchFileProcessor, ProcessResult
from llm_editor.utils import (
    get_article_prompt_txt_dir,
    get_article_md_dir,
    read_file,
    write_file,
    get_logger,
)

# 初始化 logger
logger = get_logger("article_llm_process")


class ArticleLLMProcessor(BatchFileProcessor):
    """
    文章 LLM 处理器
    
    继承 BatchFileProcessor，实现文章的批量 LLM 处理逻辑
    """
    
    def __init__(
        self,
        llm_client: LLMClient,
        input_dir: Path,
        output_dir: Path,
        num_threads: int = 2
    ):
        """
        初始化文章处理器
        
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
        处理单个文章文件
        
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


def main() -> None:
    """主函数"""
    # 路径配置
    input_dir = get_article_prompt_txt_dir()
    output_dir = get_article_md_dir()
    
    # 创建 LLM 客户端
    logger.info("Initializing LLM client...")
    llm_client = LLMClient.from_env()
    num_threads = llm_client.get_num_threads()
    
    logger.info(f"Input directory: {input_dir}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Using {num_threads} threads")
    
    # 创建处理器并执行
    processor = ArticleLLMProcessor(
        llm_client=llm_client,
        input_dir=input_dir,
        output_dir=output_dir,
        num_threads=num_threads
    )
    
    result = processor.run()
    result.log_summary("Articles")
    
    if result.all_success:
        logger.info("All articles processed successfully!")
    else:
        logger.warning("Some articles failed to process")


if __name__ == "__main__":
    main()
