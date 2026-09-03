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
  const current = Math.min(
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

  // Remove o modal de dentro do card antes de exibi-lo.
  // Assim position:fixed é sempre relativo à viewport, nunca à seção.
  if(modal.parentElement !== document.body){
    document.body.appendChild(modal);
  }

  // Remove o foco de seções antes do primeiro frame visível do modal.
  document.body.classList.remove("section-focus-mode");
  document.querySelectorAll(".section-focus-active,.section-focus-dim").forEach(el=>{
    el.classList.remove("section-focus-active","section-focus-dim");
  });

  const pageY = window.scrollY || document.documentElement.scrollTop || 0;
  modal.dataset.pageScrollY = String(pageY);
  modal.dataset.prevBodyOverflow = document.body.style.overflow || "";
  modal.dataset.prevHtmlOverflow = document.documentElement.style.overflow || "";

  // Trava o fundo sem alterar a posição da página.
  document.body.style.overflow = "hidden";
  document.documentElement.style.overflow = "hidden";

  const label = projectionMode === "year" ? "ano" : "mês";
  $("projectionModalSubtitle").textContent = `Selecione o ${label} previsto`;
  modal.setAttribute("aria-hidden", "false");
  modal.classList.add("open");
  renderProjectionOptions();
}
''')

text = replace_function(text, 'closeProjectionModal', 'toggleProjectionAccordion', r'''
function closeProjectionModal(){
  const modal = $("projectionModal");
  if(!modal) return;

  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");

  document.body.style.overflow = modal.dataset.prevBodyOverflow || "";
  document.documentElement.style.overflow = modal.dataset.prevHtmlOverflow || "";
}
''')

text = re.sub(
    r'\n?/\* restore-contemplation-month-year:start \*/.*?/\* restore-contemplation-month-year:end \*/\n?',
    '\n',
    text,
    flags=re.S,
)

css = r'''
/* restore-contemplation-month-year:start */
.contemplation-picker-row .period-choice{display:block!important}
#projectionModalSubtitle{display:block!important}

/* Modal já nasce no estado final, sem animação de posição. */
.contemplation-modal{
  position:fixed!important;
  inset:0!important;
  display:none!important;
  align-items:flex-end!important;
  justify-content:center!important;
  overscroll-behavior:contain!important;
  transform:none!important;
  transition:none!important;
}
.contemplation-modal.open{
  display:flex!important;
}
.contemplation-sheet{
  transform:none!important;
  transition:none!important;
  margin:0!important;
}
.contemplation-accordion{
  overscroll-behavior:contain!important;
}
/* restore-contemplation-month-year:end */
'''
text = text.replace('</style>', css + '\n</style>', 1)

index_path.write_text(text, encoding='utf-8')

sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v27', sw)
    sw_path.write_text(sw, encoding='utf-8')
