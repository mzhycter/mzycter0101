#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资源下载器
功能：下载图片、视频、文档等各类资源，支持批量下载、断点续传
"""

import requests
import os
import re
import argparse
from urllib.parse import urlparse, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time


class ResourceDownloader:
    """资源下载器"""
    
    def __init__(self, max_workers=5, timeout=30, retry=3):
        self.max_workers = max_workers
        self.timeout = timeout
        self.retry = retry
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.download_stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
    
    def get_filename(self, url, default_name='download'):
        """从URL提取文件名"""
        parsed = urlparse(url)
        path = unquote(parsed.path)
        filename = os.path.basename(path)
        
        if not filename or '.' not in filename:
            filename = f"{default_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 清理非法字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return filename
    
    def get_file_size(self, url):
        """获取文件大小"""
        try:
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            size = int(response.headers.get('content-length', 0))
            return size
        except:
            return 0
    
    def format_size(self, size):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    def download_file(self, url, save_dir='downloads', filename=None, overwrite=False):
        """
        下载单个文件
        
        Args:
            url: 资源URL
            save_dir: 保存目录
            filename: 文件名，None则自动提取
            overwrite: 是否覆盖已存在文件
        
        Returns:
            下载结果字典
        """
        result = {
            'url': url,
            'success': False,
            'filepath': None,
            'size': 0,
            'error': None
        }
        
        try:
            # 创建保存目录
            os.makedirs(save_dir, exist_ok=True)
            
            # 确定文件名
            if not filename:
                filename = self.get_filename(url)
            
            filepath = os.path.join(save_dir, filename)
            result['filepath'] = filepath
            
            # 检查文件是否存在
            if os.path.exists(filepath) and not overwrite:
                result['success'] = True
                result['size'] = os.path.getsize(filepath)
                result['error'] = '文件已存在，跳过下载'
                print(f"[跳过] {filename} 已存在")
                return result
            
            # 获取文件大小
            total_size = self.get_file_size(url)
            
            # 下载文件
            print(f"[下载] {filename} ({self.format_size(total_size)})")
            
            for attempt in range(self.retry):
                try:
                    response = self.session.get(url, timeout=self.timeout, stream=True)
                    response.raise_for_status()
                    
                    # 断点续传
                    resume_pos = 0
                    if os.path.exists(filepath):
                        resume_pos = os.path.getsize(filepath)
                        if resume_pos < total_size:
                            headers = {'Range': f'bytes={resume_pos}-'}
                            response = self.session.get(url, headers=headers, stream=True)
                    
                    mode = 'ab' if resume_pos > 0 else 'wb'
                    downloaded = resume_pos
                    
                    with open(filepath, mode) as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                
                                # 显示进度
                                if total_size > 0:
                                    percent = (downloaded / total_size) * 100
                                    print(f"\r[进度] {percent:.1f}% ({self.format_size(downloaded)}/{self.format_size(total_size)})", end='')
                    
                    print()  # 换行
                    result['success'] = True
                    result['size'] = os.path.getsize(filepath)
                    print(f"[成功] {filename} 下载完成")
                    break
                    
                except requests.RequestException as e:
                    if attempt < self.retry - 1:
                        print(f"[重试] 第 {attempt + 2} 次尝试...")
                        time.sleep(2)
                    else:
                        raise e
                        
        except Exception as e:
            result['error'] = str(e)
            print(f"[失败] {url}: {e}")
        
        return result
    
    def download_batch(self, urls, save_dir='downloads', overwrite=False):
        """
        批量下载文件
        
        Args:
            urls: URL列表
            save_dir: 保存目录
            overwrite: 是否覆盖
        
        Returns:
            下载结果列表
        """
        self.download_stats = {'total': len(urls), 'success': 0, 'failed': 0, 'skipped': 0}
        results = []
        
        print(f"\n{'='*50}")
        print(f"批量下载任务开始")
        print(f"总文件数: {len(urls)}")
        print(f"保存目录: {save_dir}")
        print(f"{'='*50}\n")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.download_file, url, save_dir, None, overwrite): url
                for url in urls
            }
            
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                
                if result['success']:
                    if '已存在' in str(result.get('error', '')):
                        self.download_stats['skipped'] += 1
                    else:
                        self.download_stats['success'] += 1
                else:
                    self.download_stats['failed'] += 1
        
        # 打印统计
        print(f"\n{'='*50}")
        print("下载完成统计:")
        print(f"  成功: {self.download_stats['success']}")
        print(f"  失败: {self.download_stats['failed']}")
        print(f"  跳过: {self.download_stats['skipped']}")
        print(f"{'='*50}\n")
        
        return results
    
    def download_images_from_html(self, html_content, base_url, save_dir='downloads/images'):
        """从HTML内容中提取并下载所有图片"""
        from bs4 import BeautifulSoup
        from urllib.parse import urljoin
        
        soup = BeautifulSoup(html_content, 'html.parser')
        img_urls = []
        
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src:
                full_url = urljoin(base_url, src)
                img_urls.append(full_url)
        
        return self.download_batch(img_urls, save_dir)


def main():
    parser = argparse.ArgumentParser(description='资源下载器')
    parser.add_argument('urls', nargs='+', help='资源URL（支持多个）')
    parser.add_argument('-o', '--output', default='downloads', help='保存目录')
    parser.add_argument('-w', '--workers', type=int, default=5, help='并发下载数')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已存在文件')
    
    args = parser.parse_args()
    
    downloader = ResourceDownloader(max_workers=args.workers)
    
    if len(args.urls) == 1:
        downloader.download_file(args.urls[0], args.output, overwrite=args.overwrite)
    else:
        downloader.download_batch(args.urls, args.output, overwrite=args.overwrite)


if __name__ == '__main__':
    main()
