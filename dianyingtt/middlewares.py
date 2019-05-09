import scrapy
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random

class MyUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent
        
        
# 随机代理器
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from collections import defaultdict
import json
import random

class RandomHttpProxyMiddleware(HttpProxyMiddleware):

    def __init__(self, auth_encoding='latin-1', proxy_list_file=None):
        if not proxy_list_file:
            raise NotConfigured

        self.auth_encoding = auth_encoding
        # 分别用两个列表维护HTTP和HTTPS的代理，{'http': [...], 'https': [...]}
        self.proxies = defaultdict(list)

        # 从json文件中读取代理服务器信息，填入self.proxies
        with open(proxy_list_file) as f:
            proxy_list = json.load(f)
            for proxy in proxy_list:
                scheme = proxy['proxy_scheme']
                url = proxy['proxy']
        self.proxies[scheme].append(self._get_proxy(url, scheme))

    @classmethod
    def from_crawler(cls, crawler):
        # 从配置文件中读取用户验证信息的编码
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'latain-1')
        # 从配置文件中读取代理服务器列表文件（json）的路径
        proxy_list_file = crawler.settings.get('HTTPPROXY_PROXY_LIST_FILE')
        return cls(auth_encoding, proxy_list_file)

    def _set_proxy(self, request, scheme):
        # 随机选择一个代理
        creds, proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
        if creds:
            request.headers['Proxy-Authorization'] = b'Basic ' + creds
            

            
            
            
            
