#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将百度同步盘中的「数字教材/」站点同步到本 GitHub 仓库目录（isad-textbook/）。

用法：
    python sync_from_baidu.py

规则：
  - 仅从源（百度盘）复制到本仓库；不删除本仓库中已有的文件（安全策略）。
  - 自动排除：备份目录（. 开头）、临时脚本(_*.py)、_review_counts.json、*.bak*。
  - 保留本仓库自有文件：.git / .gitignore / README.md / LICENSE / .nojekyll / 本脚本。
  - 同时把父目录的「数字教材_离线版.zip」复制到本仓库根。
"""
import os
import shutil

SRC = r"C:/Users/sghpe/Desktop/BaiduSyncdisk/课程/2026信息系统分析与设计/课件/数字教材"
PARENT = os.path.dirname(SRC)
DST = os.path.dirname(os.path.abspath(__file__))  # 本脚本所在目录 = 仓库根

# 本仓库自有的、不应被源覆盖的文件/目录
REPO_META = {".git", ".gitignore", "README.md", "LICENSE", ".nojekyll",
             "sync_from_baidu.py"}

def should_skip(name):
    if name in REPO_META:
        return True
    if name.startswith("."):           # 备份目录 .edit_backup* / .req*_backup* / .wpp_backup / .workbuddy
        return True
    if name.startswith("_"):           # _req12.py / _review_counts.json 等
        return True
    if ".bak" in name.lower():
        return True
    return False

def sync_dir(src, dst):
    os.makedirs(dst, exist_ok=True)
    for name in os.listdir(src):
        if should_skip(name):
            continue
        s = os.path.join(src, name)
        d = os.path.join(dst, name)
        if os.path.isdir(s):
            sync_dir(s, d)
        else:
            if not os.path.exists(d) or os.path.getsize(s) != os.path.getsize(d):
                shutil.copy2(s, d)
                print("  更新:", os.path.relpath(d, DST))

def main():
    if not os.path.isdir(SRC):
        raise SystemExit(f"源目录不存在: {SRC}")
    print("同步源:", SRC)
    print("同步到:", DST)
    sync_dir(SRC, DST)
    # 离线包
    zip_src = os.path.join(PARENT, "数字教材_离线版.zip")
    zip_dst = os.path.join(DST, "数字教材_离线版.zip")
    if os.path.exists(zip_src):
        if (not os.path.exists(zip_dst)) or os.path.getsize(zip_src) != os.path.getsize(zip_dst):
            shutil.copy2(zip_src, zip_dst)
            print("  更新离线包: 数字教材_离线版.zip")
    print("完成。请用 git add -A && git commit && git push 发布。")

if __name__ == "__main__":
    main()
