"""
LLM相关工具模块。

提供LLM接口和模拟实现。
"""


class MockLLM:
    """LLM的模拟实现，用于开发测试"""

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def oracle(self, prompt: str) -> str:
        """模拟LLM响应，返回预设的响应格式"""
        print(f"[LLM调用] 提示词长度: {len(prompt)}")
        print(f"[LLM调用] 提示词预览: {prompt[:50]}...")

        # 这里是模拟回复，实际应该调用真实的LLM服务
        mock_response = '''
```python
# 基于示例和函数规格的模拟实现
def generated_function():
    # 这里是LLM生成的代码实现
    pass
```

<output_repr>30</output_repr>
'''
        return mock_response
