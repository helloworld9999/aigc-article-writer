#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI文章撰写工具 - Web服务启动脚本

这是项目的主要启动脚本，用于启动Web界面服务。
运行此脚本后，可以通过浏览器访问 http://localhost:5000 使用工具。

使用方法:
    python run.py

环境要求:
    - Python 3.8+
    - 已安装项目依赖 (pip install -r requirements.txt)
"""

import os
import sys
from src.config import get_config

def main():
    """主函数 - 启动Web服务"""
    print("=" * 50)
    print("🚀 AI文章撰写工具")
    print("=" * 50)

    try:
        # 检查Python版本
        if sys.version_info < (3, 8):
            print("❌ 错误: 需要Python 3.8或更高版本")
            print(f"   当前版本: {sys.version}")
            sys.exit(1)

        print("✅ Python版本检查通过")

        # 加载配置
        config = get_config()
        print("✅ 配置加载成功")

        # 创建必要的目录
        os.makedirs("articles", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        print("✅ 目录结构检查完成")

        # 导入并创建Flask应用
        from src.web_interface import create_app
        app = create_app()
        print("✅ Web应用创建成功")

        # 获取配置参数
        host = config.get('WEB_HOST', '127.0.0.1')
        port = int(config.get('WEB_PORT', 5000))
        debug = config.get('DEBUG', 'false').lower() == 'true'

        print(f"🌐 服务地址: http://{host}:{port}")
        print(f"🔧 调试模式: {'开启' if debug else '关闭'}")
        print("💡 按 Ctrl+C 停止服务")
        print("🚀 正在启动服务器...")
        print("-" * 50)

        # 启动Flask应用
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=False,  # 避免重复启动
            threaded=True        # 支持多线程
        )

    except KeyboardInterrupt:
        print("\n🛑 服务已停止")
        sys.exit(0)
    except ImportError as e:
        print(f"❌ 模块导入错误: {e}")
        print("💡 请确保已安装所有依赖: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 请检查配置文件和依赖是否正确安装")
        sys.exit(1)

if __name__ == "__main__":
    main()
