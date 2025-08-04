# DeepSeek模块安装和使用指南

## 概述

本项目已成功集成了DeepSeek API模块，提供了以下功能：

1. **查询用户余额** - 查看DeepSeek账户余额信息
2. **对话接口** - 支持单轮和多轮对话
3. **模型管理** - 获取可用模型列表

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 设置DeepSeek API密钥
export DEEPSEEK_API_KEY="your_deepseek_api_key"

# 可选：设置API基础URL（默认为https://api.deepseek.com）
export DEEPSEEK_BASE_URL="https://api.deepseek.com"
```

### 3. 启动服务器

```bash
python run.py
```

服务器将在 `http://localhost:5000` 启动。

## 文件结构

```
backend/
├── app/
│   ├── api/
│   │   └── deepseek_api.py          # DeepSeek API路由
│   ├── services/
│   │   └── deepseek_service.py      # DeepSeek服务层
│   └── config.py                    # 配置文件（已更新）
├── requirements.txt                  # 依赖文件（已更新）
├── DEEPSEEK_API_USAGE.md           # API使用文档
├── test_deepseek.py                # 测试脚本
└── README_DEEPSEEK.md              # 本文件
```

## 功能特性

### 1. 查询余额接口

- **路径**: `GET /api/deepseek/balance`
- **功能**: 查询当前用户的DeepSeek账户余额
- **返回**: 包含总余额、赠金余额、充值余额等信息

### 2. 对话接口

#### 单轮对话
- **路径**: `POST /api/deepseek/chat/single`
- **功能**: 创建简单的单轮对话

#### 多轮对话
- **路径**: `POST /api/deepseek/chat/continue`
- **功能**: 基于对话历史继续多轮对话

#### 完整对话
- **路径**: `POST /api/deepseek/chat`
- **功能**: 发送完整的对话请求，支持自定义参数

### 3. 模型管理

- **路径**: `GET /api/deepseek/models`
- **功能**: 获取可用的DeepSeek模型列表

## 测试

### 运行测试脚本

```bash
python test_deepseek.py
```

测试脚本会验证以下功能：
- 获取模型列表
- 查询用户余额
- 单轮对话
- 多轮对话
- 完整对话接口

### 手动测试

使用curl命令测试：

```bash
# 获取模型列表
curl -X GET "http://localhost:5000/api/deepseek/models"

# 查询余额
curl -X GET "http://localhost:5000/api/deepseek/balance"

# 单轮对话
curl -X POST "http://localhost:5000/api/deepseek/chat/single" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "model": "deepseek-chat"}'
```

## API文档

详细的API文档请参考：[DEEPSEEK_API_USAGE.md](DEEPSEEK_API_USAGE.md)

## 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| DEEPSEEK_API_KEY | "" | DeepSeek API密钥（必需） |
| DEEPSEEK_BASE_URL | "https://api.deepseek.com" | DeepSeek API基础URL |

### 配置文件

在 `app/config.py` 中已添加DeepSeek相关配置：

```python
# DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
```

## 错误处理

所有接口都包含完善的错误处理机制：

- **400**: 请求参数错误
- **401**: API密钥无效
- **500**: 服务器内部错误

错误响应格式：
```json
{
  "error": "错误描述信息"
}
```

## 注意事项

1. **API密钥安全**: 请妥善保管您的DeepSeek API密钥，不要将其提交到版本控制系统
2. **Token使用**: 对话会消耗token，请注意控制对话长度
3. **模型限制**: 不同模型可能有不同的参数限制，请参考DeepSeek官方文档
4. **错误重试**: 建议在生产环境中添加适当的错误处理和重试机制

## 更新日志

- **v1.0.0**: 初始版本，包含基础对话和余额查询功能
- 支持单轮、多轮对话
- 支持余额查询
- 支持模型列表获取
- 完善的错误处理机制

## 技术支持

如果遇到问题，请检查：

1. API密钥是否正确设置
2. 网络连接是否正常
3. 服务器是否正常启动
4. 查看服务器日志获取详细错误信息

更多信息请参考DeepSeek官方文档：https://api-docs.deepseek.com/ 