from enum import Enum
from typing import Optional


class EnvVar(Enum):
    """Environment variable definitions with (key, default_value, type)"""

    @property
    def key(self) -> str:
        return self.value[0]

    @property
    def default(self) -> Optional[str]:
        return self.value[1]

    @property
    def var_type(self) -> type:
        return self.value[2]
