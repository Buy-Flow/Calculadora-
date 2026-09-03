from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Remove versão anterior, se existir.
text = re.sub(r'\n?<!-- floating-nav-v1:start -->.*?<!-- floating-nav-v1:end -->\n?', '\n', text, flags=re.S)
text = re.sub(r'\n?/\* floating-nav-v1:start \*/.*?/\* floating-nav-v1:end \*/\n?', '\n', text, flags=re.S)
text = re.sub(r'\n?/\* floating-nav-v1-js:start \*/.*?/\* floating-nav-v1-js:end \*/\n?', '\n', text, flags=re.S)

css = r'''
/* floating-nav-v1:start */
.floating-nav-trigger{
  position:fixed;
  right:10px;
  top:50%;
  transform:translateY(-50%);
  z-index:1402;
  width:48px;
  height:48px;
  border:1px solid rgba(255,255,255,.22);
  border-radius:50%;
  background:linear-gradient(145deg,#1f2937,#111827);
  color:#fff;
  box-shadow:0 12px 28px rgba(16,24,40,.24);
  display:flex;
  align-items:center;
  justify-content:center;
  padding:0;
  transition:transform .18s ease, box-shadow .18s ease, background .18s ease;
  -webkit-tap-highlight-color:transparent;
}
.floating-nav-trigger:active{transform:translateY(-50%) scale(.94)}
.floating-nav-trigger.open{background:linear-gradient(145deg,#c8161d,#971118);box-shadow:0 12px 28px rgba(151,17,24,.28)}
.floating-nav-trigger-icon{
  width:20px;
  height:20px;
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:3px;
  transition:transform .2s ease;
}
.floating-nav-trigger-icon i{
  display:block;
  border-radius:3px;
  background:#fff;
}
.floating-nav-trigger.open .floating-nav-trigger-icon{transform:rotate(45deg)}

.floating-nav-backdrop{
  position:fixed;
  inset:0;
  z-index:1398;
  background:rgba(16,24,40,.16);
  opacity:0;
  visibility:hidden;
  transition:opacity .18s ease, visibility .18s ease;
  backdrop-filter:blur(1px);
}
.floating-nav-backdrop.open{opacity:1;visibility:visible}

.floating-nav-panel{
  position:fixed;
  z-index:1401;
  right:66px;
  top:50%;
  width:min(310px,calc(100vw - 86px));
  max-height:min(74vh,610px);
  padding:9px;
  border:1px solid rgba(228,231,236,.95);
  border-radius:22px;
  background:rgba(255,255,255,.98);
  box-shadow:0 24px 60px rgba(16,24,40,.24);
  transform:translateY(-50%) translateX(12px) scale(.96);
  transform-origin:right center;
  opacity:0;
  visibility:hidden;
  pointer-events:none;
  overflow-y:auto;
  overscroll-behavior:contain;
  scrollbar-width:none;
  transition:transform .2s ease, opacity .18s ease, visibility .18s ease;
}
.floating-nav-panel::-webkit-scrollbar{display:none}
.floating-nav-panel.open{
  transform:translateY(-50%) translateX(0) scale(1);
  opacity:1;
  visibility:visible;
  pointer-events:auto;
}
.floating-nav-list{display:flex;flex-direction:column;gap:6px}
.floating-nav-item{
  width:100%;
  border:1px solid #e4e7ec;
  border-radius:14px;
  background:#f2f4f7;
  color:#101828;
  padding:10px 11px;
  display:grid;
  grid-template-columns:34px 1fr 18px;
  gap:9px;
  align-items:center;
  text-align:left;
  box-shadow:0 1px 2px rgba(16,24,40,.03);
}
.floating-nav-item:active{background:#e9edf2;transform:scale(.99)}
.floating-nav-item-icon{
  width:34px;
  height:34px;
  border-radius:10px;
  display:flex;
  align-items:center;
  justify-content:center;
  background:#fff;
  border:1px solid #e4e7ec;
  font-size:16px;
}
.floating-nav-item-copy{min-width:0}
.floating-nav-item-copy strong{
  display:block;
  font-size:12.5px;
  line-height:1.12;
  font-weight:950;
  color:#101828;
}
.floating-nav-item-copy small{
  display:block;
  margin-top:3px;
  font-size:10px;
  line-height:1.22;
  font-weight:750;
  color:#667085;
}
.floating-nav-item-arrow{
  color:#98a2b3;
  font-size:18px;
  line-height:1;
  font-weight:900;
  text-align:center;
}

@media (max-width:380px){
  .floating-nav-trigger{right:8px;width:44px;height:44px}
  .floating-nav-panel{right:58px;width:calc(100vw - 72px);padding:7px;border-radius:18px}
  .floating-nav-item{grid-template-columns:31px 1fr 16px;padding:9px;gap:7px}
  .floating-nav-item-icon{width:31px;height:31px;font-size:15px}
  .floating-nav-item-copy strong{font-size:11.5px}
  .floating-nav-item-copy small{font-size:9.3px}
}
/* floating-nav-v1:end */
'''
text = text.replace('</style>', css + '\n</style>', 1)

