"""
函数规格工具模块。

提供函数签名、文档、注解等规格信息的获取功能。
"""

import inspect
from typing import Dict, Any, Callable


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
