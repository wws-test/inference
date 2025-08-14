#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
from typing import Optional, List
from datetime import datetime

class XinferenceDevTool:
    def __init__(self):
        self.repo_root = self._get_repo_root()

    def _get_repo_root(self) -> str:
        """获取仓库根目录"""
        try:
            result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], 
                                 capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            print("错误: 当前目录不是 Git 仓库")
            sys.exit(1)

    def _run_command(self, command: List[str], error_msg: str) -> bool:
        """执行 Git 命令"""
        try:
            subprocess.run(command, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"错误: {error_msg}")
            print(f"详细信息: {e}")
            return False

    def setup_repo(self):
        """配置仓库远程源"""
        print("\n正在配置仓库...")
        
        # 检查是否已配置 upstream
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if 'upstream' not in result.stdout:
            self._run_command(
                ['git', 'remote', 'add', 'upstream', 'https://github.com/xorbitsai/inference.git'],
                "添加 upstream 远程源失败"
            )
            print("成功添加 upstream 远程源")
        else:
            print("upstream 远程源已配置")
        input("\n按回车键继续...")

    def create_feature_branch(self):
        """创建新的功能分支"""
        print("\n=== 创建功能分支 ===")
        branch_name = input("请输入分支名称 (不需要添加 feature/ 前缀): ").strip()
        if not branch_name:
            print("分支名称不能为空")
            return

        if not branch_name.startswith('feature/'):
            branch_name = f'feature/{branch_name}'
        
        print(f"\n正在创建分支 {branch_name}...")
        
        # 检查分支是否已存在
        result = subprocess.run(['git', 'branch'], capture_output=True, text=True)
        if branch_name in result.stdout:
            print(f"分支 {branch_name} 已存在")
            choice = input("是否切换到该分支? (y/n): ")
            if choice.lower() == 'y':
                self._run_command(['git', 'checkout', branch_name], "切换分支失败")
        else:
            self._run_command(['git', 'checkout', '-b', branch_name], "创建分支失败")
        input("\n按回车键继续...")

    def sync_with_upstream(self):
        """同步上游更新"""
        print("\n正在同步上游更新...")
        
        # 保存当前分支
        current_branch = subprocess.run(['git', 'branch', '--show-current'], 
                                     capture_output=True, text=True).stdout.strip()
        
        # 同步主分支
        steps = [
            (['git', 'checkout', 'main'], "切换到 main 分支失败"),
            (['git', 'fetch', 'upstream'], "获取上游更新失败"),
            (['git', 'merge', 'upstream/main'], "合并上游更新失败"),
            (['git', 'push', 'origin', 'main'], "推送到远程失败")
        ]
        
        for command, error_msg in steps:
            if not self._run_command(command, error_msg):
                input("\n按回车键继续...")
                return False
        
        # 如果当前不在 main 分支，更新功能分支
        if current_branch != 'main':
            print(f"\n正在更新分支 {current_branch}...")
            steps = [
                (['git', 'checkout', current_branch], "切换回功能分支失败"),
                (['git', 'merge', 'main'], "合并主分支更新失败")
            ]
            for command, error_msg in steps:
                if not self._run_command(command, error_msg):
                    input("\n按回车键继续...")
                    return False
        
        print("同步完成")
        input("\n按回车键继续...")
        return True

    def commit_changes(self):
        """提交更改"""
        print("\n=== 提交更改 ===")
        print("提交类型:")
        valid_types = {
            'feat': '新功能',
            'fix': '修复缺陷',
            'docs': '文档更新',
            'style': '代码格式',
            'refactor': '代码重构',
            'test': '测试相关',
            'chore': '构建相关'
        }
        
        type_list = list(valid_types.items())
        for i, (type_name, desc) in enumerate(type_list, 1):
            print(f"{i}. {desc} ({type_name})")
        
        while True:
            try:
                type_choice = int(input("\n请选择提交类型 (1-7): "))
                if 1 <= type_choice <= len(type_list):
                    commit_type = type_list[type_choice - 1][0]
                    break
                else:
                    print("无效的选择，请重试")
            except ValueError:
                print("请输入数字")
        
        message = input("\n请输入提交信息: ").strip()
        if not message:
            print("提交信息不能为空")
            input("\n按回车键继续...")
            return False

        full_message = f"{commit_type}: {message}"
        result = self._run_command(['git', 'commit', '-m', full_message], "提交更改失败")
        input("\n按回车键继续...")
        return result

    def create_tag(self):
        """创建版本标签"""
        print("\n=== 创建版本标签 ===")
        version = input("请输入版本号 (例如: 1.0.0): ").strip()
        if not version:
            print("版本号不能为空")
            input("\n按回车键继续...")
            return False

        if not version.startswith('v'):
            version = f'v{version}'
        
        message = input("请输入标签信息 (可选，直接回车使用默认信息): ").strip()
        if not message:
            message = f"Release {version}"
        
        steps = [
            (['git', 'tag', '-a', version, '-m', message], "创建标签失败"),
            (['git', 'push', 'origin', version], "推送标签失败")
        ]
        
        for command, error_msg in steps:
            if not self._run_command(command, error_msg):
                input("\n按回车键继续...")
                return False
        
        print(f"成功创建并推送标签 {version}")
        input("\n按回车键继续...")
        return True

    def show_status(self):
        """显示当前状态"""
        print("\n=== Xinference 开发状态 ===")
        
        # 显示当前分支
        current_branch = subprocess.run(['git', 'branch', '--show-current'], 
                                     capture_output=True, text=True).stdout.strip()
        print(f"\n当前分支: {current_branch}")
        
        # 显示最近的提交
        print("\n最近的提交:")
        subprocess.run(['git', 'log', '--oneline', '-n', '5'])
        
        # 显示未提交的更改
        print("\n未提交的更改:")
        subprocess.run(['git', 'status', '-s'])
        
        input("\n按回车键继续...")

    def merge_main(self):
        """合并主分支到当前分支"""
        print("\n=== 合并主分支 ===")
        
        # 获取所有本地分支
        result = subprocess.run(['git', 'branch'], capture_output=True, text=True)
        branches = [b.strip('* ') for b in result.stdout.strip().split('\n')]
        feature_branches = [b for b in branches if b.startswith('feature/')]
        
        if not feature_branches:
            print("错误: 没有找到任何功能分支")
            input("\n按回车键继续...")
            return False
            
        # 显示可用的功能分支
        print("\n可用的功能分支:")
        for i, branch in enumerate(feature_branches, 1):
            print(f"{i}. {branch}")
            
        # 选择要合并的分支
        while True:
            try:
                choice = int(input(f"\n请选择要合并的分支 (1-{len(feature_branches)}): "))
                if 1 <= choice <= len(feature_branches):
                    target_branch = feature_branches[choice - 1]
                    break
                else:
                    print("无效的选择，请重试")
            except ValueError:
                print("请输入数字")
        
        # 切换到目标分支
        if not self._run_command(['git', 'checkout', target_branch], "切换到目标分支失败"):
            input("\n按回车键继续...")
            return False
            
        print(f"\n已切换到分支: {target_branch}")
        choice = input("确认要将 main 分支的更新合并到当前分支吗? (y/n): ")
        if choice.lower() != 'y':
            print("已取消合并操作")
            input("\n按回车键继续...")
            return False
            
        # 先更新 main 分支
        steps = [
            (['git', 'fetch', 'upstream'], "获取上游更新失败"),
            (['git', 'checkout', 'main'], "切换到 main 分支失败"),
            (['git', 'merge', 'upstream/main'], "合并上游更新失败"),
            (['git', 'push', 'origin', 'main'], "推送到远程失败"),
            (['git', 'checkout', target_branch], "切换回开发分支失败"),
            (['git', 'merge', 'main'], "合并主分支更新失败")
        ]
        
        for command, error_msg in steps:
            if not self._run_command(command, error_msg):
                input("\n按回车键继续...")
                return False
        
        print(f"\n已成功将 main 分支的更新合并到 {target_branch}")
        input("\n按回车键继续...")
        return True

    def switch_branch(self):
        """切换分支"""
        print("\n=== 切换分支 ===")
        
        # 获取所有分支信息
        result = subprocess.run(['git', 'branch'], capture_output=True, text=True)
        branches = [b.strip('* ') for b in result.stdout.strip().split('\n')]
        current_branch = subprocess.run(['git', 'branch', '--show-current'], 
                                     capture_output=True, text=True).stdout.strip()
        
        # 显示所有分支，并标记当前分支
        print("\n可用的分支:")
        for i, branch in enumerate(branches, 1):
            current = "（当前）" if branch == current_branch else ""
            print(f"{i}. {branch} {current}")
            
        # 选择要切换的分支
        while True:
            try:
                choice = int(input(f"\n请选择要切换的分支 (1-{len(branches)}): "))
                if 1 <= choice <= len(branches):
                    target_branch = branches[choice - 1]
                    break
                else:
                    print("无效的选择，请重试")
            except ValueError:
                print("请输入数字")
        
        # 如果选择当前分支，直接返回
        if target_branch == current_branch:
            print(f"\n已经在 {target_branch} 分支上")
            input("\n按回车键继续...")
            return True
            
        # 检查是否有未提交的更改
        status = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True).stdout.strip()
        if status:
            print("\n警告: 当前有未提交的更改")
            print("\n未提交的更改:")
            subprocess.run(['git', 'status', '-s'])
            
            choice = input("\n是否要暂存这些更改后切换分支? (y/n): ")
            if choice.lower() == 'y':
                # 暂存更改
                if not self._run_command(['git', 'stash', 'save', f"自动暂存: 切换到 {target_branch} 分支"],
                                      "暂存更改失败"):
                    input("\n按回车键继续...")
                    return False
                print("已暂存更改")
            else:
                print("已取消切换分支")
                input("\n按回车键继续...")
                return False
        
        # 切换分支
        if not self._run_command(['git', 'checkout', target_branch], "切换分支失败"):
            input("\n按回车键继续...")
            return False
            
        print(f"\n已成功切换到 {target_branch} 分支")
        
        # 如果之前有暂存的更改，询问是否恢复
        if status and choice.lower() == 'y':
            restore_choice = input("\n是否要恢复暂存的更改? (y/n): ")
            if restore_choice.lower() == 'y':
                if not self._run_command(['git', 'stash', 'pop'], "恢复暂存更改失败"):
                    print("警告: 恢复暂存更改失败，您的更改仍然保存在 stash 中")
                else:
                    print("已恢复暂存的更改")
        
        input("\n按回车键继续...")
        return True

