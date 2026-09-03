from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Remove qualquer versão anterior do ajuste de crédito.
text = re.sub(r'\n?<!-- contemplation-credit-v1:start -->.*?<!-- contemplation-credit-v1:end -->\n?', '\n', text, flags=re.S)
text = re.sub(r'\n?/\* contemplation-credit-v1:start \*/.*?/\* contemplation-credit-v1:end \*/\n?', '\n', text, flags=re.S)
text = re.sub(r'\n?/\* contemplation-credit-v1-js:start \*/.*?/\* contemplation-credit-v1-js:end \*/\n?', '\n', text, flags=re.S)

# O crédito não deve aparecer dentro do pop-up de contemplação.
# Ele fica somente na tela principal e no menu lateral.
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

# Insere o ajuste logo antes do atalho Contemplação prevista.
anchor = '    <button class="floating-nav-item contemplation-shortcut"'
if anchor in text and 'id="floatingNavCredit"' not in text:
    text = text.replace(anchor, credit_html + '\n' + anchor, 1)

css = r'''
/* contemplation-credit-v1:start */
/* O seletor de contemplação não altera a cor do conteúdo ao fundo. */
.contemplation-modal{
  background:transparent!important;
  backdrop-filter:none!important;
  -webkit-backdrop-filter:none!important;
}

/* Crédito rápido dentro do menu lateral. */
.floating-nav-credit{
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
.floating-nav-credit-shortcuts{
  display:flex;
  gap:5px;
  overflow-x:auto;
  padding-top:6px;
  scrollbar-width:none;
}
.floating-nav-credit-shortcuts::-webkit-scrollbar{display:none}
.floating-nav-credit-shortcuts .credit-chip{
  flex:0 0 auto;
  padding:5px 7px;
  font-size:9.5px!important;
  border-radius:999px;
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
        refreshMenuCredit();
      });
      quickShortcuts.appendChild(button);
    });
  };

  const refreshMenuCredit = () => {
    syncFromMain();
    renderQuickShortcuts();
  };

  const applyQuickCredit = () => {
    const raw = quick.value;
    if(!raw || !String(raw).trim()){
      refreshMenuCredit();
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

    refreshMenuCredit();
  };

  document.querySelectorAll('#floatingNavCredit [data-main-credit-step]').forEach(button => {
    button.addEventListener('click', () => {
      const mainId = button.getAttribute('data-main-credit-step');
      const mainButton = mainId ? document.getElementById(mainId) : null;
      if(mainButton){
        mainButton.click();
        refreshMenuCredit();
      }
    });
  });

  trigger?.addEventListener('click', () => requestAnimationFrame(refreshMenuCredit));

  if(panel && 'MutationObserver' in window){
    const observer = new MutationObserver(() => {
      if(panel.classList.contains('open')) refreshMenuCredit();
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

  source.addEventListener('change', refreshMenuCredit);
  refreshMenuCredit();
})();
/* contemplation-credit-v1-js:end */
'''
text = text.replace('</body>', '<script>\n' + js + '\n</script>\n</body>', 1)

index_path.write_text(text, encoding='utf-8')

sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v23', sw)
    sw_path.write_text(sw, encoding='utf-8')
