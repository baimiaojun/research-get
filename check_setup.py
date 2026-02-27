#!/usr/bin/env python3
"""
配置检查脚本 - 支持DeepSeek和Claude
"""
import os
import sys
import asyncio


def check_env_vars():
    """检查环境变量"""
    print("📋 检查环境变量配置...")

    # 检查AI服务配置
    ai_service = os.getenv('AI_SERVICE', 'none').lower()
    print(f"   ✓ AI服务: {ai_service}")

    # 必需的环境变量
    required = ['WECOM_WEBHOOK_URL']

    # 根据AI服务添加对应的API Key检查
    if ai_service == 'claude':
        required.append('CLAUDE_API_KEY')
    elif ai_service == 'deepseek':
        required.append('DEEPSEEK_API_KEY')

    missing = []

    for var in required:
        value = os.getenv(var)
        if not value:
            missing.append(var)
            print(f"   ❌ {var}: 未配置")
        else:
            # 显示部分值用于验证
            if 'API_KEY' in var:
                masked = value[:10] + '...' if len(value) > 10 else value[:5] + '...'
                print(f"   ✅ {var}: {masked}")
            else:
                masked = value[:40] + '...' if len(value) > 40 else value
                print(f"   ✅ {var}: {masked}")

    if missing:
        print(f"\n❌ 缺少环境变量: {', '.join(missing)}")
        return False

    print("\n✅ 所有必需的环境变量已配置")
    return True


async def test_deepseek_api(api_key):
    """测试DeepSeek API"""
    import aiohttp

    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 5
            }
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            async with session.post(
                "https://api.deepseek.com/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    print("   ✅ DeepSeek API 连接成功")
                    return True
                else:
                    result = await response.text()
                    print(f"   ❌ DeepSeek API 失败 ({response.status}): {result[:100]}")
                    return False
    except Exception as e:
        print(f"   ❌ DeepSeek API 测试失败: {e}")
        return False


def test_ai_service():
    """测试AI服务"""
    ai_service = os.getenv('AI_SERVICE', 'none').lower()

    if ai_service == 'none':
        print("\n📋 AI服务: 未启用")
        print("   ℹ️  将使用原始摘要")
        return True

    elif ai_service == 'deepseek':
        print("\n📋 测试DeepSeek API...")
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            print("   ❌ DEEPSEEK_API_KEY 未配置")
            return False

        try:
            return asyncio.run(test_deepseek_api(api_key))
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
            return False

    elif ai_service == 'claude':
        print("\n📋 测试Claude API...")
        # 简化的Claude测试
        api_key = os.getenv('CLAUDE_API_KEY')
        if not api_key:
            print("   ❌ CLAUDE_API_KEY 未配置")
            return False
        print("   ℹ️  Claude API配置已就绪")
        return True

    else:
        print(f"\n⚠️  未知的AI服务: {ai_service}")
        return True  # 不阻止继续


async def test_wecom_async(webhook):
    """异步测试企业微信"""
    try:
        import aiohttp
    except ImportError:
        print("   ⚠️  正在安装aiohttp...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'aiohttp', '-q'])
        import aiohttp

    payload = {
        "msgtype": "text",
        "text": {
            "content": "✅ 学术推送系统配置成功！\n\n配置检查通过，系统运行正常。"
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as response:
                result = await response.json()

                if result.get('errcode') == 0:
                    print("   ✅ 企业微信推送成功")
                    print("   📱 请检查企业微信群消息")
                    return True
                else:
                    print(f"   ❌ 推送失败")
                    print(f"   错误码: {result.get('errcode')}")
                    print(f"   错误信息: {result.get('errmsg')}")
                    return False
    except Exception as e:
        print(f"   ❌ 企业微信测试失败: {e}")
        return False


def test_wecom():
    """测试企业微信"""
    print("\n📋 测试企业微信Webhook...")

    webhook = os.getenv('WECOM_WEBHOOK_URL')
    if not webhook:
        print("   ❌ WECOM_WEBHOOK_URL 未配置")
        return False

    try:
        return asyncio.run(test_wecom_async(webhook))
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🔍 学术推送系统 - 配置检查工具")
    print("=" * 60)

    checks = [
        ("环境变量配置", check_env_vars),
        ("AI服务连接", test_ai_service),
        ("企业微信推送", test_wecom),
    ]

    results = []
    for name, func in checks:
        try:
            result = func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ {name}检查失败: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    print("📊 检查结果汇总")
    print("=" * 60)

    for i, (name, _) in enumerate(checks):
        status = "✅ 通过" if results[i] else "❌ 失败"
        print(f"{status} - {name}")

    print("=" * 60)

    if all(results):
        print("\n🎉 所有检查通过！系统配置成功！")
        sys.exit(0)
    else:
        print("\n⚠️  部分检查失败")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n💥 程序异常: {e}")
        sys.exit(1)
