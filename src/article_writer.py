#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章撰写器模块
负责基于新闻内容撰写高质量文章
"""

import os
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
from datetime import datetime
import json
import re

class ArticleWriter:
    """文章撰写器类"""
    
    def __init__(self):
        """初始化文章撰写器"""
        # 加载配置
        try:
            from .config import get_config
            self.config = get_config()
        except ImportError:
            # 如果配置模块不可用，使用环境变量
            self.config = None

        # 初始化AI客户端
        self.ai_clients = {}
        self._init_ai_clients()

        # 当前使用的AI模型
        self.current_ai_model = self._get_best_available_model()

        # 文章模板
        self.article_templates = {
            'breaking_news': {
                'title_format': '【独家】{topic}：{key_point}',
                'structure': ['导语', '事件详情', '背景分析', '影响评估', '专家观点', '结语']
            },
            'analysis': {
                'title_format': '深度解析：{topic}背后的{angle}',
                'structure': ['引言', '现状分析', '原因探讨', '趋势预测', '建议对策', '总结']
            },
            'feature': {
                'title_format': '{topic}全景：{subtitle}',
                'structure': ['开篇', '核心内容', '多角度分析', '案例展示', '未来展望', '结尾']
            }
        }

    def _init_ai_clients(self):
        """初始化AI客户端"""
        # OpenAI客户端
        openai_key = self.config.OPENAI_API_KEY if self.config else os.getenv('OPENAI_API_KEY')
        if openai_key and OPENAI_AVAILABLE:
            try:
                import openai
                self.ai_clients['openai'] = openai.OpenAI(api_key=openai_key)
                print("✅ OpenAI客户端初始化成功")
            except Exception as e:
                print(f"❌ OpenAI客户端初始化失败: {e}")

        # 可以在这里添加其他AI模型的初始化
        # 例如：Claude, Gemini等

    def _get_best_available_model(self):
        """获取最佳可用的AI模型"""
        if 'openai' in self.ai_clients:
            return 'openai'

        # 如果没有AI模型可用，使用模板模式
        return 'template'

    def _is_ai_available(self):
        """检查是否有可用的AI模型"""
        return len(self.ai_clients) > 0

    def write_article(self, news_data, article_type='breaking_news', style='professional'):
        """撰写文章"""
        try:
            # 分析新闻内容
            analysis = self._analyze_news_content(news_data)
            
            # 生成文章标题
            title = self._generate_title(news_data, analysis, article_type)
            
            # 生成文章内容
            content = self._generate_content(news_data, analysis, article_type, style)
            
            # 组装完整文章
            article = self._format_article(title, content, news_data)

            # 评估文章质量
            quality_result = self._assess_article_quality(article, news_data)

            # 如果质量不达标且有AI可用，尝试改进
            if quality_result['total_score'] < 0.7 and self._is_ai_available():
                print(f"文章质量评分: {quality_result['total_score']:.2f}，尝试改进...")
                improved_content = self._improve_article_content(content, quality_result['suggestions'])
                if improved_content:
                    article = self._format_article(title, improved_content, news_data)
                    # 重新评估改进后的文章质量
                    quality_result = self._assess_article_quality(article, news_data)

            # 保存文章到文件
            filename = self._save_article_to_file(article, news_data)

            # 保存到数据库
            article_id = self._save_to_database(article, news_data, analysis, quality_result, article_type, style)

            return {
                'title': title,
                'content': content,
                'article': article,
                'filename': filename,
                'article_id': article_id,
                'analysis': analysis,
                'quality': quality_result
            }
            
        except Exception as e:
            print(f"文章撰写失败: {e}")
            return self._generate_fallback_article(news_data)
    
    def _analyze_news_content(self, news_data):
        """分析新闻内容"""
        analysis = {
            'key_points': self._extract_key_points(news_data['content']),
            'entities': self._extract_entities(news_data['content']),
            'sentiment': self._analyze_sentiment(news_data['content']),
            'category': self._categorize_news(news_data['title']),
            'urgency': self._assess_urgency(news_data)
        }
        return analysis
    
    def _generate_title(self, news_data, analysis, article_type):
        """生成文章标题"""
        if self._is_ai_available():
            return self._generate_ai_title(news_data, analysis, article_type)
        else:
            return self._generate_template_title(news_data, analysis, article_type)
    
    def _generate_ai_title(self, news_data, analysis, article_type):
        """使用AI生成标题"""
        prompt = f"""
        基于以下新闻信息，生成一个吸引人的{article_type}类型文章标题：

        原标题：{news_data['title']}
        关键点：{', '.join(analysis['key_points'][:3])}
        类别：{analysis['category']}
        情感：{analysis['sentiment']}

        要求：
        1. 标题要有新闻价值和吸引力
        2. 体现独家或首发特色
        3. 长度控制在15-25字
        4. 避免夸大或误导
        5. 使用中文

        请只返回标题，不要其他内容。
        """

        try:
            if self.current_ai_model == 'openai' and 'openai' in self.ai_clients:
                model_name = self.config.OPENAI_MODEL if self.config else "gpt-3.5-turbo"
                max_tokens = self.config.OPENAI_MAX_TOKENS if self.config else 100
                temperature = self.config.OPENAI_TEMPERATURE if self.config else 0.7

                response = self.ai_clients['openai'].chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=min(max_tokens, 100),  # 标题不需要太多token
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()
            else:
                raise Exception("没有可用的AI模型")

        except Exception as e:
            print(f"AI标题生成失败: {e}")
            return self._generate_template_title(news_data, analysis, article_type)
    
    def _generate_template_title(self, news_data, analysis, article_type):
        """使用模板生成标题"""
        template = self.article_templates[article_type]['title_format']
        
        # 提取主题和关键点
        topic = analysis['entities'][0] if analysis['entities'] else '重要事件'
        key_point = analysis['key_points'][0] if analysis['key_points'] else '最新进展'
        
        return template.format(topic=topic, key_point=key_point, angle='深层原因')
    
    def _generate_content(self, news_data, analysis, article_type, style):
        """生成文章内容"""
        if self._is_ai_available():
            return self._generate_ai_content(news_data, analysis, article_type, style)
        else:
            return self._generate_template_content(news_data, analysis, article_type)
    
    def _generate_ai_content(self, news_data, analysis, article_type, style):
        """使用AI生成内容"""
        structure = self.article_templates[article_type]['structure']
        
        prompt = f"""
        基于以下新闻信息，撰写一篇{style}风格的{article_type}类型文章：
        
        原新闻：
        标题：{news_data['title']}
        内容：{news_data['content'][:1000]}
        来源：{news_data['source']}
        
        分析结果：
        关键点：{', '.join(analysis['key_points'])}
        实体：{', '.join(analysis['entities'])}
        类别：{analysis['category']}
        
        文章结构：{' -> '.join(structure)}
        
        要求：
        1. 文章长度800-1200字
        2. 语言流畅，逻辑清晰
        3. 体现独家分析和深度思考
        4. 避免抄袭原文，要有原创观点
        5. 包含数据支撑和专业分析
        6. 结构完整，每个部分都要充实
        
        请按照指定结构撰写完整文章。
        """
        
        try:
            if self.current_ai_model == 'openai' and 'openai' in self.ai_clients:
                model_name = self.config.OPENAI_MODEL if self.config else "gpt-3.5-turbo"
                max_tokens = self.config.OPENAI_MAX_TOKENS if self.config else 2000
                temperature = self.config.OPENAI_TEMPERATURE if self.config else 0.8

                response = self.ai_clients['openai'].chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()
            else:
                raise Exception("没有可用的AI模型")

        except Exception as e:
            print(f"AI生成内容失败: {e}")
            return self._generate_template_content(news_data, analysis, article_type)
    
    def _generate_template_content(self, news_data, analysis, article_type):
        """使用模板生成内容"""
        try:
            from .article_templates import template_manager
            return template_manager.generate_structure_content(article_type, news_data, analysis)
        except ImportError:
            # 如果模板模块不可用，使用简化版本
            return self._generate_simple_template_content(news_data, analysis, article_type)

    def _generate_simple_template_content(self, news_data, analysis, article_type):
        """生成简化的模板内容"""
        structure = self.article_templates[article_type]['structure']
        content_parts = []

        for section in structure:
            if section == '导语' or section == '引言' or section == '开篇':
                part = f"## {section}\n\n据{news_data['source']}报道，{news_data['title']}。这一事件引发了广泛关注，本文将对此进行深入分析。\n"
            elif section == '事件详情' or section == '现状分析' or section == '核心内容':
                part = f"## {section}\n\n{news_data['content'][:200]}...\n\n从目前掌握的信息来看，此事件具有以下特点：\n"
                for i, point in enumerate(analysis['key_points'][:3], 1):
                    part += f"{i}. {point}\n"
                part += "\n"
            elif section == '背景分析' or section == '原因探讨':
                part = f"## {section}\n\n要理解这一事件的深层含义，需要从多个角度进行分析。相关专家指出，这一现象的出现并非偶然，而是多种因素共同作用的结果。\n"
            else:
                part = f"## {section}\n\n综合以上分析，我们可以看出这一事件的重要意义。未来发展值得持续关注。\n"

            content_parts.append(part)

        return '\n'.join(content_parts)

    def _assess_article_quality(self, article, news_data):
        """评估文章质量"""
        try:
            from .article_quality import assess_article_quality
            return assess_article_quality(article, news_data)
        except ImportError:
            # 如果质量评估模块不可用，返回默认评分
            return {
                'total_score': 0.7,
                'scores': {},
                'grade': 'B',
                'suggestions': []
            }

    def _improve_article_content(self, content, suggestions):
        """根据建议改进文章内容"""
        if not suggestions or not self._is_ai_available():
            return None

        improvement_prompt = f"""
        请根据以下建议改进文章内容：

        原文内容：
        {content[:1000]}...

        改进建议：
        {chr(10).join(f"- {suggestion}" for suggestion in suggestions)}

        要求：
        1. 保持原文的核心信息和观点
        2. 根据建议进行针对性改进
        3. 确保文章结构清晰、逻辑连贯
        4. 使用中文撰写

        请返回改进后的完整文章内容。
        """

        try:
            if self.current_ai_model == 'openai' and 'openai' in self.ai_clients:
                response = self.ai_clients['openai'].chat.completions.create(
                    model=self.config.OPENAI_MODEL if self.config else "gpt-3.5-turbo",
                    messages=[{"role": "user", "content": improvement_prompt}],
                    max_tokens=self.config.OPENAI_MAX_TOKENS if self.config else 2000,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"文章改进失败: {e}")

        return None

    def _save_article_to_file(self, article, news_data):
        """保存文章到文件"""
        try:
            # 确保articles目录存在
            articles_dir = "articles"
            if not os.path.exists(articles_dir):
                os.makedirs(articles_dir)

            # 生成文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_title = re.sub(r'[^\w\s-]', '', news_data['title'])[:30]
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            filename = f"{timestamp}_{safe_title}.md"

            # 保存文件
            filepath = os.path.join(articles_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(article)

            print(f"✅ 文章已保存到文件: {filename}")
            return filename

        except Exception as e:
            print(f"❌ 保存文章到文件失败: {e}")
            return None

    def _save_to_database(self, article, news_data, analysis, quality_result, article_type, style):
        """保存文章到数据库"""
        try:
            from .database import get_database_manager
            db_manager = get_database_manager()

            if not db_manager.available:
                print("数据库不可用，跳过数据库保存")
                return None

            # 提取标题
            title_match = re.search(r'^# (.+)', article, re.MULTILINE)
            title = title_match.group(1) if title_match else news_data['title']

            # 提取纯文本内容（去除Markdown格式）
            content_lines = article.split('\n')
            content_start = 0
            for i, line in enumerate(content_lines):
                if line.strip() == '---' and i > 0:
                    content_start = i + 1
                    break

            content = '\n'.join(content_lines[content_start:])
            content = re.sub(r'#{1,6}\s+', '', content)  # 移除标题标记
            content = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', content)  # 移除粗体/斜体
            content = content.strip()

            # 准备数据库数据
            article_data = {
                'title': title,
                'content': content,
                'summary': news_data.get('summary', '')[:500],  # 限制摘要长度
                'article_type': article_type,
                'writing_style': style,
                'source_news_id': str(news_data.get('id', '')),
                'source_news_title': news_data.get('title', ''),
                'source_news_url': news_data.get('link', ''),
                'quality_score': quality_result.get('total_score', 0.0),
                'quality_grade': quality_result.get('grade', 'C')
            }

            article_id = db_manager.save_article(article_data)

            if article_id:
                print(f"✅ 文章已保存到数据库，ID: {article_id}")
            else:
                print("❌ 保存文章到数据库失败")

            return article_id

        except ImportError:
            print("数据库模块不可用，跳过数据库保存")
            return None
        except Exception as e:
            print(f"❌ 保存文章到数据库失败: {e}")
            return None

    def _format_article(self, title, content, news_data):
        """格式化文章"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        article = f"""# {title}

