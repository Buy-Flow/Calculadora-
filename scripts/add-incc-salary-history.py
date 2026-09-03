from pathlib import Path

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Atualiza os cards principais: substitui o pouco intuitivo "15 de 20 / 5 de 20"
# por métricas diretamente comparáveis usando a mesma base de R$ 300.
old_salary_card = '''        <div class="incc-history-card salary">
          <span>Salário mínimo subiu mais</span>
          <strong>15 de 20 anos</strong>
          <small>Acumulado aproximado: +406% • média composta: 8,44% a.a.</small>
        </div>'''
new_salary_card = '''        <div class="incc-history-card salary">
          <span>Média anual do salário mínimo</span>
          <strong>8,44% a.a.</strong>
          <small>R$ 300 → R$ 1.518,00 • valorização acumulada de +406%</small>
        </div>'''
if old_salary_card in text:
    text = text.replace(old_salary_card, new_salary_card, 1)

old_incc_card = '''        <div class="incc-history-card incc">
          <span>INCC-M subiu mais</span>
          <strong>5 de 20 anos</strong>
          <small>Acumulado aproximado: +274% • média composta: 6,82% a.a.</small>
        </div>'''
new_incc_card = '''        <div class="incc-history-card incc">
          <span>Média anual do INCC-M</span>
          <strong>6,82% a.a.</strong>
          <small>R$ 300 → R$ 1.122,17 • valorização acumulada de +274%</small>
        </div>'''
if old_incc_card in text:
    text = text.replace(old_incc_card, new_incc_card, 1)

# Também lida com uma execução anterior já parcialmente alterada.
text = text.replace('<span>Salário mínimo subiu mais</span>\n          <strong>15 de 20 anos</strong>\n          <small>Acumulado aproximado: +406% • média composta: 8,44% a.a.</small>', '<span>Média anual do salário mínimo</span>\n          <strong>8,44% a.a.</strong>\n          <small>R$ 300 → R$ 1.518,00 • valorização acumulada de +406%</small>', 1)
text = text.replace('<span>INCC-M subiu mais</span>\n          <strong>5 de 20 anos</strong>\n          <small>Acumulado aproximado: +274% • média composta: 6,82% a.a.</small>', '<span>Média anual do INCC-M</span>\n          <strong>6,82% a.a.</strong>\n          <small>R$ 300 → R$ 1.122,17 • valorização acumulada de +274%</small>', 1)

# Torna as barras uma comparação de valor final, que é mais fácil de explicar ao cliente.
text = text.replace('<div class="incc-bar-head"><span>💰 Salário mínimo</span><strong>+406%</strong></div>', '<div class="incc-bar-head"><span>💰 Salário mínimo em 2025</span><strong>R$ 1.518</strong></div>', 1)
text = text.replace('<div class="incc-bar-head"><span>🏗️ INCC-M</span><strong>+274%</strong></div>', '<div class="incc-bar-head"><span>🏗️ R$ 300 corrigidos pelo INCC</span><strong>R$ 1.122</strong></div>', 1)

# Reforça o destaque monetário principal.
old_summary = '''      <div class="incc-money-summary">
        <span>Diferença acumulada em 2025</span>
        <strong>R$ 395,83 a mais</strong>
        <small>Partindo da mesma base de R$ 300 no fim de 2005: salário mínimo chegou a R$ 1.518,00; o mesmo valor reajustado apenas pelo INCC-M chegaria a aproximadamente R$ 1.122,17. O salário ficou cerca de 35,27% acima desse valor equivalente.</small>
      </div>'''
new_summary = '''      <div class="incc-money-summary">
        <span>Mesma largada: R$ 300 no fim de 2005</span>
        <strong>R$ 395,83 de diferença</strong>
        <small>Em 2025: salário mínimo R$ 1.518,00 × equivalente pelo INCC-M R$ 1.122,17. O salário terminou 35,27% acima do valor corrigido pelo INCC.</small>
      </div>'''
if old_summary in text:
    text = text.replace(old_summary, new_summary, 1)

# Se ainda não houver o resumo monetário, insere após as barras.
if 'Mesma largada: R$ 300 no fim de 2005' not in text and 'Diferença acumulada em 2025' not in text:
    marker = '      <div class="incc-client-argument">'
    if marker in text:
        text = text.replace(marker, new_summary + '\n\n' + marker, 1)

