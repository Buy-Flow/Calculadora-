from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Remove qualquer versão anterior dos controles rápidos do menu.
text = re.sub(r'\n?<!-- contemplation-credit-v1:start -->.*?<!-- contemplation-credit-v1:end -->\n?', '\n', text, flags=re.S)
text = re.sub(r'\n?/\* contemplation-credit-v1:start \*/.*?/\* contemplation-credit-v1:end \*/\n?', '\n', text, flags=re.S)
text = re.sub(r'\n?/\* contemplation-credit-v1-js:start \*/.*?/\* contemplation-credit-v1-js:end \*/\n?', '\n', text, flags=re.S)

# O crédito fica no menu lateral, nunca dentro do pop-up de contemplação.
credit_html = r'''
<!-- contemplation-credit-v1:start -->
<div class="floating-nav-credit" id="floatingNavCredit">
  <label for="navCreditQuick">Valor da carta</label>

  <div class="floating-nav-credit-input">
    <span>R$</span>
    <input
      id="navCreditQuick"
      type="text"
      inputmode="decimal"
      autocomplete="off"
      enterkeyhint="done"
      value="0,00"
    >
  </div>

  <div class="floating-nav-credit-steps">
    <button type="button" data-main-credit-step="creditMinus100">-100</button>
    <button type="button" data-main-credit-step="creditMinus10">-10</button>
    <button type="button" data-main-credit-step="creditPlus10">+10</button>
    <button type="button" data-main-credit-step="creditPlus100">+100</button>
  </div>

  <div class="floating-nav-credit-shortcuts" id="navCreditShortcuts"></div>
</div>
<!-- contemplation-credit-v1:end -->
'''

anchor = '    <button class="floating-nav-item contemplation-shortcut"'
if anchor in text and 'id="floatingNavCredit"' not in text:
    text = text.replace(anchor, credit_html + '\n' + anchor, 1)

# Transforma Contemplação prevista em um controle rápido sempre visível.
# O título continua abrindo o seletor completo; os chips alteram direto.
contemplation_html = r'''
<div class="floating-nav-contemplation" id="floatingNavContemplation">
  <button class="floating-nav-contemplation-head" type="button" data-nav-action="contemplation">
    <span class="floating-nav-item-icon">📅</span>
    <span>Contemplação prevista</span>
  </button>
  <div class="floating-nav-contemplation-shortcuts" id="navContemplationShortcuts"></div>
</div>
'''
text = re.sub(
    r'    <button class="floating-nav-item contemplation-shortcut".*?</button>',
    contemplation_html.rstrip(),
    text,
    count=1,
    flags=re.S,
)

