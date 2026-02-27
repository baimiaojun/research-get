"""
学术资讯每日推送系统 - 主入口
"""
import asyncio
import sys
from src.config import get_config
from src.utils.logger import setup_logger, get_logger
from src.utils.cache import PaperCache
from src.fetchers.arxiv_fetcher import ArxivFetcher
from src.filters.keyword_filter import KeywordFilter
from src.filters.deduplicator import Deduplicator
from src.summarizers.claude_summarizer import ClaudeSummarizer
from src.summarizers.deepseek_summarizer import DeepSeekSummarizer
from src.notifiers.formatter import MarkdownFormatter
from src.notifiers.wecom_notifier import WeComNotifier


async def main():
    """主流程"""
    logger = None  # 初始化为None，避免未定义错误

    try:
        # 1. 加载配置
        print("=" * 60)
        print("🎓 学术资讯每日推送系统")
        print("=" * 60)

        config = get_config()

        # 2. 初始化日志
        setup_logger(log_dir=config.log_dir, log_level=config.log_level)
        logger = get_logger()

        logger.info("系统启动")
        logger.info(f"配置加载完成")
        logger.info(f"  - 论文数量: {config.papers_to_send}")
        logger.info(f"  - Claude模型: {config.claude_model}")

        # 3. 初始化组件
        logger.info("初始化组件...")

        # 缓存管理器
        cache = PaperCache(
            cache_dir=config.cache_dir,
            cache_days=config.cache_days
        )

        # 数据获取器
        fetchers = []
        if config.enable_arxiv:
            fetchers.append(ArxivFetcher(max_results=config.arxiv_max_results))
            logger.info("  ✅ arXiv数据源")

        if not fetchers:
            logger.error("❌ 没有启用任何数据源，退出")
            return

        # 内容过滤器
        keyword_filter = KeywordFilter(keywords_file=config.keywords_file)
        deduplicator = Deduplicator()

        # AI摘要生成器
        if config.ai_service == "claude":
            if not config.claude_api_key:
                logger.error("❌ 使用Claude服务需要配置CLAUDE_API_KEY")
                return
            summarizer = ClaudeSummarizer(
                api_key=config.claude_api_key,
                model=config.claude_model,
                max_tokens=config.ai_max_tokens,
                temperature=config.ai_temperature,
                prompts_file=config.prompts_file,
            )
        elif config.ai_service == "deepseek":
            if not config.deepseek_api_key:
                logger.error("❌ 使用DeepSeek服务需要配置DEEPSEEK_API_KEY")
                return
            summarizer = DeepSeekSummarizer(
                api_key=config.deepseek_api_key,
                model=config.deepseek_model,
                max_tokens=config.ai_max_tokens,
                temperature=config.ai_temperature,
                prompts_file=config.prompts_file,
            )
        elif config.ai_service == "none":
            logger.warning("⚠️  未启用AI摘要服务，将使用原始摘要")
            summarizer = None
        else:
            logger.error(f"❌ 不支持的AI服务: {config.ai_service}")
            return

        # 格式化器和通知器
        formatter = MarkdownFormatter()
        notifier = WeComNotifier(webhook_url=config.wecom_webhook_url)

        logger.info("组件初始化完成")

        # 4. 获取论文
        logger.info("")
        logger.info("=" * 60)
        logger.info("📥 第一步: 获取论文")
        logger.info("=" * 60)

        # 并发获取所有数据源
        fetch_tasks = [
            fetcher.fetch_papers(days=config.fetch_days)
            for fetcher in fetchers
        ]
        all_papers_lists = await asyncio.gather(*fetch_tasks)

        # 合并所有论文
        all_papers = []
        for papers in all_papers_lists:
            all_papers.extend(papers)

        logger.info(f"总共获取到 {len(all_papers)} 篇论文")

        if not all_papers:
            logger.warning("没有获取到任何论文")
            # 发送空日报
            empty_message = formatter._format_empty_digest()
            await notifier.send_markdown(empty_message)
            return

        # 5. 去重
        logger.info("")
        logger.info("=" * 60)
        logger.info("🔄 第二步: 去重处理")
        logger.info("=" * 60)

        unique_papers = deduplicator.deduplicate(all_papers)

        # 6. 过滤已推送论文
        logger.info("")
        logger.info("=" * 60)
        logger.info("🗂️  第三步: 过滤已推送论文")
        logger.info("=" * 60)

        unpushed_papers = cache.filter_unpushed(unique_papers)

        if not unpushed_papers:
            logger.warning("所有论文都已推送过")
            # 发送提示消息
            message = formatter._format_empty_digest()
            await notifier.send_markdown(message)
            return

        # 7. 关键词评分和排序
        logger.info("")
        logger.info("=" * 60)
        logger.info("🎯 第四步: 关键词评分")
        logger.info("=" * 60)

        scored_papers = keyword_filter.get_top_papers(
            unpushed_papers,
            count=config.papers_to_send,
            min_score=0.0,  # 不设置最低分数，确保能选出论文
        )

        if not scored_papers:
            logger.warning("没有论文通过筛选")
            message = formatter._format_empty_digest()
            await notifier.send_markdown(message)
            return

        # 提取论文和分数
        selected_papers = [paper for paper, score in scored_papers]
        scores = [score for paper, score in scored_papers]

        logger.info(f"选出 {len(selected_papers)} 篇论文")
        for i, (paper, score) in enumerate(scored_papers, 1):
            logger.info(f"  {i}. [{score:.1f}分] {paper.title[:60]}...")

        # 8. 生成AI摘要
        logger.info("")
        logger.info("=" * 60)
        logger.info("🤖 第五步: 生成AI摘要")
        logger.info("=" * 60)

        if summarizer:
            selected_papers = await summarizer.summarize_and_update(selected_papers)
            logger.info("摘要生成完成")
        else:
            # 使用原始摘要
            for paper in selected_papers:
                paper.summary = paper.abstract[:200] + "..."
            logger.info("使用原始摘要（未启用AI服务）")

        # 9. 格式化消息
        logger.info("")
        logger.info("=" * 60)
        logger.info("📝 第六步: 格式化消息")
        logger.info("=" * 60)

        markdown_message = formatter.format_digest(selected_papers)

        message_chars = len(markdown_message)
        message_bytes = len(markdown_message.encode('utf-8'))
        logger.info(f"消息长度: {message_chars} 字符 ({message_bytes} 字节)")

        if message_bytes > 4096:
            logger.error(f"⚠️  警告: 消息仍超过4096字节限制！")
        else:
            logger.info(f"✅ 消息长度符合要求（< 4096字节）")

        # 10. 推送到企业微信
        logger.info("")
        logger.info("=" * 60)
        logger.info("📤 第七步: 推送消息")
        logger.info("=" * 60)

        success = await notifier.send_markdown(markdown_message)

        if not success:
            logger.error("消息推送失败")
            return

        # 11. 更新缓存
        logger.info("")
        logger.info("=" * 60)
        logger.info("💾 第八步: 更新缓存")
        logger.info("=" * 60)

        cache.mark_batch_as_pushed(selected_papers)

        # 12. 完成
        logger.info("")
        logger.info("=" * 60)
        logger.info("✅ 任务完成！")
        logger.info("=" * 60)
        logger.info(f"成功推送 {len(selected_papers)} 篇论文")

        # 打印统计信息
        cache_stats = cache.get_stats()
        logger.info("")
        logger.info("📊 统计信息:")
        logger.info(f"  - 本次推送: {len(selected_papers)} 篇")
        logger.info(f"  - 缓存总数: {cache_stats['total_count']} 篇")
        logger.info(f"  - 平均分数: {sum(scores) / len(scores):.1f}")

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        if logger:
            logger.exception(f"❌ 系统错误: {e}")
        else:
            print(f"\n❌ 配置加载失败: {e}")
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # 运行主流程
    asyncio.run(main())
