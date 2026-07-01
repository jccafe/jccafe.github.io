import os
import datetime
import sys
from html.parser import HTMLParser

# 解決 Windows 控制台 CP950 編碼問題
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'title':
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data

def get_html_title(file_path):
    parser = TitleParser()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            parser.feed(content)
            return parser.title.strip()
    except Exception as e:
        print(f"警告: 無法解析 {file_path} 的標題 - {e}")
        return ""

def scan_html_files():
    html_files = []
    exclude_dirs = {'.git', '.venv', 'docs', '.agents', '__pycache__', 'node_modules'}
    
    for root, dirs, files in os.walk('.'):
        # 修改 dirs 以排除特定目錄，os.walk 就不會遞迴深入這些資料夾
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
        
        for file in files:
            if file.lower().endswith('.html') and file.lower() != 'index.html':
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, '.')
                # 統一 URL 為斜線
                url_path = rel_path.replace('\\', '/')
                
                title = get_html_title(full_path)
                if not title:
                    # 如果沒有標題，以主檔名作為預設顯示
                    title = os.path.splitext(file)[0]
                
                html_files.append({
                    'path': url_path,
                    'title': title,
                    'name': file,
                    'dir': os.path.dirname(rel_path).replace('\\', '/') or '根目錄'
                })
    
    # 依目錄與檔名排序
    html_files.sort(key=lambda x: (x['dir'], x['title']))
    return html_files

