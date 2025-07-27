import React, { useState } from 'react';
import { Descriptions, Tabs, Statistic, Tag } from 'antd';
import KLineChart from './KLineChart';
import { formatDate } from '../utils/formatters';

const { TabPane } = Tabs;

const CompanyInfoCard = ({ company }) => {
  const [activeTab, setActiveTab] = useState('basic');

  const statusColor = company.status === '在市' ? 'green' : 'red';

  return (
    <div style={{ margin: '-16px -24px' }}>
      <Tabs activeKey={activeTab} onChange={setActiveTab}>
        <TabPane tab="基本信息" key="basic">
          <Descriptions bordered column={2}>
            <Descriptions.Item label="股票代码">
              <Tag color="blue">{company.ts_code}</Tag>
            </Descriptions.Item>
            <Descriptions.Item label="公司全称">{company.fullname}</Descriptions.Item>
            <Descriptions.Item label="上市状态">
              <Tag color={statusColor}>{company.status}</Tag>
            </Descriptions.Item>
            <Descriptions.Item label="交易所">{company.exchange}</Descriptions.Item>
            <Descriptions.Item label="上市日期">{formatDate(company.list_date)}</Descriptions.Item>
            <Descriptions.Item label="行业">{company.industry}</Descriptions.Item>
            <Descriptions.Item label="注册资本">0</Descriptions.Item>
            <Descriptions.Item label="员工人数">{company.employees}</Descriptions.Item>
            <Descriptions.Item label="成立日期">{formatDate(company.setup_date)}</Descriptions.Item>
            <Descriptions.Item label="董事长">{company.chairman || '未知'}</Descriptions.Item>
            <Descriptions.Item label="公司网址">
              {company.website ? (
                <a href={company.website} target="_blank" rel="noreferrer">
                  {company.website}
                </a>
              ) : '--'}
            </Descriptions.Item>
          </Descriptions>
        </TabPane>

        <TabPane tab="财务数据" key="financial">
          <Descriptions bordered column={2}>
            <Descriptions.Item label="主营业务" span={2}>
              {company.main_business || '暂无信息'}
            </Descriptions.Item>
            <Descriptions.Item label="经营范围" span={2}>
              {company.business_scope || '暂无信息'}
            </Descriptions.Item>
          </Descriptions>
        </TabPane>
      </Tabs>

      <div style={{ marginTop: 20 }}>
        <h3>近期走势</h3>
        <KLineChart tsCode={company.ts_code} />
      </div>
    </div>
  );
};

export default CompanyInfoCard;