**发布时间：** {timestamp}
**信息来源：** {news_data['source']}
**原文链接：** {news_data['link']}

---

{content}

---

*本文为AI辅助撰写的原创分析文章，仅供参考。*
"""
        return article
    
    def _extract_key_points(self, content):
        """提取关键点"""
        # 简单实现：提取包含数字或重要词汇的句子
        sentences = re.split(r'[。！？]', content)
        key_points = []
        
        important_patterns = [
            r'\d+%', r'\d+万', r'\d+亿', r'\d+年', r'\d+月',
            r'宣布', r'发布', r'启动', r'完成', r'增长', r'下降'
        ]
        
        for sentence in sentences:
            if any(re.search(pattern, sentence) for pattern in important_patterns):
                key_points.append(sentence.strip())
        
        return key_points[:5]
    
    def _extract_entities(self, content):
        """提取实体（简单实现）"""
        # 这里可以使用更复杂的NER模型
        import jieba.posseg as pseg
        
        entities = []
        words = pseg.cut(content)
        
        for word, flag in words:
            if flag in ['nr', 'ns', 'nt'] and len(word) > 1:  # 人名、地名、机构名
                entities.append(word)
        
        return list(set(entities))[:10]
    
    def _analyze_sentiment(self, content):
        """分析情感"""
        positive_words = ['好', '优秀', '成功', '增长', '提升', '改善', '突破', '创新']
        negative_words = ['坏', '失败', '下降', '问题', '危机', '困难', '风险', '担忧']
        
        import jieba
        words = list(jieba.cut(content))
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _categorize_news(self, title):
        """新闻分类"""
        categories = {
            '经济': ['经济', '金融', '股市', '投资', 'GDP', '通胀', '贸易'],
            '科技': ['科技', '人工智能', '互联网', '5G', '芯片', '创新'],
            '政治': ['政府', '政策', '法律', '外交', '会议', '领导'],
            '社会': ['社会', '民生', '教育', '医疗', '环境', '文化'],
            '体育': ['体育', '奥运', '世界杯', '比赛', '运动员'],
            '娱乐': ['娱乐', '明星', '电影', '音乐', '综艺']
        }
        
        for category, keywords in categories.items():
            if any(keyword in title for keyword in keywords):
                return category
        
        return '综合'
    
    def _assess_urgency(self, news_data):
        """评估紧急程度"""
        urgent_keywords = ['突发', '紧急', '重大', '严重', '危机', '事故']
        
        if any(keyword in news_data['title'] for keyword in urgent_keywords):
            return 'high'
        elif (datetime.now() - news_data['publish_time']).total_seconds() < 3600:  # 1小时内
            return 'medium'
        else:
            return 'low'
    
    def _generate_fallback_article(self, news_data):
        """生成备用文章（当AI不可用时）"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return f"""# 【独家报道】{news_data['title']}

**发布时间：** {timestamp}
**信息来源：** {news_data['source']}

## 事件概述

{news_data['summary']}

## 详细内容

{news_data['content'][:500]}...

## 分析观点

这一事件值得关注，我们将持续跟踪报道。

---

*本文基于公开信息整理，仅供参考。*
"""
