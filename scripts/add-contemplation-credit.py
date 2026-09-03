from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Remove versão anterior, se existir.
text = re.sub(r'\n?<!-- contemplation-credit-v1:start -->.*?<!-- contemplation-credit-v1:end -->\n?', '\n', text, flags=re.S)
text = re.sub(r'\n?/\* contemplation-credit-v1:start \*/.*?/\* contemplation-credit-v1:end \*/\n?', '\n', text, flags=re.S)
text = re.sub(r'\n?/\* contemplation-credit-v1-js:start \*/.*?/\* contemplation-credit-v1-js:end \*/\n?', '\n', text, flags=re.S)

credit_html = r'''
<!-- contemplation-credit-v1:start -->
<div class="contemplation-credit-quick credit-control">
  <label for="projectionCreditQuick">Valor da carta</label>

  <div class="credit-main contemplation-credit-main">
    <div class="credit-input-wrap">
      <span>R$</span>
      <input
        id="projectionCreditQuick"
        class="money-input"
        type="text"
        inputmode="decimal"
        autocomplete="off"
        enterkeyhint="done"
        value="0,00"
      >
    </div>

    <div class="credit-steps-mini contemplation-credit-steps">
      <button class="credit-step mini" type="button" data-main-credit-step="creditMinus100">-100</button>
      <button class="credit-step mini" type="button" data-main-credit-step="creditMinus10">-10</button>
      <button class="credit-step mini" type="button" data-main-credit-step="creditPlus10">+10</button>
      <button class="credit-step mini" type="button" data-main-credit-step="creditPlus100">+100</button>
    </div>
  </div>

  <div class="credit-shortcuts contemplation-credit-shortcuts" id="projectionCreditShortcuts"></div>
</div>
<!-- contemplation-credit-v1:end -->
'''

anchor = '          <div class="contemplation-accordion">'
if anchor in text:
    text = text.replace(anchor, credit_html + '\n' + anchor, 1)

css = r'''
/* contemplation-credit-v1:start */
.contemplation-credit-quick{
  margin:0 12px 12px;
  padding:0;
}
.contemplation-credit-quick>label{
  display:block;
  margin:0 0 7px 2px;
  color:#475467;
  font-size:11px;
  line-height:1.1;
  font-weight:900;
}
.contemplation-credit-main{
  width:100%;
}
.contemplation-credit-main .credit-input-wrap{
  width:100%;
}
.contemplation-credit-steps{
  width:100%;
}
.contemplation-credit-shortcuts{
  margin-top:8px;
  padding-bottom:1px;
}
#projectionCreditQuick{
  width:100%;
  min-width:0;
}
/* contemplation-credit-v1:end */
'''
text = text.replace('</style>', css + '\n</style>', 1)

js = r'''
/* contemplation-credit-v1-js:start */
(function(){
  const quick = document.getElementById('projectionCreditQuick');
  const source = document.getElementById('credit');
  const quickShortcuts = document.getElementById('projectionCreditShortcuts');
  const openBtn = document.getElementById('projectionNumberBtn');
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
        syncFromMain();
        requestAnimationFrame(renderQuickShortcuts);
      });
      quickShortcuts.appendChild(button);
    });
  };

  const refreshModalCredit = () => {
    syncFromMain();
    renderQuickShortcuts();
  };

  const applyQuickCredit = () => {
    const raw = quick.value;
    if(!raw || !String(raw).trim()){
      refreshModalCredit();
      return;
    }

    source.value = raw;

    if(typeof formatMoneyField === 'function'){
      formatMoneyField(source);
    }

    syncFromMain();

    if(typeof renderCreditShortcuts === 'function'){
      renderCreditShortcuts();
    }

    renderQuickShortcuts();

    if(typeof calculate === 'function'){
      calculate();
    }
  };

  document.querySelectorAll('[data-main-credit-step]').forEach(button => {
    button.addEventListener('click', () => {
      const mainId = button.getAttribute('data-main-credit-step');
      const mainButton = mainId ? document.getElementById(mainId) : null;
      if(mainButton){
        mainButton.click();
        refreshModalCredit();
      }
    });
  });

  openBtn?.addEventListener('click', () => {
    requestAnimationFrame(refreshModalCredit);
  });

  quick.addEventListener('focus', syncFromMain);
  quick.addEventListener('change', applyQuickCredit);
  quick.addEventListener('blur', applyQuickCredit);
  quick.addEventListener('keydown', event => {
    if(event.key === 'Enter'){
      event.preventDefault();
      applyQuickCredit();
      quick.blur();
    }
  });

  source.addEventListener('change', refreshModalCredit);
  refreshModalCredit();
})();
/* contemplation-credit-v1-js:end */
'''
text = text.replace('</body>', '<script>\n' + js + '\n</script>\n</body>', 1)

index_path.write_text(text, encoding='utf-8')

sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v18', sw)
    sw_path.write_text(sw, encoding='utf-8')