css = r'''
/* contemplation-credit-v1:start */
/* O seletor de contemplação não altera a cor do conteúdo ao fundo. */
.contemplation-modal{
  background:transparent!important;
  backdrop-filter:none!important;
  -webkit-backdrop-filter:none!important;
}

/* Crédito rápido dentro do menu lateral. */
.floating-nav-credit,
.floating-nav-contemplation{
  width:100%;
  padding:9px;
  border:1px solid #e4e7ec;
  border-radius:17px;
  background:#fff;
  box-shadow:0 4px 12px rgba(16,24,40,.07);
}
.floating-nav-credit>label{
  display:block;
  margin:0 0 6px 1px;
  color:#667085;
  font-size:10px;
  line-height:1;
  font-weight:900;
  text-transform:uppercase;
  letter-spacing:.2px;
}
.floating-nav-credit-input{
  height:38px;
  display:flex;
  align-items:center;
  gap:5px;
  padding:0 9px;
  border:1px solid #d0d5dd;
  border-radius:12px;
  background:#fff;
}
.floating-nav-credit-input span{
  color:#667085;
  font-size:11px;
  font-weight:900;
}
.floating-nav-credit-input input{
  min-width:0;
  width:100%;
  border:0;
  outline:0;
  background:transparent;
  color:#101828;
  font-size:15px;
  font-weight:950;
  padding:0;
}
.floating-nav-credit-steps{
  display:grid;
  grid-template-columns:repeat(4,minmax(0,1fr));
  gap:5px;
  margin-top:6px;
}
.floating-nav-credit-steps button{
  height:30px;
  padding:0 2px;
  border:1px solid #e4e7ec;
  border-radius:10px;
  background:#fff;
  color:#b42318;
  font-size:10px;
  font-weight:950;
}
.floating-nav-credit-shortcuts,
.floating-nav-contemplation-shortcuts{
  display:flex;
  gap:5px;
  overflow-x:auto;
  scrollbar-width:none;
  overscroll-behavior-x:contain;
  -webkit-overflow-scrolling:touch;
}
.floating-nav-credit-shortcuts{padding-top:6px}
.floating-nav-credit-shortcuts::-webkit-scrollbar,
.floating-nav-contemplation-shortcuts::-webkit-scrollbar{display:none}
.floating-nav-credit-shortcuts .credit-chip{
  flex:0 0 auto;
  padding:5px 7px;
  font-size:9.5px!important;
  border-radius:999px;
}

/* Contemplação rápida: título + chips horizontais, igual aos atalhos da carta. */
.floating-nav-contemplation{
  border-color:#fecaca;
  box-shadow:0 4px 12px rgba(200,22,29,.08);
}
.floating-nav-contemplation-head{
  width:100%;
  min-height:34px;
  padding:0 1px 7px;
  border:0;
  background:transparent;
  color:#101828;
  display:grid;
  grid-template-columns:28px 1fr;
  gap:9px;
  align-items:center;
  text-align:left;
  font-size:12px;
  line-height:1.08;
  font-weight:900;
}
.floating-nav-contemplation-head .floating-nav-item-icon{
  background:#fff5f5;
  border-color:#fee2e2;
}
.floating-nav-contemplation-shortcuts{
  padding:1px 0 0;
}
.floating-nav-contemplation-chip{
  flex:0 0 auto;
  min-height:30px;
  padding:5px 9px;
  border:1px solid #e4e7ec;
  border-radius:999px;
  background:#fff;
  color:#475467;
  font-size:10px;
  line-height:1;
  font-weight:900;
  white-space:nowrap;
}
.floating-nav-contemplation-chip.active{
  background:#fff1f2;
  border-color:#efc5c8;
  color:#c8161d;
}
/* contemplation-credit-v1:end */
'''
text = text.replace('</style>', css + '\n</style>', 1)

