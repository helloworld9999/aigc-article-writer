# 建议的开发命令

## Windows系统命令
- `dir` - 列出目录内容
- `cd` - 切换目录
- `type` - 查看文件内容
- `findstr` - 在文件中搜索文本
- `copy` - 复制文件
- `del` - 删除文件
- `md` - 创建目录

## Python环境管理
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 停用虚拟环境
deactivate

# 安装依赖
pip install -r requirements.txt

# 更新依赖
pip freeze > requirements.txt
```

## 项目运行命令
```bash
# 运行主程序
python main.py

# 直接启动Web界面
python -c "from src.web_interface import create_app; app = create_app(); app.run(host='0.0.0.0', port=5000, debug=True)"
```

## 开发工具命令
```bash
# 代码格式化 (如果安装了black)
black src/ main.py

# 代码检查 (如果安装了flake8)
flake8 src/ main.py

# 运行测试 (如果有测试文件)
python -m pytest tests/
```

## Git命令
```bash
# 查看状态
git status

# 添加文件
git add .

# 提交更改
git commit -m "描述信息"

# 推送到远程
git push origin main
```

## 环境配置
```bash
# 复制环境变量模板
copy .env.example .env

# 编辑环境变量文件
notepad .env
```