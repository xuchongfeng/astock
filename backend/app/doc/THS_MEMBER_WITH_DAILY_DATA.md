# 同花顺概念成分股涨幅信息功能说明

## 功能概述

为同花顺概念成分股API增加了`trade_date`参数支持，关联`stock_daily`表获取成分股在指定交易日的涨幅信息，并按涨幅倒序排序返回。

## 新增功能特性

### 1. 参数支持
- **新增参数**: `trade_date` (交易日期，格式: YYYY-MM-DD)
- **原有参数**: 保持兼容，包括 `ts_code`, `con_code`, `is_new`, `page`, `pageSize`, `sortFields`

### 2. 数据关联
- **关联表**: `stock_daily` (股票日线数据表)
- **关联条件**: `ths_member.con_code = stock_daily.ts_code` 且 `stock_daily.trade_date = trade_date`
- **关联方式**: LEFT JOIN，确保即使没有日线数据的成分股也能返回

### 3. 涨幅信息
- **涨跌幅**: `pct_chg` (百分比)
- **涨跌额**: `change` (绝对数值)
- **收盘价**: `close` (当日收盘价)
- **昨收价**: `pre_close` (前一日收盘价)
- **成交量**: `vol` (手数)
- **成交额**: `amount` (元)
- **换手率**: `turnover_rate` (百分比)

### 4. 排序规则
- **有trade_date参数**: 按涨幅倒序排序 (`pct_chg` DESC)
- **无trade_date参数**: 保持原有排序逻辑

## API接口变化

### 请求示例

#### 1. 获取所有成分股（原有功能）
```http
GET /api/ths_member/?page=1&pageSize=20
```

#### 2. 获取指定日期的成分股涨幅信息（新功能）
```http
GET /api/ths_member/?page=1&pageSize=20&trade_date=2024-01-15
```

#### 3. 获取指定板块的成分股涨幅信息
```http
GET /api/ths_member/?ts_code=885001.TI&trade_date=2024-01-15&page=1&pageSize=50
```

### 响应格式

#### 原有格式（无trade_date参数）
```json
{
  "data": [
    {
      "id": 1,
      "ts_code": "885001.TI",
      "con_code": "000001.SZ",
      "con_name": "平安银行",
      "weight": 5.2,
      "in_date": "2020-01-01",
      "out_date": null,
      "is_new": "Y",
      "created_at": "2024-01-01",
      "updated_at": "2024-01-01"
    }
  ],
  "total": 100
}
```

#### 新格式（有trade_date参数）
```json
{
  "data": [
    {
      "id": 1,
      "ts_code": "885001.TI",
      "con_code": "000001.SZ",
      "con_name": "平安银行",
      "weight": 5.2,
      "in_date": "2020-01-01",
      "out_date": null,
      "is_new": "Y",
      "created_at": "2024-01-01",
      "updated_at": "2024-01-01",
      "pct_chg": 2.5,
      "change": 0.15,
      "close": 6.15,
      "pre_close": 6.00,
      "vol": 150000,
      "amount": 922500.00,
      "turnover_rate": 1.2
    }
  ],
  "total": 100,
  "trade_date": "2024-01-15"
}
```

## 技术实现

### 1. 服务层 (`ths_member_service.py`)

新增函数 `get_ths_member_with_daily_data`:

```python
def get_ths_member_with_daily_data(filters=None, trade_date=None, query_only=False):
    """
    获取成分股数据，关联stock_daily表获取涨幅信息
    """
    # 构建基础查询，关联stock_daily表
    query = db.session.query(
        ThsMember,
        StockDaily.pct_chg.label('pct_chg'),
        StockDaily.change.label('change'),
        StockDaily.close.label('close'),
        StockDaily.pre_close.label('pre_close'),
        StockDaily.vol.label('vol'),
        StockDaily.amount.label('amount'),
        StockDaily.turnover_rate.label('turnover_rate')
    ).outerjoin(
        StockDaily,
        db.and_(
            ThsMember.con_code == StockDaily.ts_code,
            StockDaily.trade_date == trade_date
        )
    )
    
    # 应用过滤条件
    if filters:
        for attr, value in filters.items():
            if hasattr(ThsMember, attr):
                query = query.filter(getattr(ThsMember, attr) == value)
    
    # 如果有交易日期，按涨幅倒序排序
    if trade_date:
        query = query.order_by(desc(StockDaily.pct_chg))
    
    if query_only:
        return query
    return query.all()
```

