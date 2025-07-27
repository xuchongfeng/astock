import React from 'react';
import { useParams } from 'react-router-dom';
import { Card, Row, Col, Tabs, Descriptions, Tag, Statistic } from 'antd';
import KLineChart from '../components/KLineChart';

const { TabPane } = Tabs;

const CompanyDetail = () => {
  const { id } = useParams();

  // 实际应用中应该从API获取数据
  const company = {
    id: parseInt(id),
    ts_code: '600519.SH',
    symbol: '600519',
    name: '贵州茅台',
    industry: '饮料制造业',
    fullname: '贵州茅台酒股份有限公司',
    list_date: '2001-08-27',
    exchange: 'SSE',
    chairman: '丁雄军',
    reg_capital: 125619.78,
    setup_date: '1999-11-20',
    province: '贵州省',
    website: 'www.moutaichina.com',
    employees: 29971,
    status: '在市',
    main_business: '茅台酒及系列产品的生产与销售',
    business_scope: '茅台酒系列产品的生产与销售;饮料、食品、包装材料的生产与销售等',
    market: '主板',
    area: '贵州'
  };

  return (
    <Card title={`${company.name} (${company.ts_code})`} bordered={false}>
      <Tabs defaultActiveKey="basic">
        <TabPane tab="基本信息" key="basic">
          <Descriptions bordered column={2}>
            <Descriptions.Item label="股票代码">
              <Tag color="blue">{company.ts_code}</Tag>
            </Descriptions.Item>
            <Descriptions.Item label="公司全称">{company.fullname}</Descriptions.Item>
            <Descriptions.Item label="上市状态">
              <Tag color="green">{company.status}</Tag>
            </Descriptions.Item>
            <Descriptions.Item label="交易所">{company.exchange}</Descriptions.Item>
            <Descriptions.Item label="上市日期">{company.list_date}</Descriptions.Item>
            <Descriptions.Item label="行业">{company.industry}</Descriptions.Item>
            <Descriptions.Item label="注册资本">
              "0万元"
            </Descriptions.Item>
            <Descriptions.Item label="员工人数">{company.employees.toLocaleString()}</Descriptions.Item>
            <Descriptions.Item label="成立日期">{company.setup_date}</Descriptions.Item>
            <Descriptions.Item label="省份">{company.province}</Descriptions.Item>
            <Descriptions.Item label="董事长">{company.chairman || '未知'}</Descriptions.Item>
            <Descriptions.Item label="公司网址">
              <a href={`http://${company.website}`} target="_blank" rel="noreferrer">
                {company.website}
              </a>
            </Descriptions.Item>
          </Descriptions>
        </TabPane>

        <TabPane tab="财务数据" key="financial">
          <Row gutter={16}>
            <Col span={12}>
              <Card title="主营业务">
                <p>{company.main_business}</p>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="经营范围">
                <p>{company.business_scope}</p>
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane tab="历史行情" key="history">
          <div style={{ height: 500 }}>
            <KLineChart tsCode={company.ts_code} />
          </div>
        </TabPane>
      </Tabs>
    </Card>
  );
};

export default CompanyDetail;