"""
缓存管理模块
用于记录已推送的论文，避免重复推送
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Set, Dict, Any
from src.utils.logger import get_logger

logger = get_logger()


class PaperCache:
    """论文缓存管理"""

    def __init__(self, cache_dir: str = "data/cache", cache_days: int = 7):
        """
        初始化缓存

        Args:
            cache_dir: 缓存目录
            cache_days: 缓存保留天数
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.cache_file = self.cache_dir / "pushed_papers.json"
        self.cache_days = cache_days

        self.cache: Dict[str, Any] = self._load_cache()
        self._clean_old_entries()

    def _load_cache(self) -> Dict[str, Any]:
        """
        从文件加载缓存

        Returns:
            缓存字典
        """
        if not self.cache_file.exists():
            logger.info("缓存文件不存在，创建新缓存")
            return {}

        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
            logger.info(f"加载缓存成功，包含 {len(cache)} 条记录")
            return cache
        except Exception as e:
            logger.error(f"加载缓存失败: {e}")
            return {}

    def _save_cache(self) -> None:
        """保存缓存到文件"""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
            logger.debug(f"缓存已保存: {len(self.cache)} 条记录")
        except Exception as e:
            logger.error(f"保存缓存失败: {e}")

    def _clean_old_entries(self) -> None:
        """清理过期的缓存条目"""
        cutoff_date = datetime.now() - timedelta(days=self.cache_days)
        cutoff_timestamp = cutoff_date.timestamp()

        original_count = len(self.cache)
        self.cache = {
            paper_id: info
            for paper_id, info in self.cache.items()
            if info.get("timestamp", 0) > cutoff_timestamp
        }

        removed_count = original_count - len(self.cache)
        if removed_count > 0:
            logger.info(f"清理了 {removed_count} 条过期缓存（保留 {self.cache_days} 天）")
            self._save_cache()

    def is_pushed(self, paper_id: str) -> bool:
        """
        检查论文是否已推送

        Args:
            paper_id: 论文ID（如arXiv ID）

        Returns:
            是否已推送
        """
        return paper_id in self.cache

    def mark_as_pushed(self, paper_id: str, paper_title: str = "") -> None:
        """
        标记论文为已推送

        Args:
            paper_id: 论文ID
            paper_title: 论文标题（可选）
        """
        self.cache[paper_id] = {
            "title": paper_title,
            "timestamp": datetime.now().timestamp(),
            "date": datetime.now().isoformat(),
        }
        logger.debug(f"标记为已推送: {paper_id}")

    def mark_batch_as_pushed(self, papers: list) -> None:
        """
        批量标记论文为已推送

        Args:
            papers: Paper对象列表
        """
        for paper in papers:
            paper_id = getattr(paper, "arxiv_id", None) or getattr(paper, "url", "")
            paper_title = getattr(paper, "title", "")
            if paper_id:
                self.mark_as_pushed(paper_id, paper_title)

        self._save_cache()
        logger.info(f"批量标记 {len(papers)} 篇论文为已推送")

    def filter_unpushed(self, papers: list) -> list:
        """
        过滤出未推送的论文

        Args:
            papers: Paper对象列表

        Returns:
            未推送的论文列表
        """
        unpushed = []
        for paper in papers:
            paper_id = getattr(paper, "arxiv_id", None) or getattr(paper, "url", "")
            if paper_id and not self.is_pushed(paper_id):
                unpushed.append(paper)

        logger.info(f"过滤结果: {len(papers)} 篇论文 → {len(unpushed)} 篇未推送")
        return unpushed

    def get_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息

        Returns:
            统计信息字典
        """
        if not self.cache:
            return {
                "total_count": 0,
                "oldest_date": None,
                "newest_date": None,
            }

        timestamps = [info["timestamp"] for info in self.cache.values()]
        return {
            "total_count": len(self.cache),
            "oldest_date": datetime.fromtimestamp(min(timestamps)).isoformat(),
            "newest_date": datetime.fromtimestamp(max(timestamps)).isoformat(),
        }
