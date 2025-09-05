# 同花顺热榜数据使用说明

## 功能概述

同花顺热榜数据功能集成了同花顺App的热榜数据，提供实时的市场热点信息，帮助投资者了解市场关注焦点和投资机会。

## 数据来源

- **数据接口**: Tushare Pro API - `ths_hot`
- **参考文档**: [https://tushare.pro/document/2?doc_id=320](https://tushare.pro/document/2?doc_id=320)
- **更新频率**: 每日盘中4次，收盘后4次，最晚22点更新

## 支持的热榜类型

1. **热股** - A股热门股票排行
2. **ETF** - 交易所交易基金排行
3. **可转债** - 可转换债券排行
4. **行业板块** - 行业板块热度排行
5. **概念板块** - 概念板块热度排行
6. **期货** - 期货品种热度排行
7. **港股** - 港股热门股票排行
8. **热基** - 热门基金排行
9. **美股** - 美股热门股票排行

## 数据字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| trade_date | Date | 交易日期 |
| data_type | String | 数据类型（热榜类型） |
| ts_code | String | 股票/基金代码 |
| ts_name | String | 股票/基金名称 |
| rank | Integer | 排行名次 |
| pct_change | Float | 涨跌幅（%） |
| current_price | Float | 当前价格 |
| concept | Text | 概念标签（JSON格式） |
| rank_reason | Text | 上榜解读 |
| hot | Float | 热度值 |
| rank_time | String | 排行榜获取时间 |

## API接口

### 1. 获取热榜数据列表

```http
GET /api/ths_hot/?page=1&pageSize=20&data_type=热股&start_date=2024-01-01&end_date=2024-01-15
```

**参数说明**:
- `page`: 页码（默认1）
- `pageSize`: 每页数量（默认20）
- `data_type`: 数据类型筛选
- `start_date`: 开始日期
- `end_date`: 结束日期
- `search`: 搜索关键词（股票代码、名称、标签）
- `sortFields`: 排序字段（如：rank,-trade_date）

### 2. 获取最新热榜数据

```http
GET /api/ths_hot/latest?data_type=热股&limit=100
```

**参数说明**:
- `data_type`: 数据类型（可选）
- `limit`: 返回数量限制（默认100）

### 3. 根据日期和类型获取数据

```http
GET /api/ths_hot/by-date-type?trade_date=2024-01-15&data_type=热股
```

### 4. 根据股票代码获取历史数据

```http
GET /api/ths_hot/by-ts-code/000001.SZ?limit=50
```

### 5. 获取统计信息

```http
GET /api/ths_hot/statistics?start_date=2024-01-01&end_date=2024-01-15
```

## 使用场景

### 1. 市场热点分析
- 了解当日市场关注焦点
- 分析热门股票和板块
- 跟踪市场情绪变化

### 2. 投资机会发现
- 发现热门概念和题材
- 识别市场热点轮动
- 寻找投资标的

### 3. 风险监控
- 监控市场过度炒作
- 识别投资风险点
- 跟踪市场情绪指标

### 4. 策略研究
- 热点轮动策略研究
- 市场情绪指标构建
- 量化投资策略开发

## 数据初始化

### 1. 运行初始化脚本

```bash
cd backend
python app/scripts/init_ths_hot.py
```

### 2. 配置Tushare Token

在运行脚本前，需要设置Tushare Pro的访问token：

```python
import tushare as ts
ts.set_token('your_tushare_token')
```

### 3. 自定义初始化参数

```python
# 指定日期范围和类型
init_ths_hot_data(
    start_date='2024-01-01',
    end_date='2024-01-15',
    market_types=['热股', '概念板块']
)
```

## 注意事项

1. **API限制**: Tushare Pro接口有调用频率限制，建议合理控制请求频率
2. **数据质量**: 热榜数据可能存在延迟，建议结合其他数据源进行交叉验证
3. **投资风险**: 热榜数据仅供参考，不构成投资建议，投资需谨慎
4. **数据更新**: 热榜数据每日多次更新，建议定期同步最新数据

## 常见问题

### Q: 为什么某些热榜类型没有数据？
A: 不同热榜类型的数据更新时间和可用性可能不同，建议检查Tushare接口文档或联系客服。

### Q: 热度值是如何计算的？
A: 热度值由同花顺平台根据用户关注度、搜索量、讨论热度等综合计算得出。

### Q: 如何获取历史热榜数据？
A: 可以通过日期范围查询获取历史数据，或使用股票代码查询特定标的的历史上榜记录。

### Q: 数据更新频率如何？
A: 每日盘中4次，收盘后4次，最晚22点更新，具体时间可能因市场情况有所调整。

## 技术支持

如有技术问题或建议，请联系：
- 项目维护者: [Xu ChongFeng]
- 邮箱: [far.far.away.away@gmail.com]
- 项目地址: [GitHub Repository URL] 