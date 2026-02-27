#!/usr/bin/env python3
"""
测试AI摘要生成
"""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from src.config import get_config
from src.summarizers.deepseek_summarizer import DeepSeekSummarizer
from src.fetchers.base import Paper
from datetime import datetime

# 测试论文
test_paper = Paper(
    title="Attention Is All You Need",
    authors=["Vaswani et al."],
    abstract="""The dominant sequence transduction models are based on complex recurrent or
    convolutional neural networks that include an encoder and a decoder. The best performing
    models also connect the encoder and decoder through an attention mechanism. We propose a
    new simple network architecture, the Transformer, based solely on attention mechanisms,
    dispensing with recurrence and convolutions entirely. Experiments on two machine translation
    tasks show these models to be superior in quality while being more parallelizable and
    requiring significantly less time to train.""",
    url="https://arxiv.org/abs/1706.03762",
    published_date=datetime.now(),
    source="arxiv",
)

async def test():
    config = get_config()

    print("=" * 60)
    print("🧪 测试DeepSeek摘要生成")
    print("=" * 60)
    print(f"\n论文标题: {test_paper.title}\n")

    # 创建summarizer
    summarizer = DeepSeekSummarizer(
        api_key=config.deepseek_api_key,
        model=config.deepseek_model,
        max_tokens=config.ai_max_tokens,
        temperature=config.ai_temperature,
        prompts_file=config.prompts_file,
    )

    print("正在生成摘要...\n")

    # 生成摘要
    summary = await summarizer.summarize(test_paper)

    print("=" * 60)
    print("📝 生成的摘要:")
    print("=" * 60)
    print(summary)
    print("\n" + "=" * 60)
    print(f"摘要长度: {len(summary)} 字符")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test())
