#!/usr/bin/env python3
"""
配置检查脚本 - 验证所有设置是否正确
可以通过GitHub Actions手动运行，无需本地环境
"""
import os
import sys


def check_env_vars():
    """检查环境变量"""
    print("📋 检查环境变量配置...")
    required = ['CLAUDE_API_KEY', 'WECOM_WEBHOOK_URL']
    missing = []

    for var in required:
        value = os.getenv(var)
        if not value:
            missing.append(var)
            print(f"   ❌ {var}: 未配置")
        else:
            # 显示部分值用于验证
            if var == 'CLAUDE_API_KEY':
                masked = value[:10] + '...' + value[-10:] if len(value) > 20 else value[:5] + '...'
                print(f"   ✅ {var}: {masked}")
            else:
                masked = value[:30] + '...' if len(value) > 30 else value
                print(f"   ✅ {var}: {masked}")

    if missing:
        print(f"\n❌ 缺少环境变量: {', '.join(missing)}")
        print("\n💡 请在GitHub仓库设置中添加这些Secrets：")
        print("   Settings → Secrets and variables → Actions → New repository secret")
        return False

    print("\n✅ 所有必需的环境变量已配置")
    return True


def test_claude_api():
    """测试Claude API连接"""
    print("\n📋 测试Claude API连接...")

    try:
        import anthropic
    except ImportError:
        print("   ⚠️  正在安装anthropic库...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'anthropic', '-q'])
        import anthropic

    try:
        api_key = os.getenv('CLAUDE_API_KEY')
        if not api_key:
            print("   ❌ CLAUDE_API_KEY 未配置")
            return False

        # 验证API Key格式
        if not api_key.startswith('sk-ant-'):
            print(f"   ⚠️  API Key格式可能不正确（应以 'sk-ant-' 开头）")
            print(f"   当前格式: {api_key[:10]}...")

        client = anthropic.Anthropic(api_key=api_key)

        # 发送测试请求
        print("   正在测试API调用...")
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            messages=[{"role": "user", "content": "Hello"}]
        )

        print("   ✅ Claude API 连接成功")
        print(f"   模型: {response.model}")
        print(f"   响应: {response.content[0].text[:50]}...")
        return True

    except anthropic.AuthenticationError:
        print("   ❌ Claude API 认证失败")
        print("   💡 请检查：")
        print("      1. API Key是否正确")
        print("      2. API Key是否已激活")
        print("      3. 访问 https://console.anthropic.com/ 查看API Keys状态")
        return False
    except anthropic.RateLimitError:
        print("   ⚠️  API调用频率限制")
        print("   💡 稍后再试或检查账户额度")
        return False
    except Exception as e:
        print(f"   ❌ Claude API 测试失败: {e}")
        print(f"   错误类型: {type(e).__name__}")
        return False