### 2. API层 (`ths_member_api.py`)

修改 `list_ths_member` 函数:

```python
@bp.route('/', methods=['GET'])
def list_ths_member():
    # 获取trade_date参数
    trade_date_str = request.args.get('trade_date')
    trade_date = None
    if trade_date_str:
        try:
            trade_date = datetime.strptime(trade_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid trade_date format. Expected YYYY-MM-DD format.'}), 400
    
    # 根据是否有trade_date参数选择不同的服务函数
    if trade_date:
        # 使用新函数获取带涨幅的数据
        query = get_ths_member_with_daily_data(filters, trade_date, query_only=True)
        # ... 处理数据并返回
    else:
        # 使用原有函数
        query = get_all_ths_member(filters, query_only=True)
        # ... 原有逻辑
```

### 3. 前端页面 (`ThsIndexPage.js`)

#### 修改成分股数据获取
```javascript
const fetchMemberData = async (ts_code) => {
  // 获取当前选中的交易日期
  const selectedDate = form.getFieldValue('trade_date');
  let tradeDate = null;
  
  if (selectedDate) {
    tradeDate = selectedDate.format('YYYY-MM-DD');
  } else {
    // 如果没有选择日期，使用当前记录的交易日期
    const currentRecord = data.find(item => item.ts_code === ts_code);
    if (currentRecord && currentRecord.trade_date) {
      tradeDate = currentRecord.trade_date;
    }
  }
  
  const res = await thsMemberApi.getByTsCode(ts_code, { 
    page_size: 100,
    trade_date: tradeDate
  });
  // ... 处理响应
};
```

#### 更新成分股表格列定义
```javascript
const memberColumns = [
  // 原有列
  { title: '股票代码', dataIndex: 'con_code', key: 'con_code' },
  { title: '股票名称', dataIndex: 'con_name', key: 'con_name' },
  
  // 新增涨幅相关列
  { 
    title: '涨跌幅', 
    dataIndex: 'pct_chg', 
    key: 'pct_chg',
    render: (value) => {
      if (value === null || value === undefined) return '-';
      const color = value > 0 ? '#f5222d' : value < 0 ? '#52c41a' : '#666';
      return <span style={{ color, fontWeight: 'bold' }}>
        {value > 0 ? '+' : ''}{value}%
      </span>;
    }
  },
  { title: '涨跌额', dataIndex: 'change', key: 'change' },
  { title: '收盘价', dataIndex: 'close', key: 'close' },
  { title: '成交量', dataIndex: 'vol', key: 'vol' },
  // ... 其他列
];
```

## 使用场景

### 1. 概念板块分析
- 查看某日概念板块内成分股的表现
- 分析成分股涨跌分布
- 识别板块内表现最好和最差的股票

### 2. 投资决策支持
- 根据成分股涨幅选择投资标的
- 分析板块整体表现趋势
- 评估板块内个股的相对表现

### 3. 风险控制
- 监控板块内高风险股票
- 分析板块整体风险暴露
- 识别异常波动的成分股

## 测试验证

### 运行测试脚本
```bash
cd backend
python3 test_ths_member_with_daily_data.py
```

### 测试要点
1. **原有功能兼容性**: 不带trade_date参数时功能正常
2. **新功能正确性**: 带trade_date参数时返回涨幅信息
3. **数据排序**: 按涨幅倒序排序
4. **错误处理**: 无效日期格式返回400错误
5. **数据完整性**: 涨幅相关字段正确返回

## 注意事项

### 1. 数据依赖
- 需要`stock_daily`表中有对应的日线数据
- 如果某只股票在指定日期没有数据，涨幅字段将为null

### 2. 性能考虑
- 关联查询可能影响性能，建议添加适当的索引
- 大量数据时注意分页处理

### 3. 向后兼容
- 原有API调用不受影响
- 新增参数为可选参数

## 总结

通过新增`trade_date`参数支持，同花顺概念成分股API现在能够：

1. **获取涨幅信息**: 关联`stock_daily`表获取成分股的涨跌幅、涨跌额等数据
2. **智能排序**: 按涨幅倒序排序，便于分析
3. **保持兼容**: 原有功能完全不受影响
4. **增强分析**: 为概念板块分析提供更丰富的数据支持

这个功能为前端页面提供了更完整的成分股信息展示，用户可以直观地看到概念板块内各成分股的表现情况，有助于投资决策和风险分析。 