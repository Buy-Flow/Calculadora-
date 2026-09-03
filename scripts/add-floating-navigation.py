from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Remove versões anteriores do menu flutuante.
text = re.sub(r'\n?<!-- floating-nav-v1:start -->.*?<!-- floating-nav-v1:end -->\n?', '\n', text, flags=re.S)
text = re.sub(r'\n?/\* floating-nav-v1:start \*/.*?/\* floating-nav-v1:end \*/\n?', '\n', text, flags=re.S)
text = re.sub(r'\n?/\* floating-nav-v1-js:start \*/.*?/\* floating-nav-v1-js:end \*/\n?', '\n', text, flags=re.S)

css = r'''
/* floating-nav-v1:start */
.floating-nav-trigger{
  position:fixed;
  right:0;
  top:50%;
  transform:translateY(-50%);
  z-index:1402;
  width:34px;
  height:86px;
  border:0;
  background:transparent;
  padding:0;
  touch-action:pan-y;
  -webkit-tap-highlight-color:transparent;
  transition:opacity .16s ease, transform .16s ease;
}
.floating-nav-trigger::before{
  content:"";
  position:absolute;
  right:0;
  top:10px;
  width:9px;
  height:66px;
  border-radius:10px 0 0 10px;
  background:#344054;
  box-shadow:-2px 4px 12px rgba(16,24,40,.16);
}
.floating-nav-trigger::after{
  content:"";
  position:absolute;
  right:3px;
  top:28px;
  width:3px;
  height:30px;
  border-radius:999px;
  background:rgba(255,255,255,.92);
}
.floating-nav-trigger:active{transform:translateY(-50%) translateX(-2px)}
.floating-nav-trigger.open{
  opacity:0;
  pointer-events:none;
  transform:translateY(-50%) translateX(12px);
}

/* Painel branco sólido, sem blur e sem backdrop. */
.floating-nav-panel{
  position:fixed;
  z-index:1401;
  right:8px;
  top:50%;
  width:min(230px,calc(100vw - 30px));
  max-height:82vh;
  padding:9px;
  border:1px solid #eaecf0;
  border-radius:24px;
  background:#fff;
  box-shadow:0 18px 42px rgba(16,24,40,.18);
  transform:translateY(-50%) translateX(20px) scale(.98);
  transform-origin:right center;
  opacity:0;
  visibility:hidden;
  pointer-events:none;
  overflow-y:auto;
  overscroll-behavior:contain;
  scrollbar-width:none;
  transition:transform .2s ease, opacity .16s ease, visibility .16s ease;
}
.floating-nav-panel::-webkit-scrollbar{display:none}
.floating-nav-panel.open{
  transform:translateY(-50%) translateX(0) scale(1);
  opacity:1;
  visibility:visible;
  pointer-events:auto;
}
.floating-nav-list{
  display:flex;
  flex-direction:column;
  align-items:stretch;
  gap:9px;
}
.floating-nav-item{
  width:100%;
  min-height:44px;
  border:1px solid #e4e7ec;
  border-radius:17px;
  background:#fff;
  color:#101828;
  padding:8px 10px;
  display:grid;
  grid-template-columns:28px 1fr;
  gap:9px;
  align-items:center;
  text-align:left;
  box-shadow:0 4px 12px rgba(16,24,40,.07);
  -webkit-tap-highlight-color:transparent;
  transition:transform .14s ease, box-shadow .14s ease, border-color .14s ease;
}
.floating-nav-item:active{
  transform:scale(.985);
  border-color:#d0d5dd;
  box-shadow:0 2px 7px rgba(16,24,40,.08);
}
.floating-nav-item-icon{
  width:28px;
  height:28px;
  border-radius:10px;
  display:flex;
  align-items:center;
  justify-content:center;
  background:#f8fafc;
  border:1px solid #eef2f6;
  font-size:14px;
  line-height:1;
}
.floating-nav-item-copy{min-width:0}
.floating-nav-item-copy strong{
  display:block;
  font-size:12px;
  line-height:1.08;
  font-weight:900;
  color:#101828;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.floating-nav-item.contemplation-shortcut{
  border-color:#fecaca;
  box-shadow:0 4px 12px rgba(200,22,29,.08);
}
.floating-nav-item.contemplation-shortcut .floating-nav-item-icon{
  background:#fff5f5;
  border-color:#fee2e2;
}

@media (max-width:380px){
  .floating-nav-trigger{width:32px;height:78px}
  .floating-nav-trigger::before{top:10px;width:8px;height:58px}
  .floating-nav-trigger::after{right:3px;top:26px;width:3px;height:26px}
  .floating-nav-panel{right:7px;width:min(218px,calc(100vw - 26px));padding:8px;border-radius:22px}
  .floating-nav-list{gap:8px}
  .floating-nav-item{min-height:42px;padding:7px 9px;grid-template-columns:27px 1fr;gap:8px;border-radius:16px}
  .floating-nav-item-icon{width:27px;height:27px;font-size:13px}
  .floating-nav-item-copy strong{font-size:11.5px}
}
/* floating-nav-v1:end */
'''
text = text.replace('</style>', css + '\n</style>', 1)

