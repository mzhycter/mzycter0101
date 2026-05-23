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
