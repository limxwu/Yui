from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 定义属性并指定类型，Pydantic 会自动做类型转换
    server_port: int = 8080  # 默认值
    deepseek_api_key: Optional[str] = None
    # 配置：读取 .env 文件
    model_config = SettingsConfigDict(env_file=".env", populate_by_name=True)
