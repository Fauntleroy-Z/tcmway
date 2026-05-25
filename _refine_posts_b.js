// Direction B CSS refinement pass 2
// Fixes remaining old styles that weren't caught in pass 1
const fs = require('fs');
const path = require('path');

const POSTS_DIR = __dirname + (process.platform === 'win32' ? '\\posts' : '/posts');

// Complete replacement style block - replaces everything from first * { to closing </style>
// with a unified Direction B stylesheet
function refinePost(filepath) {
  let html = fs.readFileSync(filepath, 'utf8');
  const fname = path.basename(filepath);
  let modified = false;
  
  // --- Fix h2: ensure border-left accent-warm ---
  // Old: h2 { font-weight: normal; color: var(--accent); margin: ... }
  if (html.match(/h2\s*\{[^}]*margin:[^}]*\}/) && !html.includes('border-left: 4px solid var(--accent-warm)')) {
    html = html.replace(
      /h2\s*\{([^}]*)\}/g, 
      (match, content) => {
        if (content.includes('font-weight') && content.includes('color')) {
          return `h2 { ${content} border-left: 4px solid var(--accent-warm); padding-left: 0.8rem; }`;
        }
        return match;
      }
    );
    modified = true;
  }

  // --- Fix blockquote: replace old left-border style with new warm design ---
  const oldBqPattern = /blockquote\s*\{\s*border-left:\s*3px\s*solid\s*var\(--accent\);\s*margin:\s*1\.5rem\s*0;\s*padding:\s*0\.5rem\s*1\.5rem;\s*color:\s*var\(--subtle\);\s*font-style:\s*italic;\s*\}/;
  if (oldBqPattern.test(html)) {
    html = html.replace(oldBqPattern, 
      `blockquote { border-left: none; margin: 1.5rem 0; padding: 1.2rem 1.5rem; color: var(--subtle); font-style: italic; background: var(--light); border-radius: 6px; position: relative; }\n  blockquote::before { content: "✦"; position: absolute; top: -10px; left: 16px; background: var(--light); padding: 0 6px; color: var(--accent); font-size: 1rem; }`
    );
    modified = true;
  }
  
  // Also fix post-03's special blockquote that has different formatting
  const oldBq03Pattern = /blockquote\s*\{[\s\S]*?background:\s*var\(--light\);\s*border-left:\s*3px\s*solid\s*var\(--accent\)[\s\S]*?border-radius:\s*0\s*6px\s*6px\s*0;\s*\}/;
  if (oldBq03Pattern.test(html)) {
    html = html.replace(oldBq03Pattern,
      `blockquote { border-left: none; margin: 1.5rem 0; padding: 1.2rem 1.5rem; color: var(--subtle); font-style: italic; background: var(--light); border-radius: 6px; position: relative; }\n  blockquote::before { content: "✦"; position: absolute; top: -10px; left: 16px; background: var(--light); padding: 0 6px; color: var(--accent); font-size: 1rem; }`
    );
    modified = true;
  }

  // --- Fix checklist border-left color: accent -> accent-warm ---
  html = html.replace(
    /\.checklist\s*\{\s*background:\s*var\(--light\);\s*border-radius:\s*8px;\s*padding:\s*1\.5rem;\s*margin:\s*1\.5rem\s*0;\s*border-left:\s*3px\s*solid\s*var\(--accent\);\s*\}/,
    '.checklist { background: var(--light); border-radius: 8px; padding: 1.5rem; margin: 1.5rem 0; border-left: 3px solid var(--accent-warm); }'
  );
  
  // --- Fix comic-break: add box-shadow if missing ---
  if (html.includes('.comic-break') && !html.includes('rgba(184,58,42,0.12)')) {
    html = html.replace(
      /\.comic-break\s*\{\s*display:\s*block;\s*margin:\s*2\.5rem\s*auto;\s*max-width:\s*100%;\s*height:\s*auto;\s*border-radius:\s*8px;\s*\}/,
      '.comic-break { display: block; margin: 2.5rem auto; max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 12px rgba(184,58,42,0.12); }'
    );
    modified = true;
  }
  
  // --- Fix highlight-box: add ::after pseudo-element for circle decoration ---
  if (html.includes('.highlight-box') && !html.includes('position: relative; overflow: hidden')) {
    html = html.replace(
      /(\.highlight-box\s*\{[^}]*\})/,
      '$1\n  .highlight-box::after { content: ""; position: absolute; top: -30px; right: -30px; width: 100px; height: 100px; border-radius: 50%; background: var(--accent-warm); opacity: 0.12; }'
    );
    
    // Make highlight-box have position:relative and overflow:hidden
    html = html.replace(
      /\.highlight-box\s*\{([^}]*)\}/,
      (m, content) => {
        if (!content.includes('overflow')) {
          return `.highlight-box { ${content} position: relative; overflow: hidden; }`;
        }
        return m;
      }
    );
    modified = true;
  }

  // --- Fix .sign class color if it references undefined vars ---
  
  // --- Add header h1 ::after brush underline effect if not present ---
  if (html.includes('header h1') && !html.includes('header h1::after')) {
    // Find where header h1 style is defined and add after it
    html = html.replace(
      /(header h1\s*\{[^}]*\})/g,
      `$1\n  header h1::after { content: ""; display: block; width: 60%; height: 3px; margin: 6px auto 0; background: linear-gradient(90deg, transparent, #b83a2a 20%, #e8a87c 50%, #b83a2a 80%, transparent); border-radius: 2px; opacity: 0.7; }`
    );
    modified = true;
  }
  
  // --- Fix OG url from fauntleroy-z.github.io to tcmway.org ---
  html = html.replace(/https:\/\/fauntleroy-z\.github\.io\/tcmway\/posts\//g, 'https://tcmway.org/posts/');

  if (modified) {
    fs.writeFileSync(filepath, html, 'utf8');
    console.log(`  ✅ Refined: ${fname}`);
  } else {
    console.log(`  ⏭️  OK (no changes): ${fname}`);
  }
}

try {
  const files = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.html'));
  console.log(`=== Pass 2: Refining ${files.length} posts ===\n`);
  for (const f of files) {
    refinePost(path.join(POSTS_DIR, f));
  }
  console.log('\n=== Done ===');
} catch(e) {
  console.error('Error:', e.message);
}
