import requests
import json
from typing import Dict, List, Optional, Any
from app import db
from app.utils.code import reformat_stock_code


class XueqiuService:
    """雪球API服务类"""
    
    def __init__(self, token: str = None, cookies: str = None):
        """
        初始化雪球服务
        :param token: 雪球API token
        :param cookies: 雪球cookies字符串
        """
        self.token = token
        self.cookies = cookies
        self.base_url = "https://xueqiu.com"
        self.api_url = "https://stock.xueqiu.com"
        self.session = requests.Session()
        
        # 设置基础headers
        self.session.headers.update({
            'Host': 'stock.xueqiu.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-platform': '"macOS"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'Referer': 'https://xueqiu.com/',
            'Origin': 'https://xueqiu.com',
            'priority': 'u=1, i'
        })
        
        # 设置cookies
        if cookies:
            self.session.headers.update({'Cookie': cookies})
        
        # 设置token
        if token:
            self.session.headers.update({'Authorization': f'Bearer {token}'})

    def _make_request(self, method: str, url: str, params: Dict = None, data: Dict = None, headers: Dict = None) -> Dict:
        """
        发送HTTP请求
        :param method: HTTP方法
        :param url: 请求URL
        :param params: 查询参数
        :param data: 请求数据
        :param headers: 请求头
        :return: 响应数据
        """
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, headers=headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=headers)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON解析失败: {str(e)}")

    def get_portfolio_groups(self, user_id: str = None) -> List[Dict]:
        """
        获取用户的个股分组列表
        :param user_id: 用户ID (可选)
        :return: 分组列表
        """
        url = f"{self.api_url}/v5/stock/portfolio/list.json"
        params = {
            'system': 'true'
        }
        if user_id:
            params['user_id'] = user_id
        return self._make_request('GET', url, params=params)

    def get_group_stocks(self, group_id: str) -> List[Dict]:
        """
        获取分组的股票列表
        :param group_id: 分组ID
        :return: 股票列表
        """
        url = f"{self.api_url}/v5/stock/portfolio/stock/list.json"
        params = {
            'category': 1,
            'size': 1000,
            'pid': group_id
        }
        return self._make_request('GET', url, params=params)

    def create_portfolio_group(self, name: str, description: str = None) -> Dict:
        """
        创建新的分组
        :param name: 分组名称
        :param description: 分组描述
        :return: 创建的分组信息
        """
        url = f"{self.api_url}/v5/stock/portfolio/create.json"
        data = {
            'name': name,
            'description': description or '',
            'type': 'stock'
        }
        return self._make_request('POST', url, data=data)

    def add_stock_to_group(self, group_id: str, stock_code: str, stock_name: str = None) -> Dict:
        """
        向分组添加股票
        :param group_id: 分组ID
        :param stock_code: 股票代码
        :param stock_name: 股票名称
        :return: 添加结果
        """
        url = f"{self.api_url}/v5/stock/portfolio/stock/modify_portfolio.json"
        symbols = reformat_stock_code(stock_code)
        data = {
            'pid': group_id,
            'symbols': [symbols],
            'pname': stock_name or stock_code
        }
        return self._make_request('POST', url, data=data)

    def remove_stock_from_group(self, group_id: str, stock_code: str) -> Dict:
        """
        从分组移除股票
        :param group_id: 分组ID
        :param stock_code: 股票代码
        :return: 移除结果
        """
        url = f"{self.api_url}/v5/stock/portfolio/stock/remove.json"
        data = {
            'portfolio_id': group_id,
            'symbol': stock_code
        }
        return self._make_request('POST', url, data=data)

    def update_portfolio_group(self, group_id: str, name: str = None, description: str = None) -> Dict:
        """
        更新分组信息
        :param group_id: 分组ID
        :param name: 新分组名称
        :param description: 新分组描述
        :return: 更新结果
        """
        url = f"{self.api_url}/v5/stock/portfolio/update.json"
        data = {
            'portfolio_id': group_id
        }
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        return self._make_request('PUT', url, data=data)

    def delete_portfolio_group(self, group_id: str) -> Dict:
        """
        删除分组
        :param group_id: 分组ID
        :return: 删除结果
        """
        url = f"{self.api_url}/v5/stock/portfolio/delete.json"
        data = {
            'portfolio_id': group_id
        }
        return self._make_request('DELETE', url, data=data)

    def get_stock_info(self, stock_code: str) -> Dict:
        """
        获取股票基本信息
        :param stock_code: 股票代码
        :return: 股票信息
        """
        url = f"{self.api_url}/v5/stock/quote.json"
        params = {
            'symbol': stock_code
        }
        return self._make_request('GET', url, params=params)

    def search_stocks(self, keyword: str) -> List[Dict]:
        """
        搜索股票
        :param keyword: 搜索关键词
        :return: 搜索结果
        """
        url = f"{self.api_url}/v5/stock/search.json"
        params = {
            'keyword': keyword
        }
        return self._make_request('GET', url, params=params)

    def get_user_info(self) -> Dict:
        """
        获取用户信息
        :return: 用户信息
        """
        url = f"{self.api_url}/v5/user/info.json"
        return self._make_request('GET', url)

    def login(self, username: str, password: str) -> Dict:
        """
        登录雪球账户
        :param username: 用户名
        :param password: 密码
        :return: 登录结果
        """
        url = f"{self.base_url}/service/v5/stock/biz/quote/stock_list.json"
        data = {
            'username': username,
            'password': password
        }
        return self._make_request('POST', url, data=data)

