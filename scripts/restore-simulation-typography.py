from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Remove uma versão anterior desta correção, se existir.
text = re.sub(
    r'\n?/\* simulation-original-type:start \*/.*?/\* simulation-original-type:end \*/\n?',
    '\n',
    text,
    flags=re.S,
)

css = r'''
/* simulation-original-type:start */
/* Mantém o card Dados da simulação com a tipografia compacta original. */
.form.section .tag{font-size:11px!important}
.form.section .field label{font-size:11px!important;line-height:normal!important}
.form.section .field small{font-size:11px!important;line-height:normal!important}
.form.section .compact-grid .field label{font-size:9px!important}
.form.section .compact-projection small{font-size:9px!important;line-height:normal!important}
.form.section .credit-control label{font-size:10px!important}
.form.section .credit-chip{font-size:10px!important}
.form.section .triple-btn{font-size:11px!important}
.form.section #insuranceBtn{font-size:10.5px!important}
/* simulation-original-type:end */
'''

text = text.replace('</style>', css + '\n</style>', 1)
index_path.write_text(text, encoding='utf-8')

# Força atualização do PWA após a correção visual.
sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v21', sw)
    sw_path.write_text(sw, encoding='utf-8')
