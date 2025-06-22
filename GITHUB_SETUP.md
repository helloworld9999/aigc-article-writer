# GitHub 提交指南

## 🚀 将AI文章撰写工具提交到GitHub

### 步骤1: 在GitHub上创建新仓库

1. **访问GitHub**: https://github.com
2. **登录账户**: 使用您的GitHub账户登录
3. **创建新仓库**: 点击右上角 "+" → "New repository"
4. **仓库配置**:
   ```
   Repository name: aigc-wenzhang
   Description: AI-powered article writing tool that analyzes real-time news and generates high-quality exclusive reports
   Visibility: Public (推荐) 或 Private
   
   ❌ 不要勾选 "Add a README file"
   ❌ 不要勾选 "Add .gitignore" 
   ❌ 不要选择 License
   ```
5. **点击 "Create repository"**

### 步骤2: 添加远程仓库

在项目目录中执行以下命令（替换YOUR_USERNAME为您的GitHub用户名）：

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/aigc-wenzhang.git

# 验证远程仓库
git remote -v
```

### 步骤3: 推送代码到GitHub

```bash
# 推送主分支到GitHub
git push -u origin master

# 或者如果您的默认分支是main
git branch -M main
git push -u origin main
```

### 步骤4: 创建发布版本（可选）

```bash
# 创建v1.0.0标签
git tag -a v1.0.0 -m "Release version 1.0.0: AI文章撰写工具首次发布"

# 推送标签到GitHub
git push origin v1.0.0
```

## 🔧 如果遇到问题

### 问题1: 认证失败
如果推送时遇到认证问题，请：

1. **使用Personal Access Token**:
   - 访问 GitHub Settings → Developer settings → Personal access tokens
   - 生成新的token，选择repo权限
   - 使用token作为密码

2. **或者使用SSH**:
   ```bash
   # 生成SSH密钥
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   
   # 添加SSH密钥到GitHub
   # 复制 ~/.ssh/id_rsa.pub 内容到 GitHub Settings → SSH keys
   
   # 使用SSH URL
   git remote set-url origin git@github.com:YOUR_USERNAME/aigc-wenzhang.git
   ```

### 问题2: 分支名称问题
如果GitHub默认分支是main而不是master：

```bash
# 重命名本地分支
git branch -M main

# 推送到main分支
git push -u origin main
```

### 问题3: 文件过大
如果有文件过大无法推送：

```bash
# 检查大文件
git ls-files | xargs ls -la | sort -k5 -rn | head

# 移除大文件并重新提交
git rm large_file.db
git commit -m "Remove large database file"
```

## 📋 推送后的验证清单

推送成功后，请在GitHub上验证：

- [ ] ✅ 所有源代码文件已上传
- [ ] ✅ README.md正确显示
- [ ] ✅ 项目描述和标签设置正确
- [ ] ✅ LICENSE文件可见
- [ ] ✅ .gitignore正常工作
- [ ] ✅ 发布版本标签创建成功

## 🎯 推荐的GitHub仓库设置

### 仓库描述
```
AI-powered article writing tool that analyzes real-time news and generates high-quality exclusive reports
```

### 主题标签 (Topics)
```
ai, article-writing, news-analysis, flask, python, web-app, openai, nlp, journalism, content-generation
```

### 仓库设置建议
- ✅ 启用 Issues（用于bug报告和功能请求）
- ✅ 启用 Wiki（用于详细文档）
- ✅ 启用 Discussions（用于社区交流）
- ✅ 设置分支保护规则（如果是团队项目）

## 🌟 提升项目可见性

### 1. 完善README徽章
在README.md顶部添加状态徽章：
```markdown
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/aigc-wenzhang.svg)](https://github.com/YOUR_USERNAME/aigc-wenzhang/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/aigc-wenzhang.svg)](https://github.com/YOUR_USERNAME/aigc-wenzhang/network)
[![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/aigc-wenzhang.svg)](https://github.com/YOUR_USERNAME/aigc-wenzhang/issues)
```

### 2. 创建GitHub Pages（可选）
如果想要项目主页：
- 在仓库设置中启用GitHub Pages
- 选择source为main分支的docs文件夹或README.md

### 3. 设置社交预览
在仓库设置中上传社交预览图片，让分享链接更美观。

## 📞 获取帮助

如果在提交过程中遇到问题：

1. **GitHub文档**: https://docs.github.com/
2. **Git文档**: https://git-scm.com/doc
3. **常见问题**: 查看GitHub的故障排除指南

---

## 🎉 完成后的下一步

项目成功提交到GitHub后，您可以：

1. **分享项目**: 将GitHub链接分享给其他人
2. **持续开发**: 继续添加新功能和改进
3. **社区建设**: 鼓励其他开发者贡献代码
4. **文档维护**: 保持README和文档的更新
5. **版本管理**: 定期发布新版本

**祝您的开源项目获得成功！** 🚀
