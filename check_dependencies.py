#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖检查脚本
检查项目依赖是否正确安装
"""

import sys
import subprocess
import importlib
from pathlib import Path

# 必需的依赖包
REQUIRED_PACKAGES = {
    'requests': '>=2.31.0',
    'beautifulsoup4': '>=4.12.0',
    'feedparser': '>=6.0.10',
    'jieba': '>=0.42.1',
    'flask': '>=2.3.0',
    'newspaper3k': '>=0.2.8'
}

# 可选的依赖包
OPTIONAL_PACKAGES = {
    'openai': '>=1.0.0',
    'python-dotenv': '>=1.0.0',
    'schedule': '>=1.2.0',
    'sqlalchemy': '>=2.0.0',
    'pandas': '>=2.0.0',
    'numpy': '>=1.24.0',
    'matplotlib': '>=3.7.0',
    'seaborn': '>=0.12.0'
}

def check_python_version():
    """检查Python版本"""
    print("检查Python版本...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("   需要Python 3.8或更高版本")
        return False
    else:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True

def check_package(package_name, version_requirement=None):
    """检查单个包是否安装"""
    try:
        module = importlib.import_module(package_name)
        
        # 获取版本信息
        version = getattr(module, '__version__', 'unknown')
        
        print(f"✅ {package_name}: {version}")
        return True
        
    except ImportError:
        print(f"❌ {package_name}: 未安装")
        return False

def check_required_packages():
    """检查必需的包"""
    print("\n检查必需依赖包...")
    missing_packages = []
    
    for package, version in REQUIRED_PACKAGES.items():
        if not check_package(package, version):
            missing_packages.append(package)
    
    return missing_packages

def check_optional_packages():
    """检查可选的包"""
    print("\n检查可选依赖包...")
    missing_packages = []
    
    for package, version in OPTIONAL_PACKAGES.items():
        if not check_package(package, version):
            missing_packages.append(package)
    
    return missing_packages

def check_project_structure():
    """检查项目结构"""
    print("\n检查项目结构...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'src/__init__.py',
        'src/news_analyzer.py',
        'src/article_writer.py',
        'src/web_interface.py',
        'templates/index.html'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}: 文件不存在")
            missing_files.append(file_path)
    
    return missing_files

def check_environment_config():
    """检查环境配置"""
    print("\n检查环境配置...")
    
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if env_example.exists():
        print("✅ .env.example: 存在")
    else:
        print("❌ .env.example: 不存在")
    
    if env_file.exists():
        print("✅ .env: 存在")
        return True
    else:
        print("⚠️  .env: 不存在（可选）")
        print("   提示: 复制 .env.example 为 .env 并配置相关参数")
        return False

def install_missing_packages(packages):
    """安装缺失的包"""
    if not packages:
        return True
    
    print(f"\n发现 {len(packages)} 个缺失的包:")
    for package in packages:
        print(f"  - {package}")
    
    install = input("\n是否自动安装缺失的包? (y/n): ").lower().strip()
    
    if install == 'y':
        try:
            # 尝试使用当前Python解释器
            import subprocess
            cmd = ['pip', 'install'] + packages
            print(f"执行命令: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ 包安装成功")
                return True
            else:
                print(f"❌ 包安装失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 安装过程中出错: {e}")
            return False
    
    return False

def main():
    """主函数"""
    print("=== AI文章撰写工具依赖检查 ===\n")
    
    # 检查Python版本
    if not check_python_version():
        print("\n❌ Python版本检查失败，请升级Python版本")
        return False
    
    # 检查项目结构
    missing_files = check_project_structure()
    if missing_files:
        print(f"\n❌ 项目结构不完整，缺少 {len(missing_files)} 个文件")
        return False
    
    # 检查环境配置
    check_environment_config()
    
    # 检查必需依赖
    missing_required = check_required_packages()
    
    # 检查可选依赖
    missing_optional = check_optional_packages()
    
    # 处理缺失的包
    if missing_required:
        print(f"\n❌ 缺少 {len(missing_required)} 个必需依赖包")
        if not install_missing_packages(missing_required):
            print("请手动安装缺失的必需依赖包:")
            print(f"pip install {' '.join(missing_required)}")
            return False
    
    if missing_optional:
        print(f"\n⚠️  缺少 {len(missing_optional)} 个可选依赖包")
        print("这些包不是必需的，但可以提供额外功能:")
        for package in missing_optional:
            print(f"  - {package}")
        
        install_missing_packages(missing_optional)
    
    # 最终检查
    print("\n=== 检查完成 ===")
    
    if not missing_required and not missing_files:
        print("✅ 所有必需依赖都已满足，项目可以正常运行")
        
        # 提供运行建议
        print("\n🚀 运行建议:")
        print("1. 复制 .env.example 为 .env 并配置API密钥")
        print("2. 运行 python main.py 启动应用")
        print("3. 运行 python test_basic.py 进行基本测试")
        
        return True
    else:
        print("❌ 存在未解决的依赖问题，请先解决后再运行项目")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
