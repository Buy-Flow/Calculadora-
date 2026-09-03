from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Remove uma versão anterior do efeito, se existir.
text = re.sub(
    r'\n?/\* section-focus-v1:start \*/.*?/\* section-focus-v1:end \*/\n?',
    '\n',
    text,
    flags=re.S,
)
text = re.sub(
    r'\n?/\* section-focus-v1-js:start \*/.*?/\* section-focus-v1-js:end \*/\n?',
    '\n',
    text,
    flags=re.S,
)

css = r'''
/* section-focus-v1:start */
/*
  Destaca automaticamente a seção que ocupa a maior parte da tela.
  O efeito é propositalmente suave para preservar a leitura e o desempenho.
*/
.section{
  transition:opacity .24s ease, filter .24s ease, transform .24s ease, box-shadow .24s ease;
  transform-origin:center center;
}
body.section-focus-mode .section.section-focus-dim{
  opacity:.48;
  filter:blur(.9px) saturate(.82);
  transform:scale(.994);
}
body.section-focus-mode .section.section-focus-active{
  opacity:1;
  filter:none;
  transform:scale(1);
  position:relative;
  z-index:3;
  box-shadow:0 18px 44px rgba(16,24,40,.14);
}

@media (min-width:769px){
  body.section-focus-mode .section.section-focus-dim{
    opacity:.56;
    filter:blur(.7px) saturate(.86);
  }
}

@media (prefers-reduced-motion:reduce){
  .section{transition:none!important}
}
/* section-focus-v1:end */
'''
text = text.replace('</style>', css + '\n</style>', 1)

js = r'''
/* section-focus-v1-js:start */
(function(){
  const sections = Array.from(document.querySelectorAll('.section'));
  if(sections.length < 2) return;

  let ticking = false;

  const clearFocus = () => {
    document.body.classList.remove('section-focus-mode');
    sections.forEach(section => {
      section.classList.remove('section-focus-active', 'section-focus-dim');
    });
  };

  const modalIsOpen = () => !!document.querySelector(
    'dialog[open], .projection-modal.open, .modal.open, [role="dialog"][aria-hidden="false"]'
  );

  const updateFocus = () => {
    ticking = false;

    if(modalIsOpen()){
      clearFocus();
      return;
    }

    const vh = Math.max(window.innerHeight || 0, document.documentElement.clientHeight || 0);
    if(!vh){
      clearFocus();
      return;
    }

    let bestSection = null;
    let bestVisible = 0;
    let secondVisible = 0;

    sections.forEach(section => {
      const rect = section.getBoundingClientRect();
      const visible = Math.max(
        0,
        Math.min(rect.bottom, vh) - Math.max(rect.top, 0)
      );

      if(visible > bestVisible){
        secondVisible = bestVisible;
        bestVisible = visible;
        bestSection = section;
      }else if(visible > secondVisible){
        secondVisible = visible;
      }
    });

    const viewportShare = bestVisible / vh;
    const leadShare = (bestVisible - secondVisible) / vh;

    // Só ativa quando uma seção realmente domina a tela.
    if(!bestSection || viewportShare < .56 || leadShare < .10){
      clearFocus();
      return;
    }

    document.body.classList.add('section-focus-mode');
    sections.forEach(section => {
      const active = section === bestSection;
      section.classList.toggle('section-focus-active', active);
      section.classList.toggle('section-focus-dim', !active);
    });
  };

  const scheduleUpdate = () => {
    if(ticking) return;
    ticking = true;
    requestAnimationFrame(updateFocus);
  };

  window.addEventListener('scroll', scheduleUpdate, {passive:true});
  window.addEventListener('resize', scheduleUpdate, {passive:true});
  document.addEventListener('click', () => setTimeout(scheduleUpdate, 0), true);

  if('ResizeObserver' in window){
    const observer = new ResizeObserver(scheduleUpdate);
    sections.forEach(section => observer.observe(section));
  }

  scheduleUpdate();
})();
/* section-focus-v1-js:end */
'''
text = text.replace('</body>', '<script>\n' + js + '\n</script>\n</body>', 1)

index_path.write_text(text, encoding='utf-8')

# Força o PWA a buscar a versão nova.
sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v20', sw)
    sw_path.write_text(sw, encoding='utf-8')
