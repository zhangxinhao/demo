"""\
AgentHeaven的AutoFunc工具模块。

本模块提供`autofunc`装饰器，允许基于示例和函数规格
使用大型语言模型(LLM)自动实现函数功能。

警告：这是临时实现，可能会发生大的变动。
TODO：
    - 改为AutoFunc类以集成缓存功能
    - 添加示例选择/验证策略
"""

import inspect
import json
import re
from typing import List, Dict, Any, Callable, Literal

from jinja_utils import load_jinja_env


# 简单的LLM打桩实现
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


def parse_md(response: str, recurse: bool = False, mode: Literal["list", "dict"] = "dict"):
    """\
    解析类markdown格式字符串为结构化块。

    此函数从输入字符串中提取块，支持以下格式:

    - XML样式标签（如 <tag>...</tag>）
    - 围栏代码块（如 ```python ... ```、```sql ... ```），语言是可选的且大小写敏感。
      缺少语言时默认为"markdown"
    - 块之间的普通文本

    参数:
        response (str): 要解析的输入字符串。

        recurse (bool, 可选): 如果为True，递归解析嵌套块。默认为False。

        mode (Literal["list", "dict"], 可选):

            - "list": 返回块列表，每个块为包含'key'和'value'的字典
            - "dict": 返回扁平化字典，嵌套块使用点分隔键。注意重复键会被覆盖

            默认为"dict"。

    返回:
        Union[list[dict], dict]: 解析后的结构，根据``mode``返回列表或字典。

    示例:
        >>> parse_md("<think>Hello!</think>\\nSome textual output.\\n```sql\\nSELECT *\\nFROM table;\\n```\\n<rating>\\n```json\\n{\\\"rating\\\": 5}\\n```</rating>")
        {'think': 'Hello!', 'text': 'Some textual output.', 'sql': 'SELECT *\\nFROM table;', 'rating': '```json\\n{"rating": 5}\\n```'}

        >>> parse_md("<think>Hello!</think>\\nSome textual output.\\n```sql\\nSELECT *\\nFROM table;\\n```\\n<rating>\\n```json\\n{\\\"rating\\\": 5}\\n```</rating>", recurse=True)
        {'think.text': 'Hello!', 'text': 'Some textual output.', 'sql': 'SELECT *\\nFROM table;', 'rating.json': '{"rating": 5}'}

        >>> parse_md("<think>Hello!</think>\\nSome textual output.\\n```sql\\nSELECT *\\nFROM table;\\n```\\n<rating>\\n```json\\n{\\\"rating\\\": 5}\\n```</rating>", mode="list")
        [{'key': 'think', 'value': 'Hello!'}, {'key': 'text', 'value': 'Some textual output.'}, {'key': 'sql', 'value': 'SELECT *\\nFROM table;'}, {'key': 'rating', 'value': '```json\\n{"rating": 5}\\n```'}]
    """
    blocks = list()
    pattern = re.compile(r"(<(\w+)>([\s\S]*?)<\/\2>)|(```(\w*)\n([\s\S]*?)\n```)")

    last_end = 0
    for match in pattern.finditer(response):
        start, end = match.span()
        if last_end < start:
            content = response[last_end:start].strip()
            if content:
                blocks.append({"key": "text", "value": content})
        if match.group(1):
            tag = match.group(2)
            content = match.group(3).strip()
            blocks.append(
                {
                    "key": tag,
                    "value": ((parse_md(content, recurse=recurse, mode="list") if content else list()) if recurse else content),
                }
            )
        elif match.group(4):
            lang = match.group(5) if match.group(5) else "markdown"
            content = match.group(6).strip()
            blocks.append({"key": lang, "value": content})
        last_end = end
    if last_end < len(response):
        content = response[last_end:].strip()
        if content:
            blocks.append({"key": "text", "value": content})

    if mode == "list":
        return blocks
    elif mode == "dict":
        parsed = dict()

        def _dfs(blocks, prefix=None):
            prefix = prefix or list()
            for block in blocks:
                if isinstance(block["value"], list):
                    _dfs(block["value"], prefix=prefix + [block["key"]])
                else:
                    parsed[".".join(prefix + [block["key"]])] = block["value"]

        _dfs(blocks)
        return parsed


def get_func_spec(func: Callable) -> Dict[str, Any]:
    """获取函数的详细规格信息，包括签名、文档、注解等"""
    sig = inspect.signature(func)
    return {
        'name': func.__name__,
        'signature': str(sig),
        'docstring': inspect.getdoc(func) or '',
        'annotations': getattr(func, '__annotations__', {}),
        'parameters': {
            name: {
                'annotation': param.annotation if param.annotation != inspect.Parameter.empty else None,
                'default': param.default if param.default != inspect.Parameter.empty else None,
            }
            for name, param in sig.parameters.items()
        }
    }


