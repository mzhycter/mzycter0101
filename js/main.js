/**
 * mzycter0101 - 主脚本文件
 */

// 工具详情数据
const toolsData = {
    'web-scraper': {
        title: '网页内容抓取器',
        desc: '一个强大的网页内容抓取工具，支持提取网页文本、链接、图片和元数据。可以将抓取结果保存为JSON、TXT或Markdown格式，方便后续处理和分析。',
        usage: `# 基本用法
python web_scraper.py https://example.com

# 指定输出格式和文件名
python web_scraper.py https://example.com -o output -f markdown

# 使用CSS选择器提取特定区域
python web_scraper.py https://example.com -s ".article-content"

# 仅提取文本，不提取链接和图片
python web_scraper.py https://example.com --no-extract-all`,
        features: [
            '支持多种输出格式 (JSON/TXT/Markdown)',
            '自动检测页面编码',
            '提取页面元数据 (标题、描述、关键词)',
            'CSS选择器支持精确提取',
            '自动清理脚本和样式标签',
            '提取所有链接和图片'
        ],
        dependencies: 'pip install requests beautifulsoup4'
    },
    'resource-downloader': {
        title: '资源下载器',
        desc: '高效的资源批量下载工具，支持多线程并发下载、断点续传。可以下载图片、视频、文档等各类资源，并自动处理文件名。',
        usage: `# 下载单个文件
python resource_downloader.py https://example.com/file.zip

# 批量下载多个文件
python resource_downloader.py url1 url2 url3 -o downloads

# 设置并发数和覆盖已存在文件
python resource_downloader.py url1 url2 -w 10 --overwrite`,
        features: [
            '多线程并发下载',
            '断点续传支持',
            '自动文件名处理',
            '下载进度显示',
            '批量下载统计',
            '支持各类资源类型'
        ],
        dependencies: 'pip install requests beautifulsoup4'
    },
    'data-monitor': {
        title: '数据监控工具',
        desc: '智能数据监控工具，可以监控网页内容变化、价格波动等。支持设置检查间隔和通知条件，适合用于价格追踪、内容更新检测等场景。',
        usage: `# 添加监控任务
python data_monitor.py add --name "价格监控" --url https://example.com/product \\
    --type price --selector ".price" --notify value_decrease

# 列出所有任务
python data_monitor.py list

# 执行一次检查
python data_monitor.py check

# 启动持续监控
python data_monitor.py run`,
        features: [
            '内容变化监控',
            '价格波动追踪',
            '自定义检查间隔',
            '多种通知条件',
            '历史记录对比',
            '任务管理功能'
        ],
        dependencies: 'pip install requests beautifulsoup4'
    },
    'file-processor': {
        title: '文件批量处理器',
        desc: '强大的文件批量处理工具，支持批量重命名、按扩展名/日期整理文件、查找重复文件、清理空目录等功能。',
        usage: `# 批量重命名（使用正则表达式）
python file_processor.py rename -d ./photos -p "\\.jpg$" -r ".png"

# 使用模板批量重命名
python file_processor.py template -d ./photos -t "photo_{num}" --start 1

# 按扩展名整理文件
python file_processor.py organize-ext -d ./downloads

# 查找重复文件
python file_processor.py duplicates -d ./documents -m content

# 预览模式（不实际执行）
python file_processor.py rename -d ./test --dry-run`,
        features: [
            '正则表达式批量重命名',
            '模板化命名支持',
            '按扩展名/日期整理',
            '重复文件检测',
            '空目录清理',
            '预览模式'
        ],
        dependencies: '无需额外依赖'
    },
    'text-processor': {
        title: '文本处理工具',
        desc: '多功能文本处理工具，支持文本清洗、编码检测、关键词提取、信息提取、大小写转换等功能。',
        usage: `# 清洗文本（移除HTML、URL等）
python text_processor.py clean -i input.txt -o output.txt \\
    --remove-html --remove-urls --remove-emails

# 统计文本信息
python text_processor.py count -i article.txt

# 提取关键词
python text_processor.py keywords -i article.txt --top 20

# 提取文本中的信息（邮箱、URL、电话等）
python text_processor.py extract -i data.txt

# 大小写转换
python text_processor.py case -i input.txt --case-type upper -o output.txt`,
        features: [
            '文本清洗和格式化',
            '自动编码检测',
            '关键词提取',
            '信息提取（邮箱/URL/电话）',
            '大小写转换',
            'JSON格式化'
        ],
        dependencies: 'pip install chardet'
    },
    'system-tools': {
        title: '系统工具集',
        desc: '系统信息和资源监控工具集，可以查看系统信息、CPU/内存/磁盘状态、进程管理、网络信息等。',
        usage: `# 查看系统信息
python system_tools.py info

# 查看CPU信息
python system_tools.py cpu

# 查看内存信息
python system_tools.py memory

# 查看磁盘信息
python system_tools.py disk

# 列出占用内存最高的进程
python system_tools.py process --sort memory --top 20

# 终止进程
python system_tools.py kill --pid 1234

# 查看环境变量
python system_tools.py env --filter PATH`,
        features: [
            '系统信息查看',
            'CPU/内存/磁盘监控',
            '进程管理和监控',
            '网络信息查看',
            '环境变量管理',
            '命令执行功能'
        ],
        dependencies: 'pip install psutil'
    },
    'plagiarism-checker': {
        title: '论文查重工具',
        desc: '基于 N-gram 指纹、SimHash 算法和余弦相似度的多算法论文查重检测工具。支持单次对比和批量查重，可生成详细的 JSON 查重报告。',
        usage: `# 对比两篇文本
python plagiarism_checker.py compare -a paper_a.txt -b paper_b.txt

# 批量查重（将源文件与目录中所有文件对比）
python plagiarism_checker.py batch -s thesis.txt -d ./references/ -o report.json

# 自定义相似度阈值
python plagiarism_checker.py compare -a a.txt -b b.txt -t 0.2`,
        features: [
            'N-gram Jaccard 相似度',
            'SimHash 指纹算法',
            '余弦相似度计算',
            '综合加权评分',
            '批量查重报告',
            '可自定义阈值'
        ],
        dependencies: '无需额外依赖（纯Python实现）'
    },
    'literature-search': {
        title: '文献检索工具',
        desc: '多源学术文献搜索工具，支持 CrossRef、Semantic Scholar、Google Scholar 等数据源。可自动生成 APA、MLA、BibTeX 等多种引用格式。',
        usage: `# 搜索文献（默认使用 CrossRef + Semantic Scholar）
python literature_search.py "deep learning"

# 指定搜索来源
python literature_search.py "machine learning" -s crossref semantic

# 生成 APA 引用格式
python literature_search.py "transformer" -f citations -c apa

# 保存为文本格式
python literature_search.py "GPT" -o results.txt -f txt`,
        features: [
            'CrossRef API 检索',
            'Semantic Scholar API',
            'Google Scholar 解析',
            'APA/MLA/BibTeX 引用',
            '批量结果保存',
            'DOI 自动提取'
        ],
        dependencies: 'pip install requests beautifulsoup4'
    },
    'article-checker': {
        title: '文章查验工具',
        desc: '综合文章质量分析工具，从可读性、SEO友好度、文章结构、词汇丰富度等多个维度进行评分，生成详细的质量分析报告。',
        usage: `# 分析文章质量
python article_checker.py -i article.txt

# 保存分析报告为 JSON
python article_checker.py -i article.txt -o report.json`,
        features: [
            '综合质量评分 (A-F)',
            '可读性分析',
            'SEO 友好度检测',
            '文章结构评估',
            '词汇丰富度 (TTR)',
            '改进建议输出'
        ],
        dependencies: '无需额外依赖（纯Python实现）'
    },
    'json-toolkit': {
        title: 'JSON 工具集',
        desc: '多功能 JSON 处理工具，支持格式化、校验、路径提取、嵌套展平、差异对比以及 JSON 与 CSV 互转。',
        usage: `# 格式化 JSON
python json_toolkit.py format -i data.json -o formatted.json

# 校验 JSON
python json_toolkit.py validate -i data.json

# 提取路径值
python json_toolkit.py extract -i data.json -p "data.users.0.name"

# 对比两个 JSON
python json_toolkit.py diff -a old.json -b new.json

# JSON 转 CSV
python json_toolkit.py to-csv -i data.json

# CSV 转 JSON
python json_toolkit.py to-json -i data.csv`,
        features: [
            'JSON 格式化/美化',
            '语法校验',
            '点号路径提取',
            '嵌套结构展平',
            'JSON 差异对比',
            'JSON ↔ CSV 互转'
        ],
        dependencies: '无需额外依赖（纯Python实现）'
    },
    'image-processor': {
        title: '图片处理工具',
        desc: '批量图片处理工具，支持压缩、格式转换、尺寸调整、文字水印添加和 EXIF 元数据读取。',
        usage: `# 压缩单张图片
python image_processor.py compress -i photo.jpg -q 80

# 批量压缩目录下所有图片
python image_processor.py compress -i ./photos --batch -r

# 格式转换
python image_processor.py convert -i photo.png -o photo.webp -f WEBP

# 调整尺寸
python image_processor.py resize -i photo.jpg -W 800

# 添加水印
python image_processor.py watermark -i photo.jpg -t "mzycter" -p bottom-right

# 读取 EXIF 信息
python image_processor.py exif -i photo.jpg`,
        features: [
            '批量图片压缩',
            '格式转换 (PNG/JPG/WEBP)',
            '尺寸缩放',
            '文字水印',
            'EXIF 信息读取',
            '递归目录处理'
        ],
        dependencies: 'pip install Pillow'
    },
    'password-toolkit': {
        title: '密码与安全工具',
        desc: '集密码生成、强度分析、哈希计算、Base64编解码、安全令牌生成于一体的安全工具集。',
        usage: `# 生成16位强密码
python password_toolkit.py generate -l 16

# 生成易记密码短语
python password_toolkit.py generate --passphrase -w 5

# 分析密码强度
python password_toolkit.py analyze -p "MyP@ssw0rd!"

# 计算文本哈希
python password_toolkit.py hash -t "hello world" -a sha256

# 计算文件哈希
python password_toolkit.py hash -f document.pdf

# Base64 编码/解码
python password_toolkit.py base64 -t "hello"
python password_toolkit.py base64 -t "aGVsbG8=" -d

# 生成安全令牌
python password_toolkit.py token -l 32`,
        features: [
            '随机密码生成',
            '密码短语生成',
            '密码强度分析',
            'MD5/SHA1/SHA256/SHA512',
            'Base64 编解码',
            '安全令牌生成'
        ],
        dependencies: '无需额外依赖（纯Python实现）'
    }
};

