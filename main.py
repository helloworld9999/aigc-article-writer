#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI文章撰写工具主程序
功能：分析实时热点新闻，撰写高质量独家首发报道
"""

import os
import sys
# # from dotenv import load_dotenv
from src.news_analyzer import NewsAnalyzer
from src.article_writer import ArticleWriter
from src.web_interface import create_app

def main():
    """主程序入口"""
    # load_dotenv()
    
    print("=== AI文章撰写工具 ===")
    print("1. 启动Web界面")
    print("2. 命令行模式")
    
    choice = input("请选择模式 (1/2): ").strip()
    
    if choice == "1":
        # 启动Web界面
        app = create_app()
        app.run(host='0.0.0.0', port=5000, debug=True)
    elif choice == "2":
        # 命令行模式
        analyzer = NewsAnalyzer()
        writer = ArticleWriter()
        
        print("正在分析热点新闻...")
        hot_news = analyzer.get_trending_news()
        
        if hot_news:
            print(f"发现 {len(hot_news)} 条热点新闻")
            for i, news in enumerate(hot_news[:5], 1):
                print(f"{i}. {news['title']}")
            
            choice = input("请选择要撰写文章的新闻编号 (1-5): ").strip()
            try:
                selected_news = hot_news[int(choice) - 1]
                print(f"正在为新闻撰写文章: {selected_news['title']}")
                
                article = writer.write_article(selected_news)
                print("\n=== 生成的文章 ===")
                print(article)
                
                # 保存文章
                filename = f"articles/article_{selected_news['id']}.md"
                os.makedirs("articles", exist_ok=True)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(article)
                print(f"\n文章已保存到: {filename}")
                
            except (ValueError, IndexError):
                print("无效的选择")
        else:
            print("未找到热点新闻")
    else:
        print("无效的选择")

if __name__ == "__main__":
    main()
