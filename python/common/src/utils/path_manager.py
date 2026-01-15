import os
from pathlib import Path
from typing import Union, Optional

from common.path_type import PathType


class PathManager:
    """路径管理器"""

    def __init__(self):
        self._project_root: Optional[str] = None

    @property
    def project_root(self) -> str:
        if self._project_root is None:
            self._project_root = self._find_project_root()
        return self._project_root

    def _find_project_root(self) -> str:
        """查找项目根目录"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 从utils向上3层到项目根目录
        return os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

    def get_absolute_path(self, path: Union[str, Path]) -> str:
        """将路径转换为绝对路径"""
        path_str = str(path)
        if os.path.isabs(path_str):
            return path_str
        return os.path.join(self.project_root, path_str)

    def get_dir(self, path_type: PathType) -> str:
        """获取指定类型的目录绝对路径"""
        return self.get_absolute_path(path_type.value)

    def ensure_dir_exists(self, path: Union[str, Path, PathType]) -> bool:
        """确保目录存在"""
        try:
            if isinstance(path, PathType):
                abs_path = self.get_dir(path)
            else:
                abs_path = self.get_absolute_path(path)
            os.makedirs(abs_path, exist_ok=True)
            return True
        except Exception as e:
            print(f"创建目录失败: {path}, 错误: {str(e)}")
            return False


# 全局单例
_path_manager_instance: Optional[PathManager] = None


def get_path_manager() -> PathManager:
    """获取全局路径管理器实例"""
    global _path_manager_instance
    if _path_manager_instance is None:
        _path_manager_instance = PathManager()
    return _path_manager_instance
