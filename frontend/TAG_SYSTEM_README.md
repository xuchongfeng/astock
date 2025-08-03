# 股票标签系统

## 概述

股票标签系统允许用户为股票添加自定义标签，以便更好地管理和分类股票。系统包含两个主要表：

### 数据库表结构

#### 1. 股票标签表 (tag)
```sql
CREATE TABLE tag (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    name VARCHAR(64) NOT NULL UNIQUE COMMENT '标签名称',
    description VARCHAR(255) COMMENT '标签描述',
    color VARCHAR(16) DEFAULT '#1890ff' COMMENT '标签颜色',
    category VARCHAR(32) DEFAULT 'trend' COMMENT '标签分类：trend-走势，status-状态，custom-自定义',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票标签表';
```

#### 2. 股票标签关联表 (stock_tag)
```sql
CREATE TABLE stock_tag (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    ts_code VARCHAR(16) NOT NULL COMMENT '股票代码',
    tag_id INT NOT NULL COMMENT '标签ID',
    user_id INT NULL COMMENT '用户ID（NULL表示系统标签）',
    start_date DATE NULL COMMENT '标签开始日期',
    end_date DATE NULL COMMENT '标签结束日期',
    note TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (tag_id) REFERENCES tag(id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    UNIQUE KEY uk_stock_tag_user (ts_code, tag_id, user_id),
    INDEX idx_ts_code (ts_code),
    INDEX idx_tag_id (tag_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票标签关联表';
```

## 前端功能

### 1. API 文件
- `src/api/tagApi.js` - 标签相关的API接口

### 2. 组件
- `src/components/TagSelector.js` - 标签选择器组件
- `src/components/StockTags.js` - 股票标签展示组件

### 3. 页面
- `src/pages/TagManagementPage.js` - 标签管理页面
- `src/pages/StockTagPage.js` - 股票标签管理页面

## 功能特性

### 标签管理
- 创建、编辑、删除标签
- 设置标签颜色和分类
- 标签分类：走势、状态、自定义

### 股票标签
- 为股票添加多个标签
- 设置标签的有效期（开始日期、结束日期）
- 添加备注信息
- 支持用户个人标签和系统标签

### 标签展示
- 在股票列表中显示标签
- 标签颜色区分
- 支持标签管理（添加、编辑、删除）
- 限制显示数量，超出部分用"+N"表示

## 使用方法

### 1. 标签管理
访问 `/tag-management` 页面：
- 创建新标签
- 编辑现有标签
- 删除标签
- 设置标签颜色和分类

### 2. 股票标签管理
访问 `/stock-tag` 页面：
- 查看所有股票标签
- 添加新的股票标签
- 编辑现有股票标签
- 删除股票标签

### 3. 在股票列表中显示标签
在持仓记录中，每只股票都会显示其关联的标签，用户可以：
- 查看标签
- 添加新标签
- 编辑现有标签
- 删除标签

## 组件使用示例

### TagSelector 组件
```jsx
import TagSelector from '../components/TagSelector';

// 多选模式
<TagSelector 
  value={selectedTags} 
  onChange={setSelectedTags}
  mode="multiple"
  showCreate={true}
  showManage={true}
/>

// 单选模式
<TagSelector 
  value={selectedTag} 
  onChange={setSelectedTag}
  mode="single"
  category="trend"
/>
```

### StockTags 组件
```jsx
import StockTags from '../components/StockTags';

// 显示股票标签
<StockTags 
  tsCode="000001.SZ"
  showManage={true}
  maxDisplay={3}
  onTagsChange={(tags) => console.log('标签变化:', tags)}
/>
```

## 路由配置

在 `App.js` 中已添加以下路由：
- `/tag-management` - 标签管理页面
- `/stock-tag` - 股票标签管理页面

## 注意事项

1. 标签名称必须唯一
2. 股票标签支持有效期设置
3. 用户只能管理自己的标签
4. 系统标签对所有用户可见
5. 标签颜色使用十六进制格式

## 后续扩展

1. 标签筛选功能
2. 标签统计报表
3. 标签导入导出
4. 标签模板功能
5. 标签权限管理 