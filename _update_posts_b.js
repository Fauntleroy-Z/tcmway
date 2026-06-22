// Direction B batch updater for TCM Way blog posts
// Updates CSS variables, image paths, and injects brand-symbol SVG into all post HTML files

const fs = require('fs');
const path = require('path');

const POSTS_DIR = __dirname + (process.platform === 'win32' ? '\\posts' : '/posts');

// === 1. New Direction B :root CSS block ===
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

// === 2. Additional Direction B styles to append/merge ===
const EXTRA_STYLES = `
  h2 { font-weight: normal; color: var(--accent); margin: 2rem 0 1rem; font-size: 1.3rem; border-left: 4px solid var(--accent-warm); padding-left: 0.8rem; }
  blockquote { border-left: none; margin: 1.5rem 0; padding: 1.2rem 1.5rem; color: var(--subtle); font-style: italic; background: var(--light); border-radius: 6px; position: relative; }
  blockquote::before { content: "✦"; position: absolute; top: -10px; left: 16px; background: var(--light); padding: 0 6px; color: var(--accent); font-size: 1rem; }
  .highlight-box { background: linear-gradient(135deg, #fef0e2 0%, #f5dcc4 100%); border-radius: 10px; padding: 1.8rem; margin: 2rem 0; text-align: center; position: relative; overflow: hidden; }
  .highlight-box::after { content: ""; position: absolute; top: -30px; right: -30px; width: 100px; height: 100px; border-radius: 50%; background: var(--accent-warm); opacity: 0.12; }
  .checklist { background: var(--light); border-radius: 8px; padding: 1.5rem; margin: 1.5rem 0; border-left: 3px solid var(--accent-warm); }
  .checklist p { margin-bottom: 0.8rem; font-weight: bold; color: var(--accent); font-family: -apple-system, sans-serif; font-size: 0.95rem; }
  .checklist ul { list-style: none; padding: 0; margin: 0; }
  .checklist li { padding: 0.4rem 0; padding-left: 1.6rem; position: relative; font-size: 0.92rem; border-bottom: 1px dashed var(--border); }
  .checklist li:last-child { border-bottom: none; }
  .checklist li::before { content: "☽"; position: absolute; left: 0; color: var(--accent); font-size: 0.9rem; }
  .comic-break { display: block; margin: 2.5rem auto; max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 12px rgba(184,58,42,0.12); }`;

// === 3. Brand symbol SVG to inject after <header> ===
const BRAND_SYMBOL_SVG = `<svg class="brand-symbol" viewBox="0 0 80 80" width="64" height="64" style="display:block;margin:0 auto 1rem;">
    <circle cx="40" cy="40" r="36" fill="none" stroke="#b83a2a" stroke-width="2" stroke-dasharray="4 3"/>
    <ellipse cx="40" cy="44" rx="22" ry="20" fill="#e8a87c"/>
    <circle cx="34" cy="36" r="4" fill="#b83a2a"/>
    <circle cx="46" cy="36" r="4" fill="#b83a2a"/>
    <polygon points="24,26 20,14 28,22" fill="#b83a2a" stroke="#b83a2a" stroke-width="1"/>
    <polygon points="56,26 60,14 52,22" fill="#b83a2a" stroke="#b83a2a" stroke-width="1"/>
    <path d="M36 48 Q40 54 44 48" fill="none" stroke="#b83a2a" stroke-width="1.5" stroke-linecap="round"/>
    <circle cx="40" cy="62" r="5" fill="#c9a84c" opacity="0.85" stroke="#b83a2a" stroke-width="1"/>
    <path d="M38 62 L40 65 L42 62" fill="#b83a2a" opacity="0.5"/>
  </svg>`;

// Image path replacements
const IMAGE_REPLACEMENTS = [
  [/owl-mascot-v3\.mini\.webp/g, 'ollie-mini-warm.svg'],
  [/owl-mascot-v3\.png/g, 'ollie-warm.svg'],
];

// OG image replacements
const OG_REPLACEMENTS = [
  [/https:\/\/fauntleroy-z\.github\.io\/tcmway\/images\/owl-mascot-v3\.png/g, 'https://tcmway.net/images/ollie-warm.svg'],
  [/https:\/\/fauntleroy-z\.github\.io\/tcmway\/images\/comic-01-exhaustion\.png/g, 'https://tcmway.net/images/ollie-warm.svg'],
  [/https:\/\/fauntleroy-z\.github\.io\/tcmway\/images\/comic-03-qi\.png/g, 'https://tcmway.net/images/ollie-warm.svg'],
  [/(<meta property="og:image" content=")https:\/\/tcmway\.net\/images\/owl-mascot-v3\.png(")/g, '$1https://tcmway.net/images/ollie-warm.svg$2'],
];

