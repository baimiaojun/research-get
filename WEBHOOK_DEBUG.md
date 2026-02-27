# 🔧 企业微信Webhook调试指南

## 问题现象

在GitHub Actions中推送失败,错误码 **93000 - invalid webhook url**

但在本地测试webhook正常工作 ✅

## 🎯 解决方案

### 方案1: 检查GitHub Secrets配置（最可能的原因）

GitHub Secrets中的URL可能包含**多余的空格、换行符或引号**。

#### 操作步骤:

1. **打开GitHub仓库** → Settings → Secrets and variables → Actions

2. **找到 `WECOM_WEBHOOK_URL`**,点击**Update**

3. **重要!** 复制webhook URL时要注意:
   - ❌ 不要包含空格
   - ❌ 不要包含换行符
   - ❌ 不要包含引号
   - ❌ 不要有任何多余字符
   - ✅ 只复制纯URL

4. **正确的URL格式**:
   ```
   https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```

5. **粘贴时检查**:
   - 确保URL前后没有空格
   - 确保是完整的URL(从https开始)
   - 确保key参数完整

6. **保存后重新运行测试**

---

### 方案2: 重新生成Webhook (如果方案1无效)

企业微信的Webhook可能已过期或被禁用。

#### 操作步骤:

1. **打开企业微信** → 进入目标群

2. **点击群设置** → 群机器人

3. **删除旧机器人**:
   - 找到之前添加的机器人
   - 点击删除

4. **添加新机器人**:
   - 点击"添加群机器人"
   - 给机器人起个名字(如"学术推送")
   - 点击确定

5. **复制新的Webhook URL**:
   - 系统会显示Webhook地址
   - **小心复制完整URL**
   - 不要包含多余字符

6. **更新GitHub Secret**:
   - GitHub仓库 → Settings → Secrets → Actions
   - 找到 `WECOM_WEBHOOK_URL`
   - Update更新为新URL

7. **重新运行测试**

---

### 方案3: 验证IP限制 (少见)

企业微信可能限制某些IP访问。

#### 检查方法:

1. **本地测试**(已验证✅):
   ```bash
   python3 debug_webhook.py
   ```

2. **GitHub Actions测试**:
   - 查看Actions运行日志
   - 记录错误信息

3. **对比结果**:
   - 本地成功 + GitHub失败 = 可能是IP限制
   - 两者都失败 = Webhook本身问题

#### 解决办法:
- 联系企业微信管理员
- 查看是否有IP白名单设置
- 或考虑使用其他推送方式

---

## 🧪 调试工具

### 本地测试webhook

运行调试脚本:
```bash
python3 debug_webhook.py
```

这个脚本会:
1. ✅ 验证webhook URL格式
2. ✅ 测试实际连接
3. ✅ 提供详细错误信息
4. ✅ 生成curl测试命令

### 手动测试webhook

使用curl命令:
```bash
curl -X POST 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=你的key' \
  -H 'Content-Type: application/json' \
  -d '{
    "msgtype": "text",
    "text": {
      "content": "手动测试"
    }
  }'
```

**期望结果**:
```json
{"errcode":0,"errmsg":"ok"}
```

---

## ✅ 验证步骤

完成修复后,按以下步骤验证:

1. **运行配置检查**:
   - GitHub → Actions
   - "🔍 检查配置" workflow
   - Run workflow

2. **查看输出**:
   - 应该显示 `✅ 企业微信推送成功`
   - 企业微信群收到测试消息

3. **运行完整推送**:
   - "Daily Academic Digest" workflow
   - Run workflow
   - 验证收到学术资讯

---

## 📋 常见错误码

| 错误码 | 含义 | 解决方法 |
|-------|------|---------|
| 0 | 成功 | 正常 ✅ |
| 93000 | Webhook URL无效 | 检查URL格式、重新生成webhook |
| 93001 | 机器人不存在 | 重新添加机器人 |
| 93004 | Webhook已被禁用 | 重新生成webhook |
| 45009 | 接口调用超限 | 等待一段时间后重试 |

---

## 🆘 仍然无法解决?

如果尝试以上方法仍然失败:

1. **检查系统状态**:
   - 访问 https://work.weixin.qq.com/ 查看服务状态

2. **查看详细日志**:
   - GitHub Actions → 点击失败的运行
   - 展开"运行配置检查"步骤
   - 复制完整错误信息

3. **提交Issue**:
   - 提供完整错误日志
   - 说明尝试过的解决方案
   - 提供webhook URL格式(隐藏key部分)

---

## 💡 最佳实践

1. **定期更新webhook**:
   - 企业微信webhook可能会过期
   - 建议每季度更新一次

2. **保存备份**:
   - 保存webhook URL到安全位置
   - 多个群使用不同机器人

3. **监控推送**:
   - 定期检查是否收到推送
   - 设置GitHub Actions通知

4. **测试环境**:
   - 使用单独的测试群
   - 避免在主群频繁测试
