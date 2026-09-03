from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')


def replace_function(source, name, next_name, new_code):
    start = source.find(f'function {name}(')
    if start == -1:
        return source
    end = source.find(f'\nfunction {next_name}(', start)
    if end == -1:
        return source
    return source[:start] + new_code.rstrip() + '\n\n' + source[end + 1:]


# Restaura o comportamento original: número separado dos botões Mês/Ano.
text = replace_function(text, 'updateProjectionNumber', 'setProjectionContemplation', r'''
function updateProjectionNumber(){
  const input = $("projectionContemplation");
  const btn = $("projectionNumberBtn");
  if(btn && input) btn.textContent = input.value || "1";
}
''')

text = replace_function(text, 'renderProjectionOptions', 'openProjectionModal', r'''
function renderProjectionOptions(){
  const box = $("projectionOptions");
  if(!box) return;

  const max = projectionMaxValue();
  const current =
    Math.min(
      Math.max(parseInt($("projectionContemplation")?.value || "1",10) || 1,1),
      max
    );

  if(parseInt($("projectionContemplation").value || "1",10) !== current){
    $("projectionContemplation").value = current;
    updateProjectionNumber();
  }

  let options = "";
  for(let i=1;i<=max;i++){
    options += `
      <button
        type="button"
        class="contemplation-option${i === current ? " active" : ""}"
        data-projection-value="${i}"
      >${i}</button>`;
  }
  box.innerHTML = options;

  box.querySelectorAll("[data-projection-value]").forEach(btn=>{
    btn.onclick = ()=>{
      setProjectionContemplation(btn.dataset.projectionValue, false);
      closeProjectionModal();
    };
  });

  // Rola somente a área interna do modal. Não usa scrollIntoView,
  // pois no Android ele pode deslocar a página inteira para cima.
  requestAnimationFrame(()=>{
    const activeOption = box.querySelector(".contemplation-option.active");
    const scroller = box.closest(".contemplation-accordion");
    if(!activeOption || !scroller) return;

    const optionTop = activeOption.offsetTop;
    const optionBottom = optionTop + activeOption.offsetHeight;
    const visibleTop = scroller.scrollTop;
    const visibleBottom = visibleTop + scroller.clientHeight;

    if(optionTop < visibleTop){
      scroller.scrollTop = Math.max(optionTop - 8, 0);
    }else if(optionBottom > visibleBottom){
      scroller.scrollTop = Math.max(optionBottom - scroller.clientHeight + 8, 0);
    }
  });
}
''')

text = replace_function(text, 'openProjectionModal', 'closeProjectionModal', r'''
function openProjectionModal(){
  const modal = $("projectionModal");
  if(!modal) return;

  // Guarda a posição exata antes de abrir para impedir qualquer salto visual.
  const pageY = window.scrollY || document.documentElement.scrollTop || 0;
  modal.dataset.pageScrollY = String(pageY);

  const label = projectionMode === "year" ? "ano" : "mês";
  $("projectionModalSubtitle").textContent = `Selecione o ${label} previsto`;
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
  renderProjectionOptions();

  requestAnimationFrame(()=>{
    const currentY = window.scrollY || document.documentElement.scrollTop || 0;
    if(Math.abs(currentY - pageY) > 1){
      window.scrollTo(0, pageY);
    }
  });
}
''')

text = replace_function(text, 'closeProjectionModal', 'toggleProjectionAccordion', r'''
function closeProjectionModal(){
  const modal = $("projectionModal");
  if(!modal) return;

  const pageY = Number(modal.dataset.pageScrollY);
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");

  if(Number.isFinite(pageY)){
    requestAnimationFrame(()=>{
      const currentY = window.scrollY || document.documentElement.scrollTop || 0;
      if(Math.abs(currentY - pageY) > 1){
        window.scrollTo(0, pageY);
      }
    });
  }
}
''')

# A versão simplificada escondia os botões Mês/Ano. Reexibe no fim do CSS.
text = re.sub(
    r'\n?/\* restore-contemplation-month-year:start \*/.*?/\* restore-contemplation-month-year:end \*/\n?',
    '\n',
    text,
    flags=re.S,
)

css = r'''
/* restore-contemplation-month-year:start */
.contemplation-picker-row .period-choice{
  display:block!important;
}
#projectionModalSubtitle{
  display:block!important;
}
.contemplation-modal,
.contemplation-accordion{
  overscroll-behavior:contain;
}
/* restore-contemplation-month-year:end */
'''
text = text.replace('</style>', css + '\n</style>', 1)

index_path.write_text(text, encoding='utf-8')

# Força atualização do PWA.
sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v24', sw)
    sw_path.write_text(sw, encoding='utf-8')
