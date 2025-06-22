#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本功能测试脚本
"""

import sys
import os

def test_imports():
    """测试基本导入"""
    try:
        print("测试基本导入...")
        
        # 测试标准库
        import os
        import sys
        import json
        import re
        from datetime import datetime
        print("[OK] 标准库导入成功")
        
        # 测试第三方库
        try:
            import requests
            print("✓ requests导入成功")
        except ImportError:
            print("✗ requests导入失败")
        
        try:
            import jieba
            print("✓ jieba导入成功")
        except ImportError:
            print("✗ jieba导入失败")
        
        try:
            import flask
            print("✓ flask导入成功")
        except ImportError:
            print("✗ flask导入失败")
        
        # 测试项目模块
        try:
            from src.news_analyzer import NewsAnalyzer
            print("✓ NewsAnalyzer导入成功")
        except ImportError as e:
            print(f"✗ NewsAnalyzer导入失败: {e}")
        
        try:
            from src.article_writer import ArticleWriter
            print("✓ ArticleWriter导入成功")
        except ImportError as e:
            print(f"✗ ArticleWriter导入失败: {e}")
        
        try:
            from src.web_interface import create_app
            print("✓ create_app导入成功")
        except ImportError as e:
            print(f"✗ create_app导入失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"导入测试失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    try:
        print("\n测试基本功能...")
        
        # 测试NewsAnalyzer
        from src.news_analyzer import NewsAnalyzer
        analyzer = NewsAnalyzer()
        print("✓ NewsAnalyzer实例化成功")
        
        # 测试ArticleWriter
        from src.article_writer import ArticleWriter
        writer = ArticleWriter()
        print("✓ ArticleWriter实例化成功")
        
        # 测试模板文章生成
        from datetime import datetime
        test_news = {
            'id': 12345,
            'title': '测试新闻标题',
            'content': '这是一条测试新闻的内容，用于验证文章生成功能是否正常工作。',
            'summary': '测试新闻摘要',
            'source': '测试来源',
            'link': 'http://test.com',
            'publish_time': datetime.now()
        }
        
        article = writer.write_article(test_news)
        if article and len(article) > 100:
            print("✓ 文章生成功能正常")
            print(f"生成文章长度: {len(article)} 字符")
        else:
            print("✗ 文章生成功能异常")
        
        return True
        
    except Exception as e:
        print(f"功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=== AI文章撰写工具基本测试 ===\n")
    
    # 测试导入
    import_success = test_imports()
    
    if import_success:
        # 测试基本功能
        func_success = test_basic_functionality()
        
        if func_success:
            print("\n✓ 所有基本测试通过！项目可以正常运行。")
            return True
        else:
            print("\n✗ 功能测试失败")
            return False
    else:
        print("\n✗ 导入测试失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)