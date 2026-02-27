"""
配置管理模块
使用pydantic-settings从环境变量加载配置
"""
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """系统配置"""

    # 必需配置
    wecom_webhook_url: str = Field(..., description="企业微信Webhook URL")

    # AI服务配置（根据ai_service选择）
    ai_service: str = Field(default="deepseek", description="AI服务提供商: claude, deepseek, qwen, none")

    # Claude API配置（使用Claude时必需）
    claude_api_key: Optional[str] = Field(default=None, description="Claude API密钥")
    claude_model: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="Claude模型"
    )

    # DeepSeek API配置（使用DeepSeek时必需）
    deepseek_api_key: Optional[str] = Field(default=None, description="DeepSeek API密钥")
    deepseek_model: str = Field(default="deepseek-chat", description="DeepSeek模型")

    # 通用AI配置
    ai_max_tokens: int = Field(default=200, description="摘要最大token数")
    ai_temperature: float = Field(default=0.7, description="生成温度")

    # 可选配置
    papers_to_send: int = Field(default=6, description="每日推送论文数量")
    log_level: str = Field(default="INFO", description="日志级别")
    enable_arxiv: bool = Field(default=True, description="是否启用arXiv数据源")
    enable_paperswithcode: bool = Field(default=False, description="是否启用Papers with Code")
    enable_huggingface: bool = Field(default=False, description="是否启用Hugging Face")

    # 文件路径
    keywords_file: str = Field(default="config/keywords.yml", description="关键词配置文件")
    prompts_file: str = Field(default="config/prompts.yml", description="提示词配置文件")
    cache_dir: str = Field(default="data/cache", description="缓存目录")
    log_dir: str = Field(default="logs", description="日志目录")

    # 数据获取配置
    arxiv_max_results: int = Field(default=50, description="arXiv最大结果数")
    fetch_days: int = Field(default=1, description="获取最近几天的论文")

    # 缓存配置
    cache_days: int = Field(default=7, description="缓存保留天数")

    @field_validator("wecom_webhook_url")
    @classmethod
    def validate_webhook_url(cls, v: str) -> str:
        """验证企业微信Webhook URL格式"""
        if not v.startswith("https://qyapi.weixin.qq.com/"):
            raise ValueError(
                "企业微信Webhook URL必须以 'https://qyapi.weixin.qq.com/' 开头"
            )
        return v

    @field_validator("ai_service")
    @classmethod
    def validate_ai_service(cls, v: str) -> str:
        """验证AI服务选择"""
        valid_services = ["claude", "deepseek", "qwen", "none"]
        v_lower = v.lower()
        if v_lower not in valid_services:
            raise ValueError(f"AI服务必须是: {', '.join(valid_services)}")
        return v_lower

    @field_validator("claude_api_key")
    @classmethod
    def validate_claude_key(cls, v: Optional[str]) -> Optional[str]:
        """验证Claude API Key格式"""
        if v and not v.startswith("sk-ant-"):
            raise ValueError("Claude API Key应该以 'sk-ant-' 开头")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """验证日志级别"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"日志级别必须是: {', '.join(valid_levels)}")
        return v_upper

    @field_validator("papers_to_send", mode="before")
    @classmethod
    def validate_papers_count(cls, v) -> int:
        """验证论文数量（处理空字符串）"""
        # 处理空字符串或None，使用默认值
        if v is None or v == "":
            return 6
        # 转换为整数
        try:
            v_int = int(v)
        except (ValueError, TypeError):
            return 6
        # 验证范围
        if v_int < 1 or v_int > 20:
            raise ValueError("每日推送论文数量应在1-20之间")
        return v_int

    class Config:
        """pydantic配置"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 全局配置实例
def get_config() -> Config:
    """获取配置实例"""
    return Config()
