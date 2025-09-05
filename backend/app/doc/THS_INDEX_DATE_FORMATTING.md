# 同花顺概念板块日期格式化

## 修改概述

本次修改为同花顺概念板块相关的所有日期字段添加了统一的格式化展示，确保所有日期都以 `YYYY-MM-DD` 格式显示，包括前端展示、后端数据返回和查询参数处理。

## 修改内容

### 1. 前端页面修改 (`ThsIndexPage.js`)

#### 1.1 表格列日期格式化
为表格列添加了日期格式化渲染：

- **交易日** (`trade_date`): 使用 `formatDate(value, 'YYYY-MM-DD')` 格式化
- **创建时间** (`created_at`): 使用 `formatDate(value, 'YYYY-MM-DD')` 格式化  
- **更新时间** (`updated_at`): 使用 `formatDate(value, 'YYYY-MM-DD')` 格式化

#### 1.2 查询参数日期格式化
在发送查询请求时，自动将 `DatePicker` 组件的 moment 对象转换为 `YYYY-MM-DD` 格式：

```javascript
// 处理查询参数，格式化日期字段
const queryParams = { ...params };
if (queryParams.filters && queryParams.filters.trade_date) {
  // 将 moment 对象格式化为 YYYY-MM-DD 字符串
  queryParams.filters.trade_date = queryParams.filters.trade_date.format('YYYY-MM-DD');
}
```

### 2. 后端API修改 (`ths_index_daily_api.py`)

#### 2.1 日期参数处理
添加了日期参数格式验证和转换逻辑：

```python
# 处理日期参数，将YYYY-MM-DD格式转换为date对象
if key == 'trade_date':
    try:
        # 尝试解析YYYY-MM-DD格式的日期
        date_obj = datetime.strptime(value, '%Y-%m-%d').date()
        filters[key] = date_obj
    except ValueError:
        # 如果解析失败，返回错误信息
        return jsonify({'error': f'Invalid date format for {key}. Expected YYYY-MM-DD format.'}), 400
```

**特点：**
- 自动将 `YYYY-MM-DD` 格式的字符串转换为 Python `date` 对象
- 验证日期格式的正确性
- 对错误格式返回 400 错误和明确的错误信息

### 3. 后端模型修改

#### 3.1 ThsIndex 模型 (`ths_index.py`)

修改了 `as_dict()` 方法，为以下字段添加日期格式化：

- `list_date` (上市日期)
- `created_at` (创建时间)
- `updated_at` (更新时间)

#### 3.2 ThsIndexDaily 模型 (`ths_index_daily.py`)

修改了 `as_dict()` 方法，为以下字段添加日期格式化：

- `trade_date` (交易日)
- `created_at` (创建时间)
- `updated_at` (更新时间)

#### 3.3 ThsMember 模型 (`ths_member.py`)

修改了 `as_dict()` 方法，为以下字段添加日期格式化：

- `in_date` (纳入日期)
- `out_date` (剔除日期)
- `created_at` (创建时间)
- `updated_at` (更新时间)

### 4. 日期格式化逻辑

所有模型的 `as_dict()` 方法都使用相同的格式化逻辑：

```python
def as_dict(self):
    """返回字典格式，日期字段格式化为YYYY-MM-DD"""
    result = {}
    for c in self.__table__.columns:
        value = getattr(self, c.name)
        
        # 格式化日期字段
        if isinstance(value, datetime):
            result[c.name] = value.strftime('%Y-%m-%d')
        elif isinstance(value, db.Date):
            result[c.name] = value.strftime('%Y-%m-%d') if value else None
        else:
            result[c.name] = value
            
    return result
```

**特点：**
- 支持 `datetime` 和 `db.Date` 类型
- 统一格式为 `YYYY-MM-DD`
- 处理 `None` 值，避免格式化错误
- 保持其他字段类型不变

## 影响的字段

### ThsIndex (同花顺概念板块基础信息)
- `list_date`: 上市日期
- `created_at`: 创建时间
- `updated_at`: 更新时间

### ThsIndexDaily (同花顺概念板块日线数据)
- `trade_date`: 交易日
- `created_at`: 创建时间
- `updated_at`: 更新时间

### ThsMember (同花顺概念板块成分股)
- `in_date`: 纳入日期
- `out_date`: 剔除日期
- `created_at`: 创建时间
- `updated_at`: 更新时间

## 前端展示效果

修改后，前端表格中的日期字段将以以下格式显示：

- **之前**: `2024-01-01T10:00:00` 或 `2024-01-01 00:00:00`
- **之后**: `2024-01-01`

## 查询参数格式

### 支持的日期格式
- **正确格式**: `YYYY-MM-DD` (如: `2024-01-01`)
- **错误格式**: 任何不符合 `YYYY-MM-DD` 的格式

### 查询示例
```javascript
// 前端发送的查询参数
{
  ts_code: '000001.SH',
  trade_date: '2024-01-01',  // 自动格式化为 YYYY-MM-DD
  page: 1,
  page_size: 20
}
```

### 错误处理
如果日期格式不正确，API 将返回 400 错误：
```json
{
  "error": "Invalid date format for trade_date. Expected YYYY-MM-DD format."
}
```

## 兼容性

- 保持了原有接口的所有功能
- 日期格式从 ISO 格式转换为更友好的 `YYYY-MM-DD` 格式
- 不影响数据库存储，只影响数据展示和查询
- 支持空值处理，避免格式化错误
- 自动处理前端 DatePicker 组件的日期格式转换

## 测试

### 1. 日期格式化测试
可以使用提供的测试脚本 `test_date_formatting.py` 来验证模型日期格式化：

```bash
cd backend
python3 test_date_formatting.py
```

### 2. 查询参数格式测试
可以使用提供的测试脚本 `test_trade_date_format.py` 来验证查询参数格式转换：

```bash
cd backend
python3 test_trade_date_format.py
```

## 注意事项

1. 确保前端正确导入 `formatDate` 工具函数
2. 后端模型修改后，所有通过 `as_dict()` 返回的数据都会自动格式化
3. 查询参数中的 `trade_date` 必须使用 `YYYY-MM-DD` 格式
4. 如果需要在其他地方使用原始日期格式，可以直接访问模型属性而不是调用 `as_dict()`
5. 前端 DatePicker 组件会自动转换为正确的日期格式

## 相关文件

- `frontend/src/pages/ThsIndexPage.js` - 前端页面
- `frontend/src/utils/formatters.js` - 日期格式化工具
- `backend/app/api/ths_index_daily_api.py` - 后端API（日期参数处理）
- `backend/app/models/ths_index.py` - 概念板块基础信息模型
- `backend/app/models/ths_index_daily.py` - 概念板块日线数据模型
- `backend/app/models/ths_member.py` - 概念板块成分股模型
- `backend/test_date_formatting.py` - 日期格式化测试脚本
- `backend/test_trade_date_format.py` - 查询参数格式测试脚本 