def test_wecom_webhook():
    """测试企业微信Webhook"""
    print("\n📋 测试企业微信Webhook...")

    try:
        import requests
    except ImportError:
        print("   ⚠️  正在安装requests库...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests', '-q'])
        import requests

    try:
        webhook = os.getenv('WECOM_WEBHOOK_URL')
        if not webhook:
            print("   ❌ WECOM_WEBHOOK_URL 未配置")
            return False

        # 验证Webhook URL格式
        if not webhook.startswith('https://qyapi.weixin.qq.com/'):
            print(f"   ⚠️  Webhook URL格式可能不正确")
            print(f"   应该以 'https://qyapi.weixin.qq.com/' 开头")
            print(f"   当前: {webhook[:40]}...")

        # 发送测试消息
        print("   正在发送测试消息...")
        payload = {
            "msgtype": "text",
            "text": {
                "content": "✅ 学术推送系统配置成功！\n\n这是一条测试消息，说明你的配置完全正确。\n每天早上8:00会自动推送学术资讯。\n\n🎉 开始享受每日学术资讯吧！"
            }
        }

        response = requests.post(webhook, json=payload, timeout=10)
        result = response.json()

        if result.get('errcode') == 0:
            print("   ✅ 企业微信推送测试成功")
            print("   📱 请检查企业微信群，应该收到一条测试消息")
            return True
        else:
            print(f"   ❌ 企业微信推送失败")
            print(f"   错误码: {result.get('errcode')}")
            print(f"   错误信息: {result.get('errmsg')}")
            print("\n   💡 可能的原因：")
            print("      1. Webhook URL不正确")
            print("      2. 机器人已被删除")
            print("      3. 网络连接问题")
            return False

    except requests.Timeout:
        print("   ❌ 请求超时")
        print("   💡 可能是网络问题，请稍后重试")
        return False
    except requests.RequestException as e:
        print(f"   ❌ 网络请求失败: {e}")
        return False
    except Exception as e:
        print(f"   ❌ 企业微信测试失败: {e}")
        print(f"   错误类型: {type(e).__name__}")
        return False


def test_optional_config():
    """测试可选配置"""
    print("\n📋 检查可选配置...")

    optional_vars = {
        'PAPERS_TO_SEND': '每日推送论文数量',
        'LOG_LEVEL': '日志级别',
        'ENABLE_ARXIV': '是否启用arXiv数据源',
    }

    found_any = False
    for var, desc in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value} ({desc})")
            found_any = True

    if not found_any:
        print("   ℹ️  未配置可选参数（使用默认值）")

    print("\n   💡 可选配置说明：")
    print("      - PAPERS_TO_SEND: 每日推送论文数量（默认6篇）")
    print("      - LOG_LEVEL: 日志级别 DEBUG/INFO/WARNING（默认INFO）")
    print("      - ENABLE_ARXIV: 启用arXiv数据源（默认true）")


def main():
    """主函数"""
    print("=" * 60)
    print("🔍 学术推送系统 - 配置检查工具")
    print("=" * 60)

    checks = [
        ("环境变量配置", check_env_vars),
        ("Claude API连接", test_claude_api),
        ("企业微信推送", test_wecom_webhook),
    ]

    results = []
    for name, func in checks:
        try:
            result = func()
            results.append(result)
        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ {name}检查时发生意外错误: {e}")
            results.append(False)

    # 检查可选配置（不影响结果）
    try:
        test_optional_config()
    except Exception as e:
        print(f"\n⚠️  可选配置检查失败: {e}")

    # 总结
    print("\n" + "=" * 60)
    print("📊 检查结果汇总")
    print("=" * 60)

    for i, (name, _) in enumerate(checks):
        status = "✅ 通过" if results[i] else "❌ 失败"
        print(f"{status} - {name}")

    print("=" * 60)

    if all(results):
        print("\n🎉 恭喜！所有检查都通过了！")
        print("\n✨ 你的学术推送系统已经配置完成！")
        print("\n📅 系统将在每天早上8:00（北京时间）自动推送学术资讯")
        print("📱 推送内容会发送到你配置的企业微信群")
        print("\n💡 下一步：")
        print("   1. 检查企业微信群是否收到测试消息")
        print("   2. 运行 'Daily Academic Digest' 工作流测试完整推送")
        print("   3. 编辑 config/keywords.yml 自定义关注领域")
        print("\n🔗 更多信息请查看：")
        print("   - README.md - 项目说明")
        print("   - SETUP_TUTORIAL.md - 详细教程")
        print("   - docs/faq.md - 常见问题")
        sys.exit(0)
    else:
        print("\n⚠️  部分检查失败，请根据上方提示修复问题")
        print("\n💡 常见问题：")
        print("   1. 检查Secrets名称是否完全正确（区分大小写）")
        print("   2. 检查API Key和Webhook URL是否完整复制")
        print("   3. 查看详细错误信息了解具体原因")
        print("\n📖 需要帮助？")
        print("   - 查看 SETUP_TUTORIAL.md 详细教程")
        print("   - 查看 docs/faq.md 常见问题")
        print("   - 提交 Issue 寻求帮助")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n💥 程序异常终止: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
