#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统工具集
功能：系统信息、进程管理、定时任务
"""

import os
import sys
import platform
import psutil
import argparse
import subprocess
from datetime import datetime
import json


class SystemTools:
    """系统工具集"""
    
    def __init__(self):
        self.system_info = self._get_system_info()
    
    def _get_system_info(self):
        """获取系统信息"""
        return {
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
        }
    
    def get_system_info(self):
        """打印系统信息"""
        info = {
            '操作系统': f"{self.system_info['system']} {self.system_info['release']}",
            '主机名': self.system_info['node'],
            '架构': self.system_info['machine'],
            '处理器': self.system_info['processor'] or '未知',
            'Python版本': self.system_info['python_version'],
        }
        
        print("\n" + "="*50)
        print("系统信息")
        print("="*50)
        for key, value in info.items():
            print(f"  {key}: {value}")
        print("="*50)
        
        return info
    
    def get_cpu_info(self):
        """获取CPU信息"""
        info = {
            '物理核心': psutil.cpu_count(logical=False),
            '逻辑核心': psutil.cpu_count(logical=True),
            'CPU使用率': f"{psutil.cpu_percent(interval=1)}%",
            'CPU频率': f"{psutil.cpu_freq().current:.0f} MHz" if psutil.cpu_freq() else '未知',
        }
        
        print("\n" + "="*50)
        print("CPU信息")
        print("="*50)
        for key, value in info.items():
            print(f"  {key}: {value}")
        print("="*50)
        
        return info
    
    def get_memory_info(self):
        """获取内存信息"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        info = {
            '总内存': self._format_size(mem.total),
            '已用内存': self._format_size(mem.used),
            '可用内存': self._format_size(mem.available),
            '内存使用率': f"{mem.percent}%",
            '交换分区总量': self._format_size(swap.total),
            '交换分区使用': self._format_size(swap.used),
        }
        
        print("\n" + "="*50)
        print("内存信息")
        print("="*50)
        for key, value in info.items():
            print(f"  {key}: {value}")
        print("="*50)
        
        return info
    
    def get_disk_info(self):
        """获取磁盘信息"""
        print("\n" + "="*50)
        print("磁盘信息")
        print("="*50)
        
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                info = {
                    '挂载点': partition.mountpoint,
                    '文件系统': partition.fstype,
                    '总容量': self._format_size(usage.total),
                    '已用': self._format_size(usage.used),
                    '可用': self._format_size(usage.free),
                    '使用率': f"{usage.percent}%",
                }
                disks.append(info)
                
                print(f"\n  [{partition.mountpoint}]")
                for key, value in info.items():
                    if key != '挂载点':
                        print(f"    {key}: {value}")
            except PermissionError:
                continue
        
        print("\n" + "="*50)
        return disks
    
    def get_network_info(self):
        """获取网络信息"""
        print("\n" + "="*50)
        print("网络信息")
        print("="*50)
        
        # 网络接口
        interfaces = psutil.net_if_addrs()
        
        for name, addrs in interfaces.items():
            print(f"\n  [{name}]")
            for addr in addrs:
                if addr.family == 2:  # IPv4
                    print(f"    IPv4: {addr.address}")
                elif addr.family == 23:  # IPv6
                    print(f"    IPv6: {addr.address[:30]}...")
        
        # 网络统计
        net_io = psutil.net_io_counters()
        print(f"\n  网络统计:")
        print(f"    发送: {self._format_size(net_io.bytes_sent)}")
        print(f"    接收: {self._format_size(net_io.bytes_recv)}")
        
        print("\n" + "="*50)
    
    def list_processes(self, sort_by='memory', top=10):
        """
        列出进程
        
        Args:
            sort_by: 排序方式 (memory/cpu/name)
            top: 显示数量
        """
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'memory': pinfo['memory_info'].rss if pinfo['memory_info'] else 0,
                    'cpu': pinfo['cpu_percent'] or 0,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # 排序
        if sort_by == 'memory':
            processes.sort(key=lambda x: x['memory'], reverse=True)
        elif sort_by == 'cpu':
            processes.sort(key=lambda x: x['cpu'], reverse=True)
        else:
            processes.sort(key=lambda x: x['name'])
        
        print(f"\n{'='*70}")
        print(f"进程列表 (按{sort_by}排序，前{top}个)")
        print(f"{'='*70}")
        print(f"{'PID':<10} {'名称':<30} {'内存':<15} {'CPU':<10}")
        print(f"{'-'*70}")
        
        for p in processes[:top]:
            print(f"{p['pid']:<10} {p['name'][:28]:<30} {self._format_size(p['memory']):<15} {p['cpu']:.1f}%")
        
        print(f"{'='*70}")
    
    def kill_process(self, pid):
        """终止进程"""
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            proc.terminate()
            print(f"[成功] 已终止进程: {name} (PID: {pid})")
        except psutil.NoSuchProcess:
            print(f"[错误] 进程不存在: {pid}")
        except psutil.AccessDenied:
            print(f"[错误] 权限不足，无法终止进程: {pid}")
    
    def get_env_vars(self, filter_str=None):
        """获取环境变量"""
        print("\n" + "="*50)
        print("环境变量")
        print("="*50)
        
        for key, value in os.environ.items():
            if filter_str and filter_str.lower() not in key.lower():
                continue
            print(f"  {key}: {value[:50]}{'...' if len(value) > 50 else ''}")
        
        print("="*50)
    
    def run_command(self, command, timeout=60):
        """运行命令"""
        print(f"\n[执行] {command}")
        print("-"*50)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"[错误] {result.stderr}")
            
            return result.returncode
        except subprocess.TimeoutExpired:
            print(f"[错误] 命令执行超时 ({timeout}秒)")
            return -1
    
    def _format_size(self, size):
        """格式化大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"


def main():
    parser = argparse.ArgumentParser(description='系统工具集')
    parser.add_argument('command', choices=['info', 'cpu', 'memory', 'disk', 
                                            'network', 'process', 'kill', 'env', 'run'],
                       help='操作命令')
    parser.add_argument('--sort', choices=['memory', 'cpu', 'name'], 
                       default='memory', help='进程排序方式')
    parser.add_argument('--top', type=int, default=10, help='显示数量')
    parser.add_argument('--pid', type=int, help='进程PID')
    parser.add_argument('--filter', help='过滤字符串')
    parser.add_argument('--cmd', help='要执行的命令')
    parser.add_argument('--timeout', type=int, default=60, help='命令超时时间')
    
    args = parser.parse_args()
    
    tools = SystemTools()
    
    if args.command == 'info':
        tools.get_system_info()
    elif args.command == 'cpu':
        tools.get_cpu_info()
    elif args.command == 'memory':
        tools.get_memory_info()
    elif args.command == 'disk':
        tools.get_disk_info()
    elif args.command == 'network':
        tools.get_network_info()
    elif args.command == 'process':
        tools.list_processes(args.sort, args.top)
    elif args.command == 'kill':
        if args.pid:
            tools.kill_process(args.pid)
        else:
            print("错误: 需要指定 --pid")
    elif args.command == 'env':
        tools.get_env_vars(args.filter)
    elif args.command == 'run':
        if args.cmd:
            tools.run_command(args.cmd, args.timeout)
        else:
            print("错误: 需要指定 --cmd")


if __name__ == '__main__':
    main()
