# 同花顺指数日线数据接口 - 增加指数名称

## 修改概述

本次修改为同花顺指数日线数据的列表接口增加了指数名称字段，通过关联查询 `ths_index` 表来获取对应的指数名称信息。

## 修改内容

### 1. 服务层修改 (`ths_index_daily_service.py`)

新增了 `get_all_ths_index_daily_with_name()` 方法：

```python
def get_all_ths_index_daily_with_name(filters=None, query_only=False):
    """获取包含指数名称的指数日线数据"""
    query = db.session.query(
        ThsIndexDaily,
        ThsIndex.name.label('index_name')
    ).join(
        ThsIndex, 
        ThsIndexDaily.ts_code == ThsIndex.ts_code, 
        isouter=True
    )
    
    if filters:
        for attr, value in filters.items():
            if hasattr(ThsIndexDaily, attr):
                query = query.filter(getattr(ThsIndexDaily, attr) == value)
    
    if query_only:
        return query
    return query.all()
```

**特点：**
- 使用 LEFT JOIN 关联 `ths_index` 表
- 通过 `ts_code` 字段进行关联
- 支持原有的过滤条件
- 返回包含指数名称的完整数据

### 2. API 层修改 (`ths_index_daily_api.py`)

修改了 `list_ths_index_daily()` 接口：

- 使用新的服务方法 `get_all_ths_index_daily_with_name()`
- 调整了排序逻辑，支持关联查询的字段排序
- 格式化返回数据，将指数名称添加到每条记录中

**返回数据格式：**
```json
{
  "data": [
    {
      "id": 1,
      "ts_code": "000001.SH",
      "trade_date": "2024-01-01",
      "close": 3000.0,
      "open": 2990.0,
      "high": 3010.0,
      "low": 2980.0,
      "pre_close": 2985.0,
      "avg_price": 2995.0,
      "change": 15.0,
      "pct_change": 0.5,
      "vol": 1000000.0,
      "turnover_rate": 2.5,
      "total_mv": 500000000000.0,
      "float_mv": 300000000000.0,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "index_name": "上证指数"
    }
  ],
  "total": 100
}
```

## 数据库关联关系

- `ths_index_daily.ts_code` ↔ `ths_index.ts_code`
- 使用 LEFT JOIN 确保即使没有对应指数名称的记录也能正常返回

## 兼容性

- 保持了原有接口的所有功能
- 新增的 `index_name` 字段为可选字段（可能为 NULL）
- 原有的过滤、分页、排序功能完全兼容

## 测试

可以使用提供的测试脚本 `test_ths_index_daily_with_name.py` 来验证修改：

```bash
cd backend
python test_ths_index_daily_with_name.py
```

## 注意事项

1. 确保 `ths_index` 表中有对应的指数基础数据
2. 如果某个 `ts_code` 在 `ths_index` 表中不存在，`index_name` 字段将为 NULL
3. 排序功能已优化，支持关联查询的字段排序

## 相关文件

- `backend/app/services/ths_index_daily_service.py` - 服务层
- `backend/app/api/ths_index_daily_api.py` - API 层
- `backend/app/models/ths_index_daily.py` - 指数日线模型
- `backend/app/models/ths_index.py` - 指数基础信息模型
- `backend/test_ths_index_daily_with_name.py` - 测试脚本 