import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Select, Spin, Tabs } from 'antd';
import { BarChartOutlined, StockOutlined } from '@ant-design/icons';
import IndustryStats from '@/components/IndustryStats';
import IndustryRanking from '@/components/IndustryRanking';
import { industryApi } from '@/api/industryApi';
import { industryStatsApi } from '@/api/industryStatsApi';

const { TabPane } = Tabs;

const IndustryStatsPage = () => {
  const [industries, setIndustries] = useState([]);
  const [selectedIndustry, setSelectedIndustry] = useState(null);
  const [loading, setLoading] = useState(true);
  const [rankingData, setRankingData] = useState([]);
  const [activeTab, setActiveTab] = useState('stats');

  // 获取行业列表
  useEffect(() => {
    const fetchIndustries = async () => {
      setLoading(true);
      try {
        const response = await industryApi.getAllIndustries();
        setIndustries(response);
        if (response.length > 0) {
          setSelectedIndustry(response[0].id);
        }
      } catch (error) {
        console.error('获取行业列表失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchIndustries();
  }, []);

  // 获取行业排行榜
  useEffect(() => {
    const fetchRanking = async () => {
      try {
        const today = new Date().toISOString().split('T')[0];
        const data = await industryStatsApi.getIndustryRanking('total_amount', today, 10);
        setRankingData(data);
      } catch (error) {
        console.error('获取行业排行榜失败:', error);
      }
    };

    fetchRanking();
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <Card title="行业统计分析" bordered={false}>
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={24}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                <Select
                  value={selectedIndustry}
                  onChange={setSelectedIndustry}
                  style={{ width: 300 }}
                  loading={loading}
                >
                  {industries.map(industry => (
                    <Select.Option key={industry.id} value={industry.id}>
                      {industry.name}
                    </Select.Option>
                  ))}
                </Select>

                {selectedIndustry && (
                  <div>
                    当前选择:
                    <span style={{ marginLeft: 8, fontWeight: 'bold' }}>
                      {industries.find(i => i.id === selectedIndustry)?.name}
                    </span>
                  </div>
                )}
              </div>

              <Tabs activeKey={activeTab} onChange={setActiveTab}>
                <TabPane tab="行业统计" key="stats" />
                <TabPane tab="行业排行" key="ranking" />
              </Tabs>
            </div>
          </Col>
        </Row>

        <Spin spinning={loading}>
          {activeTab === 'stats' && selectedIndustry ? (
            <IndustryStats
              industryId={selectedIndustry}
              industryName={industries.find(i => i.id === selectedIndustry)?.name}
            />
          ) : (
            <IndustryRanking data={rankingData} />
          )}
        </Spin>
      </Card>
    </div>
  );
};

export default IndustryStatsPage;