// DOM元素
const navbar = document.querySelector('.navbar');
const navLinks = document.querySelectorAll('.nav-link');
const navToggle = document.querySelector('.nav-toggle');
const navLinksContainer = document.querySelector('.nav-links');
const sections = document.querySelectorAll('.section');
const modal = document.getElementById('tool-modal');

// 页面初始化
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initScrollEffects();
    initAnimations();
    initCounterAnimation();
    highlightCode();
});

// 导航功能
function initNavigation() {
    // 点击导航链接
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = link.getAttribute('data-section');
            switchSection(sectionId);
            
            // 更新活动状态
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // 移动端关闭菜单
            navLinksContainer.classList.remove('active');
        });
    });
    
    // 移动端菜单切换
    navToggle.addEventListener('click', () => {
        navLinksContainer.classList.toggle('active');
    });
}

// 切换页面区域
function switchSection(sectionId) {
    sections.forEach(section => {
        section.classList.remove('active');
        if (section.id === sectionId) {
            section.classList.add('active');
            // 滚动到顶部
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
}

// 滚动效果
function initScrollEffects() {
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        // 导航栏阴影
        if (currentScroll > 50) {
            navbar.style.boxShadow = 'var(--shadow-md)';
        } else {
            navbar.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });
}

// 初始化动画
function initAnimations() {
    // 工具卡片入场动画
    const cards = document.querySelectorAll('.tool-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('fade-in');
                }, index * 100);
            }
        });
    }, { threshold: 0.1 });
    
    cards.forEach(card => observer.observe(card));
}

