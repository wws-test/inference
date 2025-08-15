#!/usr/bin/env python3
"""
测试开发模式功能的脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_dev_mode_imports():
    """测试开发模式相关的导入是否正常"""
    try:
        from xinference.deploy.cmdline import start_local_cluster
        from xinference.deploy.local import main
        from xinference.api.restful_api import run, RESTfulAPI
        print("✓ 开发模式相关模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 开发模式相关模块导入失败: {e}")
        return False

def test_dev_mode_help():
    """测试xinference-local --dev帮助信息"""
    try:
        import subprocess
        result = subprocess.run(
            ["xinference-local", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if "--dev" in result.stdout:
            print("✓ xinference-local --dev选项已添加")
            return True
        else:
            print("✗ xinference-local --dev选项未找到")
            return False
    except Exception as e:
        print(f"✗ 测试xinference-local帮助失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试开发模式功能...")
    print("=" * 50)
    
    tests = [
        test_dev_mode_imports,
        test_dev_mode_help,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ 测试异常: {e}")
        print()
    
    print("=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 开发模式功能实现成功！")
        print("\n使用方法:")
        print("1. 启动开发模式: xinference-local --dev")
        print("2. 前端将在 http://localhost:3000 启动（支持热更新）")
        print("3. 后端API在 http://localhost:9997 运行")
        print("4. 修改前端代码后会自动刷新")
        return 0
    else:
        print("❌ 部分测试失败，请检查实现")
        return 1

if __name__ == "__main__":
    sys.exit(main())