function updatePost(filepath) {
  let html = fs.readFileSync(filepath, 'utf8');
  const fname = path.basename(filepath);
  
  // Step 1: Replace :root CSS variables
  // Match various formats of :root blocks
  const rootPatterns = [
    /:root\s*\{[^}]*--bg:\s*#fdfaf5[^}]*\}/,
    /:root\s*\{[\s\S]*?--bg:\s*#fdfaf5[\s\S]*?\}/
  ];
  
  for (const pattern of rootPatterns) {
    if (pattern.test(html)) {
      html = html.replace(pattern, NEW_CSS_ROOT);
      break;
    }
  }

  // Step 2: Add extra Direction B-specific styles if not already present
  // We need to add h2 border-left, blockquote redesign, checklist moon marker, etc.
  // Find the closing </style> and insert before it
  
  // Check if we already have Direction B markers
  if (!html.includes('☽') && !html.includes('--gold')) {
    // Insert extra styles before closing </style>
    html = html.replace(/<\/style>/, EXTRA_STYLES + '\n</style>');
  }
  
  // Fix duplicate h2 definitions - remove old simple h2 if new one exists
  html = html.replace(/h2\s*\{\s*font-weight:\s*normal;\s*color:\s*var\(--accent\);\s*margin:[\d.]+rem\s*[\d.]+\s*[\d.]+rem;\s*font-size:\s*1\.3rem;\s*\}/g, 
    'h2 { font-weight: normal; color: var(--accent); margin: 2rem 0 1rem; font-size: 1.3rem; border-left: 4px solid var(--accent-warm); padding-left: 0.8rem; }');
  
  // Fix old blockquote style
  html = html.replace(/blockquote\s*\{\s*border-left:\s*3px\s*solid\s*var\(--accent\);\s*margin:[\d.]+rem\s*[\d.]+;\s*padding:[\d.]+rem\s*[\d.]+rem;\s*color:\s*var\(--subtle\);\s*font-style:\s*italic;\s*\}/g,
    'blockquote { border-left: none; margin: 1.5rem 0; padding: 1.2rem 1.5rem; color: var(--subtle); font-style: italic; background: var(--light); border-radius: 6px; position: relative; }\n  blockquote::before { content: "\\2726"; position: absolute; top: -10px; left: 16px; background: var(--light); padding: 0 6px; color: var(--accent); font-size: 1rem; }');

  // Fix old checklist li::before
  html = html.replace(/\.checklist li::before\s*\{\s*content:\s*"☐"[^}]*\}/g,
    '.checklist li::before { content: "☽"; position: absolute; left: 0; color: var(--accent); font-size: 0.9rem; }');
  
  // Fix old checklist li (add dashed border)
  html = html.replace(/(\.checklist li\s*\{[^}]*)(\})/g, 
    '$1 border-bottom: 1px dashed var(--border); $2');

  // Fix highlight-box gradient colors
  html = html.replace(/background:\s*linear-gradient\(135deg,\s*#f5ede0[^)]+\)/g,
    'background: linear-gradient(135deg, #fef0e2 0%, #f5dcc4 100%)');
    
  // Step 3: Update OG image meta tags
  for (const [pattern, replacement] of OG_REPLACEMENTS) {
    html = html.replace(pattern, replacement);
  }
  
  // Step 4: Inject brand-symbol SVG after <header> opening tag (but before content inside)
  if (!html.includes('class="brand-symbol"')) {
    html = html.replace(/<header>\s*/g, '<header>\n  ' + BRAND_SYMBOL_SVG + '\n  ');
  }
  
  // Also inject after any existing header that has nav
  // Handle case where <header>\n  <h1> exists without SVG yet
  
  // Step 5: Fix clock-table hover color for post 05
  html = html.replace(/#ede5d6/g, '#f5dcc4');
  
  // Write back
  fs.writeFileSync(filepath, html, 'utf8');
  console.log(`  ✅ Updated: ${fname}`);
  return true;
}

// Main execution
console.log('=== TCM Way Direction B Batch Updater ===\n');
console.log('Posts directory:', POSTS_DIR);

try {
  const files = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.html'));
  console.log(`Found ${files.length} posts to update.\n`);
  
  let success = 0;
  let fail = 0;
  
  for (const file of files) {
    const fpath = path.join(POSTS_DIR, file);
    try {
      updatePost(fpath);
      success++;
    } catch(e) {
      console.log(`  ❌ Error updating ${file}: ${e.message}`);
      fail++;
    }
  }
  
  console.log(`\n=== Done: ${success} updated, ${fail} failed ===`);
} catch(e) {
  console.error('Fatal error:', e.message);
  process.exit(1);
}
