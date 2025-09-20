import os
import importlib.util
from typing import Optional, Union, List, Dict, Any
from jinja2 import Environment, FileSystemLoader, ChoiceLoader, PrefixLoader
from jinja2.ext import Extension
from jinja2 import nodes
from jinja2.parser import Parser


class SimpleTransExtension(Extension):
    """
    简化的翻译扩展，直接返回原文本内容
    """
    tags = {'trans'}

    def parse(self, parser: Parser) -> nodes.Node:
        lineno = next(parser.stream).lineno
        # 解析到 {% endtrans %} 之间的内容
        node = parser.parse_statements(['name:endtrans'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_render_trans', []), [], [], node).set_lineno(lineno)
    
    def _render_trans(self, caller):
        # 直接返回原文本，不做翻译处理
        return caller()


def value_repr(value: Any, cutoff: int = 256) -> str:
    """
    格式化值的字符串表示，支持截断
    
    Args:
        value: 要格式化的值
        cutoff: 最大字符长度，-1表示不截断
        
    Returns:
        格式化后的字符串
    """
    result = repr(value)
    if cutoff > 0 and len(result) > cutoff:
        result = result[:cutoff] + "..."
    return result


def load_jinja_env(path: Optional[Union[str, List[str], Dict[str, str]]] = None, **kwargs) -> Environment:
    """
    加载Jinja2环境，支持多种路径配置方式
    
    Args:
        path (Optional[Union[str,List[str],Dict[str,str]]]): 模板文件根目录
            - 字符串：单个模板目录路径
            - 列表：多个模板目录路径，使用ChoiceLoader
            - 字典：环境名称到路径的映射，使用PrefixLoader
            - None：默认使用相对路径 "resources"
        **kwargs: Jinja2 Environment的其他参数
        
    Returns:
        Environment: Jinja2环境实例
    """
    # 默认使用相对路径
    if path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "resources")
    
    # 根据path类型创建相应的加载器
    if isinstance(path, str):
        # 单个路径，直接使用FileSystemLoader
        paths = [os.path.abspath(path)]
        loader = FileSystemLoader(paths[0])
    elif isinstance(path, dict):
        # 字典映射，使用PrefixLoader
        paths = {k: os.path.abspath(v) for k, v in path.items()}
        loader = PrefixLoader({k: FileSystemLoader(v) for k, v in paths.items()})
    else:
        # 列表路径，使用ChoiceLoader
        paths = [os.path.abspath(p) for p in path]
        # 只加载存在的目录
        valid_paths = [p for p in paths if os.path.exists(p) and os.path.isdir(p)]
        loader = ChoiceLoader([FileSystemLoader(p) for p in valid_paths])
    
    # 加载自定义过滤器
    filters = {}
    path_list = list(paths.values()) if isinstance(paths, dict) else (paths if isinstance(paths, list) else [paths])
    
    for p in path_list:
        filters_path = os.path.join(p, "filters")
        if os.path.exists(filters_path) and os.path.isdir(filters_path):
            # 查找所有Python过滤器文件
            for filename in os.listdir(filters_path):
                if filename.endswith(".py") and not filename.startswith("_"):
                    try:
                        filter_file_path = os.path.join(filters_path, filename)
                        filter_name = filename[:-3]  # 去掉.py扩展名
                        
                        # 动态加载过滤器模块
                        spec = importlib.util.spec_from_file_location(filter_name, filter_file_path)
                        filter_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(filter_module)
                        
                        # 获取同名函数作为过滤器
                        filter_func = getattr(filter_module, filter_name, None)
                        if filter_func and callable(filter_func):
                            filters[filter_name] = filter_func
                    except Exception:
                        # 忽略加载失败的过滤器
                        pass
    
    # 创建Jinja2环境，添加简化的翻译扩展
    extensions = kwargs.get("../extensions", [])
    extensions.append(SimpleTransExtension)
    other_kwargs = {k: v for k, v in kwargs.items() if k != "extensions"}
    env = Environment(loader=loader, extensions=extensions, **other_kwargs)
    
    # 注册内置过滤器
    env.filters['value_repr'] = value_repr
    
    # 注册自定义过滤器
    for filter_name, filter_func in filters.items():
        env.filters[filter_name] = filter_func
    
    return env
