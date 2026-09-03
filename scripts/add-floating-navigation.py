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
  width:10px;
  height:66px;
  border:0;
  border-radius:9px 0 0 9px;
  background:#344054;
  box-shadow:-2px 4px 12px rgba(16,24,40,.16);
  padding:0;
  touch-action:pan-y;
  -webkit-tap-highlight-color:transparent;
  transition:opacity .16s ease, transform .16s ease;
}
.floating-nav-trigger::before{
  content:"";
  position:absolute;
  left:3px;
  top:18px;
  width:3px;
  height:30px;
  border-radius:999px;
  background:rgba(255,255,255,.9);
}
.floating-nav-trigger:active{transform:translateY(-50%) translateX(-2px)}
.floating-nav-trigger.open{
  opacity:0;
  pointer-events:none;
  transform:translateY(-50%) translateX(8px);
}

/* Sem fundo, sem blur e sem caixa geral: aparecem apenas os atalhos. */
.floating-nav-panel{
  position:fixed;
  z-index:1401;
  right:7px;
  top:50%;
  width:min(214px,calc(100vw - 34px));
  max-height:78vh;
  padding:0;
  border:0;
  border-radius:0;
  background:transparent;
  box-shadow:none;
  transform:translateY(-50%) translateX(18px);
  opacity:0;
  visibility:hidden;
  pointer-events:none;
  overflow-y:auto;
  overscroll-behavior:contain;
  scrollbar-width:none;
  transition:transform .18s ease, opacity .16s ease, visibility .16s ease;
}
.floating-nav-panel::-webkit-scrollbar{display:none}
.floating-nav-panel.open{
  transform:translateY(-50%) translateX(0);
  opacity:1;
  visibility:visible;
  pointer-events:auto;
}
.floating-nav-list{
  display:flex;
  flex-direction:column;
  align-items:stretch;
  gap:4px;
}
.floating-nav-item{
  width:100%;
  min-height:38px;
  border:1px solid #d0d5dd;
  border-radius:10px;
  background:rgba(242,244,247,.98);
  color:#101828;
  padding:6px 9px;
  display:grid;
  grid-template-columns:24px 1fr;
  gap:7px;
  align-items:center;
  text-align:left;
  box-shadow:0 3px 10px rgba(16,24,40,.08);
  -webkit-tap-highlight-color:transparent;
}
.floating-nav-item:active{
  background:#e4e7ec;
  transform:translateX(1px);
}
.floating-nav-item-icon{
  width:24px;
  height:24px;
  border-radius:7px;
  display:flex;
  align-items:center;
  justify-content:center;
  background:#fff;
  border:1px solid #e4e7ec;
  font-size:13px;
  line-height:1;
}
.floating-nav-item-copy{min-width:0}
.floating-nav-item-copy strong{
  display:block;
  font-size:11.5px;
  line-height:1.08;
  font-weight:900;
  color:#101828;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

@media (max-width:380px){
  .floating-nav-trigger{width:9px;height:58px}
  .floating-nav-trigger::before{left:3px;top:16px;width:3px;height:26px}
  .floating-nav-panel{right:6px;width:min(202px,calc(100vw - 30px))}
  .floating-nav-item{min-height:36px;padding:5px 8px;grid-template-columns:23px 1fr;gap:6px}
  .floating-nav-item-icon{width:23px;height:23px;font-size:12px}
  .floating-nav-item-copy strong{font-size:11px}
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
    if(endX - startX < -18) setOpen(true);
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
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v14', sw)
    sw_path.write_text(sw, encoding='utf-8')
