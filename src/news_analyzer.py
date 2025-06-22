#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻分析器模块
负责获取和分析实时热点新闻
"""

import requests
import feedparser
import jieba
from collections import Counter
from datetime import datetime, timedelta
from newspaper import Article
import json
import time

class NewsAnalyzer:
    """新闻分析器类"""
    
    def __init__(self):
        """初始化新闻分析器"""
        from .news_sources import get_news_sources
        self.news_sources = self._convert_sources_format(get_news_sources())
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        # 配置参数
        self.timeout = 8  # 减少超时时间
        self.max_retries = 1  # 减少重试次数
        self.max_sources = 4  # 限制同时处理的源数量

    def _convert_sources_format(self, sources):
        """转换新闻源格式以兼容现有代码"""
        converted = []
        for source in sources:
            if source['type'] == 'rss':
                converted.append({
                    'name': source['name'],
                    'rss_url': source['url'],
                    'type': 'rss'
                })
            elif source['type'] == 'api':
                converted.append({
                    'name': source['name'],
                    'api_url': source['url'],
                    'type': 'api'
                })
        return converted

    def get_trending_news(self, limit=20):
        """获取热点新闻"""
        all_news = []
        processed_sources = 0

        # 只处理前几个源以提高速度
        for source in self.news_sources[:self.max_sources]:
            try:
                if source['type'] == 'rss':
                    news_items = self._parse_rss_feed(source['rss_url'], source['name'])
                elif source['type'] == 'api':
                    news_items = self._parse_api_feed(source['api_url'], source['name'])

                all_news.extend(news_items)
                processed_sources += 1

                # 如果已经获得足够的新闻，提前退出
                if len(all_news) >= limit * 2:
                    break

                time.sleep(0.5)  # 减少等待时间

            except Exception as e:
                print(f"获取 {source['name']} 新闻失败: {e}")
                continue

        # 按时间排序并去重
        unique_news = self._deduplicate_news(all_news)
        trending_news = sorted(unique_news, key=lambda x: x['publish_time'], reverse=True)

        return trending_news[:limit]

    def _extract_content(self, url, fallback_content):
        """提取文章内容"""
        try:
            # 方法1: 使用newspaper3k
            from newspaper import Article
            article = Article(url, language='zh')
            article.download()
            article.parse()

            if article.text and len(article.text) > 100:
                return article.text
        except Exception as e:
            print(f"Newspaper3k提取失败: {e}")

        try:
            # 方法2: 直接请求页面并解析
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # 尝试多种内容选择器
            content_selectors = [
                '.article-content',
                '.content',
                '.post-content',
                '.entry-content',
                'article',
                '.main-content',
                '#content',
                '.news-content'
            ]

            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    text = content_elem.get_text(strip=True)
                    if len(text) > 100:
                        return text

            # 如果没有找到特定选择器，尝试提取所有段落
            paragraphs = soup.find_all('p')
            if paragraphs:
                text = ' '.join([p.get_text(strip=True) for p in paragraphs])
                if len(text) > 100:
                    return text

        except Exception as e:
            print(f"直接解析失败: {e}")

        # 如果所有方法都失败，返回摘要
        return fallback_content if fallback_content else "无法获取文章内容"

    def _parse_rss_feed(self, rss_url, source_name):
        """解析RSS源"""
        try:
            # 设置feedparser的User-Agent和超时
            import feedparser
            feedparser.USER_AGENT = self.headers['User-Agent']

            # 解析RSS（设置超时）
            import socket
            socket.setdefaulttimeout(self.timeout)
            feed = feedparser.parse(rss_url)

            if not feed.entries:
                print(f"RSS源 {source_name} 没有返回任何条目")
                return []

            news_items = []

            for entry in feed.entries[:20]:  # 限制处理数量
                try:
                    # 处理发布时间
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        publish_time = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        publish_time = datetime(*entry.updated_parsed[:6])
                    else:
                        publish_time = datetime.now()

                    news_item = {
                        'id': abs(hash(entry.title + entry.link)),
                        'title': entry.title.strip(),
                        'link': entry.link,
                        'summary': getattr(entry, 'summary', '').strip(),
                        'publish_time': publish_time,
                        'source': source_name,
                        'content': ''
                    }

                    # 暂时不获取完整内容以提高速度，使用摘要作为内容
                    news_item['content'] = news_item['summary'] or news_item['title']

                    news_items.append(news_item)

                except Exception as e:
                    print(f"处理RSS条目失败: {e}")
                    continue

            return news_items

        except Exception as e:
            print(f"解析RSS源 {source_name} 失败: {e}")
            return []
    
    def _parse_api_feed(self, api_url, source_name):
        """解析API源（示例实现）"""
        # 这里是示例实现，实际需要根据具体API调整
        try:
            response = requests.get(api_url, headers=self.headers, timeout=10)
            # 根据实际API格式解析数据
            return []
        except Exception as e:
            print(f"解析API源失败: {e}")
            return []
    
    def _deduplicate_news(self, news_list):
        """新闻去重"""
        seen_titles = set()
        unique_news = []
        
        for news in news_list:
            # 简单的标题相似度去重
            title_words = set(jieba.cut(news['title']))
            is_duplicate = False
            
            for seen_title in seen_titles:
                seen_words = set(jieba.cut(seen_title))
                similarity = len(title_words & seen_words) / len(title_words | seen_words)
                if similarity > 0.7:  # 相似度阈值
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_titles.add(news['title'])
                unique_news.append(news)
        
        return unique_news
    
    def analyze_trending_topics(self, news_list):
        """分析热点话题"""
        all_words = []
        
        for news in news_list:
            # 分词并过滤停用词
            words = jieba.cut(news['title'] + ' ' + news['summary'])
            filtered_words = [word for word in words if len(word) > 1 and word.isalnum()]
            all_words.extend(filtered_words)
        
        # 统计词频
        word_freq = Counter(all_words)
        trending_topics = word_freq.most_common(10)
        
        return trending_topics
    
    def get_news_sentiment(self, news_content):
        """分析新闻情感倾向（简单实现）"""
        positive_words = ['好', '优秀', '成功', '增长', '提升', '改善', '突破']
        negative_words = ['坏', '失败', '下降', '问题', '危机', '困难', '风险']
        
        words = jieba.cut(news_content)
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
