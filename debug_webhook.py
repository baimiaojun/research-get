#!/usr/bin/env python3
"""
企业微信Webhook调试工具
帮助诊断webhook连接问题
"""
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()


def validate_webhook_url():
    """验证webhook URL格式"""
    print("🔍 步骤1: 验证Webhook URL格式")
    print("-" * 60)

    webhook = os.getenv('WECOM_WEBHOOK_URL', '')

    if not webhook:
        print("   ❌ 环境变量 WECOM_WEBHOOK_URL 未设置")
        return False

    print(f"   📍 当前Webhook URL:")
    print(f"   {webhook}")
    print()

    # 检查URL格式
    if not webhook.startswith('https://qyapi.weixin.qq.com/'):
        print("   ⚠️  URL不是标准的企业微信webhook格式")
        print("   正确格式应该是: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=...")
        return False

    if 'key=' not in webhook:
        print("   ⚠️  URL中缺少key参数")
        return False

    # 提取key
    try:
        key = webhook.split('key=')[1].split('&')[0]
        print(f"   ✅ Key格式正确: {key[:10]}...{key[-10:]}")
    except:
        print("   ⚠️  无法解析key参数")
        return False

    print("   ✅ URL格式验证通过")
    return True


def test_with_requests():
    """使用requests库测试（同步）"""
    print("\n🔍 步骤2: 使用requests库测试连接")
    print("-" * 60)

    try:
        import requests
    except ImportError:
        print("   ⚠️  正在安装requests...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests', '-q'])
        import requests

    webhook = os.getenv('WECOM_WEBHOOK_URL')

    payload = {
        "msgtype": "text",
        "text": {
            "content": "🧪 Webhook调试测试消息\n\n如果看到这条消息，说明webhook工作正常！"
        }
    }

    print(f"   📤 发送测试消息...")
    print(f"   请求地址: {webhook[:50]}...")
    print(f"   请求数据: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    print()

    try:
        response = requests.post(
            webhook,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        print(f"   HTTP状态码: {response.status_code}")

        try:
            result = response.json()
            print(f"   返回结果: {json.dumps(result, ensure_ascii=False, indent=2)}")

            if result.get('errcode') == 0:
                print("\n   ✅ 企业微信推送成功！")
                print("   📱 请检查企业微信群是否收到消息")
                return True
            else:
                print(f"\n   ❌ 推送失败")
                print(f"   错误码: {result.get('errcode')}")
                print(f"   错误信息: {result.get('errmsg')}")

                # 提供错误码说明
                if result.get('errcode') == 93000:
                    print("\n   💡 错误93000说明:")
                    print("   这个错误通常表示:")
                    print("   1. Webhook URL已过期或被删除")
                    print("   2. Webhook的key参数不正确")
                    print("   3. 企业微信机器人已被移除")
                    print("\n   🔧 解决方法:")
                    print("   1. 在企业微信群中，查看机器人是否还存在")
                    print("   2. 删除旧机器人，重新添加一个新机器人")
                    print("   3. 复制新的Webhook URL")
                    print("   4. 更新GitHub Secrets中的 WECOM_WEBHOOK_URL")

                return False
        except:
            print(f"   返回内容: {response.text}")
            return False

    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
        return False


def generate_curl_command():
    """生成curl命令供手动测试"""
    print("\n🔍 步骤3: 生成curl测试命令")
    print("-" * 60)

    webhook = os.getenv('WECOM_WEBHOOK_URL')

    curl_cmd = f'''curl -X POST '{webhook}' \\
  -H 'Content-Type: application/json' \\
  -d '{{
    "msgtype": "text",
    "text": {{
      "content": "手动测试消息"
    }}
  }}'
'''

    print("   📋 你可以在终端手动运行以下命令测试:")
    print()
    print(curl_cmd)
    print()
    print("   如果返回 {\"errcode\":0,\"errmsg\":\"ok\"} 则webhook正常")
    print("   如果返回错误码93000，则需要重新生成webhook")


def provide_solution_guide():
    """提供解决方案指南"""
    print("\n" + "=" * 60)
    print("📖 重新配置Webhook指南")
    print("=" * 60)
    print("""
如果上述测试失败（错误码93000），请按以下步骤操作:

1️⃣  在企业微信打开目标群
2️⃣  点击群设置 → 群机器人
3️⃣  找到之前添加的机器人，点击删除
4️⃣  重新点击"添加群机器人"
5️⃣  复制新生成的Webhook URL（完整的URL）
6️⃣  在GitHub仓库中:
   - Settings → Secrets and variables → Actions
   - 找到 WECOM_WEBHOOK_URL
   - 点击Update更新为新的URL
7️⃣  重新运行配置检查

注意: Webhook URL看起来像这样:
https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
""")


def main():
    print("=" * 60)
    print("🧪 企业微信Webhook调试工具")
    print("=" * 60)
    print()

    # 步骤1: 验证URL格式
    if not validate_webhook_url():
        print("\n❌ URL格式验证失败，请检查配置")
        provide_solution_guide()
        sys.exit(1)

    # 步骤2: 测试连接
    if test_with_requests():
        print("\n" + "=" * 60)
        print("🎉 Webhook测试成功！")
        print("=" * 60)
        sys.exit(0)
    else:
        # 步骤3: 提供调试信息
        generate_curl_command()
        provide_solution_guide()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 程序异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