def generate_index():
    files = scan_html_files()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 產生卡片的 HTML
    cards_html = ""
    if not files:
        cards_html = """
        <div class="no-files">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-folder-open"><path d="m6 14 1.45-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.55 6a2 2 0 0 1-1.94 1.5H4a2 2 0 0 1-2-2V5c0-1.1.9-2 2-2h3.93a2 2 0 0 1 1.66.9l.82 1.2a2 2 0 0 0 1.66.9H18a2 2 0 0 1 2 2v2"/><path d="M2 10h20"/></svg>
            <p>目前尚未發現任何網頁文件。</p>
        </div>
        """
    else:
        for f in files:
            cards_html += f"""
            <div class="card" data-title="{f['title'].lower()}" data-path="{f['path'].lower()}">
                <div class="card-header">
                    <span class="badge">{f['dir']}</span>
                </div>
                <h3 class="card-title">{f['title']}</h3>
                <p class="card-path">{f['path']}</p>
                <a href="{f['path']}" class="card-link" target="_blank">
                    立即瀏覽
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </a>
            </div>
            """

    # 完整的 HTML 模板 (採用 Glassmorphism 精緻暗黑風格)
    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JCCafe 網站目錄</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+TC:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-gradient: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #0f0f1a 100%);
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.08);
            --glass-focus: rgba(255, 255, 255, 0.15);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --accent-primary: #6366f1;
            --accent-gradient: linear-gradient(135deg, #818cf8 0%, #6366f1 100%);
            --accent-glow: rgba(99, 102, 241, 0.3);
            --transition-speed: 0.3s;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Outfit', 'Noto Sans TC', sans-serif;
            background: var(--bg-gradient);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 1.5rem;
            overflow-x: hidden;
        }}

        /* 背景微光裝飾 */
        .ambient-glow-1 {{
            position: absolute;
            width: 400px;
            height: 400px;
            background: rgba(99, 102, 241, 0.15);
            filter: blur(100px);
            border-radius: 50%;
            top: -100px;
            left: -100px;
            z-index: -1;
            pointer-events: none;
        }}

        .ambient-glow-2 {{
            position: absolute;
            width: 400px;
            height: 400px;
            background: rgba(139, 92, 246, 0.12);
            filter: blur(100px);
            border-radius: 50%;
            bottom: -100px;
            right: -100px;
            z-index: -1;
            pointer-events: none;
        }}

        .container {{
            width: 100%;
            max-width: 1200px;
            position: relative;
        }}

        /* Header */
        header {{
            text-align: center;
            margin-bottom: 3rem;
            animation: fadeInDown 0.8s ease-out;
        }}

        .logo-title {{
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
            margin-bottom: 0.5rem;
        }}

        .subtitle {{
            font-size: 1.1rem;
            color: var(--text-secondary);
            font-weight: 300;
        }}

        /* Search Bar */
        .search-container {{
            max-width: 600px;
            margin: 0 auto 3rem auto;
            position: relative;
            animation: fadeInUp 0.8s ease-out 0.2s both;
        }}

        .search-input {{
            width: 100%;
            padding: 1.1rem 1.5rem 1.1rem 3.5rem;
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 50px;
            color: var(--text-primary);
            font-size: 1rem;
            font-family: inherit;
            outline: none;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            transition: all var(--transition-speed);
        }}

        .search-input:focus {{
            border-color: var(--accent-primary);
            box-shadow: 0 0 20px var(--accent-glow);
            background: rgba(255, 255, 255, 0.05);
        }}

        .search-icon {{
            position: absolute;
            left: 1.4rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-secondary);
            pointer-events: none;
            transition: color var(--transition-speed);
        }}

        .search-input:focus + .search-icon {{
            color: #818cf8;
        }}

        /* Card Grid */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
            width: 100%;
            animation: fadeInUp 0.8s ease-out 0.4s both;
        }}

        /* Card Style */
        .card {{
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 1.8rem;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            display: flex;
            flex-direction: column;
            position: relative;
            transition: all var(--transition-speed) cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
        }}

        /* 卡片光暈背景裝飾 */
        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(800px circle at var(--x, 0px) var(--y, 0px), rgba(99, 102, 241, 0.08), transparent 40%);
            opacity: 0;
            transition: opacity var(--transition-speed);
            pointer-events: none;
        }}

        .card:hover::before {{
            opacity: 1;
        }}

        .card:hover {{
            transform: translateY(-6px);
            border-color: rgba(99, 102, 241, 0.3);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4), 0 0 2px rgba(99, 102, 241, 0.2);
        }}

        .card-header {{
            margin-bottom: 1.2rem;
            display: flex;
            justify-content: flex-start;
        }}

        .badge {{
            font-size: 0.75rem;
            font-weight: 600;
            color: #a5b4fc;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.2);
            padding: 0.3rem 0.8rem;
            border-radius: 50px;
            letter-spacing: 0.5px;
        }}

        .card-title {{
            font-size: 1.25rem;
            font-weight: 600;
            line-height: 1.4;
            margin-bottom: 0.6rem;
            color: var(--text-primary);
            flex-grow: 0;
        }}

        .card-path {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-family: monospace;
            word-break: break-all;
            margin-bottom: 1.8rem;
            flex-grow: 1;
        }}

        .card-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: #818cf8;
            text-decoration: none;
            font-size: 0.95rem;
            font-weight: 600;
            transition: color var(--transition-speed);
            align-self: flex-start;
            margin-top: auto;
        }}

        .card-link svg {{
            transition: transform var(--transition-speed);
        }}

        .card:hover .card-link {{
            color: #a5b4fc;
        }}

        .card:hover .card-link svg {{
            transform: translateX(4px);
        }}

        /* Empty State */
        .no-files {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 5rem 2rem;
            background: var(--glass-bg);
            border: 1px dashed var(--glass-border);
            border-radius: 24px;
            color: var(--text-secondary);
        }}

        .no-files svg {{
            margin-bottom: 1.5rem;
            opacity: 0.5;
            color: #818cf8;
        }}

        .no-files p {{
            font-size: 1.1rem;
        }}

        /* Footer */
        footer {{
            margin-top: auto;
            padding-top: 5rem;
            padding-bottom: 1rem;
            width: 100%;
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.85rem;
            animation: fadeIn 1.2s ease-out;
        }}

        .update-time {{
            margin-bottom: 0.5rem;
            font-weight: 300;
        }}

        .copyright {{
            opacity: 0.6;
        }}

        /* Animations */
        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        /* RWD */
        @media (max-width: 640px) {{
            .logo-title {{
                font-size: 2.2rem;
            }}
            body {{
                padding: 1.5rem 1rem;
            }}
            .grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="ambient-glow-1"></div>
    <div class="ambient-glow-2"></div>

    <div class="container">
        <header>
            <h1 class="logo-title">JCCafe 網站目錄</h1>
            <p class="subtitle">網站地圖與靜態網頁自動化索引</p>
        </header>

        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="搜尋網頁標題或路徑...">
            <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        </div>

        <main class="grid" id="cardGrid">
            {cards_html}
        </main>

        <footer>
            <p class="update-time">最後更新時間：{now_str}</p>
            <p class="copyright">&copy; {datetime.datetime.now().year} JCCafe. All rights reserved.</p>
        </footer>
    </div>

    <script>
        // 本地即時搜尋過濾功能
        const searchInput = document.getElementById('searchInput');
        const cards = document.querySelectorAll('.card');
        const grid = document.getElementById('cardGrid');

        searchInput.addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase().trim();
            let visibleCount = 0;
            
            cards.forEach(card => {{
                const title = card.getAttribute('data-title');
                const path = card.getAttribute('data-path');
                
                if (title.includes(query) || path.includes(query)) {{
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            // 處理搜尋不到結果時的 Empty State
            let emptyMsg = document.getElementById('noResultsMsg');
            if (visibleCount === 0) {{
                if (!emptyMsg) {{
                    emptyMsg = document.createElement('div');
                    emptyMsg.id = 'noResultsMsg';
                    emptyMsg.className = 'no-files';
                    emptyMsg.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search-x"><path d="m13.5 8.5-5 5"/><path d="m8.5 8.5 5 5"/><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                        <p>找不到符合「${{e.target.value}}」的網頁項目。</p>
                    `;
                    grid.appendChild(emptyMsg);
                }}
            }} else {{
                if (emptyMsg) {{
                    emptyMsg.remove();
                }}
            }}
        }});

        // 卡片滑鼠懸停光暈效果 (CSS 變數)
        cards.forEach(card => {{
            card.addEventListener('mousemove', (e) => {{
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty('--x', `${{x}}px`);
                card.style.setProperty('--y', `${{y}}px`);
            }});
        }});
    </script>
</body>
</html>
"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[OK] 目錄已成功生成至 index.html，共包含 {len(files)} 個檔案。")

if __name__ == "__main__":
    generate_index()
