from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Remove somente o atalho "Aportes" do menu lateral.
text = re.sub(
    r'\s*<button class="floating-nav-item" type="button" data-nav-target="#rentInvestmentTimeline" data-open-details="true">.*?<strong>Aportes</strong>.*?</button>',
    '',
    text,
    count=1,
    flags=re.S,
)

index_path.write_text(text, encoding='utf-8')

# Força atualização do PWA.
sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v19', sw)
    sw_path.write_text(sw, encoding='utf-8')
