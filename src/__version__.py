#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI文章撰写工具 - 版本信息

包含项目的版本号、作者信息和其他元数据。
"""

# 版本信息
__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# 项目信息
__title__ = "AI文章撰写工具"
__description__ = "基于AI的智能文章撰写工具，能够分析实时热点新闻并生成高质量的独家报道"
__author__ = "AI Assistant"
__author_email__ = "ai@example.com"
__license__ = "MIT"
__copyright__ = "Copyright 2025 AI文章撰写工具"

# 项目URL
__url__ = "https://github.com/your-username/aigc-wenzhang"
__download_url__ = "https://github.com/your-username/aigc-wenzhang/archive/v1.0.0.tar.gz"

# 支持的Python版本
__python_requires__ = ">=3.8"

# 项目状态
__status__ = "Production"  # Development, Beta, Production

# 构建信息
__build_date__ = "2025-06-22"
__build_number__ = "1"

# 功能特性标志
FEATURES = {
    "web_interface": True,
    "ai_generation": True,
    "news_analysis": True,
    "quality_assessment": True,
    "database_storage": True,
    "multi_sources": True,
    "article_templates": True,
    "performance_monitoring": True,
}

# API版本
API_VERSION = "v1"

def get_version():
    """获取版本字符串"""
    return __version__

def get_version_info():
    """获取版本信息元组"""
    return __version_info__

def get_full_version():
    """获取完整版本信息"""
    return f"{__title__} v{__version__} ({__build_date__})"

def print_version_info():
    """打印版本信息"""
    print(f"{__title__}")
    print(f"版本: {__version__}")
    print(f"作者: {__author__}")
    print(f"许可证: {__license__}")
    print(f"构建日期: {__build_date__}")
    print(f"Python要求: {__python_requires__}")
    print(f"项目状态: {__status__}")

if __name__ == "__main__":
    print_version_info()
