#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文查重工具
功能：文本相似度检测、N-gram指纹比对、SimHash算法、生成查重报告
"""

import re
import os
import json
import hashlib
import argparse
from collections import Counter
from datetime import datetime


class PlagiarismChecker:
    """论文查重检测器"""

    def __init__(self, ngram_size=4, similarity_threshold=0.3):
        self.ngram_size = ngram_size
        self.similarity_threshold = similarity_threshold

    # ---- 文本预处理 ----
    @staticmethod
    def preprocess(text):
        """清洗文本：去标点、去空白、统一小写"""
        text = re.sub(r'[^\w\u4e00-\u9fff]', '', text)
        text = text.lower()
        return text

    # ---- N-gram 指纹 ----
    def get_ngrams(self, text):
        """生成 N-gram 集合"""
        text = self.preprocess(text)
        ngrams = set()
        for i in range(len(text) - self.ngram_size + 1):
            ngrams.add(text[i:i + self.ngram_size])
        return ngrams

    # ---- SimHash ----
    def simhash(self, text, hash_bits=64):
        """计算 SimHash 指纹"""
        ngrams = self.get_ngrams(text)
        v = [0] * hash_bits
        for ng in ngrams:
            h = int(hashlib.md5(ng.encode()).hexdigest(), 16)
            for i in range(hash_bits):
                v[i] += 1 if (h >> i) & 1 else -1
        fingerprint = 0
        for i in range(hash_bits):
            if v[i] > 0:
                fingerprint |= (1 << i)
        return fingerprint

    @staticmethod
    def hamming_distance(h1, h2):
        """计算汉明距离"""
        return bin(h1 ^ h2).count('1')

    def simhash_similarity(self, text1, text2, hash_bits=64):
        """基于 SimHash 计算相似度"""
        h1 = self.simhash(text1, hash_bits)
        h2 = self.simhash(text2, hash_bits)
        dist = self.hamming_distance(h1, h2)
        return 1 - dist / hash_bits

    # ---- Jaccard 相似度 ----
    def jaccard_similarity(self, text1, text2):
        """基于 N-gram Jaccard 系数计算相似度"""
        s1 = self.get_ngrams(text1)
        s2 = self.get_ngrams(text2)
        if not s1 or not s2:
            return 0.0
        intersection = len(s1 & s2)
        union = len(s1 | s2)
        return intersection / union

    # ---- 余弦相似度 ----
    def cosine_similarity(self, text1, text2):
        """基于词频向量的余弦相似度"""
        words1 = self.preprocess(text1)
        words2 = self.preprocess(text2)

        # 中文按字切分，英文按空格
        tokens1 = list(words1) if not words1 else words1.split()
        tokens2 = list(words2) if not words2 else words2.split()

        c1 = Counter(tokens1)
        c2 = Counter(tokens2)

        all_keys = set(c1.keys()) | set(c2.keys())
        dot = sum(c1[k] * c2[k] for k in all_keys)
        mag1 = sum(v ** 2 for v in c1.values()) ** 0.5
        mag2 = sum(v ** 2 for v in c2.values()) ** 0.5

        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot / (mag1 * mag2)

    # ---- 综合检测 ----
    def check(self, text1, text2):
        """综合查重检测"""
        jaccard = self.jaccard_similarity(text1, text2)
        simhash_sim = self.simhash_similarity(text1, text2)
        cosine = self.cosine_similarity(text1, text2)

        overall = (jaccard * 0.4 + simhash_sim * 0.3 + cosine * 0.3)

        return {
            'jaccard_similarity': round(jaccard, 4),
            'simhash_similarity': round(simhash_sim, 4),
            'cosine_similarity': round(cosine, 4),
            'overall_similarity': round(overall, 4),
            'suspicious': overall >= self.similarity_threshold
        }

    # ---- 批量查重 ----
    def batch_check(self, source_path, compare_dir, output_path=None):
        """
        将源文件与目录中所有文件逐一比对

        Args:
            source_path: 源文件路径
            compare_dir: 对比文件目录
            output_path: 报告输出路径
        """
        with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
            source_text = f.read()

        results = []
        for fname in os.listdir(compare_dir):
            fpath = os.path.join(compare_dir, fname)
            if not os.path.isfile(fpath):
                continue
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    cmp_text = f.read()
                r = self.check(source_text, cmp_text)
                r['file'] = fname
                results.append(r)
            except Exception as e:
                results.append({'file': fname, 'error': str(e)})

        results.sort(key=lambda x: x.get('overall_similarity', 0), reverse=True)

        report = {
            'source': source_path,
            'timestamp': datetime.now().isoformat(),
            'threshold': self.similarity_threshold,
            'results': results
        }

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"[成功] 报告已保存: {output_path}")

        # 打印摘要
        print(f"\n{'='*60}")
        print(f"查重报告 — {os.path.basename(source_path)}")
        print(f"{'='*60}")
        for r in results:
            if 'error' in r:
                print(f"  {r['file']}: 错误 - {r['error']}")
            else:
                flag = '⚠️ 疑似抄袭' if r['suspicious'] else '✅ 正常'
                print(f"  {r['file']}: 综合相似度 {r['overall_similarity']*100:.1f}%  {flag}")
        print(f"{'='*60}\n")

        return report


def main():
    parser = argparse.ArgumentParser(description='论文查重工具')
    sub = parser.add_subparsers(dest='command')

    # 单次对比
    p_cmp = sub.add_parser('compare', help='对比两篇文本')
    p_cmp.add_argument('-a', '--file-a', required=True, help='文件A')
    p_cmp.add_argument('-b', '--file-b', required=True, help='文件B')
    p_cmp.add_argument('-t', '--threshold', type=float, default=0.3, help='相似度阈值')

    # 批量查重
    p_batch = sub.add_parser('batch', help='批量查重')
    p_batch.add_argument('-s', '--source', required=True, help='源文件')
    p_batch.add_argument('-d', '--dir', required=True, help='对比目录')
    p_batch.add_argument('-o', '--output', default='report.json', help='报告输出路径')
    p_batch.add_argument('-t', '--threshold', type=float, default=0.3, help='相似度阈值')

    args = parser.parse_args()

    checker = PlagiarismChecker(similarity_threshold=args.threshold if hasattr(args, 'threshold') else 0.3)

    if args.command == 'compare':
        with open(args.file_a, 'r', encoding='utf-8', errors='ignore') as f:
            text_a = f.read()
        with open(args.file_b, 'r', encoding='utf-8', errors='ignore') as f:
            text_b = f.read()

        result = checker.check(text_a, text_b)
        print(f"\nJaccard 相似度:  {result['jaccard_similarity']*100:.1f}%")
        print(f"SimHash 相似度:  {result['simhash_similarity']*100:.1f}%")
        print(f"余弦相似度:      {result['cosine_similarity']*100:.1f}%")
        print(f"综合相似度:      {result['overall_similarity']*100:.1f}%")
        print(f"结论: {'⚠️ 疑似抄袭' if result['suspicious'] else '✅ 未检测到抄袭'}")

    elif args.command == 'batch':
        checker.batch_check(args.source, args.dir, args.output)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
