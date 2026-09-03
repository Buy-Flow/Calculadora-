from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Cards principais: métricas fáceis de comparar, sem o antigo 15 de 20 / 5 de 20.
old_grid = '''      <div class="incc-history-grid">
        <div class="incc-history-card salary">
          <span>Média anual do salário mínimo</span>
          <strong>8,44% a.a.</strong>
          <small>R$ 300 → R$ 1.518,00 • valorização acumulada de +406%</small>
        </div>
        <div class="incc-history-card incc">
          <span>Média anual do INCC-M</span>
          <strong>6,82% a.a.</strong>
          <small>R$ 300 → R$ 1.122,17 • valorização acumulada de +274%</small>
        </div>
      </div>'''
new_grid = '''      <div class="incc-history-grid">
        <div class="incc-history-card salary">
          <span>Salário mínimo • média anual</span>
          <strong>8,44% a.a.</strong>
          <small>R$ 300 → R$ 1.518,00 • +406% no período</small>
        </div>
        <div class="incc-history-card incc">
          <span>INCC-M • média anual</span>
          <strong>6,82% a.a.</strong>
          <small>R$ 300 → R$ 1.122,17 • +274% no período</small>
        </div>
      </div>'''
if old_grid in text:
    text = text.replace(old_grid, new_grid, 1)

# Compatibilidade com a versão antiga ainda presente em alguns commits.
text = text.replace('''        <div class="incc-history-card salary">
          <span>Salário mínimo subiu mais</span>
          <strong>15 de 20 anos</strong>
          <small>Acumulado aproximado: +406% • média composta: 8,44% a.a.</small>
        </div>''', '''        <div class="incc-history-card salary">
          <span>Salário mínimo • média anual</span>
          <strong>8,44% a.a.</strong>
          <small>R$ 300 → R$ 1.518,00 • +406% no período</small>
        </div>''', 1)
text = text.replace('''        <div class="incc-history-card incc">
          <span>INCC-M subiu mais</span>
          <strong>5 de 20 anos</strong>
          <small>Acumulado aproximado: +274% • média composta: 6,82% a.a.</small>
        </div>''', '''        <div class="incc-history-card incc">
          <span>INCC-M • média anual</span>
          <strong>6,82% a.a.</strong>
          <small>R$ 300 → R$ 1.122,17 • +274% no período</small>
        </div>''', 1)

# Mantém a comparação visual usando a mesma base.
text = text.replace('<div class="incc-bar-head"><span>💰 Salário mínimo</span><strong>+406%</strong></div>', '<div class="incc-bar-head"><span>💰 Salário mínimo em 2025</span><strong>R$ 1.518</strong></div>', 1)
text = text.replace('<div class="incc-bar-head"><span>🏗️ INCC-M</span><strong>+274%</strong></div>', '<div class="incc-bar-head"><span>🏗️ R$ 300 corrigidos pelo INCC</span><strong>R$ 1.122</strong></div>', 1)

# Destaque da diferença: em reais, percentual e diferença de média anual.
summary_start = text.find('      <div class="incc-money-summary">')
if summary_start != -1:
    summary_end = text.find('      </div>', summary_start)
    if summary_end != -1:
        summary_end += len('      </div>')
        summary = '''      <div class="incc-money-summary">
        <span>Diferença de valorização • mesma base de R$ 300</span>
        <strong>R$ 395,83 de diferença</strong>
        <small>Salário: 8,44% a.a. × INCC-M: 6,82% a.a. • diferença média de 1,62 p.p. ao ano. No acumulado: +406% × +274%.</small>
      </div>'''
        text = text[:summary_start] + summary + text[summary_end:]

# Texto para o cliente: sem rótulo de bastidor e sem fundo escuro.
arg_start = text.find('      <div class="incc-client-argument">')
if arg_start != -1:
    arg_end = text.find('      </div>', arg_start)
    if arg_end != -1:
        arg_end += len('      </div>')
        argument = '''      <div class="incc-client-argument">
        <strong>Partindo exatamente da mesma base de R$ 300, o salário mínimo chegou a R$ 1.518 em 2025, enquanto o mesmo valor corrigido pelo INCC-M chegaria a cerca de R$ 1.122. Nesse período, o salário cresceu em média 8,44% ao ano e o INCC-M 6,82% ao ano. Isso ajuda a colocar o reajuste da carta em perspectiva: ele atualiza o valor do crédito e, historicamente neste recorte, ficou abaixo da evolução do salário mínimo.</strong>
      </div>'''
        text = text[:arg_start] + argument + text[arg_end:]

