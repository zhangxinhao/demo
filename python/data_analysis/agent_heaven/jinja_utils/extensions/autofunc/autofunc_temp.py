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
from typing import List, Dict, Any, Callable

from jinja_utils.utils.jinja_utils import load_jinja_env
from jinja_utils.utils.llm_utils import MockLLM
from jinja_utils.utils.md_utils import parse_md
from jinja_utils.utils.func_utils import get_func_spec


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
