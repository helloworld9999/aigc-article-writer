# 代码风格和约定

## 编程语言
- Python 3.8+
- 使用UTF-8编码，文件头包含编码声明：`# -*- coding: utf-8 -*-`

## 代码风格
- 使用中文注释和文档字符串
- 类名使用PascalCase（如：`NewsAnalyzer`, `ArticleWriter`）
- 函数和变量名使用snake_case（如：`get_trending_news`, `news_sources`）
- 私有方法使用下划线前缀（如：`_parse_rss_feed`, `_deduplicate_news`）

## 文档字符串
- 使用三重引号的文档字符串
- 简洁的中文描述，如：`"""新闻分析器类"""`、`"""主程序入口"""`

## 导入规范
- 标准库导入在前
- 第三方库导入在中
- 本地模块导入在后
- 使用相对导入（如：`from .news_analyzer import NewsAnalyzer`）

## 错误处理
- 使用try-except块处理异常
- 打印中文错误信息便于调试
- 提供备用方案（如AI不可用时的模板生成）

## 配置管理
- 使用.env文件管理环境变量
- 使用python-dotenv加载配置
- 敏感信息（API密钥）通过环境变量配置