# Tabela em reais, com cabeçalhos curtos para caber no celular sem rolagem lateral.
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
start = text.find('          <table class="incc-history-table">')
end = text.find('          </table>', start)
if start != -1 and end != -1:
    end += len('          </table>')
    body = []
    for year, incc_pct, sal_pct, sal_value, incc_value, diff in rows:
        body.append(
            f'              <tr><td>{year}</td>'
            f'<td class="money">R$ {sal_value}<span class="incc-history-value-sub">+{sal_pct}</span></td>'
            f'<td class="money">R$ {incc_value}<span class="incc-history-value-sub">{incc_pct}</span></td>'
            f'<td class="diff-positive">+R$ {diff}</td></tr>'
        )
    table = '''          <table class="incc-history-table">
            <thead><tr><th>Ano</th><th>Salário</th><th>Pelo INCC</th><th>Dif.</th></tr></thead>
            <tbody>
''' + '\n'.join(body) + '''
            </tbody>
          </table>'''
    text = text[:start] + table + text[end:]

# Nota metodológica menor e objetiva.
note_start = text.find('<p class="incc-history-note">')
if note_start != -1:
    note_end = text.find('</p>', note_start)
    if note_end != -1:
        note_end += 4
        note = '<p class="incc-history-note"><strong>* Pelo INCC:</strong> simulação com a mesma base de R$ 300 no fim de 2005, corrigida ano a ano pelo INCC-M. Não representa um salário oficial. Desempenho passado não garante reajustes futuros.</p>'
        text = text[:note_start] + note + text[note_end:]

# CSS final do bloco: sobrescreve as regras antigas sem redesenhar o restante do site.
css_tag = '/* incc-client-mobile-v2 */'
css = r'''

/* incc-client-mobile-v2 */
.incc-client-argument{
  margin-top:8px;
  padding:10px;
  border:1px solid #e4e7ec;
  border-radius:12px;
  background:#fff;
  color:#344054;
}
.incc-client-argument span{display:none!important}
.incc-client-argument strong{
  display:block;
  margin:0;
  color:#344054;
  font-size:10.2px;
  line-height:1.42;
  font-weight:800;
}
.incc-history-table-wrap{
  max-height:390px;
  overflow-y:auto;
  overflow-x:hidden;
  border-top:1px solid #eef0f3;
}
.incc-history-table{
  width:100%;
  min-width:0!important;
  table-layout:fixed;
  border-collapse:collapse;
  font-size:9.2px;
}
.incc-history-table th{
  padding:7px 4px;
  font-size:7.5px;
  line-height:1.05;
  white-space:nowrap;
}
.incc-history-table th:nth-child(1){width:13%}
.incc-history-table th:nth-child(2){width:29%}
.incc-history-table th:nth-child(3){width:29%}
.incc-history-table th:nth-child(4){width:29%}
.incc-history-table td{
  padding:7px 4px;
  font-size:9px;
  line-height:1.1;
}
.incc-history-table td:first-child{font-weight:900}
.incc-history-table td.money,
.incc-history-table td.diff-positive{
  white-space:nowrap;
  overflow:hidden;
  text-overflow:clip;
}
.incc-history-value-sub{
  margin-top:2px;
  font-size:7px;
  line-height:1;
}
.incc-history-details>summary{font-size:10px;padding:10px}
.incc-history-note{font-size:7.4px;line-height:1.3;margin-top:7px}
'''
if css_tag not in text:
    text = text.replace('</style>', css + '\n</style>', 1)

index_path.write_text(text, encoding='utf-8')

# Só renova o nome do cache; a estratégia do service worker é mantida no próprio arquivo.
sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v7', sw)
    sw_path.write_text(sw, encoding='utf-8')
