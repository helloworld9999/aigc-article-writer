# 项目架构设计

## 整体架构
```
用户界面层 (UI Layer)
├── Web界面 (templates/index.html)
└── 命令行界面 (main.py)

业务逻辑层 (Business Logic Layer)
├── 新闻分析器 (NewsAnalyzer)
├── 文章撰写器 (ArticleWriter)
└── Web接口 (Flask Routes)

数据访问层 (Data Access Layer)
├── RSS新闻源
├── API新闻源
└── 文件系统存储
```

## 核心组件

### NewsAnalyzer (新闻分析器)
- **职责**: 获取、解析、去重热点新闻
- **数据源**: RSS订阅、新闻API
- **功能**: 热点话题分析、情感分析、新闻分类

### ArticleWriter (文章撰写器)
- **职责**: 基于新闻数据生成文章
- **模式**: AI生成 + 模板生成（备用）
- **支持**: 多种文章类型和写作风格

### Web Interface (Web接口)
- **技术**: Flask + Bootstrap
- **API**: RESTful接口设计
- **功能**: 新闻展示、文章生成、文件管理

## 数据流
1. 新闻获取: RSS/API → NewsAnalyzer
2. 数据处理: 去重、分析、分类
3. 用户选择: Web界面或命令行
4. 文章生成: ArticleWriter → AI/模板
5. 结果输出: 文件保存 + 界面展示

## 设计模式
- **单一职责**: 每个类专注特定功能
- **依赖注入**: 通过环境变量配置外部依赖
- **策略模式**: 支持多种文章生成策略
- **模板方法**: 文章生成的统一流程