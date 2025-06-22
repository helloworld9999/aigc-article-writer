#!/bin/bash

echo "========================================"
echo "AI文章撰写工具 - GitHub提交脚本"
echo "========================================"
echo

echo "请确保您已经在GitHub上创建了仓库！"
echo "仓库名建议: aigc-article-writer"
echo

read -p "请输入您的GitHub用户名: " username

if [ -z "$username" ]; then
    echo "错误: 用户名不能为空"
    exit 1
fi

echo
echo "正在添加远程仓库..."
git remote add origin https://github.com/$username/aigc-article-writer.git

echo
echo "验证远程仓库..."
git remote -v

echo
echo "正在推送代码到GitHub..."
git push -u origin master

echo
echo "创建发布标签..."
git tag -a v1.0.0 -m "Release version 1.0.0: AI文章撰写工具首次发布"

echo
echo "推送标签到GitHub..."
git push origin v1.0.0

echo
echo "========================================"
echo "🎉 提交完成！"
echo "========================================"
echo
echo "您的项目现在可以在以下地址访问:"
echo "https://github.com/$username/aigc-article-writer"
echo
echo "建议接下来的操作:"
echo "1. 在GitHub上设置仓库描述和标签"
echo "2. 启用Issues和Wiki功能"
echo "3. 添加项目主题标签 (Topics)"
echo "4. 考虑创建GitHub Pages展示页面"
echo
