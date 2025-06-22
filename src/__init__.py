#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI文章撰写工具 - 核心模块包

这个包包含了AI文章撰写工具的所有核心功能模块。

主要模块:
- news_analyzer: 新闻分析和获取
- article_writer: 文章撰写和生成
- article_quality: 文章质量评估
- article_templates: 文章模板管理
- database: 数据库管理
- web_interface: Web界面
- config: 配置管理
- news_sources: 新闻源配置

使用示例:
    from src.news_analyzer import NewsAnalyzer
    from src.article_writer import ArticleWriter
    from src.web_interface import create_app
"""

# 导入版本信息
from .__version__ import (
    __version__,
    __title__,
    __description__,
    __author__,
    __license__,
    get_version,
    get_full_version
)

# 导入主要类和函数
from .news_analyzer import NewsAnalyzer
from .article_writer import ArticleWriter
from .web_interface import create_app
from .config import get_config

# 定义公开的API
__all__ = [
    # 版本信息
    '__version__',
    '__title__',
    '__description__',
    '__author__',
    '__license__',
    'get_version',
    'get_full_version',

    # 主要类
    'NewsAnalyzer',
    'ArticleWriter',

    # 主要函数
    'create_app',
    'get_config',
]

# 模块级别的便捷函数
def create_news_analyzer():
    """创建新闻分析器实例"""
    return NewsAnalyzer()

def create_article_writer():
    """创建文章撰写器实例"""
    return ArticleWriter()

def create_web_app():
    """创建Web应用实例"""
    return create_app()

# 添加便捷函数到公开API
__all__.extend([
    'create_news_analyzer',
    'create_article_writer',
    'create_web_app'
])
