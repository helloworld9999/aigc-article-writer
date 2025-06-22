#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻源配置和管理模块
"""

class NewsSourceManager:
    """新闻源管理器"""
    
    def __init__(self):
        """初始化新闻源"""
        self.sources = {
            'rss_sources': [
                {
                    'name': '新浪新闻-要闻',
                    'url': 'https://rss.sina.com.cn/news/china/focus15.xml',
                    'encoding': 'utf-8',
                    'priority': 1,
                    'active': True
                },
                {
                    'name': '人民网-时政',
                    'url': 'http://www.people.com.cn/rss/politics.xml',
                    'encoding': 'utf-8',
                    'priority': 1,
                    'active': True
                },
                {
                    'name': '新华网-时政',
                    'url': 'http://www.xinhuanet.com/politics/news_politics.xml',
                    'encoding': 'utf-8',
                    'priority': 1,
                    'active': True
                },
                {
                    'name': '中国新闻网',
                    'url': 'https://www.chinanews.com.cn/rss/scroll-news.xml',
                    'encoding': 'utf-8',
                    'priority': 2,
                    'active': True
                },
                {
                    'name': '光明网',
                    'url': 'http://www.gmw.cn/rss/news.xml',
                    'encoding': 'utf-8',
                    'priority': 2,
                    'active': True
                },
                {
                    'name': '中青在线',
                    'url': 'http://news.cyol.com/rss/news.xml',
                    'encoding': 'utf-8',
                    'priority': 2,
                    'active': True
                },
                {
                    'name': '环球网',
                    'url': 'https://china.huanqiu.com/rss/china.xml',
                    'encoding': 'utf-8',
                    'priority': 3,
                    'active': True
                },
                {
                    'name': '澎湃新闻',
                    'url': 'https://www.thepaper.cn/rss/news.xml',
                    'encoding': 'utf-8',
                    'priority': 3,
                    'active': True
                }
            ],
            'api_sources': [
                {
                    'name': '今日头条',
                    'url': 'https://www.toutiao.com/api/pc/feed/',
                    'method': 'GET',
                    'params': {
                        'category': 'news_hot',
                        'utm_source': 'toutiao',
                        'widen': 1,
                        'max_behot_time': 0,
                        'max_behot_time_tmp': 0,
                        'tadrequire': True,
                        'as': 'A1A5BD6C5F5B8D6',
                        'cp': '5E5F6F7E8F9FA0B'
                    },
                    'headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Referer': 'https://www.toutiao.com/'
                    },
                    'priority': 2,
                    'active': False  # 需要特殊处理，暂时禁用
                }
            ]
        }
    
    def get_active_rss_sources(self):
        """获取活跃的RSS源"""
        return [source for source in self.sources['rss_sources'] if source['active']]
    
    def get_active_api_sources(self):
        """获取活跃的API源"""
        return [source for source in self.sources['api_sources'] if source['active']]
    
    def get_sources_by_priority(self, priority=None):
        """按优先级获取新闻源"""
        all_sources = []
        
        # RSS源
        for source in self.get_active_rss_sources():
            if priority is None or source['priority'] == priority:
                all_sources.append({
                    'name': source['name'],
                    'url': source['url'],
                    'type': 'rss',
                    'priority': source['priority'],
                    'encoding': source.get('encoding', 'utf-8')
                })
        
        # API源
        for source in self.get_active_api_sources():
            if priority is None or source['priority'] == priority:
                all_sources.append({
                    'name': source['name'],
                    'url': source['url'],
                    'type': 'api',
                    'priority': source['priority'],
                    'method': source.get('method', 'GET'),
                    'params': source.get('params', {}),
                    'headers': source.get('headers', {})
                })
        
        # 按优先级排序
        return sorted(all_sources, key=lambda x: x['priority'])
    
    def disable_source(self, source_name):
        """禁用新闻源"""
        for source in self.sources['rss_sources']:
            if source['name'] == source_name:
                source['active'] = False
                return True
        
        for source in self.sources['api_sources']:
            if source['name'] == source_name:
                source['active'] = False
                return True
        
        return False
    
    def enable_source(self, source_name):
        """启用新闻源"""
        for source in self.sources['rss_sources']:
            if source['name'] == source_name:
                source['active'] = True
                return True
        
        for source in self.sources['api_sources']:
            if source['name'] == source_name:
                source['active'] = True
                return True
        
        return False
    
    def add_rss_source(self, name, url, priority=3, encoding='utf-8'):
        """添加RSS源"""
        new_source = {
            'name': name,
            'url': url,
            'encoding': encoding,
            'priority': priority,
            'active': True
        }
        self.sources['rss_sources'].append(new_source)
        return True
    
    def get_source_stats(self):
        """获取新闻源统计信息"""
        stats = {
            'total_rss': len(self.sources['rss_sources']),
            'active_rss': len(self.get_active_rss_sources()),
            'total_api': len(self.sources['api_sources']),
            'active_api': len(self.get_active_api_sources()),
        }
        stats['total'] = stats['total_rss'] + stats['total_api']
        stats['active'] = stats['active_rss'] + stats['active_api']
        return stats

# 全局新闻源管理器实例
news_source_manager = NewsSourceManager()

def get_news_sources():
    """获取新闻源配置"""
    return news_source_manager.get_sources_by_priority()

def get_priority_sources(priority=1):
    """获取指定优先级的新闻源"""
    return news_source_manager.get_sources_by_priority(priority)