html = r'''
<!-- floating-nav-v1:start -->
<button class="floating-nav-trigger" id="floatingNavTrigger" type="button" aria-label="Abrir atalhos" aria-expanded="false"></button>
<div class="floating-nav-panel" id="floatingNavPanel" aria-hidden="true">
  <div class="floating-nav-list">
    <button class="floating-nav-item" type="button" data-nav-target=".form.section">
      <span class="floating-nav-item-icon">🧮</span>
      <span class="floating-nav-item-copy"><strong>Simulação</strong></span>
    </button>
    <button class="floating-nav-item contemplation-shortcut" type="button" data-nav-action="contemplation">
      <span class="floating-nav-item-icon">📅</span>
      <span class="floating-nav-item-copy"><strong>Contemplação prevista</strong></span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target=".lance-list.section">
      <span class="floating-nav-item-icon">🎯</span>
      <span class="floating-nav-item-copy"><strong>Lances</strong></span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target=".projection-v2.section">
      <span class="floating-nav-item-icon">📈</span>
      <span class="floating-nav-item-copy"><strong>Projeção anual</strong></span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target=".contemplation-scenarios.section">
      <span class="floating-nav-item-icon">💡</span>
      <span class="floating-nav-item-copy"><strong>Após contemplar</strong></span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target=".comparison-section.section">
      <span class="floating-nav-item-icon">⚖️</span>
      <span class="floating-nav-item-copy"><strong>Consórcio x financiamento</strong></span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target="#inccSalarySection">
      <span class="floating-nav-item-icon">💰</span>
      <span class="floating-nav-item-copy"><strong>Parcela x salário</strong></span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target="#rentInvestmentSection">
      <span class="floating-nav-item-icon">🏦</span>
      <span class="floating-nav-item-copy"><strong>Consórcio + aluguel</strong></span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target="#rentInvestmentTimeline" data-open-details="true">
      <span class="floating-nav-item-icon">🗓️</span>
      <span class="floating-nav-item-copy"><strong>Aportes</strong></span>
    </button>
  </div>
</div>
<!-- floating-nav-v1:end -->
'''
text = text.replace('<div class="toast" id="toast">', html + '\n<div class="toast" id="toast">', 1)

js = r'''
/* floating-nav-v1-js:start */
(function(){
  const trigger = document.getElementById('floatingNavTrigger');
  const panel = document.getElementById('floatingNavPanel');
  if(!trigger || !panel) return;

  let opened = false;
  let startX = null;
  let panelStartX = null;

  const setOpen = (open) => {
    opened = !!open;
    trigger.classList.toggle('open', opened);
    panel.classList.toggle('open', opened);
    trigger.setAttribute('aria-expanded', opened ? 'true' : 'false');
    panel.setAttribute('aria-hidden', opened ? 'false' : 'true');
  };

  trigger.addEventListener('click', () => setOpen(true));

  trigger.addEventListener('touchstart', event => {
    startX = event.touches && event.touches[0] ? event.touches[0].clientX : null;
  }, {passive:true});
  trigger.addEventListener('touchend', event => {
    if(startX == null) return;
    const endX = event.changedTouches && event.changedTouches[0] ? event.changedTouches[0].clientX : startX;
    if(endX - startX < -16) setOpen(true);
    startX = null;
  }, {passive:true});

  panel.addEventListener('touchstart', event => {
    panelStartX = event.touches && event.touches[0] ? event.touches[0].clientX : null;
  }, {passive:true});
  panel.addEventListener('touchend', event => {
    if(panelStartX == null) return;
    const endX = event.changedTouches && event.changedTouches[0] ? event.changedTouches[0].clientX : panelStartX;
    if(endX - panelStartX > 24) setOpen(false);
    panelStartX = null;
  }, {passive:true});

  panel.querySelectorAll('[data-nav-target]').forEach(button => {
    button.addEventListener('click', () => {
      const selector = button.getAttribute('data-nav-target');
      const target = selector ? document.querySelector(selector) : null;
      if(!target) return;

      if(button.getAttribute('data-open-details') === 'true' && target.tagName === 'DETAILS'){
        target.open = true;
      }

      setOpen(false);
      requestAnimationFrame(() => target.scrollIntoView({behavior:'smooth', block:'start'}));
    });
  });

  panel.querySelectorAll('[data-nav-action="contemplation"]').forEach(button => {
    button.addEventListener('click', () => {
      setOpen(false);
      requestAnimationFrame(() => {
        const contemplationButton = document.getElementById('projectionNumberBtn');
        if(contemplationButton){
          contemplationButton.click();
        }
      });
    });
  });

  document.addEventListener('pointerdown', event => {
    if(!opened) return;
    if(panel.contains(event.target) || trigger.contains(event.target)) return;
    setOpen(false);
  });

  document.addEventListener('keydown', event => {
    if(event.key === 'Escape') setOpen(false);
  });
})();
/* floating-nav-v1-js:end */
'''
text = text.replace('</body>', '<script>\n' + js + '\n</script>\n</body>', 1)

index_path.write_text(text, encoding='utf-8')

sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v15', sw)
    sw_path.write_text(sw, encoding='utf-8')
