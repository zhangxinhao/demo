"""
批量文件处理基类模块
提供多线程并发处理文件的通用框架
"""

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

from common import get_logger
from llm_editor.utils import ensure_dir

logger = get_logger("batch_processor")


@dataclass
class ProcessResult:
    """单个文件处理结果"""
    file_name: str
    success: bool
    elapsed_time: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    error_message: str = ""


@dataclass
class BatchResult:
    """批量处理结果"""
    total_files: int = 0
    success_count: int = 0
    fail_count: int = 0
    total_elapsed_time: float = 0.0
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    results: list[ProcessResult] = field(default_factory=list)
    
    @property
    def average_time(self) -> float:
        """平均处理时间"""
        if self.success_count == 0:
            return 0.0
        return self.total_elapsed_time / self.success_count
    
    @property
    def total_tokens(self) -> int:
        """总 token 数"""
        return self.total_prompt_tokens + self.total_completion_tokens
    
    @property
    def all_success(self) -> bool:
        """是否全部成功"""
        return self.fail_count == 0
    
    def add_result(self, result: ProcessResult) -> None:
        """添加处理结果"""
        self.results.append(result)
        if result.success:
            self.success_count += 1
            self.total_elapsed_time += result.elapsed_time
            self.total_prompt_tokens += result.prompt_tokens
            self.total_completion_tokens += result.completion_tokens
        else:
            self.fail_count += 1
    
    def log_summary(self, prefix: str = "") -> None:
        """打印处理结果摘要"""
        log_prefix = f"{prefix} " if prefix else ""
        logger.info(f"{log_prefix}Processing complete: {self.success_count} success, {self.fail_count} failed")
        logger.info(f"{log_prefix}Total LLM time: {self.total_elapsed_time:.2f}s, Average per file: {self.average_time:.2f}s")
        logger.info(
            f"{log_prefix}Total tokens - prompt: {self.total_prompt_tokens}, "
            f"completion: {self.total_completion_tokens}, total: {self.total_tokens}"
        )


class BatchFileProcessor(ABC):
    """
    批量文件处理基类
    
    提供多线程并发处理文件的通用框架。
    子类需要实现 process_file 方法来定义具体的处理逻辑。
    """
    
    def __init__(
        self,
        input_dir: Path,
        output_dir: Path,
        num_threads: int = 2,
        file_pattern: str = "*.txt"
    ):
        """
        初始化批量处理器
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            num_threads: 并发线程数
            file_pattern: 文件匹配模式
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.num_threads = num_threads
        self.file_pattern = file_pattern
    
    @abstractmethod
    def process_file(self, input_file: Path) -> ProcessResult:
        """
        处理单个文件（子类必须实现）
        
        Args:
            input_file: 输入文件路径
        
        Returns:
            ProcessResult 处理结果
        """
        raise NotImplementedError
    
    def get_input_files(self) -> list[Path]:
        """
        获取需要处理的输入文件列表
        
        Returns:
            文件路径列表
        """
        if not self.input_dir.exists():
            logger.warning(f"Input directory not found: {self.input_dir}")
            return []
        
        files = list(self.input_dir.glob(self.file_pattern))
        return sorted(files)
    
    def run(self) -> BatchResult:
        """
        执行批量处理
        
        使用线程池并发处理所有文件
        
        Returns:
            BatchResult 批量处理结果
        """
        # 获取输入文件
        input_files = self.get_input_files()
        
        if not input_files:
            logger.warning(f"No files matching '{self.file_pattern}' found in {self.input_dir}")
            return BatchResult()
        
        # 确保输出目录存在
        ensure_dir(self.output_dir)
        
        logger.info(f"Found {len(input_files)} files to process")
        logger.info(f"Using {self.num_threads} threads")
        
        # 初始化结果
        batch_result = BatchResult(total_files=len(input_files))
        
        # 使用线程池并发处理
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            # 提交所有任务
            futures = {
                executor.submit(self.process_file, input_file): input_file
                for input_file in input_files
            }
            
            # 收集结果
            for future in as_completed(futures):
                input_file = futures[future]
                try:
                    result = future.result()
                    batch_result.add_result(result)
                except Exception as e:
                    logger.error(f"Exception processing {input_file.name}: {e}")
                    batch_result.add_result(ProcessResult(
                        file_name=input_file.name,
                        success=False,
                        error_message=str(e)
                    ))
        
        return batch_result
