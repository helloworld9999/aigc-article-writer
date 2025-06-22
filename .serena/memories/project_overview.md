# AI文章撰写工具项目概览

## 项目目的
AI文章撰写工具是一个基于AI的智能文章撰写系统，能够：
- 分析当前实时热点新闻
- 自动撰写高质量的独家首发报道
- 提供Web界面和命令行两种使用模式
- 支持多种文章类型（突发新闻、深度分析、特稿报道）

## 技术栈
- **后端**: Python 3.8+ + Flask
- **前端**: HTML + Bootstrap + JavaScript
- **AI引擎**: OpenAI GPT (可选)
- **新闻获取**: RSS订阅 + 网页爬虫 (feedparser, newspaper3k)
- **文本处理**: jieba分词
- **数据处理**: pandas, numpy
- **可视化**: matplotlib, seaborn

## 核心模块
- `main.py`: 主程序入口，提供交互式选择
- `src/news_analyzer.py`: 新闻分析器，负责获取和分析热点新闻
- `src/article_writer.py`: 文章撰写器，负责基于新闻生成文章
- `src/web_interface.py`: Web界面，提供Flask API和路由
- `templates/index.html`: Web前端界面

## 项目特点
- 支持多个新闻源（新浪、网易、腾讯等）
- 智能去重和热点话题分析
- 可配置的文章类型和写作风格
- 自动保存和管理生成的文章
- 响应式Web界面