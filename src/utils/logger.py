"""
日志配置模块
使用loguru提供增强的日志功能
"""
import sys
from pathlib import Path
from datetime import datetime
from loguru import logger


def setup_logger(log_dir: str = "logs", log_level: str = "INFO") -> None:
    """
    配置日志系统

    Args:
        log_dir: 日志目录
        log_level: 日志级别
    """
    # 创建日志目录
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # 移除默认handler
    logger.remove()

    # 控制台输出 - 彩色格式
    logger.add(
        sys.stdout,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        level=log_level,
        colorize=True,
    )

    # 文件输出 - 按天轮转
    today = datetime.now().strftime("%Y%m%d")
    log_file = log_path / f"daily_push_{today}.log"

    logger.add(
        log_file,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message}"
        ),
        level="DEBUG",  # 文件记录更详细的日志
        rotation="1 day",  # 每天轮转
        retention="30 days",  # 保留30天
        compression="zip",  # 压缩旧日志
        encoding="utf-8",
    )

    logger.info(f"日志系统已初始化 - 级别: {log_level}")
    logger.info(f"日志文件: {log_file}")


def get_logger():
    """获取logger实例"""
    return logger
