#!/usr/bin/env python3
"""
测试 xinference-local 的热更新功能
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def test_hot_reload_option():
    """测试 --hot-reload 选项是否可用"""
    print("测试 xinference-local --hot-reload 选项...")
    
    try:
        # 测试帮助信息
        result = subprocess.run(
            ["xinference-local", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            if "--hot-reload" in result.stdout:
                print("✓ --hot-reload 选项已成功添加")
                return True
            else:
                print("✗ --hot-reload 选项未在帮助信息中找到")
                return False
        else:
            print(f"✗ 获取帮助信息失败: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ 命令执行超时")
        return False
    except FileNotFoundError:
        print("✗ xinference-local 命令未找到，请确保已正确安装")
        return False
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_dev_mode_option():
    """测试 --dev 选项是否仍然可用"""
    print("\n测试 xinference-local --dev 选项...")
    
    try:
        result = subprocess.run(
            ["xinference-local", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            if "--dev" in result.stdout:
                print("✓ --dev 选项仍然可用")
                return True
            else:
                print("✗ --dev 选项未找到")
                return False
        else:
            print(f"✗ 获取帮助信息失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("Xinference 热更新功能测试")
    print("=" * 50)
    
    # 测试热更新选项
    hot_reload_ok = test_hot_reload_option()
    
    # 测试开发模式选项
    dev_mode_ok = test_dev_mode_option()
    
    print("\n" + "=" * 50)
    print("测试结果总结:")
    print(f"热更新选项 (--hot-reload): {'✓ 通过' if hot_reload_ok else '✗ 失败'}")
    print(f"开发模式选项 (--dev): {'✓ 通过' if dev_mode_ok else '✗ 失败'}")
    
    if hot_reload_ok and dev_mode_ok:
        print("\n🎉 所有测试通过！热更新功能已成功添加。")
        print("\n使用方法:")
        print("1. 启动热更新模式: xinference-local --hot-reload")
        print("2. 启动开发模式: xinference-local --dev")
        print("3. 热更新模式会自动安装前端依赖并启动 React 开发服务器")
    else:
        print("\n❌ 部分测试失败，请检查代码修改。")
        sys.exit(1)

if __name__ == "__main__":
    main()
