# 展开行功能修复说明

## 问题描述

前端页面能够正常获取成分股数据，但是展开行没有显示成分股表格。用户点击概念板块名称前的展开图标时，虽然数据已经获取，但页面没有渲染成分股列表。

## 问题分析

### 根本原因

问题出现在 Ant Design Table 组件的 `expandedRowKeys` 与 `rowKey` 不匹配：

1. **rowKey 设置**: `${record.ts_code}-${record.trade_date}` (例如: `885001.TI-2024-01-15`)
2. **expandedRowKeys 存储**: 之前存储的是 `ts_code` (例如: `885001.TI`)
3. **结果**: Ant Design 无法正确识别哪些行应该展开，因为 key 格式不一致

### 代码位置

问题出现在 `frontend/src/pages/ThsIndexPage.js` 文件中：

```javascript
// 问题代码
const handleExpand = (expanded, record) => {
  // ...
  if (expanded) {
    newExpandedRows.add(record.ts_code);  // ❌ 只存储 ts_code
  } else {
    newExpandedRows.delete(record.ts_code);  // ❌ 只删除 ts_code
  }
  // ...
};

// 表格配置
<Table
  rowKey={record => `${record.ts_code}-${record.trade_date}`}  // ✅ 格式: ts_code-trade_date
  expandable={{
    expandedRowKeys: Array.from(expandedRows),  // ❌ 存储的是 ts_code
    // ...
  }}
/>
```

## 解决方案

### 修复代码

在 `handleExpand` 函数中，使用与 `rowKey` 相同的格式来管理展开状态：

```javascript
const handleExpand = (expanded, record) => {
  console.log('行展开事件:', expanded, record);
  
  if (expanded) {
    // 展开时加载成分股数据
    console.log('展开行，开始加载成分股:', record.ts_code);
    fetchMemberData(record.ts_code);
  }
  
  // ✅ 使用与rowKey相同的格式作为展开行的标识
  const rowKey = `${record.ts_code}-${record.trade_date}`;
  const newExpandedRows = new Set(expandedRows);
  if (expanded) {
    newExpandedRows.add(rowKey);  // ✅ 存储完整的 rowKey
  } else {
    newExpandedRows.delete(rowKey);  // ✅ 删除完整的 rowKey
  }
  setExpandedRows(newExpandedRows);
  console.log('更新展开行状态:', Array.from(newExpandedRows));
};
```

### 修复原理

1. **一致性**: 确保 `expandedRowKeys` 中的每个 key 都与 `rowKey` 的格式完全一致
2. **唯一性**: 每行都有唯一的 `rowKey`，避免了不同日期的同一板块混淆
3. **状态管理**: React 状态更新后，Ant Design 能正确识别展开的行

## 验证步骤

### 1. 运行测试脚本

```bash
cd backend
python3 test_expandable_table_fix.py
```

**预期结果**: 所有测试都应该通过，数据结构正常

### 2. 前端功能测试

1. 访问同花顺指数页面
2. 点击概念板块名称前的展开图标
3. 验证成分股列表是否正常显示
4. 检查控制台输出，确认没有错误

### 3. 控制台验证

前端控制台应该显示以下调试信息：

```
行展开事件: true {ts_code: "885001.TI", trade_date: "2024-01-15", ...}
展开行，开始加载成分股: 885001.TI
开始获取成分股数据: 885001.TI
发送API请求获取成分股: 885001.TI
成分股API响应: {data: {...}}
成分股数据获取成功: 885001.TI 数量: 25
更新展开行状态: ["885001.TI-2024-01-15"]
渲染展开行: 885001.TI
显示成分股表格: 885001.TI 数量: 25
```

## 技术细节

### Ant Design Table 展开行机制

1. **rowKey**: 每行的唯一标识符
2. **expandedRowKeys**: 当前展开行的 key 数组
3. **expandedRowRender**: 展开行的渲染函数
4. **onExpand**: 展开/收起事件处理函数

### 状态管理

```javascript
// 展开行状态
const [expandedRows, setExpandedRows] = useState(new Set());

// 成分股数据缓存
const [memberData, setMemberData] = useState({});

// 加载状态
const [memberLoading, setMemberLoading] = useState({});
```

### 数据流

1. 用户点击展开图标 → `handleExpand` 被调用
2. `handleExpand` 更新 `expandedRows` 状态
3. `expandedRows` 变化触发 `expandedRowRender` 重新执行
4. `expandedRowRender` 从 `memberData` 中获取数据并渲染

## 相关文件

### 修复文件
- `frontend/src/pages/ThsIndexPage.js` - 前端页面，修复了展开行逻辑

### 测试文件
- `backend/test_expandable_table_fix.py` - 验证修复效果的测试脚本

### 文档文件
- `backend/app/doc/EXPANDABLE_TABLE_FIX.md` - 本文档

## 预防措施

### 1. 代码审查要点

- 确保 `expandedRowKeys` 与 `rowKey` 格式一致
- 验证展开行状态管理的正确性
- 检查数据缓存和加载状态的逻辑

### 2. 测试验证

- 编写展开行功能的自动化测试
- 验证不同数据场景下的展开行为
- 测试展开行的性能表现

### 3. 最佳实践

- 使用一致的 key 格式
- 实现数据缓存避免重复请求
- 添加适当的加载状态和错误处理

## 总结

通过修复 `expandedRowKeys` 与 `rowKey` 的格式不匹配问题，展开行功能现在应该能正常工作。关键修复点是确保状态管理的一致性，让 Ant Design Table 组件能够正确识别和管理展开的行。

修复后，用户点击展开图标时，成分股列表应该能够正常显示，包括股票代码、名称、权重、纳入日期等信息。 