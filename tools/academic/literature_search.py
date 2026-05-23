#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文献检索工具
功能：多源学术文献搜索、元数据提取、引用格式生成、文献管理
"""

import requests
import json
import re
import argparse
import time
from datetime import datetime
from urllib.parse import quote, urljoin


class LiteratureSearcher:
    """学术文献检索器"""

    def __init__(self, timeout=15):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    # ---- Google Scholar 搜索 ----
    def search_scholar(self, query, count=10):
        """通过 Google Scholar 搜索文献"""
        results = []
        base = 'https://scholar.google.com/scholar'

        params = {
            'q': query,
            'hl': 'zh-CN',
            'num': min(count, 20)
        }

        try:
            resp = self.session.get(base, params=params, timeout=self.timeout)
            resp.raise_for_status()

            # 简单解析 HTML
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, 'html.parser')

            for item in soup.select('.gs_r.gs_or.gs_scl'):
                title_tag = item.select_one('.gs_rt a')
                if not title_tag:
                    title_tag = item.select_one('.gs_rt')

                author_info = item.select_one('.gs_a')
                snippet = item.select_one('.gs_rs')
                link_tag = item.select_one('.gs_rt a')

                result = {
                    'title': title_tag.get_text(strip=True) if title_tag else '',
                    'authors': author_info.get_text(strip=True) if author_info else '',
                    'snippet': snippet.get_text(strip=True) if snippet else '',
                    'url': link_tag['href'] if link_tag and link_tag.has_attr('href') else '',
                    'source': 'Google Scholar'
                }
                results.append(result)

        except Exception as e:
            print(f"[错误] Scholar 搜索失败: {e}")

        return results

    # ---- CrossRef (DOI) 搜索 ----
    def search_crossref(self, query, count=10):
        """通过 CrossRef API 搜索文献"""
        results = []
        base = 'https://api.crossref.org/works'

        params = {
            'query': query,
            'rows': min(count, 20),
            'select': 'DOI,title,author,published-print,abstract,URL,type'
        }

        try:
            resp = self.session.get(base, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()

            for item in data.get('message', {}).get('items', []):
                authors = ', '.join(
                    [f"{a.get('given', '')} {a.get('family', '')}".strip()
                     for a in item.get('author', [])[:5]]
                )
                year = ''
                date = item.get('published-print', {}).get('date-parts', [[]])[0]
                if date:
                    year = str(date[0]) if date else ''

                results.append({
                    'title': item.get('title', [''])[0],
                    'authors': authors,
                    'year': year,
                    'doi': item.get('DOI', ''),
                    'url': item.get('URL', ''),
                    'type': item.get('type', ''),
                    'abstract': item.get('abstract', ''),
                    'source': 'CrossRef'
                })

        except Exception as e:
            print(f"[错误] CrossRef 搜索失败: {e}")

        return results

    # ---- Semantic Scholar 搜索 ----
    def search_semantic(self, query, count=10):
        """通过 Semantic Scholar API 搜索文献"""
        results = []
        base = 'https://api.semanticscholar.org/graph/v1/paper/search'

        params = {
            'query': query,
            'limit': min(count, 20),
            'fields': 'title,authors,year,abstract,url,externalIds,citationCount'
        }

        try:
            resp = self.session.get(base, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()

            for item in data.get('data', []):
                authors = ', '.join(
                    [a.get('name', '') for a in item.get('authors', [])[:5]]
                )
                ext_ids = item.get('externalIds', {}) or {}

                results.append({
                    'title': item.get('title', ''),
                    'authors': authors,
                    'year': str(item.get('year', '')),
                    'abstract': item.get('abstract', ''),
                    'url': item.get('url', ''),
                    'doi': ext_ids.get('DOI', ''),
                    'arxiv': ext_ids.get('ArXiv', ''),
                    'citations': item.get('citationCount', 0),
                    'source': 'Semantic Scholar'
                })

        except Exception as e:
            print(f"[错误] Semantic Scholar 搜索失败: {e}")

        return results

    # ---- 综合搜索 ----
    def search(self, query, count=10, sources=None):
        """多源综合搜索"""
        sources = sources or ['crossref', 'semantic']
        all_results = []

        print(f"[搜索] 关键词: {query}")
        print(f"[搜索] 来源: {', '.join(sources)}")

        if 'scholar' in sources:
            print("[信息] 正在搜索 Google Scholar...")
            all_results.extend(self.search_scholar(query, count))
            time.sleep(2)

        if 'crossref' in sources:
            print("[信息] 正在搜索 CrossRef...")
            all_results.extend(self.search_crossref(query, count))

        if 'semantic' in sources:
            print("[信息] 正在搜索 Semantic Scholar...")
            all_results.extend(self.search_semantic(query, count))

        print(f"[成功] 共找到 {len(all_results)} 条结果")
        return all_results

    # ---- 生成引用格式 ----
    @staticmethod
    def generate_citation(item, style='apa'):
        """生成引用格式"""
        title = item.get('title', 'Unknown')
        authors = item.get('authors', 'Unknown')
        year = item.get('year', 'n.d.')
        url = item.get('url', '')
        doi = item.get('doi', '')

        if style == 'apa':
            citation = f"{authors} ({year}). {title}."
            if doi:
                citation += f" https://doi.org/{doi}"
            elif url:
                citation += f" {url}"
        elif style == 'mla':
            citation = f'{authors}. "{title}." ({year}).'
            if doi:
                citation += f" https://doi.org/{doi}"
        elif style == 'bibtex':
            key = re.sub(r'[^a-zA-Z]', '', title)[:10].lower()
            citation = (
                f"@article{{{key},\n"
                f"  title = {{{title}}},\n"
                f"  author = {{{authors}}},\n"
                f"  year = {{{year}}},\n"
            )
            if doi:
                citation += f"  doi = {{{doi}}},\n"
            citation += "}"
        else:
            citation = f"{authors}. {title}. {year}."

        return citation

    # ---- 保存结果 ----
    def save_results(self, results, output_path, format='json', citation_style='apa'):
        """保存搜索结果"""
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        elif format == 'txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, r in enumerate(results, 1):
                    f.write(f"[{i}] {r.get('title', '')}\n")
                    f.write(f"    作者: {r.get('authors', '')}\n")
                    f.write(f"    年份: {r.get('year', '')}\n")
                    f.write(f"    来源: {r.get('source', '')}\n")
                    if r.get('url'):
                        f.write(f"    链接: {r['url']}\n")
                    f.write("\n")
        elif format == 'citations':
            with open(output_path, 'w', encoding='utf-8') as f:
                for r in results:
                    f.write(self.generate_citation(r, citation_style) + '\n\n')

        print(f"[成功] 已保存到: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='文献检索工具')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('-n', '--count', type=int, default=10, help='每源结果数')
    parser.add_argument('-s', '--sources', nargs='+',
                       choices=['scholar', 'crossref', 'semantic'],
                       default=['crossref', 'semantic'], help='搜索来源')
    parser.add_argument('-o', '--output', default='results.json', help='输出文件')
    parser.add_argument('-f', '--format', choices=['json', 'txt', 'citations'],
                       default='json', help='输出格式')
    parser.add_argument('-c', '--citation-style', choices=['apa', 'mla', 'bibtex'],
                       default='apa', help='引用格式')

    args = parser.parse_args()

    searcher = LiteratureSearcher()
    results = searcher.search(args.query, args.count, args.sources)

    if results:
        searcher.save_results(results, args.output, args.format, args.citation_style)

        # 打印摘要
        print(f"\n{'='*60}")
        for i, r in enumerate(results[:5], 1):
            print(f"[{i}] {r.get('title', '')[:60]}")
            print(f"    {r.get('authors', '')[:50]} ({r.get('year', '')})")
        if len(results) > 5:
            print(f"    ... 还有 {len(results) - 5} 条结果")
        print(f"{'='*60}")


if __name__ == '__main__':
    main()