// 数字计数动画
function initCounterAnimation() {
    const counters = document.querySelectorAll('.stat-number');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-count'));
                animateCounter(entry.target, target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element, target) {
    let current = 0;
    const increment = target / 30;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 50);
}

// 显示工具详情
function showToolDetail(toolId) {
    const tool = toolsData[toolId];
    if (!tool) return;
    
    // 填充模态框内容
    modal.querySelector('.modal-title').textContent = tool.title;
    modal.querySelector('.modal-desc').textContent = tool.desc;
    
    // 使用方法
    const usageCode = modal.querySelector('.modal-usage code');
    usageCode.textContent = tool.usage;
    
    // 功能特点
    const featuresList = modal.querySelector('.features-list');
    featuresList.innerHTML = tool.features.map(f => `<li>${f}</li>`).join('');
    
    // 依赖安装
    const depsCode = modal.querySelectorAll('.modal-dependencies code')[0];
    depsCode.textContent = tool.dependencies;
    
    // 显示模态框
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // 重新高亮代码
    highlightCode();
}

// 关闭模态框
function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

// 点击模态框外部关闭
modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

// ESC键关闭模态框
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
    }
});

// 代码高亮
function highlightCode() {
    document.querySelectorAll('pre code').forEach(block => {
        hljs.highlightElement(block);
    });
}

// 工具卡片点击事件
document.querySelectorAll('.tool-card').forEach(card => {
    card.addEventListener('click', (e) => {
        // 如果点击的是按钮，不触发卡片点击
        if (e.target.closest('.btn')) return;
        
        const toolId = card.getAttribute('data-tool');
        showToolDetail(toolId);
    });
});

// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// 控制台欢迎信息
console.log('%c欢迎来到 mzycter0101 工具集!', 
    'color: #58a6ff; font-size: 20px; font-weight: bold;');
console.log('%cGitHub: https://github.com/mzhycter/mzycter0101', 
    'color: #8b949e;');
