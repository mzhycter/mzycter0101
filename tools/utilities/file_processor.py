#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件批量处理工具
功能：批量重命名、格式转换、文件整理
"""

import os
import re
import shutil
import argparse
from datetime import datetime
from pathlib import Path
import json


class FileBatchProcessor:
    """文件批量处理器"""
    
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.operations = []
    
    def log(self, message):
        """记录操作"""
        prefix = "[预览] " if self.dry_run else "[执行] "
        print(f"{prefix}{message}")
        self.operations.append(message)
    
    def batch_rename(self, directory, pattern, replacement, recursive=False):
        """
        批量重命名文件
        
        Args:
            directory: 目录路径
            pattern: 正则表达式模式
            replacement: 替换字符串
            recursive: 是否递归处理子目录
        """
        directory = Path(directory)
        if not directory.exists():
            print(f"[错误] 目录不存在: {directory}")
            return
        
        files = directory.rglob('*') if recursive else directory.glob('*')
        
        for file_path in files:
            if file_path.is_file():
                old_name = file_path.name
                new_name = re.sub(pattern, replacement, old_name)
                
                if new_name != old_name:
                    new_path = file_path.parent / new_name
                    
                    self.log(f"重命名: {old_name} -> {new_name}")
                    
                    if not self.dry_run:
                        file_path.rename(new_path)
    
    def batch_rename_with_template(self, directory, template, start_num=1, 
                                   ext_filter=None, recursive=False):
        """
        使用模板批量重命名
        
        Args:
            directory: 目录路径
            template: 命名模板 (支持 {num}, {date}, {name})
            start_num: 起始编号
            ext_filter: 扩展名过滤 (如 '.jpg')
            recursive: 是否递归
        """
        directory = Path(directory)
        files = directory.rglob('*') if recursive else directory.glob('*')
        files = [f for f in files if f.is_file()]
        
        if ext_filter:
            files = [f for f in files if f.suffix.lower() == ext_filter.lower()]
        
        files.sort(key=lambda x: x.name)
        
        for i, file_path in enumerate(files, start=start_num):
            old_name = file_path.name
            new_name = template.format(
                num=i,
                date=datetime.now().strftime('%Y%m%d'),
                name=file_path.stem,
                ext=file_path.suffix
            )
            
            if not new_name.endswith(file_path.suffix):
                new_name += file_path.suffix
            
            if new_name != old_name:
                new_path = file_path.parent / new_name
                self.log(f"重命名: {old_name} -> {new_name}")
                
                if not self.dry_run:
                    file_path.rename(new_path)
    
    def organize_by_extension(self, directory, output_dir=None):
        """
        按扩展名整理文件
        
        Args:
            directory: 源目录
            output_dir: 输出目录，None则在源目录下创建
        """
        directory = Path(directory)
        output_dir = Path(output_dir) if output_dir else directory
        
        for file_path in directory.glob('*'):
            if file_path.is_file():
                ext = file_path.suffix.lower() or 'no_extension'
                ext = ext.lstrip('.')
                
                target_dir = output_dir / ext
                target_path = target_dir / file_path.name
                
                self.log(f"移动: {file_path.name} -> {ext}/")
                
                if not self.dry_run:
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(file_path), str(target_path))
    
    def organize_by_date(self, directory, output_dir=None):
        """
        按日期整理文件
        
        Args:
            directory: 源目录
            output_dir: 输出目录
        """
        directory = Path(directory)
        output_dir = Path(output_dir) if output_dir else directory
        
        for file_path in directory.glob('*'):
            if file_path.is_file():
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                date_dir = mtime.strftime('%Y-%m')
                
                target_dir = output_dir / date_dir
                target_path = target_dir / file_path.name
                
                self.log(f"移动: {file_path.name} -> {date_dir}/")
                
                if not self.dry_run:
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(file_path), str(target_path))
    
    def find_duplicates(self, directory, method='name', delete=False):
        """
        查找重复文件
        
        Args:
            directory: 目录路径
            method: 检测方法 (name/size/content)
            delete: 是否删除重复文件
        """
        directory = Path(directory)
        files = list(directory.rglob('*'))
        files = [f for f in files if f.is_file()]
        
        seen = {}
        duplicates = []
        
        for file_path in files:
            if method == 'name':
                key = file_path.name
            elif method == 'size':
                key = file_path.stat().st_size
            elif method == 'content':
                key = self._get_file_hash(file_path)
            else:
                continue
            
            if key in seen:
                duplicates.append((file_path, seen[key]))
                self.log(f"重复: {file_path.name} (与 {seen[key]} 相同)")
                
                if delete and not self.dry_run:
                    file_path.unlink()
            else:
                seen[key] = file_path
        
        return duplicates
    
    def _get_file_hash(self, file_path, chunk_size=8192):
        """计算文件哈希"""
        import hashlib
        hasher = hashlib.md5()
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        
        return hasher.hexdigest()
    
    def clean_empty_dirs(self, directory):
        """清理空目录"""
        directory = Path(directory)
        removed = []
        
        for dir_path in sorted(directory.rglob('*'), reverse=True):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                self.log(f"删除空目录: {dir_path}")
                removed.append(dir_path)
                
                if not self.dry_run:
                    dir_path.rmdir()
        
        return removed


def main():
    parser = argparse.ArgumentParser(description='文件批量处理工具')
    parser.add_argument('command', choices=['rename', 'template', 'organize-ext', 
                                            'organize-date', 'duplicates', 'clean'],
                       help='操作命令')
    parser.add_argument('-d', '--directory', required=True, help='目标目录')
    parser.add_argument('-p', '--pattern', help='正则表达式模式')
    parser.add_argument('-r', '--replacement', help='替换字符串')
    parser.add_argument('-t', '--template', help='命名模板')
    parser.add_argument('-e', '--extension', help='扩展名过滤')
    parser.add_argument('-m', '--method', choices=['name', 'size', 'content'],
                       default='name', help='重复检测方法')
    parser.add_argument('--recursive', action='store_true', help='递归处理')
    parser.add_argument('--dry-run', action='store_true', help='预览模式')
    parser.add_argument('--delete', action='store_true', help='删除重复文件')
    parser.add_argument('--start', type=int, default=1, help='起始编号')
    
    args = parser.parse_args()
    
    processor = FileBatchProcessor(dry_run=args.dry_run)
    
    if args.command == 'rename':
        if not args.pattern or not args.replacement:
            print("错误: rename 需要 -p 和 -r 参数")
            return
        processor.batch_rename(args.directory, args.pattern, args.replacement, args.recursive)
    
    elif args.command == 'template':
        if not args.template:
            print("错误: template 需要 -t 参数")
            return
        processor.batch_rename_with_template(
            args.directory, args.template, args.start, args.extension, args.recursive
        )
    
    elif args.command == 'organize-ext':
        processor.organize_by_extension(args.directory)
    
    elif args.command == 'organize-date':
        processor.organize_by_date(args.directory)
    
    elif args.command == 'duplicates':
        processor.find_duplicates(args.directory, args.method, args.delete)
    
    elif args.command == 'clean':
        processor.clean_empty_dirs(args.directory)


if __name__ == '__main__':
    main()
