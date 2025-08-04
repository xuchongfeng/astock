# DeepSeek API 使用文档

本文档介绍了项目中集成的DeepSeek API接口的使用方法。

## 配置

在使用DeepSeek API之前，需要设置以下环境变量：

```bash
export DEEPSEEK_API_KEY="your_deepseek_api_key"
export DEEPSEEK_BASE_URL="https://api.deepseek.com"
```

## API接口

### 1. 查询用户余额

**接口地址：** `GET /api/deepseek/balance`

**描述：** 查询当前用户的DeepSeek账户余额

**请求示例：**
```bash
curl -X GET "http://localhost:5000/api/deepseek/balance" \
  -H "Authorization: Bearer your_api_key"
```

**响应示例：**
```json
{
  "is_available": true,
  "balance_infos": [
    {
      "currency": "CNY",
      "total_balance": "110.00",
      "granted_balance": "10.00",
      "topped_up_balance": "100.00"
    }
  ]
}
```

### 2. 发送对话请求

**接口地址：** `POST /api/deepseek/chat`

**描述：** 发送对话请求，支持自定义模型和参数

**请求示例：**
```bash
curl -X POST "http://localhost:5000/api/deepseek/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "你好"}
    ],
    "model": "deepseek-chat",
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

**响应示例：**
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "deepseek-chat",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "你好！有什么可以帮助你的吗？"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 5,
    "completion_tokens": 15,
    "total_tokens": 20
  }
}
```

### 3. 创建单轮对话

**接口地址：** `POST /api/deepseek/chat/single`

**描述：** 创建简单的单轮对话

**请求示例：**
```bash
curl -X POST "http://localhost:5000/api/deepseek/chat/single" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好",
    "model": "deepseek-chat",
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

### 4. 继续多轮对话

**接口地址：** `POST /api/deepseek/chat/continue`

**描述：** 基于对话历史继续多轮对话

**请求示例：**
```bash
curl -X POST "http://localhost:5000/api/deepseek/chat/continue" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_history": [
      {"role": "user", "content": "你好"},
      {"role": "assistant", "content": "你好！有什么可以帮助你的吗？"}
    ],
    "message": "请介绍一下自己",
    "model": "deepseek-chat",
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

**响应示例：**
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "deepseek-chat",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "我是DeepSeek，一个AI助手..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 30,
    "total_tokens": 55
  },
  "updated_conversation_history": [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮助你的吗？"},
    {"role": "user", "content": "请介绍一下自己"},
    {"role": "assistant", "content": "我是DeepSeek，一个AI助手..."}
  ]
}
```

### 5. 获取可用模型列表

**接口地址：** `GET /api/deepseek/models`

**描述：** 获取可用的DeepSeek模型列表

**请求示例：**
```bash
curl -X GET "http://localhost:5000/api/deepseek/models"
```

**响应示例：**
```json
{
  "models": [
    {
      "id": "deepseek-chat",
      "name": "DeepSeek Chat",
      "description": "通用对话模型"
    },
    {
      "id": "deepseek-coder",
      "name": "DeepSeek Coder",
      "description": "代码生成模型"
    },
    {
      "id": "deepseek-reasoner",
      "name": "DeepSeek Reasoner",
      "description": "推理模型"
    }
  ]
}
```

## 参数说明

### 对话参数

- **messages**: 对话消息列表，每个消息包含role和content
- **model**: 使用的模型名称，默认为"deepseek-chat"
- **temperature**: 温度参数，控制输出的随机性，范围0-1，默认为0.7
- **max_tokens**: 最大生成token数，默认为1000

### 消息格式

```json
{
  "role": "user|assistant|system",
  "content": "消息内容"
}
```

## 错误处理

所有接口在发生错误时会返回以下格式：

```json
{
  "error": "错误描述信息"
}
```

常见错误：
- 400: 请求参数错误
- 401: API密钥无效
- 500: 服务器内部错误

## 使用示例

### Python示例

```python
import requests

# 查询余额
response = requests.get("http://localhost:5000/api/deepseek/balance")
print(response.json())

# 发送对话
data = {
    "messages": [{"role": "user", "content": "你好"}],
    "model": "deepseek-chat"
}
response = requests.post("http://localhost:5000/api/deepseek/chat", json=data)
print(response.json())
```

### JavaScript示例

```javascript
// 查询余额
fetch('/api/deepseek/balance')
  .then(response => response.json())
  .then(data => console.log(data));

// 发送对话
fetch('/api/deepseek/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    messages: [{role: 'user', content: '你好'}],
    model: 'deepseek-chat'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 注意事项

1. 确保设置了正确的DEEPSEEK_API_KEY环境变量
2. 对话历史会消耗token，请注意控制对话长度
3. 不同模型可能有不同的参数限制，请参考DeepSeek官方文档
4. 建议在生产环境中添加适当的错误处理和重试机制 