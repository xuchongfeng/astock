import React, { useState, useEffect } from 'react';
import { Card, Button, Tag, Statistic } from 'antd';
import { StarFilled, StarOutlined } from '@ant-design/icons';
import { formatCurrency, formatPercent } from '@/utils/formatters';
import { watchlistApi } from '@/api/watchlistApi';

const StockItem = ({ stock, userId }) => {
  const [isInWatchlist, setIsInWatchlist] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const checkWatchlistStatus = async () => {
      try {
        const status = await watchlistApi.isInWatchlist(userId, stock.ts_code);
        setIsInWatchlist(status);
      } catch (error) {
        console.error('检查关注状态失败:', error);
      }
    };

    if (userId) {
      checkWatchlistStatus();
    }
  }, [stock.ts_code, userId]);

  const handleToggleWatchlist = async () => {
    setLoading(true);
    try {
      if (isInWatchlist) {
        await watchlistApi.removeFromWatchlist(userId, stock.ts_code);
        setIsInWatchlist(false);
      } else {
        await watchlistApi.addToWatchlist(userId, stock.ts_code);
        setIsInWatchlist(true);
      }
    } catch (error) {
      console.error('操作失败:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card
      style={{ marginBottom: 16 }}
      bodyStyle={{ padding: 16 }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <div>
          <div style={{ marginBottom: 8 }}>
            <Tag color="blue">{stock.ts_code}</Tag>
            <span style={{ fontWeight: 'bold', marginLeft: 8 }}>{stock.name}</span>
          </div>

          <div style={{ display: 'flex', gap: 16 }}>
            <Statistic
              title="最新价"
              value={formatCurrency(stock.price)}
              valueStyle={{ fontSize: 16 }}
            />
            <Statistic
              title="涨跌幅"
              value={formatPercent(stock.change_percent)}
              valueStyle={{
                fontSize: 16,
                color: stock.change_percent > 0 ? '#cf1322' : '#389e0d'
              }}
            />
          </div>
        </div>

        <div>
          <Button
            type="text"
            icon={isInWatchlist ?
              <StarFilled style={{ color: '#faad14' }} /> :
              <StarOutlined />
            }
            loading={loading}
            onClick={handleToggleWatchlist}
          >
            {isInWatchlist ? '已关注' : '关注'}
          </Button>
        </div>
      </div>
    </Card>
  );
};

export default StockItem;