from pathlib import Path
import re

path = Path('calculadora/index.html')
text = path.read_text(encoding='utf-8')

# Troca a última coluna da tabela: sai a diferença em R$ e entra quem subiu mais no ano.
text = text.replace('<th>Dif.</th>', '<th>Subiu mais</th>', 1)

winners = {
    2006: ('salary', '💰 Salário'),
    2007: ('salary', '💰 Salário'),
    2008: ('incc', '🏗️ INCC-M'),
    2009: ('salary', '💰 Salário'),
    2010: ('salary', '💰 Salário'),
    2011: ('incc', '🏗️ INCC-M'),
    2012: ('salary', '💰 Salário'),
    2013: ('salary', '💰 Salário'),
    2014: ('salary', '💰 Salário'),
    2015: ('salary', '💰 Salário'),
    2016: ('salary', '💰 Salário'),
    2017: ('salary', '💰 Salário'),
    2018: ('incc', '🏗️ INCC-M'),
    2019: ('salary', '💰 Salário'),
    2020: ('incc', '🏗️ INCC-M'),
    2021: ('incc', '🏗️ INCC-M'),
    2022: ('salary', '💰 Salário'),
    2023: ('salary', '💰 Salário'),
    2024: ('salary', '💰 Salário'),
    2025: ('salary', '💰 Salário'),
}

for year, (kind, label) in winners.items():
    pattern = rf'(<tr><td>{year}</td>.*?)(<td class="diff-positive">.*?</td>)(</tr>)'
    replacement = rf'\1<td class="winner-cell"><span class="winner-badge {kind}">{label}</span></td>\3'
    text = re.sub(pattern, replacement, text, count=1)

# Destaca discretamente o último ano da série.
text = text.replace('<tr><td>2025</td>', '<tr class="latest-year"><td>2025</td>', 1)

marker = '/* incc-table-premium-v1 */'
css = r'''

/* incc-table-premium-v1 */
.incc-history-table-wrap{
  padding:6px;
  background:#f8fafc;
}
.incc-history-table{
  border-collapse:separate!important;
  border-spacing:0 5px!important;
}
.incc-history-table thead th{
  background:transparent!important;
  border:0!important;
  color:#667085;
  font-size:7.4px!important;
  font-weight:950!important;
  letter-spacing:.18px;
  text-transform:uppercase;
}
.incc-history-table tbody tr{
  background:#fff;
  box-shadow:0 1px 2px rgba(16,24,40,.04);
}
.incc-history-table tbody td{
  border-top:1px solid #eaecf0!important;
  border-bottom:1px solid #eaecf0!important;
  padding-top:7px!important;
  padding-bottom:7px!important;
}
.incc-history-table tbody td:first-child{
  border-left:1px solid #eaecf0!important;
  border-radius:9px 0 0 9px;
  color:#344054;
}
.incc-history-table tbody td:last-child{
  border-right:1px solid #eaecf0!important;
  border-radius:0 9px 9px 0;
}
.incc-history-table th:nth-child(1){width:13%!important}
.incc-history-table th:nth-child(2){width:27%!important}
.incc-history-table th:nth-child(3){width:27%!important}
.incc-history-table th:nth-child(4){width:33%!important;text-align:right}
.incc-history-table td:nth-child(2),
.incc-history-table td:nth-child(3){font-weight:900;color:#475467}
.incc-history-value-sub{color:#98a2b3!important;font-weight:800!important}
.winner-cell{text-align:right!important;white-space:nowrap}
.winner-badge{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  min-width:66px;
  padding:4px 6px;
  border-radius:999px;
  font-size:7.4px;
  line-height:1;
  font-weight:950;
  white-space:nowrap;
}
.winner-badge.salary{background:#ecfdf3;color:#067647;border:1px solid #abefc6}
.winner-badge.incc{background:#fff7ed;color:#b54708;border:1px solid #fed7aa}
.incc-history-table tr.latest-year td{background:#f6fef9}
.incc-history-table tr.latest-year td:first-child{color:#067647}
'''

if marker not in text:
    text = text.replace('</style>', css + '\n</style>', 1)

path.write_text(text, encoding='utf-8')
