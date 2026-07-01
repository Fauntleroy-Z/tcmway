/**
 * TCM Way — "Listen to this article" TTS button
 * Uses browser SpeechSynthesis API. Zero dependencies, zero cost.
 */
(function () {
  // ========== STYLES ==========
  const style = document.createElement('style');
  style.textContent = `
.listen-tts-btn {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 9px 20px; margin: 14px 0 22px;
  background: var(--light, #fef0e2);
  border: 1.5px solid var(--border, #e8d5c0);
  border-radius: 24px; cursor: pointer;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 0.92rem; font-weight: 500;
  color: var(--accent, #b83a2a);
  transition: all 0.25s ease;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}
.listen-tts-btn:hover {
  background: #fce8d8;
  border-color: var(--accent-warm, #e8a87c);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(184,58,42,0.1);
}
.listen-tts-btn:active { transform: translateY(0); }
.listen-tts-btn.playing {
  background: var(--accent, #b83a2a);
  color: #fff;
  border-color: var(--accent, #b83a2a);
  animation: listen-pulse 1.8s ease-in-out infinite;
}
@keyframes listen-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(184,58,42,0.35); }
  50% { box-shadow: 0 0 0 8px rgba(184,58,42,0); }
}
.listen-tts-btn .icon { font-size: 1.1em; }
.listen-tts-btn .label { line-height: 1; }
.listen-tts-btn .hint {
  font-size: 0.78em; opacity: 0.7; font-weight: 400;
  margin-left: 2px;
}
  `;
  document.head.appendChild(style);

  // ========== BUTTON ==========
  function createButton() {
    const btn = document.createElement('button');
    btn.className = 'listen-tts-btn';
    btn.innerHTML = '<span class="icon">🔊</span><span class="label">Listen</span><span class="hint">· TTS</span>';
    btn.setAttribute('aria-label', 'Listen to this article with text-to-speech');
    btn.setAttribute('title', 'Click to listen · Click again to stop');
    return btn;
  }

  // Wait for DOM; place button after .last-updated
  function placeButton() {
    const meta = document.querySelector('.last-updated');
    if (!meta) return;
    const btn = createButton();
    meta.insertAdjacentElement('afterend', btn);
    return btn;
  }

  // ========== TEXT EXTRACTION ==========
  function getArticleText() {
    const article = document.querySelector('article');
    if (!article) return '';
    const clone = article.cloneNode(true);

    // Remove non-content elements
    const removals = [
      '.meta', '.last-updated', '.listen-tts-btn',
      '.post-nav', '.sources', '.ollie-speaks',
      '.comic-break', 'img', 'audio', 'figure',
      '.sign'
    ];
    removals.forEach(sel => {
      clone.querySelectorAll(sel).forEach(el => el.remove());
    });

    let text = clone.textContent || '';
    // Clean up excessive whitespace
    text = text.replace(/\s+/g, ' ').trim();
    return text;
  }

  // ========== VOICE SELECTION ==========
  function getBestVoice() {
    const voices = speechSynthesis.getVoices();
    if (voices.length === 0) return null;

    // macOS: prefer Samantha (natural US English)
    const priority = [
      'Samantha',         // macOS — excellent quality
      'Alex',             // macOS — good
      'Google US English',
      'Microsoft David',
      'Microsoft Zira',
    ];

    for (const name of priority) {
      const v = voices.find(v => v.name === name);
      if (v) return v;
    }

    // Fallback: any English voice
    return voices.find(v => v.lang.startsWith('en-')) || voices[0];
  }

  // ========== TTS LOGIC ==========
  function setupTTS(btn) {
    let speaking = false;

    btn.addEventListener('click', () => {
      if (speaking) {
        speechSynthesis.cancel();
        return;
      }

      const text = getArticleText();
      if (!text) {
        btn.innerHTML = '<span class="icon">⚠️</span><span class="label">No text found</span>';
        setTimeout(() => resetButton(btn), 2000);
        return;
      }

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'en-US';
      utterance.rate = 0.92;  // slightly slower than default for clarity
      utterance.pitch = 1.0;

      const voice = getBestVoice();
      if (voice) utterance.voice = voice;

      utterance.onstart = () => {
        speaking = true;
        btn.classList.add('playing');
        btn.innerHTML = '<span class="icon">⏸️</span><span class="label">Stop</span>';
      };

      utterance.onend = () => resetButton(btn);
      utterance.onerror = (e) => {
        if (e.error !== 'canceled' && e.error !== 'interrupted') {
          console.warn('TTS error:', e.error);
        }
        resetButton(btn);
      };

      speechSynthesis.speak(utterance);
    });

    function resetButton(b) {
      speaking = false;
      b.classList.remove('playing');
      b.innerHTML = '<span class="icon">🔊</span><span class="label">Listen</span><span class="hint">· TTS</span>';
    }
  }

  // ========== INIT ==========
  function init() {
    // Handle voice loading (async on some browsers)
    const voices = speechSynthesis.getVoices();
    
    const btn = placeButton();
    if (btn) setupTTS(btn);

    // Chrome loads voices async — re-check
    if (voices.length === 0) {
      speechSynthesis.onvoiceschanged = () => {
        // voices now available; no action needed — getBestVoice is called on click
      };
    }
  }

  // Run after DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Cleanup on page unload
  window.addEventListener('beforeunload', () => {
    speechSynthesis.cancel();
  });
})();
