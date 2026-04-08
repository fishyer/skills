---
name: workflowy
description: "Manage Workflowy outlines via API. Use when the user wants to create, read, update, delete, move, complete nodes in Workflowy, or list/export their outline."
---

# Workflowy Skill

通过 Workflowy API 管理大纲笔记。

## 认证

API Key 存储在环境变量 `WORKFLOWY_API_KEY` 中。

所有请求需携带 Header: `Authorization: Bearer $WORKFLOWY_API_KEY`

## API Base URL

```
https://workflowy.com/api/v1
```

## 核心概念

- **Node**: 大纲中的每个节点（bullet point），包含文本、备注、子节点
- **Target**: 快捷位置，如 `inbox`（收集箱）、`home`（首页）、用户自定义快捷方式
- **parent_id**: 可以是节点 UUID、target key（如 `"inbox"`、`"home"`）、或 `"None"`（顶级）

## API 端点

### 节点 CRUD

| 操作 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 创建节点 | POST | `/nodes` | Body: `{parent_id, name, note?, layoutMode?, position?}` |
| 更新节点 | POST | `/nodes/:id` | Body: `{name?, note?, layoutMode?}` |
| 获取节点 | GET | `/nodes/:id` | 返回单个节点详情 |
| 列出子节点 | GET | `/nodes?parent_id=xxx` | 返回子节点列表（无序，按 priority 排序） |
| 删除节点 | DELETE | `/nodes/:id` | 永久删除，不可恢复 |
| 移动节点 | POST | `/nodes/:id/move` | Body: `{parent_id, position?}` |
| 完成节点 | POST | `/nodes/:id/complete` | 标记为已完成 |
| 取消完成 | POST | `/nodes/:id/uncomplete` | 取消完成状态 |
| 导出全部 | GET | `/nodes-export` | 返回所有节点（限速 1次/分钟） |

### 快捷方式

| 操作 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 列出 targets | GET | `/targets` | 返回所有快捷方式（inbox、home 等） |

## Node 对象

```json
{
  "id": "6ed4b9ca-256c-bf2e-bd70-d8754237b505",
  "name": "节点文本",
  "note": "备注内容",
  "priority": 200,
  "data": { "layoutMode": "bullets" },
  "createdAt": 1753120779,
  "modifiedAt": 1753120850,
  "completedAt": null
}
```

## 使用示例

```bash
# 创建节点（加到收集箱）
curl -s -X POST "https://workflowy.com/api/v1/nodes" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"parent_id":"inbox","name":"新节点","position":"top"}'

# 列出收集箱子节点
curl -s -G "https://workflowy.com/api/v1/nodes" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY" \
  -d "parent_id=inbox"

# 获取单个节点
curl -s "https://workflowy.com/api/v1/nodes/<NODE_ID>" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"

# 更新节点
curl -s -X POST "https://workflowy.com/api/v1/nodes/<NODE_ID>" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"更新后的文本"}'

# 完成节点
curl -s -X POST "https://workflowy.com/api/v1/nodes/<NODE_ID>/complete" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"

# 移动节点
curl -s -X POST "https://workflowy.com/api/v1/nodes/<NODE_ID>/move" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"parent_id":"inbox","position":"top"}'

# 删除节点（不可恢复！）
curl -s -X DELETE "https://workflowy.com/api/v1/nodes/<NODE_ID>" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"

# 导出全部节点（限速 1次/分钟）
curl -s "https://workflowy.com/api/v1/nodes-export" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"

# 列出快捷方式
curl -s "https://workflowy.com/api/v1/targets" \
  -H "Authorization: Bearer $WORKFLOWY_API_KEY"
```

## 格式化支持

`name` 字段支持 Markdown 语法：

| Markdown | 效果 |
|----------|------|
| `# text` | H1 标题 |
| `## text` | H2 标题 |
| `### text` | H3 标题 |
| `- text` | 子节点 |
| `- [ ] text` | 未完成待办 |
| `- [x] text` | 已完成待办 |
| `**text**` | **粗体** |
| `*text*` | *斜体* |
| `~~text~~` | ~~删除线~~ |
| `` `text` `` | 行内代码 |
| `[text](url)` | 超链接 |
| `[2026-04-08]` | 日期 |
| `[2026-04-08 14:30]` | 日期+时间 |

多行文本：第一行是父节点，`\n\n` 分隔的后续行自动成为子节点。

## 注意事项

- 删除节点不可恢复，操作前需确认
- `nodes-export` 限速 1 次/分钟
- 列出子节点返回无序，需按 `priority` 字段排序（值越小越靠前）
- `position` 参数：`"top"`（默认）或 `"bottom"`
