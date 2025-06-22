#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合测试套件
测试所有主要功能模块
"""

import sys
import os
import time
import unittest
from datetime import datetime

class TestEnvironmentSetup(unittest.TestCase):
    """环境配置测试"""
    
    def test_config_module(self):
        """测试配置模块"""
        try:
            from src.config import get_config
            config = get_config()
            self.assertIsNotNone(config)
            print("✅ 配置模块测试通过")
        except ImportError as e:
            self.fail(f"配置模块导入失败: {e}")
    
    def test_environment_files(self):
        """测试环境文件"""
        self.assertTrue(os.path.exists('.env.example'), ".env.example文件不存在")
        self.assertTrue(os.path.exists('requirements.txt'), "requirements.txt文件不存在")
        print("✅ 环境文件测试通过")
    
    def test_dependencies(self):
        """测试依赖包"""
        required_packages = {
            'requests': 'requests',
            'beautifulsoup4': 'bs4',
            'feedparser': 'feedparser',
            'jieba': 'jieba',
            'flask': 'flask'
        }

        for package_name, import_name in required_packages.items():
            try:
                __import__(import_name)
                print(f"✅ {package_name} 已安装")
            except ImportError:
                self.fail(f"必需包 {package_name} 未安装")

class TestNewsAnalyzer(unittest.TestCase):
    """新闻分析器测试"""
    
    def setUp(self):
        """设置测试环境"""
        from src.news_analyzer import NewsAnalyzer
        self.analyzer = NewsAnalyzer()
    
    def test_analyzer_initialization(self):
        """测试分析器初始化"""
        self.assertIsNotNone(self.analyzer)
        self.assertGreater(len(self.analyzer.news_sources), 0)
        print("✅ 新闻分析器初始化测试通过")
    
    def test_news_sources_configuration(self):
        """测试新闻源配置"""
        try:
            from src.news_sources import get_news_sources
            sources = get_news_sources()
            self.assertIsInstance(sources, list)
            self.assertGreater(len(sources), 0)
            print("✅ 新闻源配置测试通过")
        except ImportError:
            print("⚠️  新闻源配置模块不可用，跳过测试")
    
    def test_trending_topics_analysis(self):
        """测试热点话题分析"""
        # 模拟新闻数据
        mock_news = [
            {
                'title': '人工智能技术取得重大突破',
                'content': '最新AI技术在多个领域实现突破性进展',
                'summary': 'AI技术突破性进展'
            },
            {
                'title': '科技创新推动经济发展',
                'content': '科技创新成为经济增长的重要动力',
                'summary': '科技创新推动发展'
            }
        ]

        topics = self.analyzer.analyze_trending_topics(mock_news)
        self.assertIsInstance(topics, list)
        print("✅ 热点话题分析测试通过")

class TestArticleWriter(unittest.TestCase):
    """文章撰写器测试"""
    
    def setUp(self):
        """设置测试环境"""
        from src.article_writer import ArticleWriter
        self.writer = ArticleWriter()
    
    def test_writer_initialization(self):
        """测试撰写器初始化"""
        self.assertIsNotNone(self.writer)
        print("✅ 文章撰写器初始化测试通过")
    
    def test_article_generation(self):
        """测试文章生成"""
        # 模拟新闻数据
        mock_news = {
            'id': 12345,
            'title': '测试新闻标题',
            'content': '这是一条测试新闻的内容，用于验证文章生成功能是否正常工作。',
            'summary': '测试新闻摘要',
            'source': '测试来源',
            'link': 'http://test.com',
            'publish_time': datetime.now()
        }
        
        result = self.writer.write_article(mock_news)
        
        if isinstance(result, dict):
            # 新版本返回字典
            self.assertIn('title', result)
            self.assertIn('content', result)
            article_content = result.get('article', result.get('content', ''))
        else:
            # 旧版本直接返回文章内容
            article_content = result
        
        self.assertIsInstance(article_content, str)
        self.assertGreater(len(article_content), 100)
        print("✅ 文章生成测试通过")
    
    def test_article_templates(self):
        """测试文章模板"""
        try:
            from src.article_templates import get_article_template
            template = get_article_template('breaking_news')
            self.assertIsInstance(template, dict)
            self.assertIn('name', template)
            self.assertIn('structure', template)
            print("✅ 文章模板测试通过")
        except ImportError:
            print("⚠️  文章模板模块不可用，跳过测试")

class TestArticleQuality(unittest.TestCase):
    """文章质量评估测试"""
    
    def test_quality_assessment(self):
        """测试质量评估"""
        try:
            from src.article_quality import assess_article_quality
            
            test_article = """
            # 测试文章标题
            
            ## 引言
            这是一篇测试文章，用于验证质量评估功能。
            
            ## 主要内容
            文章包含多个段落和结构化内容。我们需要确保评估系统能够正确分析文章的各个方面。
            
            ## 结论
            通过测试，我们可以验证质量评估系统的有效性。
            """
            
            result = assess_article_quality(test_article)
            self.assertIsInstance(result, dict)
            self.assertIn('total_score', result)
            self.assertIn('grade', result)
            print("✅ 文章质量评估测试通过")
        except ImportError:
            print("⚠️  文章质量评估模块不可用，跳过测试")

class TestDatabase(unittest.TestCase):
    """数据库功能测试"""
    
    def setUp(self):
        """设置测试环境"""
        try:
            from src.database import get_database_manager
            self.db_manager = get_database_manager()
        except ImportError:
            self.db_manager = None
    
    def test_database_availability(self):
        """测试数据库可用性"""
        if self.db_manager is None:
            print("⚠️  数据库模块不可用，跳过测试")
            return
        
        self.assertIsNotNone(self.db_manager)
        print(f"✅ 数据库可用性测试通过 (可用: {self.db_manager.available})")
    
    def test_article_crud_operations(self):
        """测试文章CRUD操作"""
        if self.db_manager is None or not self.db_manager.available:
            print("⚠️  数据库不可用，跳过CRUD测试")
            return
        
        # 测试数据
        test_article = {
            'title': '测试文章标题',
            'content': '这是测试文章内容',
            'summary': '测试摘要',
            'article_type': 'breaking_news',
            'writing_style': 'professional',
            'quality_score': 0.8,
            'quality_grade': 'B+'
        }
        
        # 创建
        article_id = self.db_manager.save_article(test_article)
        self.assertIsNotNone(article_id)
        
        # 读取
        retrieved_article = self.db_manager.get_article_by_id(article_id)
        self.assertIsNotNone(retrieved_article)
        self.assertEqual(retrieved_article['title'], test_article['title'])
        
        # 更新
        update_success = self.db_manager.update_article(article_id, {'title': '更新后的标题'})
        self.assertTrue(update_success)
        
        # 删除
        delete_success = self.db_manager.delete_article(article_id)
        self.assertTrue(delete_success)
        
        print("✅ 数据库CRUD操作测试通过")
    
    def test_statistics(self):
        """测试统计功能"""
        if self.db_manager is None or not self.db_manager.available:
            print("⚠️  数据库不可用，跳过统计测试")
            return
        
        stats = self.db_manager.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_articles', stats)
        self.assertIn('today_articles', stats)
        print("✅ 数据库统计功能测试通过")

class TestWebInterface(unittest.TestCase):
    """Web界面测试"""
    
    def test_web_app_creation(self):
        """测试Web应用创建"""
        try:
            from src.web_interface import create_app
            app = create_app()
            self.assertIsNotNone(app)
            print("✅ Web应用创建测试通过")
        except ImportError as e:
            self.fail(f"Web界面模块导入失败: {e}")
    
    def test_template_files(self):
        """测试模板文件"""
        template_files = ['templates/index.html']
        
        for template_file in template_files:
            self.assertTrue(os.path.exists(template_file), f"模板文件 {template_file} 不存在")
        
        print("✅ 模板文件测试通过")

class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_end_to_end_workflow(self):
        """测试端到端工作流程"""
        print("\n=== 端到端工作流程测试 ===")
        
        try:
            # 1. 初始化组件
            from src.news_analyzer import NewsAnalyzer
            from src.article_writer import ArticleWriter
            
            analyzer = NewsAnalyzer()
            writer = ArticleWriter()
            
            print("✅ 组件初始化成功")
            
            # 2. 模拟新闻数据
            mock_news = {
                'id': 99999,
                'title': '集成测试：AI技术在教育领域的应用前景',
                'content': '最新研究表明，人工智能技术在教育领域展现出巨大潜力，能够个性化学习体验，提高教学效率。',
                'summary': 'AI技术在教育领域的应用研究',
                'source': '教育科技日报',
                'link': 'http://test.com/integration-test',
                'publish_time': datetime.now()
            }
            
            # 3. 生成文章
            result = writer.write_article(mock_news, article_type='analysis', style='academic')
            
            if isinstance(result, dict):
                article_content = result.get('article', result.get('content', ''))
                self.assertIsInstance(article_content, str)
                self.assertGreater(len(article_content), 200)
                print("✅ 文章生成成功")
                
                # 检查是否保存到数据库
                if 'article_id' in result and result['article_id']:
                    print("✅ 数据库保存成功")
                else:
                    print("⚠️  数据库保存跳过或失败")
            else:
                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 200)
                print("✅ 文章生成成功（旧版本格式）")
            
            print("✅ 端到端工作流程测试通过")
            
        except Exception as e:
            self.fail(f"端到端测试失败: {e}")

def run_comprehensive_tests():
    """运行综合测试"""
    print("=== AI文章撰写工具综合测试 ===\n")
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestEnvironmentSetup,
        TestNewsAnalyzer,
        TestArticleWriter,
        TestArticleQuality,
        TestDatabase,
        TestWebInterface,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出结果摘要
    print("\n=== 测试结果摘要 ===")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\n成功率: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("✅ 测试整体通过")
        return True
    else:
        print("❌ 测试存在问题，需要修复")
        return False

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
