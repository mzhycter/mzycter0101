#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON 工具集
功能：JSON 格式化、校验、路径提取、对比差异、JSON ↔ CSV 转换
"""

import json
import csv
import argparse
import os
from collections import OrderedDict


class JsonToolkit:
    """JSON 工具集"""

    @staticmethod
    def format_json(input_path, output_path=None, indent=2, sort_keys=False):
        """格式化 JSON 文件"""
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        formatted = json.dumps(data, ensure_ascii=False, indent=indent, sort_keys=sort_keys)

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
            print(f"[成功] 已保存到: {output_path}")
        else:
            print(formatted)

    @staticmethod
    def validate_json(input_path):
        """校验 JSON 文件"""
        try:
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
            print(f"[成功] JSON 格式有效")
            print(f"  类型: {type(data).__name__}")
            if isinstance(data, list):
                print(f"  元素数: {len(data)}")
            elif isinstance(data, dict):
                print(f"  键数: {len(data)}")
            return True
        except json.JSONDecodeError as e:
            print(f"[失败] JSON 格式无效:")
            print(f"  行 {e.lineno}, 列 {e.colno}: {e.msg}")
            return False

    @staticmethod
    def extract_value(data, path):
        """按路径提取值，支持点号分隔和数组索引"""
        keys = path.split('.')
        current = data
        for key in keys:
            if key.isdigit():
                key = int(key)
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int) and key < len(current):
                current = current[key]
            else:
                return None
        return current

    @staticmethod
    def flatten(data, parent_key='', sep='.'):
        """将嵌套 JSON 展平"""
        items = OrderedDict()
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, (dict, list)):
                    items.update(JsonToolkit.flatten(v, new_key, sep))
                else:
                    items[new_key] = v
        elif isinstance(data, list):
            for i, v in enumerate(data):
                new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
                if isinstance(v, (dict, list)):
                    items.update(JsonToolkit.flatten(v, new_key, sep))
                else:
                    items[new_key] = v
        return items

    @staticmethod
    def diff(json_a, json_b):
        """对比两个 JSON 的差异"""
        flat_a = JsonToolkit.flatten(json_a)
        flat_b = JsonToolkit.flatten(json_b)

        only_a = {k: v for k, v in flat_a.items() if k not in flat_b}
        only_b = {k: v for k, v in flat_b.items() if k not in flat_a}
        changed = {k: (flat_a[k], flat_b[k]) for k in flat_a if k in flat_b and flat_a[k] != flat_b[k]}

        return {
            'only_in_a': only_a,
            'only_in_b': only_b,
            'changed': changed,
            'is_identical': not only_a and not only_b and not changed
        }

    @staticmethod
    def json_to_csv(input_path, output_path=None):
        """JSON 数组转 CSV"""
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)

        if not isinstance(data, list) or not data:
            print("[错误] JSON 必须是对象数组")
            return

        # 收集所有键
        all_keys = OrderedDict()
        for item in data:
            if isinstance(item, dict):
                for k in item.keys():
                    if k not in all_keys:
                        all_keys[k] = True

        headers = list(all_keys.keys())
        out = output_path or input_path.rsplit('.', 1)[0] + '.csv'

        with open(out, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for item in data:
                if isinstance(item, dict):
                    writer.writerow(item)

        print(f"[成功] 已转换: {out} ({len(data)} 行, {len(headers)} 列)")

    @staticmethod
    def csv_to_json(input_path, output_path=None):
        """CSV 转 JSON"""
        out = output_path or input_path.rsplit('.', 1)[0] + '.json'

        with open(input_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            data = [row for row in reader]

        with open(out, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"[成功] 已转换: {out} ({len(data)} 条记录)")


def main():
    parser = argparse.ArgumentParser(description='JSON 工具集')
    sub = parser.add_subparsers(dest='command')

    # 格式化
    p_fmt = sub.add_parser('format', help='格式化 JSON')
    p_fmt.add_argument('-i', '--input', required=True)
    p_fmt.add_argument('-o', '--output')
    p_fmt.add_argument('--indent', type=int, default=2)
    p_fmt.add_argument('--sort', action='store_true')

    # 校验
    p_val = sub.add_parser('validate', help='校验 JSON')
    p_val.add_argument('-i', '--input', required=True)

    # 提取
    p_ext = sub.add_parser('extract', help='提取路径值')
    p_ext.add_argument('-i', '--input', required=True)
    p_ext.add_argument('-p', '--path', required=True, help='点号路径，如 data.users.0.name')

    # 展平
    p_flat = sub.add_parser('flatten', help='展平嵌套 JSON')
    p_flat.add_argument('-i', '--input', required=True)

    # 对比
    p_diff = sub.add_parser('diff', help='对比两个 JSON')
    p_diff.add_argument('-a', '--file-a', required=True)
    p_diff.add_argument('-b', '--file-b', required=True)

    # JSON → CSV
    p_j2c = sub.add_parser('to-csv', help='JSON 转 CSV')
    p_j2c.add_argument('-i', '--input', required=True)
    p_j2c.add_argument('-o', '--output')

    # CSV → JSON
    p_c2j = sub.add_parser('to-json', help='CSV 转 JSON')
    p_c2j.add_argument('-i', '--input', required=True)
    p_c2j.add_argument('-o', '--output')

    args = parser.parse_args()
    toolkit = JsonToolkit()

    if args.command == 'format':
        toolkit.format_json(args.input, args.output, args.indent, args.sort)
    elif args.command == 'validate':
        toolkit.validate_json(args.input)
    elif args.command == 'extract':
        with open(args.input, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
        result = toolkit.extract_value(data, args.path)
        print(json.dumps(result, ensure_ascii=False, indent=2) if isinstance(result, (dict, list)) else result)
    elif args.command == 'flatten':
        with open(args.input, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
        flat = toolkit.flatten(data)
        for k, v in flat.items():
            print(f"  {k}: {v}")
    elif args.command == 'diff':
        with open(args.file_a, 'r', encoding='utf-8', errors='ignore') as f:
            a = json.load(f)
        with open(args.file_b, 'r', encoding='utf-8', errors='ignore') as f:
            b = json.load(f)
        result = toolkit.diff(a, b)
        if result['is_identical']:
            print("[结果] 两个 JSON 完全相同")
        else:
            if result['only_in_a']:
                print(f"\n仅在 A 中 ({len(result['only_in_a'])} 项):")
                for k, v in result['only_in_a'].items():
                    print(f"  {k}: {v}")
            if result['only_in_b']:
                print(f"\n仅在 B 中 ({len(result['only_in_b'])} 项):")
                for k, v in result['only_in_b'].items():
                    print(f"  {k}: {v}")
            if result['changed']:
                print(f"\n值不同 ({len(result['changed'])} 项):")
                for k, (va, vb) in result['changed'].items():
                    print(f"  {k}: {va} → {vb}")
    elif args.command == 'to-csv':
        toolkit.json_to_csv(args.input, args.output)
    elif args.command == 'to-json':
        toolkit.csv_to_json(args.input, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
