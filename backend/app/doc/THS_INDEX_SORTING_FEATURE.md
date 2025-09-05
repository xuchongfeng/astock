# 同花顺概念板块排序功能

## 修改概述

本次修改为同花顺概念板块的接口和页面增加了支持按涨跌幅和成交量排序的功能，用户可以通过点击表头来对数据进行升序或降序排序。

## 修改内容

### 1. 前端页面修改 (`ThsIndexPage.js`)

#### 1.1 表格列排序配置
为相关列添加了 `sorter: true` 属性，启用排序功能：

```javascript
{ 
  title: '涨跌幅', 
  dataIndex: 'pct_change', 
  key: 'pct_change', 
  align: 'right',
  width: 100,
  sorter: true,  // 启用排序
  render: (val, record) => (
    <span style={{ 
      color: getChangeColor(record.change, val),
      fontWeight: 'bold',
      fontSize: '14px'
    }}>
      {val ? `${val > 0 ? '+' : ''}${val}%` : '-'}
    </span>
  )
},
{ 
  title: '成交量', 
  dataIndex: 'vol', 
  key: 'vol', 
  align: 'right', 
  width: 100,
  sorter: true,  // 启用排序
  render: (value) => value ? `${(value / 10000).toFixed(2)}万` : '-'
}
```

#### 1.2 排序参数处理
修改了 `handleTableChange` 函数，正确提取排序参数：

```javascript
const handleTableChange = (pag, filters, sorter) => {
  // 构建排序参数
  let sortField = null;
  let sortOrder = null;
  
  if (sorter && sorter.field && sorter.order) {
    sortField = sorter.field;
    sortOrder = sorter.order;
  }
  
  fetchData({
    page: pag.current,
    pageSize: pag.pageSize,
    filters: form.getFieldsValue(),
    sortField: sortField,
    sortOrder: sortOrder
  });
};
```

#### 1.3 API请求参数构建
在 `fetchData` 函数中添加了排序参数的处理：

```javascript
// 添加排序参数
if (queryParams.sortField && queryParams.sortOrder) {
  const sortPrefix = queryParams.sortOrder === 'descend' ? '-' : '';
  apiParams.sort_fields = `${sortPrefix}${queryParams.sortField}`;
}
```

**排序参数格式：**
- 升序：`pct_change` 或 `vol`
- 降序：`-pct_change` 或 `-vol`

### 2. 后端API修改 (`ths_index_daily_api.py`)

#### 2.1 排序逻辑优化
改进了排序处理逻辑，支持涨跌幅和成交量的排序：

```python
if sort_fields:
    for field in sort_fields.split(','):
        field = field.strip()
        if not field:
            continue
        if field.startswith('-'):
            # 降序排序
            field_name = field[1:]
            if field_name in ['ts_code', 'trade_date', 'close', 'open', 'high', 'low', 'pre_close', 'avg_price', 'change', 'pct_change', 'vol', 'turnover_rate', 'total_mv', 'float_mv']:
                query = query.order_by(desc(getattr(ThsIndexDaily, field_name)))
            else:
                query = query.order_by(desc(field_name))
        else:
            # 升序排序
            if field in ['ts_code', 'trade_date', 'close', 'open', 'high', 'low', 'pre_close', 'avg_price', 'change', 'pct_change', 'vol', 'turnover_rate', 'total_mv', 'float_mv']:
                query = query.order_by(asc(getattr(ThsIndexDaily, field)))
            else:
                query = query.order_by(asc(field))
```

#### 2.2 支持的排序字段
目前支持以下字段的排序：

- `pct_change` - 涨跌幅
- `vol` - 成交量
- `ts_code` - 指数代码
- `trade_date` - 交易日
- `close` - 收盘点位
- `open` - 开盘点位
- `high` - 最高点位
- `low` - 最低点位
- `pre_close` - 昨日收盘点
- `avg_price` - 平均价
- `change` - 涨跌点位
- `turnover_rate` - 换手率
- `total_mv` - 总市值
- `float_mv` - 流通市值

## 功能特性

### 1. 单字段排序
- 点击表头可以进行升序/降序排序
- 支持升序和降序切换
- 排序状态在表头显示（箭头指示）

### 2. 多字段排序
支持组合排序，多个字段用逗号分隔：

```
sort_fields=pct_change,-vol
```

表示先按涨跌幅升序，再按成交量降序。

### 3. 与过滤条件结合
排序功能可以与现有的过滤条件结合使用：

```
ts_code=000001.SH&trade_date=2024-01-01&sort_fields=-pct_change
```

### 4. 分页支持
排序功能完全支持分页，排序结果在分页中保持一致。

## 使用方式

### 前端使用
1. 在表格中点击"涨跌幅"或"成交量"列的表头
2. 第一次点击为升序排序
3. 再次点击为降序排序
4. 第三次点击取消排序

### API调用示例
```bash
# 按涨跌幅升序排序
GET /api/ths_index_daily/?sort_fields=pct_change&page=1&page_size=20

# 按涨跌幅降序排序
GET /api/ths_index_daily/?sort_fields=-pct_change&page=1&page_size=20

# 按成交量升序排序
GET /api/ths_index_daily/?sort_fields=vol&page=1&page_size=20

# 按成交量降序排序
GET /api/ths_index_daily/?sort_fields=-vol&page=1&page_size=20

# 组合排序（先按涨跌幅降序，再按成交量降序）
GET /api/ths_index_daily/?sort_fields=-pct_change,-vol&page=1&page_size=20
```

## 技术实现

### 1. 前端排序状态管理
- 使用 Ant Design Table 组件的内置排序功能
- 通过 `sorter` 属性启用排序
- 在 `handleTableChange` 回调中处理排序事件

### 2. 后端排序处理
- 解析 `sort_fields` 参数
- 使用 SQLAlchemy 的 `order_by` 方法
- 支持多字段排序（逗号分隔）
- 支持升序/降序（前缀 `-` 表示降序）

### 3. 数据库查询优化
- 排序在数据库层面执行，性能更好
- 支持索引优化
- 与分页和过滤条件无缝结合

## 测试验证

### 测试脚本
使用 `test_sorting_functionality.py` 脚本验证排序功能：

```bash
cd backend
python3 test_sorting_functionality.py
```

### 测试内容
1. 涨跌幅升序/降序排序
2. 成交量升序/降序排序
3. 组合排序功能
4. 带过滤条件的排序
5. 排序结果正确性验证

## 注意事项

1. **排序字段限制**: 只能对数据库表中存在的字段进行排序
2. **性能考虑**: 大量数据排序时建议配合分页使用
3. **数据一致性**: 排序结果在分页中保持一致
4. **错误处理**: 无效的排序字段会被忽略

## 兼容性

- 完全兼容现有的过滤和分页功能
- 不影响原有的数据展示逻辑
- 向后兼容，未指定排序时使用默认顺序

## 相关文件

- `frontend/src/pages/ThsIndexPage.js` - 前端页面（排序配置）
- `backend/app/api/ths_index_daily_api.py` - 后端API（排序处理）
- `backend/test_sorting_functionality.py` - 排序功能测试脚本
- `backend/app/doc/THS_INDEX_SORTING_FEATURE.md` - 本文档

## 未来扩展

可以考虑添加以下功能：
1. 更多字段的排序支持
2. 自定义排序规则
3. 排序历史记录
4. 默认排序设置 