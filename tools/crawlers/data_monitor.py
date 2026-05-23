#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据监控工具
功能：监控网页变化、价格监控、内容更新提醒
"""

import requests
import json
import os
import hashlib
import time
import argparse
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


class DataMonitor:
    """数据监控器"""
    
    def __init__(self, config_file='monitor_config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def load_config(self):
        """加载配置"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'tasks': [], 'history': {}}
    
    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def add_task(self, name, url, selector=None, monitor_type='content', 
                 check_interval=300, notify_on='change'):
        """
        添加监控任务
        
        Args:
            name: 任务名称
            url: 监控URL
            selector: CSS选择器
            monitor_type: 监控类型 (content/price/availability)
            check_interval: 检查间隔（秒）
            notify_on: 通知条件 (change/value_decrease/value_increase)
        """
        task = {
            'id': hashlib.md5(f"{url}{selector}".encode()).hexdigest()[:8],
            'name': name,
            'url': url,
            'selector': selector,
            'type': monitor_type,
            'check_interval': check_interval,
            'notify_on': notify_on,
            'enabled': True,
            'created_at': datetime.now().isoformat()
        }
        
        self.config['tasks'].append(task)
        self.save_config()
        print(f"[成功] 已添加监控任务: {name}")
        return task['id']
    
    def remove_task(self, task_id):
        """移除监控任务"""
        self.config['tasks'] = [t for t in self.config['tasks'] if t['id'] != task_id]
        self.save_config()
        print(f"[成功] 已移除任务: {task_id}")
    
    def list_tasks(self):
        """列出所有任务"""
        print("\n" + "="*60)
        print("监控任务列表")
        print("="*60)
        
        for task in self.config['tasks']:
            status = "✓ 启用" if task['enabled'] else "✗ 禁用"
            print(f"\n[{task['id']}] {task['name']}")
            print(f"    URL: {task['url']}")
            print(f"    类型: {task['type']}")
            print(f"    状态: {status}")
            print(f"    间隔: {task['check_interval']}秒")
        
        if not self.config['tasks']:
            print("\n暂无监控任务")
        
        print("\n" + "="*60)
    
    def fetch_content(self, url, selector=None):
        """获取页面内容"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if selector:
                elements = soup.select(selector)
                content = '\n'.join([e.get_text(strip=True) for e in elements])
            else:
                # 移除脚本和样式
                for tag in soup(['script', 'style', 'nav', 'footer']):
                    tag.decompose()
                content = soup.get_text(separator='\n', strip=True)
            
            return content.strip()
        except Exception as e:
            print(f"[错误] 获取内容失败: {e}")
            return None
    
    def extract_price(self, content):
        """从内容中提取价格"""
        # 匹配各种价格格式
        patterns = [
            r'¥\s*([\d,]+\.?\d*)',  # ¥99.99
            r'￥\s*([\d,]+\.?\d*)',  # ￥99.99
            r'Price:\s*\$?([\d,]+\.?\d*)',  # Price: 99.99
            r'\$\s*([\d,]+\.?\d*)',  # $99.99
            r'([\d,]+\.?\d*)\s*元',  # 99.99元
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                price_str = match.group(1).replace(',', '')
                try:
                    return float(price_str)
                except:
                    continue
        return None
    
    def get_content_hash(self, content):
        """计算内容哈希"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def check_task(self, task):
        """
        检查单个任务
        
        Returns:
            检查结果字典
        """
        result = {
            'task_id': task['id'],
            'task_name': task['name'],
            'timestamp': datetime.now().isoformat(),
            'changed': False,
            'previous': None,
            'current': None,
            'alert': None
        }
        
        # 获取内容
        content = self.fetch_content(task['url'], task['selector'])
        if content is None:
            result['alert'] = '获取内容失败'
            return result
        
        current_hash = self.get_content_hash(content)
        result['current'] = {
            'hash': current_hash,
            'content': content[:500] + '...' if len(content) > 500 else content
        }
        
        # 获取历史记录
        history_key = task['id']
        if history_key in self.config['history']:
            result['previous'] = self.config['history'][history_key]
        
        # 检查变化
        if result['previous']:
            prev_hash = result['previous'].get('hash')
            
            if task['type'] == 'price':
                # 价格监控
                current_price = self.extract_price(content)
                prev_price = result['previous'].get('price')
                
                result['current']['price'] = current_price
                
                if current_price and prev_price:
                    if task['notify_on'] == 'value_decrease' and current_price < prev_price:
                        result['changed'] = True
                        result['alert'] = f"价格下降: {prev_price} -> {current_price}"
                    elif task['notify_on'] == 'value_increase' and current_price > prev_price:
                        result['changed'] = True
                        result['alert'] = f"价格上涨: {prev_price} -> {current_price}"
                    elif task['notify_on'] == 'change' and current_price != prev_price:
                        result['changed'] = True
                        result['alert'] = f"价格变化: {prev_price} -> {current_price}"
            else:
                # 内容监控
                if current_hash != prev_hash:
                    result['changed'] = True
                    result['alert'] = '内容已更新'
        else:
            # 首次检查
            if task['type'] == 'price':
                result['current']['price'] = self.extract_price(content)
            result['alert'] = '首次检查，已记录基准'
        
        # 更新历史
        self.config['history'][history_key] = result['current']
        self.save_config()
        
        return result
    
    def run_once(self):
        """运行一次检查"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始检查...")
        
        alerts = []
        for task in self.config['tasks']:
            if not task['enabled']:
                continue
            
            result = self.check_task(task)
            
            if result['changed']:
                alert_msg = f"[变更] {task['name']}: {result['alert']}"
                print(alert_msg)
                alerts.append(alert_msg)
            else:
                print(f"[正常] {task['name']}")
        
        return alerts
    
    def run_loop(self, interval=None):
        """持续运行监控"""
        print("数据监控已启动，按 Ctrl+C 停止...")
        
        try:
            while True:
                self.run_once()
                
                # 使用最小检查间隔
                min_interval = interval or min(
                    [t['check_interval'] for t in self.config['tasks']] or [300]
                )
                print(f"\n下次检查: {min_interval}秒后...")
                time.sleep(min_interval)
        except KeyboardInterrupt:
            print("\n监控已停止")


def main():
    parser = argparse.ArgumentParser(description='数据监控工具')
    parser.add_argument('command', choices=['add', 'remove', 'list', 'check', 'run'],
                       help='操作命令')
    parser.add_argument('--name', help='任务名称')
    parser.add_argument('--url', help='监控URL')
    parser.add_argument('--selector', help='CSS选择器')
    parser.add_argument('--type', choices=['content', 'price', 'availability'],
                       default='content', help='监控类型')
    parser.add_argument('--interval', type=int, default=300, help='检查间隔（秒）')
    parser.add_argument('--notify', choices=['change', 'value_decrease', 'value_increase'],
                       default='change', help='通知条件')
    parser.add_argument('--task-id', help='任务ID')
    
    args = parser.parse_args()
    
    monitor = DataMonitor()
    
    if args.command == 'add':
        if not args.url:
            print("错误: 添加任务需要 --url 参数")
            return
        monitor.add_task(
            name=args.name or '未命名任务',
            url=args.url,
            selector=args.selector,
            monitor_type=args.type,
            check_interval=args.interval,
            notify_on=args.notify
        )
    elif args.command == 'remove':
        if args.task_id:
            monitor.remove_task(args.task_id)
        else:
            print("错误: 需要指定 --task-id")
    elif args.command == 'list':
        monitor.list_tasks()
    elif args.command == 'check':
        monitor.run_once()
    elif args.command == 'run':
        monitor.run_loop()


if __name__ == '__main__':
    main()
