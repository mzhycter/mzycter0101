#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章查验工具
功能：文章质量评分、可读性分析、SEO检测、原创性评估
"""

import re
import argparse
import math
from collections import Counter


class ArticleAnalyzer:
    """文章质量分析器"""

    def __init__(self):
        self.scores = {}

    # ---- 基础统计 ----
    def analyze(self, text):
        """综合分析文章"""
        chars = len(text)
        chars_no_space = len(text.replace(' ', '').replace('\n', ''))
        chinese = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        sentences = len(re.findall(r'[。！？.!?]+', text))
        paragraphs = len([p for p in text.split('\n') if p.strip()])
        lines = len(text.split('\n'))

        # 词数估算
        word_count = chinese + english_words

        # 平均句长
        avg_sentence_len = word_count / max(sentences, 1)

        # 段落平均句数
        avg_para_sentences = sentences / max(paragraphs, 1)

        # 词汇丰富度
        tokens = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z]+', text.lower())
        unique_tokens = len(set(tokens))
        ttr = unique_tokens / max(len(tokens), 1)  # Type-Token Ratio

        # 可读性评分
        readability = self._readability_score(text, chinese, english_words, sentences, word_count)

        # SEO 评分
        seo = self._seo_score(text, chars, paragraphs, sentences)

        # 结构评分
        structure = self._structure_score(paragraphs, avg_para_sentences, sentences)

        # 综合评分
        overall = round(readability * 0.3 + seo * 0.3 + structure * 0.2 + ttr * 100 * 0.2, 1)

        return {
            'basic': {
                '总字符数': chars,
                '字符数(不含空白)': chars_no_space,
                '中文字符': chinese,
                '英文单词': english_words,
                '估算词数': word_count,
                '句子数': sentences,
                '段落数': paragraphs,
                '行数': lines,
            },
            'readability': {
                '可读性评分': readability,
                '平均句长': round(avg_sentence_len, 1),
                '词汇丰富度(TTR)': round(ttr, 4),
            },
            'seo': seo,
            'structure': structure,
            'overall_score': overall,
            'grade': self._get_grade(overall),
        }

    def _readability_score(self, text, chinese, english_words, sentences, word_count):
        """可读性评分 (0-100)"""
        if word_count == 0:
            return 0

        avg_len = word_count / max(sentences, 1)
        score = 100

        # 句子过长扣分
        if avg_len > 40:
            score -= (avg_len - 40) * 1.5
        elif avg_len < 5:
            score -= (5 - avg_len) * 5

        # 段落太少扣分
        paras = len([p for p in text.split('\n') if p.strip()])
        if paras < 3 and word_count > 200:
            score -= 10

        return max(0, min(100, round(score, 1)))

    def _seo_score(self, text, chars, paragraphs, sentences):
        """SEO 友好度评分"""
        score = 100
        issues = []

        # 文章长度
        if chars < 300:
            score -= 20
            issues.append('文章过短，建议至少300字')
        elif chars < 800:
            score -= 5
            issues.append('文章偏短，建议800字以上')

        # 段落数
        if paragraphs < 2:
            score -= 10
            issues.append('段落过少')

        # 句子数
        if sentences < 3:
            score -= 10
            issues.append('句子过少')

        # 标点使用
        punctuation = re.findall(r'[，。！？、；：""''（）\[\]【】]', text)
        if len(punctuation) < 5 and chars > 200:
            score -= 5
            issues.append('标点使用较少')

        # 数字使用（增加可信度）
        numbers = re.findall(r'\d+', text)
        if not numbers and chars > 500:
            score -= 5
            issues.append('建议添加数据支撑')

        return {
            'SEO评分': max(0, min(100, score)),
            '问题': issues,
        }

    def _structure_score(self, paragraphs, avg_para_sentences, sentences):
        """文章结构评分"""
        score = 100
        issues = []

        if paragraphs < 2:
            score -= 20
            issues.append('建议分多个段落')
        if avg_para_sentences > 8:
            score -= 10
            issues.append('段落过长，建议拆分')
        if sentences < 3:
            score -= 15
            issues.append('句子数量不足')

        return {
            '结构评分': max(0, min(100, score)),
            '问题': issues,
        }

    @staticmethod
    def _get_grade(score):
        if score >= 90:
            return 'A (优秀)'
        elif score >= 80:
            return 'B (良好)'
        elif score >= 70:
            return 'C (中等)'
        elif score >= 60:
            return 'D (及格)'
        else:
            return 'F (需改进)'

    # ---- 打印报告 ----
    def print_report(self, result):
        """打印分析报告"""
        print(f"\n{'='*55}")
        print(f"  文章质量分析报告")
        print(f"{'='*55}")

        print(f"\n📊 基础统计:")
        for k, v in result['basic'].items():
            print(f"   {k}: {v}")

        print(f"\n📖 可读性分析:")
        for k, v in result['readability'].items():
            print(f"   {k}: {v}")

        print(f"\n🔍 SEO 分析:")
        seo = result['seo']
        print(f"   SEO评分: {seo['SEO评分']}/100")
        if seo['问题']:
            for issue in seo['问题']:
                print(f"   ⚠️ {issue}")

        print(f"\n📐 结构分析:")
        st = result['structure']
        print(f"   结构评分: {st['结构评分']}/100")
        if st['问题']:
            for issue in st['问题']:
                print(f"   ⚠️ {issue}")

        print(f"\n{'─'*55}")
        print(f"  综合评分: {result['overall_score']}/100  等级: {result['grade']}")
        print(f"{'='*55}\n")


def main():
    parser = argparse.ArgumentParser(description='文章查验工具')
    parser.add_argument('-i', '--input', required=True, help='输入文件路径')
    parser.add_argument('-o', '--output', help='输出报告路径 (JSON)')

    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    analyzer = ArticleAnalyzer()
    result = analyzer.analyze(text)
    analyzer.print_report(result)

    if args.output:
        import json
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[成功] 报告已保存: {args.output}")


if __name__ == '__main__':
    main()