html = r'''
<!-- floating-nav-v1:start -->
<div class="floating-nav-backdrop" id="floatingNavBackdrop" aria-hidden="true"></div>
<button class="floating-nav-trigger" id="floatingNavTrigger" type="button" aria-label="Abrir navegação" aria-expanded="false">
  <span class="floating-nav-trigger-icon" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
</button>
<div class="floating-nav-panel" id="floatingNavPanel" aria-hidden="true">
  <div class="floating-nav-list">
    <button class="floating-nav-item" type="button" data-nav-target=".form.section">
      <span class="floating-nav-item-icon">🧮</span>
      <span class="floating-nav-item-copy"><strong>Simulação</strong><small>Carta, prazo e parcela</small></span>
      <span class="floating-nav-item-arrow">›</span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target=".lance-list.section">
      <span class="floating-nav-item-icon">🎯</span>
      <span class="floating-nav-item-copy"><strong>Tipos de lance</strong><small>Veja as opções disponíveis</small></span>
      <span class="floating-nav-item-arrow">›</span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target=".projection-v2.section">
      <span class="floating-nav-item-icon">📈</span>
      <span class="floating-nav-item-copy"><strong>Projeção anual</strong><small>Evolução da carta e parcela</small></span>
      <span class="floating-nav-item-arrow">›</span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target=".contemplation-scenarios.section">
      <span class="floating-nav-item-icon">💡</span>
      <span class="floating-nav-item-copy"><strong>Após contemplar</strong><small>Cenários de uso da carta</small></span>
      <span class="floating-nav-item-arrow">›</span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target=".comparison-section.section">
      <span class="floating-nav-item-icon">⚖️</span>
      <span class="floating-nav-item-copy"><strong>Consórcio x financiamento</strong><small>Compare custos e parcelas</small></span>
      <span class="floating-nav-item-arrow">›</span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target="#inccSalarySection">
      <span class="floating-nav-item-icon">💰</span>
      <span class="floating-nav-item-copy"><strong>Parcela x salário</strong><small>Comparativo dos últimos 18 anos</small></span>
      <span class="floating-nav-item-arrow">›</span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target="#rentInvestmentSection">
      <span class="floating-nav-item-icon">🏦</span>
      <span class="floating-nav-item-copy"><strong>Consórcio + aluguel</strong><small>Sobras aplicadas no Tesouro</small></span>
      <span class="floating-nav-item-arrow">›</span>
    </button>
    <button class="floating-nav-item" type="button" data-nav-target="#rentInvestmentTimeline" data-open-details="true">
      <span class="floating-nav-item-icon">🗓️</span>
      <span class="floating-nav-item-copy"><strong>Evolução dos aportes</strong><small>Veja os valores ano a ano</small></span>
      <span class="floating-nav-item-arrow">›</span>
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
  const backdrop = document.getElementById('floatingNavBackdrop');
  if(!trigger || !panel || !backdrop) return;

  const setOpen = (open) => {
    trigger.classList.toggle('open', open);
    panel.classList.toggle('open', open);
    backdrop.classList.toggle('open', open);
    trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    panel.setAttribute('aria-hidden', open ? 'false' : 'true');
    backdrop.setAttribute('aria-hidden', open ? 'false' : 'true');
  };

  trigger.addEventListener('click', () => setOpen(!panel.classList.contains('open')));
  backdrop.addEventListener('click', () => setOpen(false));

  panel.querySelectorAll('[data-nav-target]').forEach(button => {
    button.addEventListener('click', () => {
      const selector = button.getAttribute('data-nav-target');
      const target = selector ? document.querySelector(selector) : null;
      if(!target) return;

      if(button.getAttribute('data-open-details') === 'true' && target.tagName === 'DETAILS'){
        target.open = true;
      }

      setOpen(false);
      requestAnimationFrame(() => {
        target.scrollIntoView({behavior:'smooth', block:'start'});
      });
    });
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
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v13', sw)
    sw_path.write_text(sw, encoding='utf-8')