# 创建全局服务实例
xueqiu_service = XueqiuService(cookies="cookiesu=651752239221949; device_id=7432a8f9d9d0f488d146e8b9f6296450; s=9y117i04f0; xq_is_login=1; u=2272289326; Hm_lvt_1db88642e346389874251b5a1eded6e3=1752239221,1753378013; HMACCOUNT=567AC6520E06DE03; xq_a_token=90dddd05cc02e7e8091cc5b3afb9813636a550ed; xqat=90dddd05cc02e7e8091cc5b3afb9813636a550ed; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjIyNzIyODkzMjYsImlzcyI6InVjIiwiZXhwIjoxNzU2MTMyMTQ0LCJjdG0iOjE3NTM1NDAxNDQ1NTUsImNpZCI6ImQ5ZDBuNEFadXAifQ.OTQtxZdUgkKpAV0NV8_oY73_bb6MiobhmhltHvnQyJxJ77djCSCFHI3cyLMmfNo-AclhA36x2jOrnYauiawKliV-wBjA0rQYbB-ci_6Rz2On60YoT1AJ6j5xpYms13oBYizdiTxDG5M7q8i0XCwk3DlP_0aAjJxkogfVH8W7RJc6258Ok-RfpOguOYpZvT_KbRQi9DC2TVJxt2jRGqY0w7msZaWmhLvA2bga5kYf3CzttvLRUHf7eDw1x13izKMpZgtRVA1wnwF_fFuIDdwAwnCyJ21n7uQkdv9rPZJvFVZQF7zErxuwyClwKf_fozUGepOaaWt-UbYJcihr6UNvMw; xq_r_token=1a61b3acc5af6e7a63d2d1fa6ef6c6da99ab4b42; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1753792794; is_overseas=0; ssxmod_itna=eqmxnD0DyQAxuD4kDRrxQwbxBixwEADBP01DpxYK0CDmxjKideDUlQX23tADWuw4p5NjD0I5keOi5D/K0TeDZDGKQDqx0or0Qjxht+3i0ugGIeDti5P4Y8+Akuc6y7GRb4lF4L4MBZkD5s6OhHNxiTrBxDoxGkDivoD0IYeo4Dx1PD5xDTDWeDGDD3=4OmD0Rv7RoAK8+wregvDYpoQR+oDYHUDAuvm3OAR4i3s4iaDGeDeZOIBKxD0oPDEgh3s8e4AFQwfljozYZPbk4ds4Gagf+nDlKw4XWILXtDvPEo/RA5uYSXr3jY5Bt32deDogODN7D1YxNGY3gQ3nYeGY+r=/DQjh4Siezo=zxDixittbqQG3PNSONlENrGmZjm9eT73+2jDejGKj21BqGYetGD4lD8fx5fDliGrbD3YD; ssxmod_itna2=eqmxnD0DyQAxuD4kDRrxQwbxBixwEADBP01DpxYK0CDmxjKideDUlQX23tADWuw4p5NjD0I5keOieDAnrDhU=eDjRGfNx0yqLMI8GAYA+4TKSD1Z/PCBKeezWtt4xD") 