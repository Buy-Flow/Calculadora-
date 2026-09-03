from pathlib import Path

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Deixa a tabela monetária legível no celular.
css_marker = '.incc-history-note{margin:7px 1px 0;color:#667085;font-size:7px;line-height:1.3;font-weight:700}'
css_extra = '''.incc-history-note{margin:7px 1px 0;color:#667085;font-size:7px;line-height:1.3;font-weight:700}\n.incc-money-summary{margin-top:8px;padding:10px;border:1px solid #b7e4c7;border-radius:12px;background:#f0fdf4}\n.incc-money-summary span{display:block;color:#52705d;font-size:7px;font-weight:900;text-transform:uppercase;letter-spacing:.2px}\n.incc-money-summary strong{display:block;margin-top:3px;color:#067647;font-size:19px;line-height:1;font-weight:950}\n.incc-money-summary small{display:block;margin-top:4px;color:#475467;font-size:7.5px;line-height:1.3;font-weight:750}\n.incc-history-table{min-width:440px}\n.incc-history-table td.money{white-space:nowrap;text-align:right;font-variant-numeric:tabular-nums}\n.incc-history-table td.diff-positive{white-space:nowrap;text-align:right;color:#067647;font-weight:950}\n.incc-history-value-sub{display:block;margin-top:1px;color:#98a2b3;font-size:6px;font-weight:750}'''
if '.incc-money-summary{' not in text:
    if css_marker not in text:
        raise SystemExit('CSS marker not found')
    text = text.replace(css_marker, css_extra, 1)

bars_end = '''      </div>\n\n      <div class="incc-client-argument">'''
money_summary = '''      </div>\n\n      <div class="incc-money-summary">\n        <span>Diferença acumulada em 2025</span>\n        <strong>R$ 395,83 a mais</strong>\n        <small>Partindo da mesma base de R$ 300 no fim de 2005: salário mínimo chegou a R$ 1.518,00; o mesmo valor reajustado apenas pelo INCC-M chegaria a aproximadamente R$ 1.122,17. O salário ficou cerca de 35,27% acima desse valor equivalente.</small>\n      </div>\n\n      <div class="incc-client-argument">'''
if 'Diferença acumulada em 2025' not in text:
    if bars_end not in text:
        raise SystemExit('Bars marker not found')
    text = text.replace(bars_end, money_summary, 1)

old_argument = '“O reajuste não aumenta só a parcela: ele também atualiza o valor da sua carta. E, olhando os últimos 20 anos, o salário mínimo subiu mais que o INCC-M em 15 deles. No acumulado, foram cerca de 406% contra 274% do INCC-M.”'
new_argument = '“O reajuste não aumenta só a parcela: ele também atualiza o valor da sua carta. Partindo de R$ 300, a evolução histórica do salário mínimo levaria esse valor a R$ 1.518, enquanto pelo INCC-M chegaria a cerca de R$ 1.122. É uma diferença de aproximadamente R$ 396 — e, em 15 dos últimos 20 anos, o salário mínimo subiu mais que o INCC-M.”'
if old_argument in text:
    text = text.replace(old_argument, new_argument, 1)

start = text.find('          <table class="incc-history-table">')
end = text.find('          </table>', start)
if start == -1 or end == -1:
    raise SystemExit('History table not found')
end += len('          </table>')

rows = [
(2006,'5,05%','16,67%','350,00','315,15','34,85'),
(2007,'6,03%','8,57%','380,00','334,15','45,85'),
(2008,'11,97%','9,21%','415,00','374,15','40,85'),
(2009,'3,21%','12,05%','465,00','386,16','78,84'),
(2010,'7,57%','9,68%','510,00','415,39','94,61'),
(2011,'7,58%','6,86%','545,00','446,88','98,12'),
(2012,'7,25%','14,13%','622,00','479,28','142,72'),
(2013,'8,07%','9,00%','678,00','517,96','160,04'),
(2014,'6,74%','6,78%','724,00','552,87','171,13'),
(2015,'7,22%','8,84%','788,00','592,79','195,21'),
(2016,'6,34%','11,68%','880,00','630,37','249,63'),
(2017,'4,03%','6,48%','937,00','655,77','281,23'),
(2018,'3,97%','1,81%','954,00','681,80','272,20'),
(2019,'4,13%','4,61%','998,00','709,96','288,04'),
(2020,'8,68%','4,71%','1.045,00','771,58','273,42'),
(2021,'14,03%','5,26%','1.100,00','879,84','220,16'),
(2022,'9,41%','10,18%','1.212,00','962,63','249,37'),
(2023,'3,32%','8,91%','1.320,00','994,59','325,41'),
(2024,'6,34%','6,97%','1.412,00','1.057,64','354,36'),
(2025,'6,10%','7,51%','1.518,00','1.122,17','395,83'),
]
body = []
for year, incc_pct, sal_pct, sal_value, incc_value, diff in rows:
    body.append(
        f'              <tr><td>{year}</td>'
        f'<td class="money">R$ {sal_value}<span class="incc-history-value-sub">+{sal_pct}</span></td>'
        f'<td class="money">R$ {incc_value}<span class="incc-history-value-sub">INCC {incc_pct}</span></td>'
        f'<td class="diff-positive">+R$ {diff}</td></tr>'
    )
new_table = '''          <table class="incc-history-table">\n            <thead><tr><th>Ano</th><th>Salário mínimo</th><th>Equivalente pelo INCC*</th><th>Diferença</th></tr></thead>\n            <tbody>\n''' + '\n'.join(body) + '''\n            </tbody>\n          </table>'''
text = text[:start] + new_table + text[end:]

old_note_start = '<p class="incc-history-note">'
note_start = text.find(old_note_start)
if note_start == -1:
    raise SystemExit('History note not found')
note_end = text.find('</p>', note_start)
if note_end == -1:
    raise SystemExit('History note end not found')
note_end += 4
new_note = '<p class="incc-history-note"><strong>* Equivalente pelo INCC:</strong> não é um salário oficial. É apenas uma simulação para comparação: usamos a mesma base de R$ 300 vigente no fim de 2005 e aplicamos, ano a ano, somente o INCC-M. A coluna “Salário mínimo” mostra o valor nominal oficial vigente no fim de cada ano. Desempenho passado não garante reajustes futuros e a renda individual do cliente pode ter trajetória diferente.</p>'
text = text[:note_start] + new_note + text[note_end:]

index_path.write_text(text, encoding='utf-8')

# Renova o cache offline para os aparelhos instalados receberem a nova tabela.
sw_path = Path('calculadora/service-worker.js')
sw = sw_path.read_text(encoding='utf-8')
sw = sw.replace('calculadora-ademicon-pwa-v3', 'calculadora-ademicon-pwa-v4')
sw = sw.replace('calculadora-ademicon-pwa-v2', 'calculadora-ademicon-pwa-v4')
sw_path.write_text(sw, encoding='utf-8')