# Atualiza o argumento principal com os dados que mais chamam atenção.
argument_start = text.find('      <div class="incc-client-argument">')
if argument_start != -1:
    strong_start = text.find('        <strong>', argument_start)
    strong_end = text.find('</strong>', strong_start)
    if strong_start != -1 and strong_end != -1:
        strong_end += len('</strong>')
        new_argument = '''        <strong>“Se a gente pegar os mesmos R$ 300 de 2005 e comparar os dois caminhos, em 2025 o salário mínimo chegou a R$ 1.518, enquanto pelo INCC-M esse valor chegaria a cerca de R$ 1.122. Historicamente, foram 8,44% ao ano no salário contra 6,82% no INCC. No final, uma diferença de quase R$ 396 — 35,27% a mais. Isso mostra que o reajuste da carta não significa automaticamente que a renda fique para trás.”</strong>'''
        text = text[:strong_start] + new_argument + text[strong_end:]

# Garante o CSS das informações monetárias.
css_marker = '.incc-history-note{margin:7px 1px 0;color:#667085;font-size:7px;line-height:1.3;font-weight:700}'
if '.incc-money-summary{' not in text and css_marker in text:
    css_extra = css_marker + '''
.incc-money-summary{margin-top:8px;padding:10px;border:1px solid #b7e4c7;border-radius:12px;background:#f0fdf4}
.incc-money-summary span{display:block;color:#52705d;font-size:7px;font-weight:900;text-transform:uppercase;letter-spacing:.2px}
.incc-money-summary strong{display:block;margin-top:3px;color:#067647;font-size:19px;line-height:1;font-weight:950}
.incc-money-summary small{display:block;margin-top:4px;color:#475467;font-size:7.5px;line-height:1.3;font-weight:750}
.incc-history-table{min-width:440px}
.incc-history-table td.money{white-space:nowrap;text-align:right;font-variant-numeric:tabular-nums}
.incc-history-table td.diff-positive{white-space:nowrap;text-align:right;color:#067647;font-weight:950}
.incc-history-value-sub{display:block;margin-top:1px;color:#98a2b3;font-size:6px;font-weight:750}'''
    text = text.replace(css_marker, css_extra, 1)

# Tabela em reais: mesma base de R$ 300 e evolução ano a ano.
start = text.find('          <table class="incc-history-table">')
end = text.find('          </table>', start)
if start != -1 and end != -1:
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
    (2018,'3,97%','1,81%','954,00','681,81','272,19'),
    (2019,'4,13%','4,61%','998,00','709,96','288,04'),
    (2020,'8,68%','4,71%','1.045,00','771,59','273,41'),
    (2021,'14,03%','5,26%','1.100,00','879,84','220,16'),
    (2022,'9,41%','10,18%','1.212,00','962,64','249,36'),
    (2023,'3,32%','8,91%','1.320,00','994,60','325,40'),
    (2024,'6,34%','6,97%','1.412,00','1.057,65','354,35'),
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
    new_table = '''          <table class="incc-history-table">
            <thead><tr><th>Ano</th><th>Salário mínimo</th><th>Equivalente pelo INCC*</th><th>Diferença</th></tr></thead>
            <tbody>
''' + '\n'.join(body) + '''
            </tbody>
          </table>'''
    text = text[:start] + new_table + text[end:]

# Aviso metodológico.
note_start = text.find('<p class="incc-history-note">')
if note_start != -1:
    note_end = text.find('</p>', note_start)
    if note_end != -1:
        note_end += 4
        new_note = '<p class="incc-history-note"><strong>* Equivalente pelo INCC:</strong> não é um salário oficial. É uma simulação para comparação: usamos a mesma base de R$ 300 vigente no fim de 2005 e aplicamos, ano a ano, somente o INCC-M. A coluna “Salário mínimo” mostra o valor nominal oficial vigente no fim de cada ano. Em 15 dos 20 anos analisados, o reajuste anual do salário mínimo também foi maior que o INCC-M. Desempenho passado não garante reajustes futuros e a renda individual do cliente pode ter trajetória diferente.</p>'
        text = text[:note_start] + new_note + text[note_end:]

index_path.write_text(text, encoding='utf-8')

# Renova o cache offline para os celulares instalados receberem a nova apresentação.
sw_path = Path('calculadora/service-worker.js')
sw = sw_path.read_text(encoding='utf-8')
import re
sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v6', sw)
sw_path.write_text(sw, encoding='utf-8')
