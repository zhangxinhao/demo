"""
LLM 客户端封装模块
提供统一的大模型调用接口
"""

import os
import time
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from common import get_logger, get_path_manager

logger = get_logger("llm_client")


@dataclass
class LLMResponse:
    """LLM 响应结果"""
    content: str
    elapsed_time: float
    prompt_tokens: int
    completion_tokens: int
    
    @property
    def total_tokens(self) -> int:
        """总 token 数"""
        return self.prompt_tokens + self.completion_tokens


class LLMClient:
    """
    LLM 客户端封装类
    
    统一封装大模型调用逻辑，支持从环境变量加载配置
    """
    
    def __init__(
        self,
        api_key: str,
        model_name: str,
        base_url: str = "https://openrouter.ai/api/v1"
    ):
        """
        初始化 LLM 客户端
        
        Args:
            api_key: API 密钥
            model_name: 模型名称
            base_url: API 基础 URL
        """
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model_name = model_name
        self.base_url = base_url
    
    @classmethod
    def from_env(cls, env_path: Path | None = None) -> "LLMClient":
        """
        从环境变量创建客户端
        
        Args:
            env_path: .env 文件路径，默认为 src/.env
        
        Returns:
            LLMClient 实例
        
        Raises:
            ValueError: 缺少必要的环境变量
        """
        if env_path is None:
            env_path = get_path_manager().get_path("src/.env")
        
        load_dotenv(env_path)
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        model_name = os.getenv("MODEL_NAME")
        
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")
        if not model_name:
            raise ValueError("MODEL_NAME not found in .env file")
        
        logger.info(f"LLM client initialized with model: {model_name}")
        return cls(api_key=api_key, model_name=model_name)
    
    def call(
        self,
        prompt: str,
        file_name: str = "",
        enable_reasoning: bool = True
    ) -> LLMResponse:
        """
        调用 LLM API
        
        Args:
            prompt: 提示词内容
            file_name: 文件名（用于日志标识）
            enable_reasoning: 是否启用推理模式
        
        Returns:
            LLMResponse 响应结果
        
        Raises:
            Exception: API 调用失败
        """
        try:
            # 打印请求的字符数
            prompt_chars = len(prompt)
            log_prefix = f"[{file_name}] " if file_name else ""
            logger.info(f"{log_prefix}Request prompt chars: {prompt_chars}")
            
            start_time = time.time()
            
            # 构建请求参数
            request_params = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # 添加推理模式参数
            if enable_reasoning:
                request_params["extra_body"] = {"reasoning": {"enabled": True}}
            
            response = self.client.chat.completions.create(**request_params)
            elapsed_time = time.time() - start_time
            
            # 获取 token 使用情况
            prompt_tokens = response.usage.prompt_tokens if response.usage else 0
            completion_tokens = response.usage.completion_tokens if response.usage else 0
            
            logger.info(
                f"{log_prefix}LLM call completed in {elapsed_time:.2f}s, "
                f"prompt_tokens: {prompt_tokens}, completion_tokens: {completion_tokens}"
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                elapsed_time=elapsed_time,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens
            )
        except Exception as e:
            logger.error(f"{log_prefix}Error calling LLM: {e}")
            raise
    
    def get_num_threads(self, env_path: Path | None = None, default: int = 2) -> int:
        """
        从环境变量获取线程数配置
        
        Args:
            env_path: .env 文件路径
            default: 默认线程数
        
        Returns:
            线程数
        """
        if env_path is None:
            env_path = get_path_manager().get_path("src/.env")
        
        load_dotenv(env_path)
        
        num_threads_str = os.getenv("NUM_THREADS", str(default))
        try:
            return int(num_threads_str)
        except ValueError:
            logger.warning(f"Invalid NUM_THREADS value '{num_threads_str}', using default {default}")
            return default
