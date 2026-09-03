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
<div class="contemplation-credit-quick">
  <label for="projectionCreditQuick">Valor da carta</label>
  <div class="contemplation-credit-input-wrap">
    <span>R$</span>
    <input
      id="projectionCreditQuick"
      type="text"
      inputmode="decimal"
      autocomplete="off"
      enterkeyhint="done"
      value="0,00"
    >
  </div>
</div>
<!-- contemplation-credit-v1:end -->
'''

anchor = '          <div class="contemplation-accordion">'
if anchor in text:
    text = text.replace(anchor, credit_html + '\n' + anchor, 1)

css = r'''
/* contemplation-credit-v1:start */
.contemplation-credit-quick{
  margin:0 12px 10px;
  padding:10px;
  border:1px solid #e4e7ec;
  border-radius:16px;
  background:#fff;
  box-shadow:0 3px 10px rgba(16,24,40,.05);
}
.contemplation-credit-quick label{
  display:block;
  margin-bottom:6px;
  color:#475467;
  font-size:11px;
  line-height:1.1;
  font-weight:900;
}
.contemplation-credit-input-wrap{
  height:42px;
  display:flex;
  align-items:center;
  gap:6px;
  padding:0 11px;
  border:1px solid #d0d5dd;
  border-radius:13px;
  background:#fff;
}
.contemplation-credit-input-wrap:focus-within{
  border-color:#98a2b3;
  box-shadow:0 0 0 3px rgba(152,162,179,.12);
}
.contemplation-credit-input-wrap span{
  color:#667085;
  font-size:12px;
  font-weight:900;
}
#projectionCreditQuick{
  width:100%;
  min-width:0;
  border:0!important;
  outline:0!important;
  background:transparent!important;
  color:#101828;
  font-size:17px!important;
  line-height:1!important;
  font-weight:950!important;
  padding:0!important;
  box-shadow:none!important;
}
/* contemplation-credit-v1:end */
'''
text = text.replace('</style>', css + '\n</style>', 1)

js = r'''
/* contemplation-credit-v1-js:start */
(function(){
  const quick = document.getElementById('projectionCreditQuick');
  const source = document.getElementById('credit');
  const openBtn = document.getElementById('projectionNumberBtn');
  if(!quick || !source) return;

  const syncFromMain = () => {
    quick.value = source.value || '0,00';
  };

  const applyQuickCredit = () => {
    const raw = quick.value;
    if(!raw || !String(raw).trim()){
      syncFromMain();
      return;
    }

    source.value = raw;

    if(typeof formatMoneyField === 'function'){
      formatMoneyField(source);
    }

    quick.value = source.value;

    if(typeof renderCreditShortcuts === 'function'){
      renderCreditShortcuts();
    }

    if(typeof calculate === 'function'){
      calculate();
    }
  };

  openBtn?.addEventListener('click', () => {
    requestAnimationFrame(syncFromMain);
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

  source.addEventListener('change', syncFromMain);
  syncFromMain();
})();
/* contemplation-credit-v1-js:end */
'''
text = text.replace('</body>', '<script>\n' + js + '\n</script>\n</body>', 1)

index_path.write_text(text, encoding='utf-8')

sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v17', sw)
    sw_path.write_text(sw, encoding='utf-8')
