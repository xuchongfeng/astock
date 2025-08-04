# Tag API 使用文档

## 概述

Tag API 提供了股票标签管理功能，包括标签的创建、查询、更新、删除，以及为股票添加/移除标签等功能。

## API 接口

### 1. 标签管理

#### 1.1 获取所有标签
```
GET /api/tag/tags
```

**查询参数：**
- `category` (可选): 标签分类 (trend/status/custom)

**响应示例：**
```json
{
    "code": 200,
    "message": "获取标签列表成功",
    "data": [
        {
            "id": 1,
            "name": "强势上涨",
            "description": "股票处于强势上涨趋势",
            "color": "#f5222d",
            "category": "trend",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    ]
}
```

#### 1.2 创建标签
```
POST /api/tag/tags
```

**请求体：**
```json
{
    "name": "新标签",
    "description": "标签描述",
    "color": "#1890ff",
    "category": "trend"
}
```

#### 1.3 获取单个标签
```
GET /api/tag/tags/{tag_id}
```

#### 1.4 更新标签
```
PUT /api/tag/tags/{tag_id}
```

**请求体：**
```json
{
    "name": "更新后的标签名",
    "description": "更新后的描述",
    "color": "#52c41a"
}
```

#### 1.5 删除标签
```
DELETE /api/tag/tags/{tag_id}
```

#### 1.6 获取热门标签
```
GET /api/tag/popular
```

**查询参数：**
- `limit` (可选): 返回数量限制，默认10

### 2. 股票标签管理

#### 2.1 获取股票的标签
```
GET /api/tag/stocks/{ts_code}/tags
```

**查询参数：**
- `user_id` (可选): 用户ID，不传则获取系统标签
- `include_expired` (可选): 是否包含过期标签，默认true

**响应示例：**
```json
{
    "code": 200,
    "message": "获取股票标签成功",
    "data": [
        {
            "id": 1,
            "ts_code": "000001.SZ",
            "tag_id": 1,
            "user_id": null,
            "start_date": "2024-01-01",
            "end_date": null,
            "note": "备注信息",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
            "tag": {
                "id": 1,
                "name": "强势上涨",
                "description": "股票处于强势上涨趋势",
                "color": "#f5222d",
                "category": "trend"
            }
        }
    ]
}
```

#### 2.2 为股票添加标签
```
POST /api/tag/stocks/{ts_code}/tags
```

**请求体：**
```json
{
    "tag_id": 1,
    "user_id": 1,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "note": "备注信息"
}
```

#### 2.3 移除股票的标签
```
DELETE /api/tag/stocks/{ts_code}/tags/{tag_id}
```

**查询参数：**
- `user_id` (可选): 用户ID

#### 2.4 获取股票的标签摘要
```
GET /api/tag/stocks/{ts_code}/summary
```

**查询参数：**
- `user_id` (可选): 用户ID

**响应示例：**
```json
{
    "code": 200,
    "message": "获取股票标签摘要成功",
    "data": {
        "ts_code": "000001.SZ",
        "tags": [...],
        "trend_tags": [...],
        "status_tags": [...],
        "custom_tags": [...]
    }
}
```

#### 2.5 根据标签获取股票列表
```
GET /api/tag/tags/{tag_id}/stocks
```

**查询参数：**
- `user_id` (可选): 用户ID

## 使用示例

### Python 示例

```python
import requests

# 基础URL
base_url = "http://localhost:5000/api/tag"

# 1. 获取所有标签
response = requests.get(f"{base_url}/tags")
tags = response.json()["data"]

# 2. 创建新标签
new_tag_data = {
    "name": "我的标签",
    "description": "这是一个自定义标签",
    "color": "#1890ff",
    "category": "custom"
}
response = requests.post(f"{base_url}/tags", json=new_tag_data)
new_tag = response.json()["data"]

# 3. 为股票添加标签
stock_tag_data = {
    "tag_id": new_tag["id"],
    "user_id": 1,
    "note": "这是一个测试标签"
}
response = requests.post(f"{base_url}/stocks/000001.SZ/tags", json=stock_tag_data)

# 4. 获取股票的标签
response = requests.get(f"{base_url}/stocks/000001.SZ/tags?user_id=1")
stock_tags = response.json()["data"]

# 5. 获取股票标签摘要
response = requests.get(f"{base_url}/stocks/000001.SZ/summary?user_id=1")
summary = response.json()["data"]
```

### JavaScript 示例

```javascript
// 基础URL
const baseUrl = "http://localhost:5000/api/tag";

// 1. 获取所有标签
async function getTags() {
    const response = await fetch(`${baseUrl}/tags`);
    const data = await response.json();
    return data.data;
}

// 2. 创建新标签
async function createTag(tagData) {
    const response = await fetch(`${baseUrl}/tags`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(tagData)
    });
    const data = await response.json();
    return data.data;
}

// 3. 为股票添加标签
async function addStockTag(tsCode, tagData) {
    const response = await fetch(`${baseUrl}/stocks/${tsCode}/tags`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(tagData)
    });
    const data = await response.json();
    return data.data;
}

// 4. 获取股票标签摘要
async function getStockTagSummary(tsCode, userId) {
    const response = await fetch(`${baseUrl}/stocks/${tsCode}/summary?user_id=${userId}`);
    const data = await response.json();
    return data.data;
}
```

## 标签分类说明

- **trend**: 走势标签，表示股票的走势状态
- **status**: 状态标签，表示股票的投资状态
- **custom**: 自定义标签，用户自定义的标签

## 初始化默认标签

运行以下命令初始化默认标签：

```bash
python app/scripts/init_tag.py
```

这将创建以下默认标签：

### 走势标签
- 强势上涨
- 温和上涨
- 横盘整理
- 温和下跌
- 强势下跌
- 突破
- 回调

### 状态标签
- 关注
- 买入
- 卖出
- 持有
- 观望
- 停牌
- 退市风险

### 自定义标签
- 龙头股
- 绩优股
- 成长股
- 价值股
- 概念股
- ST股
- 新股 