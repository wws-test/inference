#!/usr/bin/env python3
"""
Xinference 快速构建脚本 (Windows友好版)
跳过UI构建，专注于Python包构建和上传
"""

import os
import sys
import subprocess
import argparse
import shutil
import time
from pathlib import Path

class Colors:
    """终端颜色"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class QuickBuilder:
    def __init__(self):
        self.repo_root = Path(__file__).parent
        self.dist_path = self.repo_root / "dist"
        self.private_repo_url = "http://192.2.123.34:8081"
        self.username = "admin"
        self.password = "admin123"
        
    def print_step(self, step, message):
        """打印步骤信息"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}[{step}] {message}{Colors.ENDC}")
        
    def print_success(self, message):
        """打印成功信息"""
        print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
        
    def print_warning(self, message):
        """打印警告信息"""
        print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")
        
    def print_error(self, message):
        """打印错误信息"""
        print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")
        
    def run_command(self, cmd, cwd=None, check=True, capture_output=False, env=None):
        """运行命令"""
        if cwd is None:
            cwd = self.repo_root
            
        print(f"执行命令: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd, 
                cwd=cwd, 
                check=check, 
                capture_output=capture_output,
                text=True,
                env=env
            )
            return result
        except subprocess.CalledProcessError as e:
            if capture_output:
                print(f"命令输出: {e.stdout}")
                print(f"错误输出: {e.stderr}")
            raise e
            
    def check_prerequisites(self):
        """检查前置条件"""
        self.print_step("检查", "前置条件")
        
        # 检查Python版本
        python_version = sys.version_info
        if python_version < (3, 7):
            self.print_error(f"Python版本过低: {python_version.major}.{python_version.minor}，需要3.7+")
            return False
        self.print_success(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # 检查twine
        try:
            self.run_command([sys.executable, "-m", "twine", "--version"], capture_output=True)
            self.print_success("twine已安装")
        except subprocess.CalledProcessError:
            self.print_warning("twine未安装，将尝试安装")
            try:
                self.run_command([sys.executable, "-m", "pip", "install", "twine"])
                self.print_success("twine安装成功")
            except subprocess.CalledProcessError:
                self.print_error("twine安装失败")
                return False
                
        return True
        
    def clean_build(self):
        """清理构建文件"""
        self.print_step("清理", "构建文件")
        
        # 清理Python构建文件
        dirs_to_clean = [
            "build", "dist", "*.egg-info", "__pycache__", ".pytest_cache"
        ]
        
        for pattern in dirs_to_clean:
            for path in self.repo_root.glob(pattern):
                if path.is_dir():
                    shutil.rmtree(path)
                    self.print_success(f"删除目录: {path}")
                else:
                    path.unlink()
                    self.print_success(f"删除文件: {path}")
                    
    def get_version(self):
        """获取当前版本"""
        try:
            result = self.run_command([sys.executable, "versioneer.py", "version"], capture_output=True)
            version = result.stdout.strip()
            return version
        except subprocess.CalledProcessError:
            # 如果versioneer失败，尝试从git获取
            try:
                result = self.run_command(["git", "describe", "--tags", "--always"], capture_output=True)
                version = result.stdout.strip()
                return version
            except subprocess.CalledProcessError:
                return "unknown"
                
    def build_package(self):
        """构建Python包（跳过UI）"""
        self.print_step("构建", "Python包（跳过UI）")
        
        try:
            # 设置环境变量，跳过UI构建
            env = os.environ.copy()
            env["NO_WEB_UI"] = "1"
            
            # 构建源码分发
            self.run_command([sys.executable, "setup.py", "sdist"], env=env)
            
            # 检查构建结果
            dist_files = list(self.dist_path.glob("*.tar.gz"))
            if dist_files:
                package_file = dist_files[0]
                self.print_success(f"包构建成功: {package_file.name}")
                return package_file
            else:
                self.print_error("包构建失败，未找到tar.gz文件")
                return None
                
        except subprocess.CalledProcessError as e:
            self.print_error(f"包构建失败: {e}")
            return None
            
    def upload_to_private_repo(self, package_file):
        """上传到私有仓库"""
        self.print_step("上传", "到私有仓库")
        
        try:
            cmd = [
                sys.executable, "-m", "twine", "upload",
                "--repository-url", self.private_repo_url,
                "--username", self.username,
                "--password", self.password,
                str(package_file)
            ]
            
            self.run_command(cmd)
            self.print_success("上传成功")
            return True
            
        except subprocess.CalledProcessError as e:
            self.print_error(f"上传失败: {e}")
            return False
            
    def show_summary(self, package_file, version):
        """显示总结信息"""
        self.print_step("完成", "构建上传总结")
        
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 快速构建上传完成！{Colors.ENDC}")
        print(f"\n{Colors.OKBLUE}📦 包文件: {Colors.ENDC}{package_file.name}")
        print(f"{Colors.OKBLUE}🏷️  版本: {Colors.ENDC}{version}")
        print(f"{Colors.OKBLUE}📊 大小: {Colors.ENDC}{package_file.stat().st_size / 1024 / 1024:.1f} MB")
        print(f"{Colors.OKBLUE}🌐 私有仓库: {Colors.ENDC}{self.private_repo_url}")
        print(f"{Colors.OKBLUE}⚠️  注意: {Colors.ENDC}此版本跳过UI构建")
        
        print(f"\n{Colors.OKCYAN}📥 安装命令:{Colors.ENDC}")
        print(f"pip3 install --extra-index-url http://{self.username}:{self.password}@192.2.123.34:8081/simple/ --trusted-host 192.2.123.34 xinference=={version}")
        
        print(f"\n{Colors.OKCYAN}🔗 仓库地址:{Colors.ENDC}")
        print(f"http://192.2.123.34:8081/simple/")
        
    def run(self, args):
        """主运行函数"""
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("=" * 60)
        print("⚡ Xinference 快速构建上传工具 (Windows友好版)")
        print("=" * 60)
        print(f"{Colors.ENDC}")
        
        start_time = time.time()
        
        try:
            # 1. 检查前置条件
            if not self.check_prerequisites():
                return False
                
            # 2. 清理构建文件
            if args.clean:
                self.clean_build()
                
            # 3. 构建Python包（跳过UI）
            package_file = self.build_package()
            if not package_file:
                return False
                
            # 4. 获取版本
            version = self.get_version()
            
            # 5. 上传到私有仓库
            if not args.skip_upload:
                if not self.upload_to_private_repo(package_file):
                    return False
            else:
                self.print_step("跳过", "上传")
                
            # 6. 显示总结
            self.show_summary(package_file, version)
            
            elapsed_time = time.time() - start_time
            print(f"\n{Colors.OKGREEN}⏱️  总耗时: {elapsed_time:.1f}秒{Colors.ENDC}")
            
            return True
            
        except KeyboardInterrupt:
            self.print_error("用户中断操作")
            return False
        except Exception as e:
            self.print_error(f"发生未知错误: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Xinference 快速构建上传工具 (Windows友好版)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python quick_build.py                    # 快速构建上传（跳过UI）
  python quick_build.py --clean           # 清理后构建上传
  python quick_build.py --skip-upload     # 只构建不上传
        """
    )
    
    parser.add_argument("--clean", action="store_true", help="清理构建文件")
    parser.add_argument("--skip-upload", action="store_true", help="跳过上传")
    
    args = parser.parse_args()
    
    builder = QuickBuilder()
    success = builder.run(args)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
