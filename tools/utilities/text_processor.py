#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本处理工具
功能：文本清洗、格式转换、编码检测、关键词提取
"""

import re
import os
import argparse
import chardet
from collections import Counter
from datetime import datetime


class TextProcessor:
    """文本处理器"""
    
    def __init__(self):
        self.stats = {}
    
    def detect_encoding(self, file_path):
        """检测文件编码"""
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)
            result = chardet.detect(raw_data)
        return result['encoding']
    
    def read_file(self, file_path, encoding=None):
        """读取文件"""
        if encoding is None:
            encoding = self.detect_encoding(file_path)
        
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            return f.read()
    
    def clean_text(self, text, options=None):
        """
        清洗文本
        
        Args:
            text: 输入文本
            options: 清洗选项字典
        
        Returns:
            清洗后的文本
        """
        options = options or {}
        
        # 移除HTML标签
        if options.get('remove_html', False):
            text = re.sub(r'<[^>]+>', '', text)
        
        # 移除URL
        if options.get('remove_urls', False):
            text = re.sub(r'https?://\S+', '', text)
        
        # 移除邮箱
        if options.get('remove_emails', False):
            text = re.sub(r'\S+@\S+\.\S+', '', text)
        
        # 移除数字
        if options.get('remove_numbers', False):
            text = re.sub(r'\d+', '', text)
        
        # 移除标点符号
        if options.get('remove_punctuation', False):
            text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        
        # 移除多余空白
        if options.get('normalize_whitespace', True):
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # 移除首尾空白
        text = text.strip()
        
        return text
    
    def extract_keywords(self, text, top_n=10, min_length=2):
        """
        简单关键词提取（基于词频）
        
        Args:
            text: 输入文本
            top_n: 返回前N个关键词
            min_length: 最小词长
        
        Returns:
            关键词列表
        """
        # 简单分词（中英文混合）
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text.lower())
        
        # 过滤停用词
        stopwords = {'的', '是', '在', '了', '和', '与', '或', '这', '那', '有', 
                    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                    'to', 'of', 'and', 'in', 'that', 'have', 'it', 'for', 'not'}
        
        words = [w for w in words if w not in stopwords and len(w) >= min_length]
        
        # 统计词频
        word_freq = Counter(words)
        
        return word_freq.most_common(top_n)
    
    def extract_info(self, text):
        """
        提取文本中的信息
        
        Args:
            text: 输入文本
        
        Returns:
            信息字典
        """
        info = {
            'emails': re.findall(r'\S+@\S+\.\S+', text),
            'urls': re.findall(r'https?://\S+', text),
            'phones': re.findall(r'1[3-9]\d{9}', text),  # 中国手机号
            'dates': re.findall(r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?', text),
            'ips': re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text),
        }
        
        return info
    
    def word_count(self, text):
        """
        统计文本信息
        
        Args:
            text: 输入文本
        
        Returns:
            统计字典
        """
        # 字符统计
        char_count = len(text)
        char_count_no_space = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
        
        # 中文统计
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        
        # 英文单词统计
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        
        # 行数统计
        lines = len(text.split('\n'))
        non_empty_lines = len([l for l in text.split('\n') if l.strip()])
        
        # 段落统计
        paragraphs = len([p for p in text.split('\n\n') if p.strip()])
        
        return {
            '总字符数': char_count,
            '字符数(不含空白)': char_count_no_space,
            '中文字符数': chinese_chars,
            '英文单词数': english_words,
            '总行数': lines,
            '非空行数': non_empty_lines,
            '段落数': paragraphs
        }
    
    def convert_case(self, text, case_type):
        """
        大小写转换
        
        Args:
            text: 输入文本
            case_type: 转换类型 (upper/lower/title/camel/snake)
        """
        if case_type == 'upper':
            return text.upper()
        elif case_type == 'lower':
            return text.lower()
        elif case_type == 'title':
            return text.title()
        elif case_type == 'camel':
            # snake_case to camelCase
            words = text.split('_')
            return words[0] + ''.join(w.capitalize() for w in words[1:])
        elif case_type == 'snake':
            # camelCase to snake_case
            return re.sub(r'([a-z])([A-Z])', r'\1_\2', text).lower()
        return text
    
    def format_json(self, text, indent=2):
        """格式化JSON"""
        import json
        try:
            data = json.loads(text)
            return json.dumps(data, ensure_ascii=False, indent=indent)
        except json.JSONDecodeError as e:
            return f"JSON解析错误: {e}"
    
    def process_file(self, input_path, output_path=None, operations=None):
        """
        处理文件
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            operations: 操作列表
        """
        operations = operations or []
        
        text = self.read_file(input_path)
        
        for op in operations:
            if op['type'] == 'clean':
                text = self.clean_text(text, op.get('options', {}))
            elif op['type'] == 'case':
                text = self.convert_case(text, op['case_type'])
            elif op['type'] == 'format_json':
                text = self.format_json(text)
        
        if output_path:
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"[成功] 已保存到: {output_path}")
        
        return text


def main():
    parser = argparse.ArgumentParser(description='文本处理工具')
    parser.add_argument('command', choices=['clean', 'count', 'keywords', 
                                            'extract', 'case', 'format'],
                       help='操作命令')
    parser.add_argument('-i', '--input', required=True, help='输入文件')
    parser.add_argument('-o', '--output', help='输出文件')
    parser.add_argument('--remove-html', action='store_true', help='移除HTML标签')
    parser.add_argument('--remove-urls', action='store_true', help='移除URL')
    parser.add_argument('--remove-emails', action='store_true', help='移除邮箱')
    parser.add_argument('--remove-numbers', action='store_true', help='移除数字')
    parser.add_argument('--case-type', choices=['upper', 'lower', 'title', 'camel', 'snake'],
                       help='大小写转换类型')
    parser.add_argument('--top', type=int, default=10, help='关键词数量')
    
    args = parser.parse_args()
    
    processor = TextProcessor()
    
    if args.command == 'clean':
        options = {
            'remove_html': args.remove_html,
            'remove_urls': args.remove_urls,
            'remove_emails': args.remove_emails,
            'remove_numbers': args.remove_numbers,
        }
        text = processor.read_file(args.input)
        result = processor.clean_text(text, options)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"[成功] 已保存到: {args.output}")
        else:
            print(result)
    
    elif args.command == 'count':
        text = processor.read_file(args.input)
        stats = processor.word_count(text)
        
        print("\n文本统计:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    elif args.command == 'keywords':
        text = processor.read_file(args.input)
        keywords = processor.extract_keywords(text, args.top)
        
        print(f"\n关键词 (前{args.top}个):")
        for word, count in keywords:
            print(f"  {word}: {count}次")
    
    elif args.command == 'extract':
        text = processor.read_file(args.input)
        info = processor.extract_info(text)
        
        print("\n提取信息:")
        for key, values in info.items():
            if values:
                print(f"\n{key}:")
                for v in values:
                    print(f"  - {v}")
    
    elif args.command == 'case':
        if not args.case_type:
            print("错误: 需要指定 --case-type")
            return
        text = processor.read_file(args.input)
        result = processor.convert_case(text, args.case_type)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
        else:
            print(result)
    
    elif args.command == 'format':
        text = processor.read_file(args.input)
        result = processor.format_json(text)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
        else:
            print(result)


if __name__ == '__main__':
    main()
