#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库模型和管理模块
"""

import os
from datetime import datetime
from typing import List, Dict, Optional

try:
    from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, Session
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False

if SQLALCHEMY_AVAILABLE:
    Base = declarative_base()
    
    class Article(Base):
        """文章模型"""
        __tablename__ = 'articles'
        
        id = Column(Integer, primary_key=True)
        title = Column(String(500), nullable=False)
        content = Column(Text, nullable=False)
        summary = Column(Text)
        article_type = Column(String(50), nullable=False)
        writing_style = Column(String(50), nullable=False)
        source_news_id = Column(String(100))
        source_news_title = Column(String(500))
        source_news_url = Column(String(1000))
        quality_score = Column(Float)
        quality_grade = Column(String(10))
        word_count = Column(Integer)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        is_deleted = Column(Boolean, default=False)
    
    class NewsSource(Base):
        """新闻源模型"""
        __tablename__ = 'news_sources'
        
        id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
        url = Column(String(1000), nullable=False)
        source_type = Column(String(20), nullable=False)  # rss, api
        is_active = Column(Boolean, default=True)
        priority = Column(Integer, default=3)
        last_fetch_time = Column(DateTime)
        fetch_count = Column(Integer, default=0)
        error_count = Column(Integer, default=0)
        created_at = Column(DateTime, default=datetime.utcnow)
    
    class WritingSession(Base):
        """写作会话模型"""
        __tablename__ = 'writing_sessions'
        
        id = Column(Integer, primary_key=True)
        session_id = Column(String(100), nullable=False)
        start_time = Column(DateTime, default=datetime.utcnow)
        end_time = Column(DateTime)
        articles_generated = Column(Integer, default=0)
        total_words = Column(Integer, default=0)
        avg_quality_score = Column(Float)
        user_agent = Column(String(500))
        ip_address = Column(String(50))
    
    class SystemStats(Base):
        """系统统计模型"""
        __tablename__ = 'system_stats'
        
        id = Column(Integer, primary_key=True)
        stat_date = Column(DateTime, nullable=False)
        total_articles = Column(Integer, default=0)
        articles_today = Column(Integer, default=0)
        avg_quality_score = Column(Float, default=0.0)
        total_words = Column(Integer, default=0)
        active_news_sources = Column(Integer, default=0)
        created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, database_url: str = None):
        """初始化数据库管理器"""
        self.database_url = database_url or os.getenv('DATABASE_URL', 'sqlite:///articles.db')
        self.engine = None
        self.SessionLocal = None
        self.available = SQLALCHEMY_AVAILABLE
        
        if self.available:
            self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        try:
            self.engine = create_engine(self.database_url, echo=False)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # 创建表
            Base.metadata.create_all(bind=self.engine)
            print("✅ 数据库初始化成功")
            
        except Exception as e:
            print(f"❌ 数据库初始化失败: {e}")
            self.available = False
    
    def get_session(self) -> Optional[Session]:
        """获取数据库会话"""
        if not self.available:
            return None
        
        try:
            return self.SessionLocal()
        except Exception as e:
            print(f"获取数据库会话失败: {e}")
            return None
    
    def save_article(self, article_data: Dict) -> Optional[int]:
        """保存文章到数据库"""
        if not self.available:
            return None
        
        session = self.get_session()
        if not session:
            return None
        
        try:
            article = Article(
                title=article_data.get('title', ''),
                content=article_data.get('content', ''),
                summary=article_data.get('summary', ''),
                article_type=article_data.get('article_type', 'breaking_news'),
                writing_style=article_data.get('writing_style', 'professional'),
                source_news_id=str(article_data.get('source_news_id', '')),
                source_news_title=article_data.get('source_news_title', ''),
                source_news_url=article_data.get('source_news_url', ''),
                quality_score=article_data.get('quality_score', 0.0),
                quality_grade=article_data.get('quality_grade', 'C'),
                word_count=len(article_data.get('content', ''))
            )
            
            session.add(article)
            session.commit()
            article_id = article.id
            session.close()
            
            return article_id
            
        except Exception as e:
            print(f"保存文章失败: {e}")
            session.rollback()
            session.close()
            return None
    
    def get_articles(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """获取文章列表"""
        if not self.available:
            return []
        
        session = self.get_session()
        if not session:
            return []
        
        try:
            articles = session.query(Article)\
                .filter(Article.is_deleted == False)\
                .order_by(Article.created_at.desc())\
                .limit(limit)\
                .offset(offset)\
                .all()
            
            result = []
            for article in articles:
                result.append({
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'summary': article.summary,
                    'article_type': article.article_type,
                    'writing_style': article.writing_style,
                    'quality_score': article.quality_score,
                    'quality_grade': article.quality_grade,
                    'word_count': article.word_count,
                    'created_at': article.created_at.isoformat(),
                    'updated_at': article.updated_at.isoformat()
                })
            
            session.close()
            return result
            
        except Exception as e:
            print(f"获取文章列表失败: {e}")
            session.close()
            return []
    
    def get_article_by_id(self, article_id: int) -> Optional[Dict]:
        """根据ID获取文章"""
        if not self.available:
            return None
        
        session = self.get_session()
        if not session:
            return None
        
        try:
            article = session.query(Article)\
                .filter(Article.id == article_id, Article.is_deleted == False)\
                .first()
            
            if not article:
                session.close()
                return None
            
            result = {
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'summary': article.summary,
                'article_type': article.article_type,
                'writing_style': article.writing_style,
                'quality_score': article.quality_score,
                'quality_grade': article.quality_grade,
                'word_count': article.word_count,
                'created_at': article.created_at.isoformat(),
                'updated_at': article.updated_at.isoformat()
            }
            
            session.close()
            return result
            
        except Exception as e:
            print(f"获取文章失败: {e}")
            session.close()
            return None
    
    def update_article(self, article_id: int, update_data: Dict) -> bool:
        """更新文章"""
        if not self.available:
            return False
        
        session = self.get_session()
        if not session:
            return False
        
        try:
            article = session.query(Article)\
                .filter(Article.id == article_id, Article.is_deleted == False)\
                .first()
            
            if not article:
                session.close()
                return False
            
            # 更新字段
            for key, value in update_data.items():
                if hasattr(article, key):
                    setattr(article, key, value)
            
            # 更新字数
            if 'content' in update_data:
                article.word_count = len(update_data['content'])
            
            article.updated_at = datetime.utcnow()
            
            session.commit()
            session.close()
            return True
            
        except Exception as e:
            print(f"更新文章失败: {e}")
            session.rollback()
            session.close()
            return False
    
    def delete_article(self, article_id: int) -> bool:
        """删除文章（软删除）"""
        if not self.available:
            return False
        
        session = self.get_session()
        if not session:
            return False
        
        try:
            article = session.query(Article)\
                .filter(Article.id == article_id, Article.is_deleted == False)\
                .first()
            
            if not article:
                session.close()
                return False
            
            article.is_deleted = True
            article.updated_at = datetime.utcnow()
            
            session.commit()
            session.close()
            return True
            
        except Exception as e:
            print(f"删除文章失败: {e}")
            session.rollback()
            session.close()
            return False
    
    def get_statistics(self) -> Dict:
        """获取统计数据"""
        if not self.available:
            return {
                'total_articles': 0,
                'today_articles': 0,
                'avg_quality_score': 0.0,
                'total_words': 0
            }
        
        session = self.get_session()
        if not session:
            return {}
        
        try:
            today = datetime.now().date()
            
            # 总文章数
            total_articles = session.query(Article)\
                .filter(Article.is_deleted == False)\
                .count()
            
            # 今日文章数
            today_articles = session.query(Article)\
                .filter(Article.is_deleted == False)\
                .filter(Article.created_at >= today)\
                .count()
            
            # 平均质量分数
            avg_quality = session.query(Article.quality_score)\
                .filter(Article.is_deleted == False)\
                .filter(Article.quality_score.isnot(None))\
                .all()
            
            avg_quality_score = 0.0
            if avg_quality:
                avg_quality_score = sum(score[0] for score in avg_quality) / len(avg_quality)
            
            # 总字数
            total_words = session.query(Article.word_count)\
                .filter(Article.is_deleted == False)\
                .all()
            
            total_word_count = sum(count[0] for count in total_words if count[0])
            
            session.close()
            
            return {
                'total_articles': total_articles,
                'today_articles': today_articles,
                'avg_quality_score': round(avg_quality_score, 2),
                'total_words': total_word_count
            }
            
        except Exception as e:
            print(f"获取统计数据失败: {e}")
            session.close()
            return {}

# 全局数据库管理器实例
db_manager = DatabaseManager()

def get_database_manager() -> DatabaseManager:
    """获取数据库管理器实例"""
    return db_manager