def show_menu():
    """显示主菜单"""
    menu_items = [
        "初始化仓库配置",
        "创建功能分支",
        "切换分支",
        "同步上游更新",
        "合并主分支到当前分支",
        "提交更改",
        "创建版本标签",
        "显示当前状态",
        "退出程序"
    ]
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== Xinference 开发管理工具 ===\n")
        for i, item in enumerate(menu_items, 1):
            print(f"{i}. {item}")
        
        try:
            choice = int(input(f"\n请选择操作 (1-{len(menu_items)}): "))
            if 1 <= choice <= len(menu_items):
                return choice
            else:
                print("无效的选择，请重试")
                input("\n按回车键继续...")
        except ValueError:
            print("请输入数字")
            input("\n按回车键继续...")

def main():
    tool = XinferenceDevTool()
    
    while True:
        choice = show_menu()
        
        if choice == 1:
            tool.setup_repo()
        elif choice == 2:
            tool.create_feature_branch()
        elif choice == 3:
            tool.switch_branch()
        elif choice == 4:
            tool.sync_with_upstream()
        elif choice == 5:
            tool.merge_main()
        elif choice == 6:
            tool.commit_changes()
        elif choice == 7:
            tool.create_tag()
        elif choice == 8:
            tool.show_status()
        elif choice == 9:
            print("\n感谢使用，再见！")
            break

if __name__ == '__main__':
    main() 