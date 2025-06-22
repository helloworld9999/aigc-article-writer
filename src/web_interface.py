#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web界面模块
提供用户友好的Web界面
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from .news_analyzer import NewsAnalyzer
from .article_writer import ArticleWriter

def create_app():
    """创建Flask应用"""
    # 设置正确的模板和静态文件路径
    template_dir = os.path.abspath('templates')
    static_dir = os.path.abspath('static')

    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir if os.path.exists(static_dir) else None)
    app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # 初始化组件
    news_analyzer = NewsAnalyzer()
    article_writer = ArticleWriter()
    
    @app.route('/')
    def index():
        """主页"""
        return render_template('index.html')
    
    @app.route('/api/news')
    def get_news():
        """获取热点新闻API"""
        try:
            limit = request.args.get('limit', 20, type=int)
            news_list = news_analyzer.get_trending_news(limit)

            # 统计时间分布
            from datetime import datetime, timedelta
            time_stats = {'today': 0, 'yesterday': 0, 'older': 0}

            # 转换datetime为字符串并统计
            for news in news_list:
                publish_time = news['publish_time']
                time_diff = datetime.now() - publish_time

                if time_diff.days == 0:
                    time_stats['today'] += 1
                elif time_diff.days == 1:
                    time_stats['yesterday'] += 1
                else:
                    time_stats['older'] += 1

                news['publish_time'] = publish_time.isoformat()

            return jsonify({
                'success': True,
                'data': news_list,
                'count': len(news_list),
                'time_stats': time_stats,
                'max_age_days': news_analyzer.max_age_days
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/topics')
    def get_trending_topics():
        """获取热点话题API"""
        try:
            news_list = news_analyzer.get_trending_news(50)
            topics = news_analyzer.analyze_trending_topics(news_list)
            
            return jsonify({
                'success': True,
                'data': [{'word': word, 'count': count} for word, count in topics]
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/articles')
    def list_articles():
        """列出已生成的文章"""
        try:
            # 尝试从数据库获取
            try:
                from .database import get_database_manager
                db_manager = get_database_manager()

                if db_manager.available:
                    articles = db_manager.get_articles()
                    return jsonify({
                        'success': True,
                        'data': articles,
                        'source': 'database'
                    })
            except ImportError:
                pass

            # 如果数据库不可用，从文件系统获取
            articles_dir = "articles"
            if not os.path.exists(articles_dir):
                return jsonify({
                    'success': True,
                    'data': [],
                    'source': 'filesystem'
                })

            articles = []
            for filename in os.listdir(articles_dir):
                if filename.endswith('.md'):
                    filepath = os.path.join(articles_dir, filename)
                    stat = os.stat(filepath)

                    # 读取文章标题
                    with open(filepath, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        title = first_line.replace('# ', '') if first_line.startswith('# ') else filename

                    articles.append({
                        'filename': filename,
                        'title': title,
                        'size': stat.st_size,
                        'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })

            # 按修改时间排序
            articles.sort(key=lambda x: x['modified_time'], reverse=True)

            return jsonify({
                'success': True,
                'data': articles,
                'source': 'filesystem'
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/articles/<filename>')
    def get_article(filename):
        """获取文章内容"""
        try:
            filepath = os.path.join("articles", filename)
            if not os.path.exists(filepath):
                return jsonify({
                    'success': False,
                    'error': '文章不存在'
                }), 404
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return jsonify({
                'success': True,
                'data': {
                    'filename': filename,
                    'content': content
                }
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/download/<filename>')
    def download_article(filename):
        """下载文章"""
        try:
            filepath = os.path.join("articles", filename)
            if not os.path.exists(filepath):
                return "文件不存在", 404

            return send_file(filepath, as_attachment=True)

        except Exception as e:
            return f"下载失败: {e}", 500

    @app.route('/api/articles/<identifier>', methods=['DELETE'])
    def delete_article(identifier):
        """删除文章（支持文件名或数据库ID）"""
        try:
            # 尝试从数据库删除（如果identifier是数字，认为是ID）
            try:
                article_id = int(identifier)
                from .database import get_database_manager
                db_manager = get_database_manager()

                if db_manager.available:
                    success = db_manager.delete_article(article_id)
                    if success:
                        return jsonify({
                            'success': True,
                            'message': '文章已从数据库删除'
                        })
                    else:
                        return jsonify({
                            'success': False,
                            'error': '数据库中未找到该文章'
                        }), 404
            except (ValueError, ImportError):
                # 不是数字ID或数据库不可用，尝试文件删除
                pass

            # 尝试从文件系统删除
            filepath = os.path.join("articles", identifier)
            if not os.path.exists(filepath):
                return jsonify({
                    'success': False,
                    'error': '文章不存在'
                }), 404

            os.remove(filepath)

            return jsonify({
                'success': True,
                'message': '文章已从文件系统删除'
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/articles/<filename>', methods=['PUT'])
    def update_article(filename):
        """更新文章内容"""
        try:
            data = request.get_json()
            new_content = data.get('content')

            if not new_content:
                return jsonify({
                    'success': False,
                    'error': '内容不能为空'
                }), 400

            filepath = os.path.join("articles", filename)
            if not os.path.exists(filepath):
                return jsonify({
                    'success': False,
                    'error': '文章不存在'
                }), 404

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return jsonify({
                'success': True,
                'message': '文章已更新'
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/write_article', methods=['POST'])
    def write_article():
        """撰写文章API"""
        try:
            data = request.get_json()

            if not data:
                return jsonify({
                    'success': False,
                    'error': '请求数据为空'
                }), 400

            news_id = data.get('news_id')
            article_type = data.get('article_type', 'breaking_news')
            writing_style = data.get('style', data.get('writing_style', 'professional'))

            if not news_id:
                return jsonify({
                    'success': False,
                    'error': '缺少新闻ID'
                }), 400

            # 获取新闻数据
            news_list = news_analyzer.get_trending_news(100)  # 获取更多新闻
            selected_news = None

            for news in news_list:
                if str(news.get('id')) == str(news_id):
                    selected_news = news
                    break

            if not selected_news:
                return jsonify({
                    'success': False,
                    'error': f'未找到指定新闻 (ID: {news_id})'
                }), 404

            # 生成文章
            result = article_writer.write_article(
                selected_news,
                article_type=article_type,
                style=writing_style
            )

            if isinstance(result, dict):
                # 新版本返回字典
                return jsonify({
                    'success': True,
                    'data': {
                        'title': result.get('title', ''),
                        'content': result.get('content', ''),
                        'article': result.get('article', ''),
                        'filename': result.get('filename', ''),
                        'article_id': result.get('article_id'),
                        'quality': result.get('quality', {}),
                        'analysis': result.get('analysis', {})
                    }
                })
            else:
                # 旧版本直接返回文章内容
                return jsonify({
                    'success': True,
                    'data': {
                        'title': selected_news.get('title', ''),
                        'content': result,
                        'article': result,
                        'filename': None,
                        'article_id': None
                    }
                })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'文章生成失败: {str(e)}'
            }), 500

    @app.route('/api/analytics/stats')
    def get_analytics_stats():
        """获取分析统计数据"""
        try:
            articles_dir = "articles"
            if not os.path.exists(articles_dir):
                return jsonify({
                    'success': True,
                    'data': {
                        'total_articles': 0,
                        'today_articles': 0,
                        'avg_quality': 0.0,
                        'article_types': {}
                    }
                })

            articles = []
            article_types = {}
            today = datetime.now().date()
            today_count = 0

            for filename in os.listdir(articles_dir):
                if filename.endswith('.md'):
                    filepath = os.path.join(articles_dir, filename)
                    stat = os.stat(filepath)
                    created_date = datetime.fromtimestamp(stat.st_ctime).date()

                    if created_date == today:
                        today_count += 1

                    # 从文件名推断文章类型
                    if 'breaking' in filename or 'urgent' in filename:
                        article_type = 'breaking_news'
                    elif 'analysis' in filename or 'deep' in filename:
                        article_type = 'analysis'
                    elif 'feature' in filename or 'special' in filename:
                        article_type = 'feature'
                    else:
                        article_type = 'other'

                    article_types[article_type] = article_types.get(article_type, 0) + 1
                    articles.append(filename)

            return jsonify({
                'success': True,
                'data': {
                    'total_articles': len(articles),
                    'today_articles': today_count,
                    'avg_quality': 8.5,  # 模拟数据
                    'article_types': article_types
                }
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/quality/assess', methods=['POST'])
    def assess_article_quality():
        """评估文章质量"""
        try:
            data = request.get_json()
            content = data.get('content')

            if not content:
                return jsonify({
                    'success': False,
                    'error': '内容不能为空'
                }), 400

            # 使用文章质量评估模块
            try:
                from .article_quality import assess_article_quality
                quality_result = assess_article_quality(content)
            except ImportError:
                # 如果模块不可用，返回模拟数据
                quality_result = {
                    'total_score': 0.75,
                    'scores': {
                        'length': 0.8,
                        'structure': 0.7,
                        'readability': 0.8,
                        'content_quality': 0.7,
                        'originality': 0.8
                    },
                    'grade': 'B+',
                    'suggestions': ['建议改进文章结构', '增加更多数据支撑']
                }

            return jsonify({
                'success': True,
                'data': quality_result
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    return app
