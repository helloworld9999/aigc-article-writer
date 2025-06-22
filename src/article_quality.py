#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章质量评估模块
"""

import re
from typing import Dict, List, Tuple

class ArticleQualityAssessor:
    """文章质量评估器"""
    
    def __init__(self):
        """初始化评估器"""
        self.quality_metrics = {
            'length': {'min': 500, 'max': 3000, 'weight': 0.2},
            'structure': {'weight': 0.25},
            'readability': {'weight': 0.2},
            'content_quality': {'weight': 0.25},
            'originality': {'weight': 0.1}
        }
    
    def assess_article(self, article_content: str, original_news: Dict = None) -> Dict:
        """评估文章质量"""
        scores = {}
        
        # 长度评估
        scores['length'] = self._assess_length(article_content)
        
        # 结构评估
        scores['structure'] = self._assess_structure(article_content)
        
        # 可读性评估
        scores['readability'] = self._assess_readability(article_content)
        
        # 内容质量评估
        scores['content_quality'] = self._assess_content_quality(article_content)
        
        # 原创性评估
        if original_news:
            scores['originality'] = self._assess_originality(article_content, original_news)
        else:
            scores['originality'] = 0.8  # 默认分数
        
        # 计算总分
        total_score = sum(
            scores[metric] * self.quality_metrics[metric]['weight']
            for metric in scores
        )
        
        return {
            'total_score': round(total_score, 2),
            'scores': scores,
            'grade': self._get_grade(total_score),
            'suggestions': self._get_suggestions(scores)
        }
    
    def _assess_length(self, content: str) -> float:
        """评估文章长度"""
        length = len(content)
        min_len = self.quality_metrics['length']['min']
        max_len = self.quality_metrics['length']['max']
        
        if length < min_len:
            return max(0.3, length / min_len)
        elif length > max_len:
            return max(0.7, 1 - (length - max_len) / max_len)
        else:
            return 1.0
    
    def _assess_structure(self, content: str) -> float:
        """评估文章结构"""
        score = 0.0
        
        # 检查是否有标题
        if content.startswith('#'):
            score += 0.2
        
        # 检查是否有段落分隔
        paragraphs = content.split('\n\n')
        if len(paragraphs) >= 3:
            score += 0.3
        elif len(paragraphs) >= 2:
            score += 0.2
        
        # 检查是否有小标题
        subheadings = re.findall(r'^##\s+.+', content, re.MULTILINE)
        if len(subheadings) >= 2:
            score += 0.3
        elif len(subheadings) >= 1:
            score += 0.2
        
        # 检查是否有列表或要点
        lists = re.findall(r'^\s*[-*+]\s+.+', content, re.MULTILINE)
        if len(lists) >= 3:
            score += 0.2
        elif len(lists) >= 1:
            score += 0.1
        
        return min(1.0, score)
    
    def _assess_readability(self, content: str) -> float:
        """评估可读性"""
        score = 0.0
        
        # 句子长度分析
        sentences = re.split(r'[。！？]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if sentences:
            avg_sentence_length = sum(len(s) for s in sentences) / len(sentences)
            
            # 理想句子长度15-30字
            if 15 <= avg_sentence_length <= 30:
                score += 0.4
            elif 10 <= avg_sentence_length <= 40:
                score += 0.3
            else:
                score += 0.2
        
        # 段落长度分析
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        if paragraphs:
            avg_paragraph_length = sum(len(p) for p in paragraphs) / len(paragraphs)
            
            # 理想段落长度100-300字
            if 100 <= avg_paragraph_length <= 300:
                score += 0.3
            elif 50 <= avg_paragraph_length <= 500:
                score += 0.2
            else:
                score += 0.1
        
        # 词汇多样性
        try:
            import jieba
            words = list(jieba.cut(content))
            unique_words = set(words)
            if len(words) > 0:
                diversity = len(unique_words) / len(words)
                if diversity > 0.6:
                    score += 0.3
                elif diversity > 0.4:
                    score += 0.2
                else:
                    score += 0.1
        except ImportError:
            score += 0.2  # 默认分数
        
        return min(1.0, score)
    
    def _assess_content_quality(self, content: str) -> float:
        """评估内容质量"""
        score = 0.0
        
        # 关键词密度检查
        quality_keywords = [
            '分析', '研究', '数据', '专家', '观点', '影响', '发展', '趋势',
            '政策', '市场', '技术', '创新', '改革', '合作', '建设'
        ]
        
        keyword_count = sum(1 for keyword in quality_keywords if keyword in content)
        score += min(0.3, keyword_count * 0.05)
        
        # 数据和事实检查
        numbers = re.findall(r'\d+(?:\.\d+)?[%万亿千百十]?', content)
        if len(numbers) >= 3:
            score += 0.2
        elif len(numbers) >= 1:
            score += 0.1
        
        # 引用和来源检查
        citations = re.findall(r'据.*?[报道|消息|了解|介绍]', content)
        if len(citations) >= 2:
            score += 0.2
        elif len(citations) >= 1:
            score += 0.1
        
        # 逻辑连接词检查
        connectors = ['因此', '然而', '此外', '同时', '另外', '总之', '综上']
        connector_count = sum(1 for connector in connectors if connector in content)
        score += min(0.3, connector_count * 0.1)
        
        return min(1.0, score)
    
    def _assess_originality(self, content: str, original_news: Dict) -> float:
        """评估原创性"""
        original_content = original_news.get('content', '') + original_news.get('summary', '')
        
        if not original_content:
            return 0.8
        
        # 简单的文本相似度检查
        try:
            import jieba
            
            # 分词
            content_words = set(jieba.cut(content))
            original_words = set(jieba.cut(original_content))
            
            # 计算Jaccard相似度
            intersection = len(content_words & original_words)
            union = len(content_words | original_words)
            
            if union == 0:
                similarity = 0
            else:
                similarity = intersection / union
            
            # 原创性分数 = 1 - 相似度
            originality = 1 - similarity
            
            # 确保分数在合理范围内
            return max(0.3, min(1.0, originality))
            
        except ImportError:
            return 0.7  # 默认分数
    
    def _get_grade(self, score: float) -> str:
        """根据分数获取等级"""
        if score >= 0.9:
            return 'A+'
        elif score >= 0.8:
            return 'A'
        elif score >= 0.7:
            return 'B+'
        elif score >= 0.6:
            return 'B'
        elif score >= 0.5:
            return 'C+'
        elif score >= 0.4:
            return 'C'
        else:
            return 'D'
    
    def _get_suggestions(self, scores: Dict) -> List[str]:
        """根据评分提供改进建议"""
        suggestions = []
        
        if scores['length'] < 0.7:
            suggestions.append("建议增加文章长度，提供更多详细信息和分析")
        
        if scores['structure'] < 0.7:
            suggestions.append("建议改进文章结构，添加小标题和段落分隔")
        
        if scores['readability'] < 0.7:
            suggestions.append("建议优化句子和段落长度，提高可读性")
        
        if scores['content_quality'] < 0.7:
            suggestions.append("建议添加更多数据、专家观点和事实支撑")
        
        if scores['originality'] < 0.7:
            suggestions.append("建议增加原创观点和独特分析角度")
        
        return suggestions

# 全局质量评估器实例
quality_assessor = ArticleQualityAssessor()

def assess_article_quality(content: str, original_news: Dict = None) -> Dict:
    """评估文章质量的便捷函数"""
    return quality_assessor.assess_article(content, original_news)
