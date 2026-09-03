from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Remove somente o gesto de arrastar o painel lateral para a direita para fechar.
# Mantém o gesto da pequena alça para abrir o menu.
text = re.sub(
    r'\n\s*let panelStartX = null;\n',
    '\n',
    text,
    count=1,
)

text = re.sub(
    r'''\n\s*panel\.addEventListener\('touchstart',\s*event\s*=>\s*\{.*?\}\s*,\s*\{passive:true\}\);\s*\n\s*panel\.addEventListener\('touchend',\s*event\s*=>\s*\{.*?\}\s*,\s*\{passive:true\}\);''',
    '',
    text,
    count=1,
    flags=re.S,
)

index_path.write_text(text, encoding='utf-8')

# Força o PWA a buscar esta versão.
sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v29', sw)
    sw_path.write_text(sw, encoding='utf-8')
