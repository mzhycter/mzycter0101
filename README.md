# 🛠️ mzycter0101 - 个人脚本与爬虫工具集

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![Tools](https://img.shields.io/badge/Tools-12-blueviolet)

**实用的Python工具集合，助力日常开发、学术研究与数据处理**

[快速开始](#-快速开始) • [工具列表](#-工具列表) • [使用文档](#-使用文档) • [贡献指南](#-贡献指南)

</div>

---

## ✨ 项目简介

这是一个个人脚本与爬虫工具集合，涵盖**爬虫工具、学术工具、实用脚本、安全工具**四大模块，旨在提高开发效率，简化日常数据处理与学术研究任务。所有工具均采用命令行操作，代码简洁易懂，支持二次开发。

### 🎯 主要特点

- 🔥 **开箱即用** - 无需复杂配置，安装依赖即可使用
- 📦 **模块化设计** - 每个工具独立运行，按需使用
- 🎨 **精美界面** - 提供暗黑风格Web展示页面
- 📝 **详细文档** - 每个工具都有完整的使用说明
- ⚡ **高效执行** - 支持多线程、断点续传等特性
- 🎓 **学术支持** - 论文查重、文献检索、文章质量分析

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/mzhycter/mzycter0101.git
cd mzycter0101

# 安装所有依赖
pip install -r requirements.txt
```

### 查看Web界面

直接在浏览器中打开 `index.html` 文件，即可查看精美的暗黑风格工具展示页面。

---

## 📦 工具列表

### 🕷️ 爬虫工具集

| 工具 | 描述 | 文件 |
|------|------|------|
| **网页内容抓取器** | 抓取网页内容、提取文本、保存为多种格式 | `tools/crawlers/web_scraper.py` |
| **资源下载器** | 批量下载图片、视频、文档，支持断点续传 | `tools/crawlers/resource_downloader.py` |
| **数据监控工具** | 监控网页变化、价格追踪、内容更新提醒 | `tools/crawlers/data_monitor.py` |

### 🎓 学术工具集

| 工具 | 描述 | 文件 |
|------|------|------|
| **论文查重工具** | N-gram/SimHash/余弦相似度多算法查重检测 | `tools/academic/plagiarism_checker.py` |
| **文献检索工具** | 多源学术文献搜索，APA/MLA/BibTeX引用生成 | `tools/academic/literature_search.py` |
| **文章查验工具** | 文章质量评分、可读性分析、SEO检测 | `tools/academic/article_checker.py` |

### 🔧 实用脚本集

| 工具 | 描述 | 文件 |
|------|------|------|
| **文件批量处理器** | 批量重命名、格式转换、文件整理、重复检测 | `tools/utilities/file_processor.py` |
| **文本处理工具** | 文本清洗、格式转换、关键词提取、编码检测 | `tools/utilities/text_processor.py` |
| **系统工具集** | 系统信息、进程管理、资源监控 | `tools/utilities/system_tools.py` |
| **JSON 工具集** | 格式化、校验、路径提取、差异对比、CSV互转 | `tools/utilities/json_toolkit.py` |
| **图片处理工具** | 批量压缩、格式转换、尺寸调整、水印添加 | `tools/utilities/image_processor.py` |

### 🔒 安全工具集

| 工具 | 描述 | 文件 |
|------|------|------|
| **密码与安全工具** | 密码生成、强度分析、哈希计算、Base64编解码 | `tools/security/password_toolkit.py` |

---

## 📖 使用文档

### 🕷️ 网页内容抓取器

```bash
python tools/crawlers/web_scraper.py https://example.com
python tools/crawlers/web_scraper.py https://example.com -o output -f markdown
python tools/crawlers/web_scraper.py https://example.com -s ".article-content"
```

### 🕷️ 资源下载器

```bash
python tools/crawlers/resource_downloader.py https://example.com/file.zip
python tools/crawlers/resource_downloader.py url1 url2 url3 -o downloads -w 10
```

### 🕷️ 数据监控工具

```bash
python tools/crawlers/data_monitor.py add --name "价格监控" --url URL --type price
python tools/crawlers/data_monitor.py list
python tools/crawlers/data_monitor.py run
```

### 🎓 论文查重工具

```bash
# 对比两篇文本
python tools/academic/plagiarism_checker.py compare -a paper_a.txt -b paper_b.txt

# 批量查重
python tools/academic/plagiarism_checker.py batch -s thesis.txt -d ./references/ -o report.json
```

### 🎓 文献检索工具

```bash
# 搜索文献
python tools/academic/literature_search.py "deep learning"

# 生成 APA 引用
python tools/academic/literature_search.py "transformer" -f citations -c apa
```

### 🎓 文章查验工具

```bash
python tools/academic/article_checker.py -i article.txt
python tools/academic/article_checker.py -i article.txt -o report.json
```

### 🔧 文件批量处理器

```bash
python tools/utilities/file_processor.py rename -d ./photos -p "\.jpg$" -r ".png"
python tools/utilities/file_processor.py organize-ext -d ./downloads
python tools/utilities/file_processor.py duplicates -d ./documents -m content
```

### 🔧 文本处理工具

```bash
python tools/utilities/text_processor.py clean -i input.txt -o output.txt --remove-html
python tools/utilities/text_processor.py keywords -i article.txt --top 20
python tools/utilities/text_processor.py extract -i data.txt
```

### 🔧 系统工具集

```bash
python tools/utilities/system_tools.py info
python tools/utilities/system_tools.py cpu
python tools/utilities/system_tools.py process --sort memory --top 20
```

### 🔧 JSON 工具集

```bash
python tools/utilities/json_toolkit.py format -i data.json -o formatted.json
python tools/utilities/json_toolkit.py diff -a old.json -b new.json
python tools/utilities/json_toolkit.py to-csv -i data.json
```

### 🔧 图片处理工具

```bash
python tools/utilities/image_processor.py compress -i photo.jpg -q 80
python tools/utilities/image_processor.py convert -i photo.png -o photo.webp -f WEBP
python tools/utilities/image_processor.py watermark -i photo.jpg -t "mzycter"
```

### 🔒 密码与安全工具

```bash
python tools/security/password_toolkit.py generate -l 16
python tools/security/password_toolkit.py analyze -p "MyP@ssw0rd!"
python tools/security/password_toolkit.py hash -t "hello" -a sha256
python tools/security/password_toolkit.py base64 -t "hello"
python tools/security/password_toolkit.py token -l 32
```

---

## 📁 项目结构

```
mzycter0101/
├── index.html              # Web展示页面
├── css/
│   └── style.css          # 暗黑风格样式
├── js/
│   └── main.js            # 页面交互脚本
├── tools/
│   ├── crawlers/          # 爬虫工具
│   │   ├── web_scraper.py
│   │   ├── resource_downloader.py
│   │   └── data_monitor.py
│   ├── academic/          # 学术工具
│   │   ├── plagiarism_checker.py
│   │   ├── literature_search.py
│   │   └── article_checker.py
│   ├── utilities/         # 实用脚本
│   │   ├── file_processor.py
│   │   ├── text_processor.py
│   │   ├── system_tools.py
│   │   ├── json_toolkit.py
│   │   └── image_processor.py
│   └── security/          # 安全工具
│       └── password_toolkit.py
├── docs/                  # 文档目录
├── assets/                # 资源文件
├── requirements.txt       # Python依赖
└── README.md             # 项目说明
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 📮 联系方式

- GitHub: [@mzhycter](https://github.com/mzhycter)
- 项目链接: [https://github.com/mzhycter/mzycter0101](https://github.com/mzhycter/mzycter0101)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！**

Built with ❤️ by mzycter

</div>
