"""
Markdown格式化模块
将论文列表格式化为企业微信Markdown消息
"""
from datetime import datetime
from typing import List
from src.fetchers.base import Paper
from src.utils.logger import get_logger

logger = get_logger()


class MarkdownFormatter:
    """Markdown格式化器"""

    def __init__(self):
        """初始化"""
        pass

    def format_digest(self, papers: List[Paper]) -> str:
        """
        格式化为学术资讯日报

        Args:
            papers: 论文列表（应该已包含summary字段）

        Returns:
            Markdown格式的消息
        """
        if not papers:
            return self._format_empty_digest()

        # 企业微信Markdown消息长度限制
        MAX_LENGTH = 4096

        # 尝试不同的论文数量，直到消息长度符合要求
        for num_papers in range(len(papers), 0, -1):
            message = self._build_message(papers[:num_papers])

            if len(message) <= MAX_LENGTH:
                if num_papers < len(papers):
                    logger.warning(f"⚠️  消息过长，已自动调整为推送 {num_papers}/{len(papers)} 篇论文")
                return message

        # 如果连1篇都超长，返回简化版本
        logger.error("❌ 消息太长，无法推送任何论文")
        return self._format_empty_digest()

    def _build_message(self, papers: List[Paper]) -> str:
        """
        构建消息内容

        Args:
            papers: 论文列表

        Returns:
            Markdown消息
        """
        # 标题
        today = datetime.now().strftime("%Y-%m-%d")
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()]

        lines = [
            f"# 🎓 学术资讯日报",
            f"**{today} {weekday}**",
            "",
            f"## 📊 今日精选 {len(papers)} 篇前沿论文",
            "",
        ]

        # 逐篇论文格式化
        for i, paper in enumerate(papers, 1):
            lines.extend(self._format_paper(i, paper))
            if i < len(papers):  # 不是最后一篇
                lines.append("---")
                lines.append("")

        # 底部信息
        lines.extend([
            "",
            "---",
            "",
            "💡 由AI自动筛选和总结 · 每日更新",
        ])

        return "\n".join(lines)

    def _format_paper(self, index: int, paper: Paper) -> List[str]:
        """
        格式化单篇论文

        Args:
            index: 序号
            paper: 论文对象

        Returns:
            格式化的行列表
        """
        lines = []

        # 标题
        title = self._escape_markdown(paper.title)
        lines.append(f"### {index}. {title}")
        lines.append("")

        # 研究方向（从分类提取）
        if paper.categories:
            # 将arXiv分类转换为易读的研究方向
            directions = self._get_research_directions(paper.categories)
            lines.append(f"**🏷️ 研究方向**: {directions}")
            lines.append("")

        # AI生成的结构化摘要
        if paper.summary:
            # 直接使用AI生成的结构化内容
            lines.append(paper.summary)
        else:
            # 降级方案：使用原始摘要
            lines.append("**💡 核心内容**")
            lines.append(paper.abstract[:200] + "...")

        lines.append("")

        # 资源链接
        link_parts = [f"[📄 查看论文]({paper.url})"]

        if paper.pdf_url:
            link_parts.append(f"[📥 PDF]({paper.pdf_url})")

        if paper.code_url:
            link_parts.append(f"[💻 代码]({paper.code_url})")

        lines.append(f"**🔗 资源**: {' · '.join(link_parts)}")
        lines.append("")

        return lines

    def _format_authors(self, authors: List[str]) -> str:
        """
        格式化作者列表

        Args:
            authors: 作者列表

        Returns:
            格式化的作者字符串
        """
        if not authors:
            return "未知"

        # 最多显示3个作者
        if len(authors) <= 3:
            return ", ".join(authors)
        else:
            return f"{', '.join(authors[:3])} et al. ({len(authors)} 位作者)"

    def _get_source_emoji(self, source: str) -> str:
        """
        获取数据源emoji

        Args:
            source: 数据源名称

        Returns:
            emoji
        """
        emoji_map = {
            "arxiv": "📚",
            "paperswithcode": "💻",
            "huggingface": "🤗",
        }
        return emoji_map.get(source.lower(), "📄")

    def _get_research_directions(self, categories: List[str]) -> str:
        """
        将arXiv分类转换为易读的研究方向

        Args:
            categories: arXiv分类列表

        Returns:
            研究方向字符串
        """
        category_map = {
            "cs.LG": "机器学习",
            "cs.AI": "人工智能",
            "cs.CV": "计算机视觉",
            "cs.CL": "自然语言处理",
            "cs.NE": "神经计算",
            "cs.RO": "机器人",
            "cs.IR": "信息检索",
            "stat.ML": "统计学习",
        }

        directions = []
        for cat in categories[:3]:  # 最多显示3个
            direction = category_map.get(cat, cat)
            if direction not in directions:
                directions.append(direction)

        return " · ".join(directions) if directions else "AI研究"

    def _escape_markdown(self, text: str) -> str:
        """
        转义Markdown特殊字符

        Args:
            text: 原始文本

        Returns:
            转义后的文本
        """
        # 企业微信Markdown支持有限，通常不需要过多转义
        # 如果遇到问题，可以添加更多转义规则
        return text

    def _format_empty_digest(self) -> str:
        """
        格式化空日报

        Returns:
            Markdown消息
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return f"""# 🎓 学术资讯日报 | {today}

## 📊 今日精选

😔 抱歉，今天暂时没有符合筛选条件的新论文。

可能的原因：
- 今天发表的新论文较少
- 关键词筛选条件较严格
- 最近推送过相似论文

💡 **建议**：
- 可以调整 `config/keywords.yml` 中的关键词
- 或者查看arXiv网站浏览更多论文

---

🤖 由学术推送系统自动生成
"""

    def format_test_message(self) -> str:
        """
        格式化测试消息

        Returns:
            测试消息
        """
        return """# 🎓 学术推送系统测试

✅ **配置成功！**

系统将在每天早上8:00自动推送最新的学术资讯。

## ✨ 功能特点

- 🤖 AI智能摘要
- 📊 每日5-8篇精选论文
- 🎯 关键词智能筛选
- 💰 成本极低（< $1/月）

## 📖 使用说明

- 修改关键词：编辑 `config/keywords.yml`
- 修改推送时间：编辑 `.github/workflows/daily_push.yml`
- 查看文档：[README.md](https://github.com/your-repo)

---

🎉 开始享受每日学术资讯吧！
"""
