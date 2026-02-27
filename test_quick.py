#!/usr/bin/env python3
"""
快速测试脚本 - 验证配置和推送
"""
import os
import sys
import asyncio

# 检查.env文件
if not os.path.exists('.env'):
    print("❌ 未找到.env文件")
    print("请先创建.env文件并填入配置")
    sys.exit(1)

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("🧪 快速测试脚本")
print("=" * 60)

# 检查配置
print("\n📋 检查配置...")

webhook = os.getenv('WECOM_WEBHOOK_URL')
ai_service = os.getenv('AI_SERVICE', 'none')

print(f"✓ AI服务: {ai_service}")
print(f"✓ 企业微信Webhook: {webhook[:50]}...")

if not webhook or webhook == "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_WEBHOOK_KEY":
    print("\n❌ 请先在.env文件中配置真实的WECOM_WEBHOOK_URL")
    print("   获取方法：企业微信群 → 群机器人 → 添加机器人 → 复制Webhook")
    sys.exit(1)

# 测试企业微信推送
print("\n📤 测试企业微信推送...")

async def test_wecom():
    import aiohttp

    payload = {
        "msgtype": "text",
        "text": {
            "content": "✅ 学术推送系统测试成功！\n\n配置正常，系统运行正常。"
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as response:
                result = await response.json()

                if result.get('errcode') == 0:
                    print("✅ 企业微信推送成功！")
                    print("📱 请检查企业微信群，应该收到测试消息")
                    return True
                else:
                    print(f"❌ 推送失败: {result}")
                    return False
    except Exception as e:
        print(f"❌ 推送失败: {e}")
        return False

# 运行测试
success = asyncio.run(test_wecom())

if success:
    print("\n" + "=" * 60)
    print("🎉 测试通过！")
    print("=" * 60)
    print("\n下一步：")
    print("1. 检查企业微信群是否收到测试消息")
    print("2. 如果收到，可以运行完整测试：")
    print("   python3 -m src.main")
    print("3. 如果满意，按照部署指南部署到GitHub")
else:
    print("\n" + "=" * 60)
    print("❌ 测试失败")
    print("=" * 60)
    print("\n请检查：")
    print("1. Webhook URL是否正确")
    print("2. 企业微信机器人是否已删除")
    print("3. 网络连接是否正常")
