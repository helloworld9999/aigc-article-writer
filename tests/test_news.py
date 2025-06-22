#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新闻获取功能
"""

from src.news_analyzer import NewsAnalyzer
from src.article_writer import ArticleWriter
from datetime import datetime

def test_news_analyzer():
    """测试新闻分析器"""
    print("测试新闻分析器...")
    
    try:
        analyzer = NewsAnalyzer()
        print("新闻分析器创建成功")
        
        # 测试热点话题分析
        test_news_list = [
            {
                'title': '人工智能技术取得重大突破',
                'summary': '最新的AI技术在多个领域实现突破性进展',
                'content': '人工智能技术在自然语言处理、计算机视觉等领域取得重大突破，为未来发展奠定基础。'
            },
            {
                'title': '新能源汽车销量创新高',
                'summary': '电动汽车市场持续增长',
                'content': '新能源汽车在全球市场表现强劲，销量创历史新高，推动绿色出行发展。'
            }
        ]
        
        topics = analyzer.analyze_trending_topics(test_news_list)
        print(f"热点话题分析结果: {topics}")
        
        return True
        
    except Exception as e:
        print(f"新闻分析器测试失败: {e}")
        return False

def test_article_writer():
    """测试文章撰写器"""
    print("测试文章撰写器...")
    
    try:
        writer = ArticleWriter()
        print("文章撰写器创建成功")
        
        # 创建测试新闻
        test_news = {
            'id': 12345,
            'title': '人工智能助力医疗诊断准确率提升',
            'content': '最新研究显示，基于深度学习的AI系统在医疗影像诊断中表现出色，准确率达到95%以上，为医疗行业带来革命性变化。该系统能够快速识别多种疾病特征，大大提高了诊断效率。',
            'summary': 'AI技术在医疗诊断领域取得重大突破，准确率超过95%',
            'source': '科技日报',
            'link': 'http://example.com/news/12345',
            'publish_time': datetime.now()
        }
        
        # 测试文章生成
        article = writer.write_article(test_news, 'breaking_news', 'professional')
        
        if article and len(article) > 200:
            print("文章生成成功!")
            print(f"文章长度: {len(article)} 字符")
            print("文章预览:")
            print("-" * 50)
            print(article[:300] + "...")
            print("-" * 50)
            
            # 保存测试文章
            import os
            os.makedirs("articles", exist_ok=True)
            with open("articles/test_article.md", "w", encoding="utf-8") as f:
                f.write(article)
            print("测试文章已保存到: articles/test_article.md")
            
            return True
        else:
            print("文章生成失败或内容过短")
            return False
            
    except Exception as e:
        print(f"文章撰写器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=== AI文章撰写工具功能测试 ===\n")
    
    # 测试新闻分析器
    analyzer_ok = test_news_analyzer()
    print()
    
    # 测试文章撰写器
    writer_ok = test_article_writer()
    print()
    
    if analyzer_ok and writer_ok:
        print("✓ 所有功能测试通过！")
        print("\n项目已准备就绪，可以开始使用：")
        print("1. 运行 'python main.py' 选择模式")
        print("2. 或直接运行 'python start_web.py' 启动Web界面")
    else:
        print("✗ 部分功能测试失败")

if __name__ == "__main__":
    main()