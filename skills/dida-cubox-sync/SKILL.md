---
name: dida-cubox-sync
description: >
  Sync Dida365 inbox URLs to Cubox with AI summaries, report to Telegram.
  Monitors Dida365 inbox for link tasks, saves them to Cubox (稍后读),
  generates Chinese summaries via GLM, and sends results to Telegram.
  Use when the user wants to set up or run the Dida365→Cubox auto-sync pipeline,
  check sync status, or troubleshoot sync issues.
---

# Dida365 → Cubox Auto Sync

自动将滴答清单收件箱中的链接任务转存到 Cubox，生成 AI 摘要，并通过 Telegram 推送报告。

## 工作流程

```
滴答清单 Inbox
  │
  ├─ 提取含 URL 的任务
  ├─ 去重检查（基于 state file）
  ├─ 保存到 Cubox
  ├─ 从滴答清单删除
  ├─ 抓取网页内容（zai-cli → fetch.py fallback）
  ├─ GLM 生成中文摘要
  └─ Telegram 推送报告 + 摘要
```

## 运行

```bash
python3 <SKILL_DIR>/sync.py
```

通常配合 cron 定时任务使用，建议每 30 分钟执行一次。

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `DIDA365_ACCESS_TOKEN` | ✅ | 滴答清单 Open API Token |
| `CUBOX_API_KEY` | ✅ | Cubox API Key（完整的保存 API URL） |
| `TELEGRAM_BOT_TOKEN` | ❌ | Telegram Bot Token，不设置则不推送 |
| `Z_AI_API_KEY` | ❌ | 智谱 GLM API Key，不设置则不生成摘要 |

## 配置

脚本内可调参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `TELEGRAM_CHAT_ID` | `5166227669` | Telegram 推送目标 Chat ID |
| `STATE_FILE` | `/home/z/my-project/.dida_cubox_sync.json` | 去重状态文件路径 |
| `ZAI_CLI` | `zai-cli` | zai-cli 命令路径 |
| `FETCH_SCRIPT` | `...web-content-fetcher/scripts/fetch.py` | 网页抓取 fallback 脚本 |

## URL 识别规则

脚本从滴答清单任务中提取 URL，支持以下格式：

1. Markdown 链接：`[标题](https://...)` → 提取 URL 和标题
2. 纯 URL 标题：`https://...` → 提取 URL，标题为空
3. URL 在内容中：标题为普通文本，content 字段以 `http` 开头 → 提取 URL 和标题

不含 URL 的任务会被跳过。

## 网页抓取策略

采用两级 fallback：

1. **zai-cli read**（首选）：速度快，适合大多数网站
2. **fetch.py**（fallback）：基于 Scrapling，支持微信公众号等 JS 渲染页面

## 摘要格式

由 GLM-4-Flash 生成，固定格式：

```
🏷️ 关键词：xxx, xxx, xxx
📝 摘要：xxxxxx
💡 亮点：xxxxxx
```

## Telegram 推送

- 同步报告：转存数量、跳过数量、清理数量
- 每篇文章单独推送摘要
- 内容超过 4000 字符自动截断
- 摘要失败时推送具体错误信息

## 依赖

- Python 3
- zai-cli（可选，用于网页抓取）
- web-content-fetcher skill（可选，fallback 网页抓取）
- scrapling, html2text, curl_cffi（fetch.py 依赖）
- curl（用于 API 调用）

## 故障排查

- **"网页读取解析失败"**：通常是 zai-cli 返回格式变化，会自动 fallback 到 fetch.py
- **"网页内容为空或过短"**：页面可能需要 JS 渲染，检查 fetch.py 是否正常工作
- **"GLM API 错误"**：检查 Z_AI_API_KEY 是否有效
- **Cubox 保存失败**：检查 CUBOX_API_KEY 是否包含完整 URL
