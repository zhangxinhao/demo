from enum import Enum
from typing import Optional


class EnvVar(Enum):
    """Environment variable definitions with (key, default_value, type)"""

    # SFTP 配置
    SFTP_HOST = ("SFTP_HOST", None, str)
    SFTP_PORT = ("SFTP_PORT", "22", int)
    SFTP_USERNAME = ("SFTP_USERNAME", None, str)
    SFTP_PASSWORD = ("SFTP_PASSWORD", None, str)

    @property
    def key(self) -> str:
        return self.value[0]

    @property
    def default(self) -> Optional[str]:
        return self.value[1]

    @property
    def var_type(self) -> type:
        return self.value[2]
