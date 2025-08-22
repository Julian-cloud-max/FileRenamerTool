#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build():
    """清理构建文件"""
    print("🧹 清理构建文件...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  删除目录: {dir_name}")
    
    # 清理Python缓存文件
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                shutil.rmtree(os.path.join(root, dir_name))
                print(f"  删除缓存: {os.path.join(root, dir_name)}")

def check_dependencies():
    """检查依赖"""
    print("📦 检查依赖...")
    
    try:
        import customtkinter
        print(f"  ✓ CustomTkinter: {customtkinter.__version__}")
    except ImportError:
        print("  ✗ CustomTkinter 未安装")
        return False
    
    try:
        import tkinter
        print("  ✓ Tkinter")
    except ImportError:
        print("  ✗ Tkinter 未安装")
        return False
    
    return True

def build_executable():
    """构建可执行文件"""
    print("🔨 构建可执行文件...")
    
    # 使用spec文件构建
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        'FileRenamerTool.spec'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("  ✓ 构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ 构建失败: {e}")
        print(f"  错误输出: {e.stderr}")
        return False

def verify_executable():
    """验证可执行文件"""
    print("✅ 验证可执行文件...")
    
    exe_path = Path('dist/FileRenamerTool.exe')
    if not exe_path.exists():
        print("  ✗ 可执行文件不存在")
        return False
    
    file_size = exe_path.stat().st_size / (1024 * 1024)  # MB
    print(f"  ✓ 文件大小: {file_size:.1f} MB")
    
    return True

def main():
    """主函数"""
    print("🚀 开始构建 FileRenamerTool...")
    print("=" * 50)
    
    # 1. 清理
    clean_build()
    
    # 2. 检查依赖
    if not check_dependencies():
        print("❌ 依赖检查失败，请安装缺失的包")
        return False
    
    # 3. 构建
    if not build_executable():
        print("❌ 构建失败")
        return False
    
    # 4. 验证
    if not verify_executable():
        print("❌ 验证失败")
        return False
    
    print("=" * 50)
    print("🎉 构建完成！")
    print("📁 可执行文件位置: dist/FileRenamerTool.exe")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 