js = r'''
/* contemplation-credit-v1-js:start */
(function(){
  const quick = document.getElementById('navCreditQuick');
  const source = document.getElementById('credit');
  const quickShortcuts = document.getElementById('navCreditShortcuts');
  const contemplationShortcuts = document.getElementById('navContemplationShortcuts');
  const panel = document.getElementById('floatingNavPanel');
  const trigger = document.getElementById('floatingNavTrigger');
  if(!quick || !source) return;

  const syncFromMain = () => {
    quick.value = source.value || '0,00';
  };

  const renderQuickShortcuts = () => {
    if(!quickShortcuts) return;

    if(typeof renderCreditShortcuts === 'function'){
      renderCreditShortcuts();
    }

    const mainButtons = Array.from(
      document.querySelectorAll('#creditShortcuts .credit-chip')
    );

    quickShortcuts.innerHTML = '';

    mainButtons.forEach(mainButton => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = mainButton.className;
      button.textContent = mainButton.textContent;
      button.disabled = !!mainButton.disabled;
      button.addEventListener('click', () => {
        mainButton.click();
        refreshMenuControls();
      });
      quickShortcuts.appendChild(button);
    });
  };

  const renderContemplationShortcuts = () => {
    if(!contemplationShortcuts) return;

    const monthsInput = document.getElementById('months');
    const projectionInput = document.getElementById('projectionContemplation');
    const totalMonths = Math.max(parseInt(monthsInput?.value || '1', 10) || 1, 1);
    const totalYears = Math.max(Math.ceil(totalMonths / 12), 1);
    const currentMonth = typeof projectionContemplationMonth === 'function'
      ? projectionContemplationMonth()
      : 1;

    const items = [
      {kind:'month', value:1, month:1, label:'1º mês'}
    ];

    for(let year=1; year<=totalYears; year++){
      items.push({
        kind:'year',
        value:year,
        month:Math.min(year * 12, totalMonths),
        label:`${year}º ano`
      });
    }

    contemplationShortcuts.innerHTML = '';

    items.forEach(item => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'floating-nav-contemplation-chip' +
        (currentMonth === item.month ? ' active' : '');
      button.textContent = item.label;
      button.dataset.kind = item.kind;
      button.dataset.value = String(item.value);

      button.addEventListener('click', event => {
        event.preventDefault();
        event.stopPropagation();
        if(!projectionInput) return;

        projectionMode = item.kind === 'year' ? 'year' : 'month';
        projectionInput.value = String(item.value);

        document.getElementById('projectionYearBtn')?.classList.toggle('active', projectionMode === 'year');
        document.getElementById('projectionMonthBtn')?.classList.toggle('active', projectionMode === 'month');

        if(typeof updateProjectionNumber === 'function'){
          updateProjectionNumber();
        }
        if(typeof calculate === 'function'){
          calculate();
        }

        renderContemplationShortcuts();
      });

      contemplationShortcuts.appendChild(button);
    });

    requestAnimationFrame(() => {
      const activeChip = contemplationShortcuts.querySelector('.floating-nav-contemplation-chip.active');
      if(!activeChip) return;
      const left = activeChip.offsetLeft;
      const right = left + activeChip.offsetWidth;
      const visibleLeft = contemplationShortcuts.scrollLeft;
      const visibleRight = visibleLeft + contemplationShortcuts.clientWidth;
      if(left < visibleLeft){
        contemplationShortcuts.scrollLeft = Math.max(left - 6, 0);
      }else if(right > visibleRight){
        contemplationShortcuts.scrollLeft = Math.max(right - contemplationShortcuts.clientWidth + 6, 0);
      }
    });
  };

  const refreshMenuControls = () => {
    syncFromMain();
    renderQuickShortcuts();
    renderContemplationShortcuts();
  };

  const applyQuickCredit = () => {
    const raw = quick.value;
    if(!raw || !String(raw).trim()){
      refreshMenuControls();
      return;
    }

    source.value = raw;

    if(typeof formatMoneyField === 'function'){
      formatMoneyField(source);
    }

    if(typeof renderCreditShortcuts === 'function'){
      renderCreditShortcuts();
    }

    if(typeof calculate === 'function'){
      calculate();
    }

    refreshMenuControls();
  };

  document.querySelectorAll('#floatingNavCredit [data-main-credit-step]').forEach(button => {
    button.addEventListener('click', () => {
      const mainId = button.getAttribute('data-main-credit-step');
      const mainButton = mainId ? document.getElementById(mainId) : null;
      if(mainButton){
        mainButton.click();
        refreshMenuControls();
      }
    });
  });

  trigger?.addEventListener('click', () => requestAnimationFrame(refreshMenuControls));

  if(panel && 'MutationObserver' in window){
    const observer = new MutationObserver(() => {
      if(panel.classList.contains('open')) refreshMenuControls();
    });
    observer.observe(panel, {attributes:true, attributeFilter:['class']});
  }

  quick.addEventListener('change', applyQuickCredit);
  quick.addEventListener('blur', applyQuickCredit);
  quick.addEventListener('keydown', event => {
    if(event.key === 'Enter'){
      event.preventDefault();
      applyQuickCredit();
      quick.blur();
    }
  });

  source.addEventListener('change', refreshMenuControls);
  refreshMenuControls();
})();
/* contemplation-credit-v1-js:end */
'''
text = text.replace('</body>', '<script>\n' + js + '\n</script>\n</body>', 1)

index_path.write_text(text, encoding='utf-8')

sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v27', sw)
    sw_path.write_text(sw, encoding='utf-8')
