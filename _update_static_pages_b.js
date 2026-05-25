// _update_static_pages_b.js — 方向B「赤縁·温暖手工感」应用到4个静态页面
// 更新: about.html, contact.html, disclaimer.html, about-owl.html

const fs = require('fs');
const path = require('path');

const files = ['about.html', 'contact.html', 'disclaimer.html', 'about-owl.html'];
const baseDir = 'C:\\\\Users\\\\Administrator\\\\tcmway-blog';

// 方向B CSS变量（完整暖色系）
const NEW_CSS_ROOT = `:root {
    --bg: #fdf6ee;
    --text: #3b2a1a;
    --accent: #b83a2a;
    --accent-warm: #e8a87c;
    --light: #fef0e2;
    --border: #e8d5c0;
    --subtle: #8a6d54;
    --gold: #c9a84c;
  }`;

// 印章风格Ollie SVG (brand-symbol)
const BRAND_SYMBOL_SVG = `<svg class="brand-symbol" viewBox="0 0 80 80" width="64" height="64" style="display:block;margin:0 auto 1rem;">
  <circle cx="40" cy="40" r="38" fill="none" stroke="#b83a2a" stroke-width="1.5" stroke-dasharray="4 3"/>
  <circle cx="40" cy="28" r="10" fill="#b83a2a"/>
  <ellipse cx="35" cy="26" rx="2.5" ry="3" fill="#fdf6ee"/>
  <ellipse cx="45" cy="26" rx="2.5" ry="3" fill="#fdf6ee"/>
  <path d="M38 29 Q40 32 42 29" stroke="#fdf6ee" stroke-width="1.5" fill="none" stroke-linecap="round"/>
  <path d="M30 22 Q40 14 50 22 L48 24 Q40 18 32 24 Z" fill="#e8a87c"/>
  <path d="M30 34 Q40 44 50 34 L48 38 Q40 46 32 38 Z" fill="#e8a87c"/>
  <ellipse cx="40" cy="36" rx="7" ry="9" fill="#e8a87c"/>
  <path d="M37 33 L39 37 L35 36 Z" fill="#b83a2a"/>
  <path d="M43 33 L41 37 L45 36 Z" fill="#b83a2a"/>
  <circle cx="52" cy="54" r="5" fill="none" stroke="#c9a84c" stroke-width="1.2"/>
  <path d="M49 54 A3 3 0 1 1 55 54" fill="#c9a84c"/>
  <path d="M55 51 A3 3 0 1 1 49 51" fill="#c9a84c"/>
</svg>`;

let successCount = 0;

files.forEach(file => {
  const filePath = path.join(baseDir, file);
  
  try {
    let html = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    // 1. 替换 :root CSS变量为方向B暖色系
    const oldRootRegex = /:root\s*\{[^}]*--bg:\s*#?\w+;[^}]*--text:\s*#?\w+;[^}]*--accent:\s*#?\w+;[^}]*\}/;
    if (oldRootRegex.test(html)) {
      html = html.replace(oldRootRegex, NEW_CSS_ROOT);
      modified = true;
    }
    
    // 2. 替换旧OG image路径
    if (html.includes('fauntleroy-z.github.io/tcmway/images/')) {
      html = html.replace(/fauntleroy-z\.github\.io\/tcmway\/images\//g, 'tcmway.org/images/');
      modified = true;
    }
    
    // 3. 替换旧OG URL
    if (html.includes('fauntleroy-z.github.io/tcmway/')) {
      html = html.replace(/fauntleroy-z\.github\.io\/tcmway\//g, 'tcmway.org/');
      modified = true;
    }
    
    // 4. 在header h1后面注入brand-symbol SVG
    if (!html.includes('class="brand-symbol"')) {
      // 匹配 <h1>TCM Way</h1> 后面紧跟的 \n 或 <nav>
      const headerH1Regex = /(<header>\s*<h1>TCM Way<\/h1>)/;
      if (headerH1Regex.test(html)) {
        html = html.replace(headerH1Regex, `$1\n  ${BRAND_SYMBOL_SVG}`);
        modified = true;
      }
    }
    
    // 5. 添加方向B特有样式到 </style> 前
    const dirBExtras = `
  /* ===== Direction B: 赤縁·温暖手工感 ===== */
  header h1 { position: relative; display: inline-block; }
  header h1::after {
    content: '';
    position: absolute;
    bottom: -4px; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(90deg, #b83a2a 0%, #e8a87c 60%, transparent 100%);
    border-radius: 2px;
  }
  h2 { border-left: 4px solid var(--accent-warm); padding-left: 0.8rem !important; }
  h3 { border-left: 3px solid var(--accent-warm); padding-left: 0.6rem; }
  blockquote { 
    background: var(--light); 
    border-left: none; 
    padding: 1rem 1.5rem 1rem 2rem; 
    margin: 1.5rem 0; 
    border-radius: 4px; 
    position: relative; 
  }
  blockquote::before { content: "\\270E"; color: var(--accent); font-size: 1.2rem; position: absolute; left: 0.6rem; top: 0.9rem; }
  .warning { border-left-color: var(--accent) !important; }
  .email-box { border-color: var(--accent) !important; }
  .bonus-box { background: linear-gradient(135deg, #fef0e2 0%, #f8dcc8 100%) !important; }`;
    
    if (!html.includes('Direction B')) {
      html = html.replace(/(<\/style>)/s, `${dirBExtras}\n$1`);
      modified = true;
    }

    if (modified) {
      fs.writeFileSync(filePath, html, 'utf8');
      console.log(`✅ ${file} — updated (Direction B applied)`);
      successCount++;
    } else {
      console.log(`⚠️ ${file} — no changes needed`);
    }
  } catch (err) {
    console.error(`❌ ${file} — ERROR:`, err.message);
  }
});

console.log(`\n===== Done: ${successCount}/${files.length} static pages updated =====`);
