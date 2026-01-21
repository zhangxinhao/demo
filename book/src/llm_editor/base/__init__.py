"""
公共基类模块
提供批量处理器等通用功能
"""

from common.client import LLMClient, LLMResponse
from llm_editor.base.batch_processor import BatchFileProcessor, ProcessResult, BatchResult

__all__ = [
    "LLMClient",
    "LLMResponse",
    "BatchFileProcessor",
    "ProcessResult",
    "BatchResult",
]
