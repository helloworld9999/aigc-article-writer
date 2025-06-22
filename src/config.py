#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
负责加载和管理应用配置
"""

import os
from typing import Optional, List
from pathlib import Path

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

class Config:
    """应用配置类"""
    
    def __init__(self):
        """初始化配置"""
        # 加载环境变量
        if DOTENV_AVAILABLE:
            env_file = Path('.env')
            if env_file.exists():
                load_dotenv(env_file)
        
        # AI模型配置
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
        self.OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.8'))
        
        # 其他AI模型
        self.CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
        self.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        
        # Flask配置
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
        self.FLASK_ENV = os.getenv('FLASK_ENV', 'development')
        self.FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
        
        # 数据库配置
        self.DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///articles.db')
        self.DATABASE_ECHO = os.getenv('DATABASE_ECHO', 'False').lower() == 'true'
        
        # 新闻源配置
        self.NEWS_API_KEY = os.getenv('NEWS_API_KEY')
        self.TENCENT_NEWS_API_KEY = os.getenv('TENCENT_NEWS_API_KEY')
        self.NEWS_FETCH_TIMEOUT = int(os.getenv('NEWS_FETCH_TIMEOUT', '10'))
        self.NEWS_FETCH_RETRY = int(os.getenv('NEWS_FETCH_RETRY', '3'))
        self.NEWS_CACHE_DURATION = int(os.getenv('NEWS_CACHE_DURATION', '1800'))
        self.MAX_NEWS_PER_SOURCE = int(os.getenv('MAX_NEWS_PER_SOURCE', '20'))
        self.NEWS_MAX_AGE_DAYS = int(os.getenv('NEWS_MAX_AGE_DAYS', '3'))
        
        # 文章配置
        self.ARTICLES_DIR = os.getenv('ARTICLES_DIR', 'articles')
        self.MAX_ARTICLES_PER_USER = int(os.getenv('MAX_ARTICLES_PER_USER', '100'))
        self.MAX_ARTICLES_PER_DAY = int(os.getenv('MAX_ARTICLES_PER_DAY', '50'))
        self.ARTICLE_MIN_LENGTH = int(os.getenv('ARTICLE_MIN_LENGTH', '500'))
        self.ARTICLE_MAX_LENGTH = int(os.getenv('ARTICLE_MAX_LENGTH', '2000'))
        self.AI_FALLBACK_ENABLED = os.getenv('AI_FALLBACK_ENABLED', 'True').lower() == 'true'
        
        # Web服务配置
        self.WEB_HOST = os.getenv('WEB_HOST', '0.0.0.0')
        self.WEB_PORT = int(os.getenv('WEB_PORT', '5000'))
        self.WEB_THREADS = int(os.getenv('WEB_THREADS', '4'))
        
        # 缓存配置
        self.CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
        self.CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))
        
        # 日志配置
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
        self.LOG_MAX_SIZE = int(os.getenv('LOG_MAX_SIZE', '10485760'))
        self.LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', '5'))
        
        # 安全配置
        self.ALLOWED_HOSTS = self._parse_list(os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1'))
        self.CORS_ORIGINS = self._parse_list(os.getenv('CORS_ORIGINS', 'http://localhost:3000'))
        
        # 性能配置
        self.REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
        self.MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', '16777216'))
        
        # 确保必要的目录存在
        self._ensure_directories()
    
    def _parse_list(self, value: str) -> List[str]:
        """解析逗号分隔的字符串为列表"""
        if not value:
            return []
        return [item.strip() for item in value.split(',') if item.strip()]
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        directories = [
            self.ARTICLES_DIR,
            os.path.dirname(self.LOG_FILE) if self.LOG_FILE else 'logs'
        ]
        
        for directory in directories:
            if directory:
                Path(directory).mkdir(parents=True, exist_ok=True)
    
    def is_ai_enabled(self) -> bool:
        """检查是否启用了AI功能"""
        return bool(self.OPENAI_API_KEY or self.CLAUDE_API_KEY or self.GEMINI_API_KEY)
    
    def get_available_ai_models(self) -> List[str]:
        """获取可用的AI模型列表"""
        models = []
        if self.OPENAI_API_KEY:
            models.append('openai')
        if self.CLAUDE_API_KEY:
            models.append('claude')
        if self.GEMINI_API_KEY:
            models.append('gemini')
        return models
    
    def validate_config(self) -> List[str]:
        """验证配置并返回警告信息"""
        warnings = []
        
        # 检查关键配置
        if not self.is_ai_enabled() and not self.AI_FALLBACK_ENABLED:
            warnings.append("未配置AI API密钥且未启用备用模式，文章生成功能可能受限")
        
        if self.SECRET_KEY == 'dev-secret-key-change-in-production':
            warnings.append("使用默认密钥，生产环境中请更改SECRET_KEY")
        
        if not self.NEWS_API_KEY:
            warnings.append("未配置新闻API密钥，可能影响新闻获取功能")
        
        return warnings

# 全局配置实例
config = Config()

def get_config() -> Config:
    """获取配置实例"""
    return config

def reload_config():
    """重新加载配置"""
    global config
    config = Config()
    return config
