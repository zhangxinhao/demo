"""
Markdown解析工具模块。

提供markdown格式字符串的解析功能。
"""

import re
from typing import List, Dict, Any, Union, Literal


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