def autofunc(examples: List[Dict[str, Any]] = None, hints: List[str] = None, **llm_kwargs) -> Callable:
    """\
    使用LLM推理自动实现函数的装饰器。

    该装饰器将函数体替换为基于LLM的实现，LLM根据函数规格、示例和提示
    推断函数逻辑，生成可执行代码并产生函数输出。

    TODO：这是临时实现，可能会发生大的变动。待办事项：
        - 改为AutoFunc类以集成缓存功能
        - 添加示例选择/验证策略

    参数:
        examples (List[Dict[str, Any]], 可选): 输入输出示例列表。
            每个示例应该是包含"inputs"和"output"键的字典。
            "inputs"应该是参数名到值的映射字典。
            可选地，可以使用"expected"代替"output"。
        hints (List[str], 可选): 用于指导LLM的额外提示或上下文。
        **llm_kwargs: 传递给LLM构造函数的额外关键字参数。

    返回:
        Callable: 包装目标函数的装饰器函数。

    异常:
        AutoFuncError: 如果LLM生成无效的可执行代码或
            函数执行时发生错误。

    示例:
        >>> @autofunc(
        ...     examples=[
        ...         {"inputs": {"x": 5}, "output": 25},
        ...         {"inputs": {"x": 3}, "output": 9},
        ...     ],
        ...     hints=["此函数计算输入的平方"]
        ... )
        ... def square(x: int) -> int:
        ...     '''计算输入数字的平方。'''
        ...     pass
        >>> square(4)
        16

        >>> @autofunc(
        ...     examples=[
        ...         {"inputs": {"a": 3, "b": 4}, "output": 49},
        ...         {"inputs": {"a": 5, "b": 6}, "output": 53},
        ...     ],
        ...     hints=["涉及一个魔法数字"]
        ... )
        ... def add_magic_number(a: int, b: int) -> int:
        ...     '''两个数字相加再加上一个魔法常数。'''
        ...     pass
        >>> add_magic_number(1, 2)
        45
    """
    env = load_jinja_env()
    template = env.get_template("autofunc/default.jinja")

    def decorator(func: Callable) -> Callable:
        funcspec = get_func_spec(func)

        def funcimpl(*args, **kwargs):
            # 将位置参数映射到对应的参数名
            sig = inspect.signature(func)
            param_names = list(sig.parameters.keys())
            inputs = {name: arg for name, arg in zip(param_names, args)}
            inputs.update(kwargs)

            # 构建LLM提示词
            prompt_str = template.render(funcspec=funcspec, examples=examples or list(), inputs=inputs,
                                         hints=hints or list())
            print(f"[调试] 生成的提示词:\n{prompt_str}")

            # 调用LLM获取响应
            llm = MockLLM(**llm_kwargs)
            response = llm.oracle(prompt_str)
            print(f"[调试] LLM响应:\n{response}")

            # 解析LLM响应并执行
            try:
                parsed = parse_md(response)
                output_repr = parsed.get("output_repr", "").strip()
                print(f"[调试] 输出表达式:\n{output_repr}")

                if not output_repr:
                    # 如果没有找到输出表达式，返回默认值
                    print("[警告] 未找到output_repr，返回默认值")
                    return "默认输出"

                return eval(output_repr)
            except Exception as e:
                print(f"[错误] 执行函数 {func.__name__} 时出错，输入 {inputs}: {e}")
                raise Exception(f"无法正确执行: {func.__name__} 输入: {inputs}")

        # 保持原函数的元数据信息
        funcimpl.__name__ = func.__name__
        funcimpl.__doc__ = func.__doc__

        return funcimpl

    return decorator


if __name__ == "__main__":
    print("测试autofunc装饰器")


    # 测试示例1：平方函数
    @autofunc(
        examples=[
            {"inputs": {"x": 5}, "output": 25},
            {"inputs": {"x": 3}, "output": 9},
        ],
        hints=["此函数计算输入的平方"]
    )
    def square(x: int) -> int:
        '''计算输入数字的平方。'''
        pass


    print("\n=== 测试平方函数 ===")
    try:
        result = square(4)
        print(f"square(4) = {result}")
    except Exception as e:
        print(f"测试出错: {e}")


    # 测试示例2：简单加法
    @autofunc(
        examples=[
            {"inputs": {"a": 1, "b": 2}, "output": 3},
            {"inputs": {"a": 5, "b": 7}, "output": 12},
        ]
    )
    def add_numbers(a: int, b: int) -> int:
        '''计算两个数字的和。'''
        pass


    print("\n=== 测试加法函数 ===")
    try:
        result = add_numbers(10, 20)
        print(f"add_numbers(10, 20) = {result}")
    except Exception as e:
        print(f"测试出错: {e}")

    print("\n测试完成")
