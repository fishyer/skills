---
name: cubox
description: "Save links, articles, and memos to Cubox (稍后读/书签收藏工具). Use when the user wants to save a URL, bookmark a page, or collect content to Cubox."
---

# Cubox Skill

通过 Cubox API 将链接、文章或笔记保存到 Cubox 收藏箱。

## 认证

API Key 存储在环境变量 `CUBOX_API_KEY` 中，值为完整的 API URL，例如：
```
https://cubox.pro/c/api/save/xxxxxxxxxxxxx
```

## 使用方式

通过 `curl` 调用，所有请求为 POST JSON 格式。

### 保存链接

```bash
curl -s -X POST "$CUBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"url","content":"<URL>","title":"<标题>","folder":"<文件夹>","tags":"<标签1>,<标签2>"}'
```

### 保存纯文本笔记

```bash
curl -s -X POST "$CUBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"memo","content":"<文本内容>","title":"<标题>","folder":"<文件夹>","tags":"<标签1>,<标签2>"}'
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `type` | 是 | `url`（收藏链接）或 `memo`（纯文本笔记） |
| `content` | 是 | 链接 URL 或笔记文本内容 |
| `title` | 否 | 标题，不传则 Cubox 自动解析 |
| `folder` | 否 | 目标文件夹，不传默认存到收集箱 |
| `tags` | 否 | 标签，多个用英文逗号分隔 |

## 返回值

```json
{"code":200,"message":"","data":null}
```

- `code: 200` → 保存成功
- 其他 code → 失败，查看 `message` 和 `data` 了解原因

## 注意事项

- Premium 用户每天 200 次 API 调用
- 保存成功后 Cubox 会自动进行文章解析和快照归档，需要一些时间
- API Key 是唯一身份凭证，不要泄露
