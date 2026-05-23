#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片处理工具
功能：批量压缩、格式转换、尺寸调整、水印添加、EXIF信息读取
"""

import os
import argparse
from datetime import datetime


class ImageProcessor:
    """图片处理器"""

    def __init__(self):
        try:
            from PIL import Image, ExifTags, ImageDraw, ImageFont
            self.pil_available = True
        except ImportError:
            self.pil_available = False
            print("[警告] 未安装 Pillow，部分功能不可用。请运行: pip install Pillow")

    def compress(self, input_path, output_path=None, quality=85):
        """压缩图片"""
        if not self.pil_available:
            return False
        from PIL import Image

        img = Image.open(input_path)
        out = output_path or self._auto_name(input_path, '_compressed')

        # 转为 RGB（处理 RGBA/P）
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        img.save(out, 'JPEG', quality=quality, optimize=True)

        orig_size = os.path.getsize(input_path)
        new_size = os.path.getsize(out)
        ratio = (1 - new_size / orig_size) * 100

        print(f"[压缩] {os.path.basename(input_path)}")
        print(f"  原始: {self._fmt_size(orig_size)} → 压缩后: {self._fmt_size(new_size)} (节省 {ratio:.1f}%)")
        return True

    def convert(self, input_path, output_path, fmt='PNG'):
        """格式转换"""
        if not self.pil_available:
            return False
        from PIL import Image

        img = Image.open(input_path)
        if fmt.upper() in ('JPEG', 'JPG') and img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        img.save(output_path, fmt.upper())

        print(f"[转换] {os.path.basename(input_path)} → {fmt.upper()} ({self._fmt_size(os.path.getsize(output_path))})")
        return True

    def resize(self, input_path, output_path=None, width=None, height=None, scale=None):
        """调整尺寸"""
        if not self.pil_available:
            return False
        from PIL import Image

        img = Image.open(input_path)
        w, h = img.size

        if scale:
            new_w, new_h = int(w * scale), int(h * scale)
        elif width and height:
            new_w, new_h = width, height
        elif width:
            ratio = width / w
            new_w, new_h = width, int(h * ratio)
        elif height:
            ratio = height / h
            new_w, new_h = int(w * ratio), height
        else:
            print("[错误] 请指定 width/height/scale")
            return False

        img = img.resize((new_w, new_h), Image.LANCZOS)
        out = output_path or self._auto_name(input_path, f'_{new_w}x{new_h}')
        img.save(out)

        print(f"[缩放] {w}x{h} → {new_w}x{new_h}")
        return True

    def add_watermark(self, input_path, output_path=None, text='mzycter',
                      position='bottom-right', opacity=128):
        """添加文字水印"""
        if not self.pil_available:
            return False
        from PIL import Image, ImageDraw, ImageFont

        img = Image.open(input_path).convert('RGBA')
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        # 字体大小自适应
        font_size = max(20, min(img.size[0], img.size[1]) // 15)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        margin = 20

        positions = {
            'top-left': (margin, margin),
            'top-right': (img.size[0] - tw - margin, margin),
            'bottom-left': (margin, img.size[1] - th - margin),
            'bottom-right': (img.size[0] - tw - margin, img.size[1] - th - margin),
            'center': ((img.size[0] - tw) // 2, (img.size[1] - th) // 2),
        }
        pos = positions.get(position, positions['bottom-right'])
        draw.text(pos, text, font=font, fill=(255, 255, 255, opacity))

        result = Image.alpha_composite(img, overlay)
        out = output_path or self._auto_name(input_path, '_watermark')
        result.convert('RGB').save(out, 'JPEG', quality=95)

        print(f"[水印] 已添加: {os.path.basename(out)}")
        return True

    def batch_compress(self, directory, quality=85, recursive=False):
        """批量压缩"""
        exts = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
        files = self._find_images(directory, exts, recursive)

        print(f"\n[批量压缩] 找到 {len(files)} 张图片")
        for f in files:
            try:
                self.compress(f, quality=quality)
            except Exception as e:
                print(f"  [失败] {f}: {e}")

    def read_exif(self, input_path):
        """读取 EXIF 信息"""
        if not self.pil_available:
            return {}
        from PIL import Image, ExifTags

        img = Image.open(input_path)
        exif_data = img._getexif()
        if not exif_data:
            print("[信息] 无 EXIF 数据")
            return {}

        info = {}
        print(f"\n{'='*45}")
        print(f"  EXIF 信息 — {os.path.basename(input_path)}")
        print(f"{'='*45}")

        for tag_id, value in exif_data.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            if isinstance(value, bytes):
                try:
                    value = value.decode('utf-8', errors='ignore')
                except:
                    value = str(value)
            info[tag] = value
            print(f"  {tag}: {value}")

        print(f"{'='*45}")
        return info

    # ---- 辅助方法 ----
    def _find_images(self, directory, exts, recursive):
        files = []
        if recursive:
            for root, _, fnames in os.walk(directory):
                for f in fnames:
                    if f.lower().endswith(exts):
                        files.append(os.path.join(root, f))
        else:
            for f in os.listdir(directory):
                if f.lower().endswith(exts):
                    files.append(os.path.join(directory, f))
        return files

    @staticmethod
    def _auto_name(path, suffix):
        base, ext = os.path.splitext(path)
        return f"{base}{suffix}{ext}"

    @staticmethod
    def _fmt_size(size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"


def main():
    parser = argparse.ArgumentParser(description='图片处理工具')
    sub = parser.add_subparsers(dest='command')

    # 压缩
    p_comp = sub.add_parser('compress', help='压缩图片')
    p_comp.add_argument('-i', '--input', required=True)
    p_comp.add_argument('-o', '--output')
    p_comp.add_argument('-q', '--quality', type=int, default=85)
    p_comp.add_argument('--batch', action='store_true')
    p_comp.add_argument('-r', '--recursive', action='store_true')

    # 转换
    p_conv = sub.add_parser('convert', help='格式转换')
    p_conv.add_argument('-i', '--input', required=True)
    p_conv.add_argument('-o', '--output', required=True)
    p_conv.add_argument('-f', '--format', default='PNG')

    # 缩放
    p_resize = sub.add_parser('resize', help='调整尺寸')
    p_resize.add_argument('-i', '--input', required=True)
    p_resize.add_argument('-o', '--output')
    p_resize.add_argument('-W', '--width', type=int)
    p_resize.add_argument('-H', '--height', type=int)
    p_resize.add_argument('-s', '--scale', type=float)

    # 水印
    p_wm = sub.add_parser('watermark', help='添加水印')
    p_wm.add_argument('-i', '--input', required=True)
    p_wm.add_argument('-o', '--output')
    p_wm.add_argument('-t', '--text', default='mzycter')
    p_wm.add_argument('-p', '--position', default='bottom-right',
                     choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'])

    # EXIF
    p_exif = sub.add_parser('exif', help='读取 EXIF')
    p_exif.add_argument('-i', '--input', required=True)

    args = parser.parse_args()
    proc = ImageProcessor()

    if args.command == 'compress':
        if args.batch:
            proc.batch_compress(args.input, args.quality, args.recursive)
        else:
            proc.compress(args.input, args.output, args.quality)
    elif args.command == 'convert':
        proc.convert(args.input, args.output, args.format)
    elif args.command == 'resize':
        proc.resize(args.input, args.output, args.width, args.height, args.scale)
    elif args.command == 'watermark':
        proc.add_watermark(args.input, args.output, args.text, args.position)
    elif args.command == 'exif':
        proc.read_exif(args.input)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
