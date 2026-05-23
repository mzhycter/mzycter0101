#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密码生成器与安全工具
功能：强密码生成、密码强度检测、哈希计算、Base64编解码
"""

import hashlib
import hmac
import base64
import secrets
import string
import argparse
import json
import os
from datetime import datetime


class PasswordGenerator:
    """密码生成器"""

    CHARS = {
        'lower': string.ascii_lowercase,
        'upper': string.ascii_uppercase,
        'digits': string.digits,
        'symbols': '!@#$%^&*()_+-=[]{}|;:,.<>?',
    }

    @classmethod
    def generate(cls, length=16, use_upper=True, use_digits=True, use_symbols=True):
        """生成随机密码"""
        pool = cls.CHARS['lower']
        if use_upper:
            pool += cls.CHARS['upper']
        if use_digits:
            pool += cls.CHARS['digits']
        if use_symbols:
            pool += cls.CHARS['symbols']

        password = ''.join(secrets.choice(pool) for _ in range(length))
        return password

    @classmethod
    def generate_passphrase(cls, words=4, separator='-'):
        """生成易记的密码短语"""
        word_list = [
            'apple', 'brave', 'cloud', 'dance', 'eagle', 'flame', 'grace',
            'heart', 'ivory', 'jewel', 'karma', 'lunar', 'magic', 'noble',
            'ocean', 'prism', 'quest', 'river', 'solar', 'tiger', 'ultra',
            'vivid', 'whale', 'xenon', 'youth', 'zebra', 'alpha', 'blaze',
            'coral', 'delta', 'ember', 'frost', 'gleam', 'haven', 'index',
            'jolly', 'knight', 'light', 'maple', 'north', 'orbit', 'pixel',
        ]
        chosen = [secrets.choice(word_list) for _ in range(words)]
        return separator.join(chosen)


class PasswordAnalyzer:
    """密码强度分析器"""

    @staticmethod
    def analyze(password):
        """分析密码强度"""
        score = 0
        feedback = []

        # 长度评分
        length = len(password)
        if length >= 16:
            score += 30
        elif length >= 12:
            score += 25
        elif length >= 8:
            score += 15
        else:
            score += 5
            feedback.append('密码过短，建议至少8位')

        # 字符类型
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_symbol = bool(re.search(r'[^a-zA-Z0-9]', password))

        types = sum([has_lower, has_upper, has_digit, has_symbol])
        score += types * 15

        if not has_upper:
            feedback.append('建议添加大写字母')
        if not has_digit:
            feedback.append('建议添加数字')
        if not has_symbol:
            feedback.append('建议添加特殊字符')

        # 唯一字符比例
        unique_ratio = len(set(password)) / max(length, 1)
        score += int(unique_ratio * 10)

        # 连续字符检测
        if re.search(r'(.)\1{2,}', password):
            score -= 10
            feedback.append('避免连续重复字符')

        # 常见模式检测
        common = ['123456', 'password', 'qwerty', 'abc123', 'admin']
        if any(c in password.lower() for c in common):
            score -= 20
            feedback.append('包含常见弱密码模式')

        score = max(0, min(100, score))

        if score >= 80:
            level = '强'
        elif score >= 60:
            level = '中等'
        elif score >= 40:
            level = '弱'
        else:
            level = '非常弱'

        return {
            'score': score,
            'level': level,
            'length': length,
            'char_types': types,
            'feedback': feedback,
        }


class HashTool:
    """哈希计算工具"""

    ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512']

    @classmethod
    def hash_text(cls, text, algorithm='sha256'):
        """计算文本哈希"""
        h = hashlib.new(algorithm)
        h.update(text.encode('utf-8'))
        return h.hexdigest()

    @classmethod
    def hash_file(cls, file_path, algorithm='sha256'):
        """计算文件哈希"""
        h = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    @classmethod
    def hash_all(cls, text):
        """计算所有算法的哈希"""
        return {alg: cls.hash_text(text, alg) for alg in cls.ALGORITHMS}

    @classmethod
    def verify(cls, text, expected_hash, algorithm='sha256'):
        """验证哈希"""
        return cls.hash_text(text, algorithm) == expected_hash.lower()


class SecurityTool:
    """安全工具集"""

    @staticmethod
    def base64_encode(text):
        return base64.b64encode(text.encode()).decode()

    @staticmethod
    def base64_decode(encoded):
        return base64.b64decode(encoded.encode()).decode()

    @staticmethod
    def generate_token(length=32):
        return secrets.token_hex(length)

    @staticmethod
    def generate_uuid():
        import uuid
        return str(uuid.uuid4())


# 需要在 PasswordAnalyzer 中使用 re
import re


def main():
    parser = argparse.ArgumentParser(description='密码生成与安全工具')
    sub = parser.add_subparsers(dest='command')

    # 生成密码
    p_gen = sub.add_parser('generate', help='生成随机密码')
    p_gen.add_argument('-l', '--length', type=int, default=16)
    p_gen.add_argument('--no-upper', action='store_true')
    p_gen.add_argument('--no-digits', action='store_true')
    p_gen.add_argument('--no-symbols', action='store_true')
    p_gen.add_argument('--passphrase', action='store_true', help='生成密码短语')
    p_gen.add_argument('-w', '--words', type=int, default=4)

    # 分析密码
    p_analyze = sub.add_parser('analyze', help='分析密码强度')
    p_analyze.add_argument('-p', '--password', help='密码')

    # 哈希
    p_hash = sub.add_parser('hash', help='计算哈希')
    p_hash.add_argument('-t', '--text', help='文本')
    p_hash.add_argument('-f', '--file', help='文件路径')
    p_hash.add_argument('-a', '--algorithm', default='sha256',
                       choices=['md5', 'sha1', 'sha256', 'sha512'])

    # Base64
    p_b64 = sub.add_parser('base64', help='Base64 编解码')
    p_b64.add_argument('-t', '--text', required=True)
    p_b64.add_argument('-d', '--decode', action='store_true')

    # Token
    p_token = sub.add_parser('token', help='生成安全令牌')
    p_token.add_argument('-l', '--length', type=int, default=32)

    args = parser.parse_args()

    if args.command == 'generate':
        if args.passphrase:
            pwd = PasswordGenerator.generate_passphrase(args.words)
            print(f"\n🔐 密码短语: {pwd}")
        else:
            pwd = PasswordGenerator.generate(
                args.length,
                use_upper=not args.no_upper,
                use_digits=not args.no_digits,
                use_symbols=not args.no_symbols
            )
            print(f"\n🔐 密码: {pwd}")
            result = PasswordAnalyzer.analyze(pwd)
            print(f"   强度: {result['level']} ({result['score']}/100)")

    elif args.command == 'analyze':
        pwd = args.password or input('请输入密码: ')
        result = PasswordAnalyzer.analyze(pwd)
        print(f"\n🔐 密码强度分析:")
        print(f"   强度: {result['level']} ({result['score']}/100)")
        print(f"   长度: {result['length']}")
        print(f"   字符类型: {result['char_types']}/4")
        if result['feedback']:
            print(f"   建议:")
            for fb in result['feedback']:
                print(f"     ⚠️ {fb}")

    elif args.command == 'hash':
        if args.text:
            result = HashTool.hash_text(args.text, args.algorithm)
            print(f"\n🔑 {args.algorithm.upper()}: {result}")
        elif args.file:
            result = HashTool.hash_file(args.file, args.algorithm)
            print(f"\n🔑 {args.file} ({args.algorithm.upper()}): {result}")

    elif args.command == 'base64':
        if args.decode:
            result = SecurityTool.base64_decode(args.text)
            print(f"\n🔓 解码: {result}")
        else:
            result = SecurityTool.base64_encode(args.text)
            print(f"\n🔒 编码: {result}")

    elif args.command == 'token':
        token = SecurityTool.generate_token(args.length)
        print(f"\n🎫 令牌: {token}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
