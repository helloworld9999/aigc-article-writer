#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能测试脚本
测试系统在不同负载下的性能表现
"""

import time
import statistics
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def test_news_fetching_performance():
    """测试新闻获取性能"""
    print("=== 新闻获取性能测试 ===")
    
    try:
        from src.news_analyzer import NewsAnalyzer
        analyzer = NewsAnalyzer()
        
        # 测试单次获取
        start_time = time.time()
        news_list = analyzer.get_trending_news(limit=10)
        end_time = time.time()
        
        fetch_time = end_time - start_time
        news_count = len(news_list)
        
        print(f"✅ 单次获取: {news_count} 条新闻，耗时 {fetch_time:.2f} 秒")
        print(f"   平均每条新闻: {fetch_time/max(news_count, 1):.3f} 秒")
        
        # 性能评估
        if fetch_time < 30:
            print("✅ 新闻获取性能良好")
        elif fetch_time < 60:
            print("⚠️  新闻获取性能一般")
        else:
            print("❌ 新闻获取性能较差")
        
        return fetch_time, news_count
        
    except Exception as e:
        print(f"❌ 新闻获取性能测试失败: {e}")
        return None, 0

def test_article_generation_performance():
    """测试文章生成性能"""
    print("\n=== 文章生成性能测试 ===")
    
    try:
        from src.article_writer import ArticleWriter
        writer = ArticleWriter()
        
        # 测试数据
        test_news = {
            'id': 88888,
            'title': '性能测试：新技术推动产业升级',
            'content': '最新技术的应用正在推动传统产业的转型升级，为经济发展注入新动力。专家表示，这一趋势将持续推进。',
            'summary': '新技术推动产业升级',
            'source': '性能测试源',
            'link': 'http://test.com/performance',
            'publish_time': datetime.now()
        }
        
        # 测试不同类型文章的生成时间
        article_types = ['breaking_news', 'analysis', 'feature']
        generation_times = []
        
        for article_type in article_types:
            start_time = time.time()
            result = writer.write_article(test_news, article_type=article_type)
            end_time = time.time()
            
            generation_time = end_time - start_time
            generation_times.append(generation_time)
            
            if isinstance(result, dict):
                article_content = result.get('article', result.get('content', ''))
            else:
                article_content = result
            
            word_count = len(article_content)
            
            print(f"✅ {article_type}: {word_count} 字符，耗时 {generation_time:.2f} 秒")
        
        avg_time = statistics.mean(generation_times)
        print(f"\n平均生成时间: {avg_time:.2f} 秒")
        
        # 性能评估
        if avg_time < 10:
            print("✅ 文章生成性能优秀")
        elif avg_time < 30:
            print("✅ 文章生成性能良好")
        elif avg_time < 60:
            print("⚠️  文章生成性能一般")
        else:
            print("❌ 文章生成性能较差")
        
        return avg_time
        
    except Exception as e:
        print(f"❌ 文章生成性能测试失败: {e}")
        return None

def test_database_performance():
    """测试数据库性能"""
    print("\n=== 数据库性能测试 ===")
    
    try:
        from src.database import get_database_manager
        db_manager = get_database_manager()
        
        if not db_manager.available:
            print("⚠️  数据库不可用，跳过性能测试")
            return None
        
        # 测试批量插入
        test_articles = []
        for i in range(10):
            test_articles.append({
                'title': f'性能测试文章 {i+1}',
                'content': f'这是第 {i+1} 篇性能测试文章的内容。' * 50,
                'summary': f'测试摘要 {i+1}',
                'article_type': 'breaking_news',
                'writing_style': 'professional',
                'quality_score': 0.8,
                'quality_grade': 'B+'
            })
        
        # 批量插入测试
        start_time = time.time()
        article_ids = []
        for article_data in test_articles:
            article_id = db_manager.save_article(article_data)
            if article_id:
                article_ids.append(article_id)
        end_time = time.time()
        
        insert_time = end_time - start_time
        print(f"✅ 批量插入 {len(article_ids)} 条记录，耗时 {insert_time:.3f} 秒")
        print(f"   平均每条记录: {insert_time/len(article_ids):.4f} 秒")
        
        # 批量查询测试
        start_time = time.time()
        articles = db_manager.get_articles(limit=50)
        end_time = time.time()
        
        query_time = end_time - start_time
        print(f"✅ 查询 {len(articles)} 条记录，耗时 {query_time:.3f} 秒")
        
        # 统计查询测试
        start_time = time.time()
        stats = db_manager.get_statistics()
        end_time = time.time()
        
        stats_time = end_time - start_time
        print(f"✅ 统计查询耗时 {stats_time:.3f} 秒")
        
        # 清理测试数据
        for article_id in article_ids:
            db_manager.delete_article(article_id)
        
        # 性能评估
        total_time = insert_time + query_time + stats_time
        if total_time < 1:
            print("✅ 数据库性能优秀")
        elif total_time < 3:
            print("✅ 数据库性能良好")
        else:
            print("⚠️  数据库性能一般")
        
        return total_time
        
    except Exception as e:
        print(f"❌ 数据库性能测试失败: {e}")
        return None

def test_concurrent_performance():
    """测试并发性能"""
    print("\n=== 并发性能测试 ===")
    
    try:
        from src.article_writer import ArticleWriter
        
        def generate_article(thread_id):
            """单个线程的文章生成任务"""
            writer = ArticleWriter()
            test_news = {
                'id': 77777 + thread_id,
                'title': f'并发测试文章 {thread_id}',
                'content': f'这是第 {thread_id} 个并发测试的文章内容。',
                'summary': f'并发测试摘要 {thread_id}',
                'source': '并发测试源',
                'link': f'http://test.com/concurrent/{thread_id}',
                'publish_time': datetime.now()
            }
            
            start_time = time.time()
            result = writer.write_article(test_news)
            end_time = time.time()
            
            return {
                'thread_id': thread_id,
                'time': end_time - start_time,
                'success': result is not None
            }
        
        # 测试不同并发数
        concurrent_levels = [2, 4]
        
        for num_threads in concurrent_levels:
            print(f"\n测试 {num_threads} 个并发线程:")
            
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(generate_article, i) for i in range(num_threads)]
                results = []
                
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        print(f"   线程执行失败: {e}")
            
            end_time = time.time()
            total_time = end_time - start_time
            
            successful_threads = sum(1 for r in results if r['success'])
            avg_thread_time = statistics.mean([r['time'] for r in results if r['success']])
            
            print(f"   总耗时: {total_time:.2f} 秒")
            print(f"   成功线程: {successful_threads}/{num_threads}")
            print(f"   平均单线程时间: {avg_thread_time:.2f} 秒")
            print(f"   并发效率: {(avg_thread_time * num_threads / total_time):.2f}")
        
        print("✅ 并发性能测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 并发性能测试失败: {e}")
        return False

def test_memory_usage():
    """测试内存使用情况"""
    print("\n=== 内存使用测试 ===")
    
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # 初始内存
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        print(f"初始内存使用: {initial_memory:.1f} MB")
        
        # 执行一些操作
        from src.news_analyzer import NewsAnalyzer
        from src.article_writer import ArticleWriter
        
        analyzer = NewsAnalyzer()
        writer = ArticleWriter()
        
        # 生成多篇文章
        for i in range(5):
            test_news = {
                'id': 66666 + i,
                'title': f'内存测试文章 {i+1}',
                'content': f'这是第 {i+1} 篇内存测试文章的内容。' * 100,
                'summary': f'内存测试摘要 {i+1}',
                'source': '内存测试源',
                'link': f'http://test.com/memory/{i}',
                'publish_time': datetime.now()
            }
            
            writer.write_article(test_news)
        
        # 最终内存
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"最终内存使用: {final_memory:.1f} MB")
        print(f"内存增长: {memory_increase:.1f} MB")
        
        # 内存评估
        if memory_increase < 50:
            print("✅ 内存使用良好")
        elif memory_increase < 100:
            print("⚠️  内存使用一般")
        else:
            print("❌ 内存使用较高")
        
        return memory_increase
        
    except ImportError:
        print("⚠️  psutil未安装，跳过内存测试")
        return None
    except Exception as e:
        print(f"❌ 内存测试失败: {e}")
        return None

def run_performance_tests():
    """运行所有性能测试"""
    print("=== AI文章撰写工具性能测试 ===\n")
    
    results = {}
    
    # 新闻获取性能
    fetch_time, news_count = test_news_fetching_performance()
    results['news_fetching'] = {'time': fetch_time, 'count': news_count}
    
    # 文章生成性能
    generation_time = test_article_generation_performance()
    results['article_generation'] = {'time': generation_time}
    
    # 数据库性能
    db_time = test_database_performance()
    results['database'] = {'time': db_time}
    
    # 并发性能
    concurrent_success = test_concurrent_performance()
    results['concurrent'] = {'success': concurrent_success}
    
    # 内存使用
    memory_increase = test_memory_usage()
    results['memory'] = {'increase': memory_increase}
    
    # 性能总结
    print("\n=== 性能测试总结 ===")
    
    if fetch_time and fetch_time < 30:
        print("✅ 新闻获取性能良好")
    
    if generation_time and generation_time < 30:
        print("✅ 文章生成性能良好")
    
    if db_time and db_time < 3:
        print("✅ 数据库性能良好")
    
    if concurrent_success:
        print("✅ 并发处理正常")
    
    if memory_increase is None or memory_increase < 50:
        print("✅ 内存使用合理")
    
    print("\n🎉 性能测试完成！")
    return results

if __name__ == "__main__":
    results = run_performance_tests()
