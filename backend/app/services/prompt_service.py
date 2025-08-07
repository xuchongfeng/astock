import logging
from typing import Dict, List, Optional
from datetime import datetime, date

logger = logging.getLogger(__name__)

class PromptService:
    """提示词服务类"""
    
    def __init__(self):
        """初始化提示词服务"""
        self.prompt_templates = {
            'stock_basic_info': self._get_stock_basic_info_prompt,
            'stock_daily_analysis': self._get_stock_daily_analysis_prompt,
            'stock_trend_analysis': self._get_stock_trend_analysis_prompt,
            'market_overview': self._get_market_overview_prompt,
            'industry_analysis': self._get_industry_analysis_prompt
        }
    
    def get_prompt(self, prompt_type: str, **kwargs) -> str:
        """
        获取指定类型的提示词
        :param prompt_type: 提示词类型
        :param kwargs: 提示词参数
        :return: 格式化的提示词
        """
        if prompt_type not in self.prompt_templates:
            raise ValueError(f"不支持的提示词类型: {prompt_type}")
        
        return self.prompt_templates[prompt_type](**kwargs)
    
    def _get_stock_basic_info_prompt(self, stock_name: str, stock_code: str, 
                                    latest_data: Dict = None) -> str:
        """
        获取个股基本信息提示词
        :param stock_name: 股票名称
        :param stock_code: 股票代码
        :param latest_data: 最新数据
        :return: 提示词
        """
        prompt = f"""你是一位专业的股票分析师。请分析股票 {stock_name}({stock_code}) 的基本信息。

请从以下方面进行分析：
1. 公司基本信息：主营业务、行业地位、核心竞争力
2. 财务指标分析：PE、PB、ROE、营收增长、净利润增长
3. 技术面分析：当前价格、成交量、技术指标
4. 基本面分析：行业前景、公司发展前景
5. 投资建议：风险提示、投资价值评估

请提供详细、客观的分析，并给出投资建议。"""
        
        if latest_data:
            prompt += f"\n\n最新数据参考：{latest_data}"
        
        return prompt
    
    def _get_stock_daily_analysis_prompt(self, stock_name: str, stock_code: str,
                                        daily_data: Dict = None, 
                                        analysis_date: date = None) -> str:
        """
        获取个股每日走势分析提示词
        :param stock_name: 股票名称
        :param stock_code: 股票代码
        :param daily_data: 当日数据
        :param analysis_date: 分析日期
        :return: 提示词
        """
        date_str = analysis_date.strftime('%Y-%m-%d') if analysis_date else "今日"
        
        prompt = f"""你是一位专业的股票分析师。请分析股票 {stock_name}({stock_code}) 在 {date_str} 的走势。

请从以下方面进行分析：
1. 价格走势：开盘价、收盘价、最高价、最低价、涨跌幅
2. 成交量分析：成交量变化、换手率、资金流向
3. 技术指标：K线形态、均线系统、MACD、KDJ等指标
4. 盘面特征：主力资金动向、大单交易情况
5. 市场情绪：投资者情绪、市场关注度
6. 短期预测：明日走势预测、支撑阻力位
7. 操作建议：买入、持有、卖出的建议

请提供详细的技术分析，并给出具体的操作建议。"""
        
        if daily_data:
            prompt += f"\n\n当日数据：{daily_data}"
        
        return prompt
    
    def _get_stock_trend_analysis_prompt(self, stock_name: str, stock_code: str,
                                        trend_data: Dict = None, 
                                        period: str = "近期") -> str:
        """
        获取个股趋势分析提示词
        :param stock_name: 股票名称
        :param stock_code: 股票代码
        :param trend_data: 趋势数据
        :param period: 分析周期
        :return: 提示词
        """
        prompt = f"""你是一位专业的股票分析师。请分析股票 {stock_name}({stock_code}) 的{period}趋势。

请从以下方面进行分析：
1. 趋势判断：上涨、下跌、震荡趋势的识别
2. 技术形态：头肩顶、双底、三角形等形态分析
3. 支撑阻力：重要支撑位、阻力位的识别
4. 量价关系：成交量与价格的关系分析
5. 资金流向：主力资金进出情况
6. 基本面变化：公司基本面变化对股价的影响
7. 行业对比：与同行业股票的对比分析
8. 中长期预测：未来1-3个月的趋势预测
9. 投资策略：中长期投资建议

请提供深入的趋势分析，并给出中长期投资建议。"""
        
        if trend_data:
            prompt += f"\n\n趋势数据：{trend_data}"
        
        return prompt
    
    def _get_market_overview_prompt(self, market_data: Dict = None,
                                   analysis_date: date = None) -> str:
        """
        获取大盘分析提示词
        :param market_data: 市场数据
        :param analysis_date: 分析日期
        :return: 提示词
        """
        date_str = analysis_date.strftime('%Y-%m-%d') if analysis_date else "今日"
        
        prompt = f"""你是一位专业的市场分析师。请分析{date_str}的A股市场整体情况。

请从以下方面进行分析：
1. 大盘指数：上证指数、深证成指、创业板指的表现
2. 市场情绪：投资者情绪、市场信心指数
3. 板块轮动：热点板块、领涨领跌板块分析
4. 资金流向：北向资金、主力资金流向
5. 成交量：市场整体成交量变化
6. 技术面：大盘技术指标、趋势判断
7. 政策面：政策影响、监管动态
8. 外围市场：美股、港股等外围市场影响
9. 市场预测：短期市场走势预测
10. 投资建议：当前市场环境下的投资策略

请提供全面的市场分析，并给出投资建议。"""
        
        if market_data:
            prompt += f"\n\n市场数据：{market_data}"
        
        return prompt
    
    def _get_industry_analysis_prompt(self, industry_name: str,
                                    industry_data: Dict = None,
                                    analysis_date: date = None) -> str:
        """
        获取行业分析提示词
        :param industry_name: 行业名称
        :param industry_data: 行业数据
        :param analysis_date: 分析日期
        :return: 提示词
        """
        date_str = analysis_date.strftime('%Y-%m-%d') if analysis_date else "当前"
        
        prompt = f"""你是一位专业的行业分析师。请分析{industry_name}行业在{date_str}的发展情况。

请从以下方面进行分析：
1. 行业概况：行业规模、发展阶段、竞争格局
2. 政策环境：相关政策、监管要求、政策影响
3. 市场需求：下游需求、消费趋势、市场空间
4. 技术发展：技术创新、技术壁垒、技术趋势
5. 产业链分析：上游、中游、下游产业链情况
6. 重点公司：行业龙头、重点公司分析
7. 投资机会：行业投资机会、风险提示
8. 发展趋势：行业未来发展趋势预测
9. 投资建议：行业投资策略建议

请提供深入的行业分析，并给出投资建议。"""
        
        if industry_data:
            prompt += f"\n\n行业数据：{industry_data}"
        
        return prompt
    
    def get_stock_analysis_prompt(self, analysis_type: str, stock_name: str, 
                                 stock_code: str, **kwargs) -> str:
        """
        获取股票分析提示词的统一接口
        :param analysis_type: 分析类型 (basic_info/daily_analysis/trend_analysis)
        :param stock_name: 股票名称
        :param stock_code: 股票代码
        :param kwargs: 其他参数
        :return: 提示词
        """
        if analysis_type == 'basic_info':
            return self._get_stock_basic_info_prompt(stock_name, stock_code, kwargs.get('latest_data'))
        elif analysis_type == 'daily_analysis':
            return self._get_stock_daily_analysis_prompt(stock_name, stock_code, 
                                                       kwargs.get('daily_data'), 
                                                       kwargs.get('analysis_date'))
        elif analysis_type == 'trend_analysis':
            return self._get_stock_trend_analysis_prompt(stock_name, stock_code,
                                                       kwargs.get('trend_data'),
                                                       kwargs.get('period', '近期'))
        else:
            raise ValueError(f"不支持的分析类型: {analysis_type}")
    
    def get_market_analysis_prompt(self, analysis_type: str, **kwargs) -> str:
        """
        获取市场分析提示词的统一接口
        :param analysis_type: 分析类型 (market_overview/industry_analysis)
        :param kwargs: 其他参数
        :return: 提示词
        """
        if analysis_type == 'market_overview':
            return self._get_market_overview_prompt(kwargs.get('market_data'),
                                                  kwargs.get('analysis_date'))
        elif analysis_type == 'industry_analysis':
            return self._get_industry_analysis_prompt(kwargs.get('industry_name'),
                                                    kwargs.get('industry_data'),
                                                    kwargs.get('analysis_date'))
        else:
            raise ValueError(f"不支持的分析类型: {analysis_type}")

# 创建全局服务实例
prompt_service = PromptService() 