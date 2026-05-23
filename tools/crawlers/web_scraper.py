#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页内容抓取工具
功能：抓取网页内容、提取文本、保存为多种格式
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from urllib.parse import urljoin, urlparse
import argparse
import re


class WebScraper:
    """网页内容抓取器"""
    
    def __init__(self, timeout=10, headers=None):
        self.timeout = timeout
        self.session = requests.Session()
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.session.headers.update(self.headers)
    
    def fetch_page(self, url, encoding=None):
        """
        获取网页内容
        
        Args:
            url: 目标URL
            encoding: 指定编码，None则自动检测
        
        Returns:
            BeautifulSoup对象
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            if encoding:
                response.encoding = encoding
            else:
                response.encoding = response.apparent_encoding
            
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"[错误] 获取页面失败: {e}")
            return None
    
    def extract_text(self, soup, selector=None, remove_scripts=True):
        """
        提取页面文本
        
        Args:
            soup: BeautifulSoup对象
            selector: CSS选择器，None则提取全部
            remove_scripts: 是否移除脚本和样式
        
        Returns:
            提取的文本
        """
        if not soup:
            return ""
        
        # 移除脚本和样式
        if remove_scripts:
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
        
        if selector:
            elements = soup.select(selector)
            text = '\n'.join([elem.get_text(strip=True) for elem in elements])
        else:
            text = soup.get_text(separator='\n', strip=True)
        
        # 清理多余空白
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    
    def extract_links(self, soup, base_url, selector='a[href]'):
        """
        提取页面链接
        
        Args:
            soup: BeautifulSoup对象
            base_url: 基础URL用于处理相对路径
            selector: 链接选择器
        
        Returns:
            链接列表 [{url, text, title}]
        """
        if not soup:
            return []
        
        links = []
        for a in soup.select(selector):
            href = a.get('href', '')
            if href and not href.startswith(('#', 'javascript:', 'mailto:')):
                full_url = urljoin(base_url, href)
                links.append({
                    'url': full_url,
                    'text': a.get_text(strip=True),
                    'title': a.get('title', '')
                })
        
        return links
    
    def extract_images(self, soup, base_url, selector='img[src]'):
        """
        提取页面图片
        
        Args:
            soup: BeautifulSoup对象
            base_url: 基础URL
            selector: 图片选择器
        
        Returns:
            图片列表 [{url, alt, title}]
        """
        if not soup:
            return []
        
        images = []
        for img in soup.select(selector):
            src = img.get('src', '')
            if src:
                full_url = urljoin(base_url, src)
                images.append({
                    'url': full_url,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
        
        return images
    
    def extract_metadata(self, soup):
        """
        提取页面元数据
        
        Args:
            soup: BeautifulSoup对象
        
        Returns:
            元数据字典
        """
        if not soup:
            return {}
        
        metadata = {
            'title': soup.title.string if soup.title else '',
            'description': '',
            'keywords': [],
            'author': '',
            'og_image': ''
        }
        
        # 提取meta标签
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            prop = meta.get('property', '').lower()
            content = meta.get('content', '')
            
            if name == 'description' or prop == 'og:description':
                metadata['description'] = content
            elif name == 'keywords':
                metadata['keywords'] = [k.strip() for k in content.split(',')]
            elif name == 'author':
                metadata['author'] = content
            elif prop == 'og:image':
                metadata['og_image'] = content
        
        return metadata
    
    def scrape(self, url, extract_all=True, selector=None):
        """
        完整抓取页面
        
        Args:
            url: 目标URL
            extract_all: 是否提取全部内容
            selector: CSS选择器
        
        Returns:
            抓取结果字典
        """
        print(f"[信息] 正在抓取: {url}")
        
        soup = self.fetch_page(url)
        if not soup:
            return None
        
        result = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'metadata': self.extract_metadata(soup),
            'text': self.extract_text(soup, selector),
        }
        
        if extract_all:
            result['links'] = self.extract_links(soup, url)
            result['images'] = self.extract_images(soup, url)
        
        print(f"[成功] 抓取完成，文本长度: {len(result['text'])} 字符")
        return result
    
    def save_result(self, result, output_path, format='json'):
        """
        保存抓取结果
        
        Args:
            result: 抓取结果
            output_path: 输出路径
            format: 格式 (json/txt/markdown)
        """
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        elif format == 'txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"URL: {result['url']}\n")
                f.write(f"标题: {result['metadata']['title']}\n")
                f.write(f"时间: {result['timestamp']}\n")
                f.write("\n" + "="*50 + "\n\n")
                f.write(result['text'])
        elif format == 'markdown':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# {result['metadata']['title']}\n\n")
                f.write(f"> 来源: {result['url']}\n")
                f.write(f"> 时间: {result['timestamp']}\n\n")
                if result['metadata']['description']:
                    f.write(f"**摘要**: {result['metadata']['description']}\n\n")
                f.write("## 正文\n\n")
                f.write(result['text'])
        
        print(f"[成功] 已保存到: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='网页内容抓取工具')
    parser.add_argument('url', help='目标URL')
    parser.add_argument('-o', '--output', default='output', help='输出文件名（不含扩展名）')
    parser.add_argument('-f', '--format', choices=['json', 'txt', 'markdown'], default='markdown', help='输出格式')
    parser.add_argument('-s', '--selector', help='CSS选择器，仅提取指定区域')
    parser.add_argument('--no-extract-all', action='store_true', help='不提取链接和图片')
    
    args = parser.parse_args()
    
    scraper = WebScraper()
    result = scraper.scrape(args.url, extract_all=not args.no_extract_all, selector=args.selector)
    
    if result:
        ext = {'json': '.json', 'txt': '.txt', 'markdown': '.md'}[args.format]
        output_path = f"{args.output}{ext}"
        scraper.save_result(result, output_path, args.format)


if __name__ == '__main__':
    main()
