# 🛠️ mzycter0101 - 个人脚本与爬虫工具集

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

**实用的Python工具集合，助力日常开发与数据处理**

[快速开始](#-快速开始) • [工具列表](#-工具列表) • [使用文档](#-使用文档) • [贡献指南](#-贡献指南)

</div>

---

## ✨ 项目简介

这是一个个人脚本与爬虫工具集合，包含多种实用的Python工具，旨在提高开发效率，简化日常数据处理任务。所有工具均采用命令行操作，代码简洁易懂，支持二次开发。

### 🎯 主要特点

- 🔥 **开箱即用** - 无需复杂配置，安装依赖即可使用
- 📦 **模块化设计** - 每个工具独立运行，按需使用
- 🎨 **精美界面** - 提供暗黑风格Web展示页面
- 📝 **详细文档** - 每个工具都有完整的使用说明
- ⚡ **高效执行** - 支持多线程、断点续传等特性

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

### 🔧 实用脚本集

| 工具 | 描述 | 文件 |
|------|------|------|
| **文件批量处理器** | 批量重命名、格式转换、文件整理 | `tools/utilities/file_processor.py` |
| **文本处理工具** | 文本清洗、格式转换、关键词提取 | `tools/utilities/text_processor.py` |
| **系统工具集** | 系统信息、进程管理、资源监控 | `tools/utilities/system_tools.py` |

---

## 📖 使用文档

### 网页内容抓取器

```bash
# 基本用法
python tools/crawlers/web_scraper.py https://example.com

# 指定输出格式和文件名
python tools/crawlers/web_scraper.py https://example.com -o output -f markdown

# 使用CSS选择器提取特定区域
python tools/crawlers/web_scraper.py https://example.com -s ".article-content"
```

**功能特点：**
- 支持多种输出格式 (JSON/TXT/Markdown)
- 自动检测页面编码
- 提取页面元数据
- CSS选择器支持

### 资源下载器

```bash
# 下载单个文件
python tools/crawlers/resource_downloader.py https://example.com/file.zip

# 批量下载
python tools/crawlers/resource_downloader.py url1 url2 url3 -o downloads

# 设置并发数
python tools/crawlers/resource_downloader.py url1 url2 -w 10 --overwrite
```

**功能特点：**
- 多线程并发下载
- 断点续传支持
- 下载进度显示
- 批量下载统计

### 数据监控工具

```bash
# 添加监控任务
python tools/crawlers/data_monitor.py add --name "价格监控" \
    --url https://example.com/product \
    --type price --selector ".price" --notify value_decrease

# 列出所有任务
python tools/crawlers/data_monitor.py list

# 启动持续监控
python tools/crawlers/data_monitor.py run
```

**功能特点：**
- 内容变化监控
- 价格波动追踪
- 自定义检查间隔
- 历史记录对比

### 文件批量处理器

```bash
# 批量重命名
python tools/utilities/file_processor.py rename -d ./photos -p "\.jpg$" -r ".png"

# 按扩展名整理文件
python tools/utilities/file_processor.py organize-ext -d ./downloads

# 查找重复文件
python tools/utilities/file_processor.py duplicates -d ./documents -m content
```

### 文本处理工具

```bash
# 清洗文本
python tools/utilities/text_processor.py clean -i input.txt -o output.txt \
    --remove-html --remove-urls

# 统计文本信息
python tools/utilities/text_processor.py count -i article.txt

# 提取关键词
python tools/utilities/text_processor.py keywords -i article.txt --top 20
```

### 系统工具集

```bash
# 查看系统信息
python tools/utilities/system_tools.py info

# 查看CPU/内存信息
python tools/utilities/system_tools.py cpu
python tools/utilities/system_tools.py memory

# 列出进程
python tools/utilities/system_tools.py process --sort memory --top 20
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
│   └── utilities/         # 实用脚本
│       ├── file_processor.py
│       ├── text_processor.py
│       └── system_tools.py
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

Made with ❤️ by mzycter

</div>
