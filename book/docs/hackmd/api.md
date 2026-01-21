# HackMD API 文档

## 基本信息

- **Base URL**: `https://api.hackmd.io/v1`
- **认证方式**: Bearer Token
- **请求头**: `Authorization: Bearer {HACKMD_API_TOKEN}`

---

## 获取用户信息

`GET /me`

**响应**: 200

```json
{
  "id": "用户ID",
  "name": "用户名",
  "email": "邮箱",
  "userPath": "用户路径",
  "photo": "头像URL",
  "teams": [{ "id": "团队ID", "name": "团队名", "path": "团队路径" }]
}
```

---

## 获取笔记列表

`GET /notes`

**响应**: 200

```json
[
  {
    "id": "笔记ID",
    "title": "标题",
    "tags": ["标签"],
    "shortId": "短ID",
    "createdAt": 1643270371245,
    "lastChangedAt": 1643270452413,
    "readPermission": "guest",
    "writePermission": "signed_in",
    "publishLink": "发布链接"
  }
]
```

---

## 获取单个笔记

`GET /notes/{noteId}`

**响应**: 200

```json
{
  "id": "笔记ID",
  "title": "标题",
  "content": "Markdown内容",
  "tags": ["标签"],
  "readPermission": "guest",
  "writePermission": "signed_in"
}
```

---

## 创建笔记

`POST /notes`

**请求体**:

| 字段 | 类型 | 可选值 |
|------|------|--------|
| title | string | |
| content | string | |
| readPermission | string | `owner`, `signed_in`, `guest` |
| writePermission | string | `owner`, `signed_in`, `guest` |
| commentPermission | string | `disabled`, `forbidden`, `owners`, `signed_in_users`, `everyone` |
| permalink | string | |

**响应**: 201，返回创建的笔记对象

**注意事项**:
- 标题优先级：content 中的 H1 标题 > YAML metadata 中的 title > title 字段 > "Untitled"
- `readPermission` 和 `writePermission` 需同时提供
- `writePermission` 必须比 `readPermission` 更严格

---

## 更新笔记

`PATCH /notes/{noteId}`

**请求体**:

| 字段 | 类型 | 可选值 |
|------|------|--------|
| content | string | |
| readPermission | string | `owner`, `signed_in`, `guest` |
| writePermission | string | `owner`, `signed_in`, `guest` |
| permalink | string | |

**响应**: 202 Accepted

---

## 删除笔记

`DELETE /notes/{noteId}`

**响应**: 204 No Content

---

## 获取阅读历史

`GET /history`

**响应**: 200，返回笔记数组（格式同"获取笔记列表"）
