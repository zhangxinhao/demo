"""
LLM 客户端封装模块
提供统一的大模型调用接口
"""

import time
from dataclasses import dataclass

from openai import OpenAI

from common import get_logger
from common.config import get_settings, EnvVar

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
    
    统一封装大模型调用逻辑，支持从配置文件加载配置
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
    def from_settings(cls) -> "LLMClient":
        """
        从配置文件创建客户端
        
        Returns:
            LLMClient 实例
        
        Raises:
            ValueError: 缺少必要的配置
        """
        settings = get_settings()
        
        api_key = settings.get(EnvVar.OPENROUTER_API_KEY)
        model_name = settings.get(EnvVar.LLM_MODEL)
        base_url = settings.get(EnvVar.LLM_BASE_URL)
        
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in config")
        if not model_name:
            raise ValueError("MODEL_NAME or LLM_MODEL not found in config")
        
        logger.info(f"LLM client initialized with model: {model_name}")
        return cls(api_key=api_key, model_name=model_name, base_url=base_url)
    
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
    
    def get_num_threads(self, default: int = 2) -> int:
        """
        从配置获取线程数
        
        Args:
            default: 默认线程数
        
        Returns:
            线程数
        """
        settings = get_settings()
        num_threads = settings.get(EnvVar.NUM_THREADS)
        if num_threads is not None:
            return num_threads
        return default
