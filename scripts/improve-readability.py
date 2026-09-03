from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Deixa a explicação do comparativo de 18 anos curta e direta.
text = re.sub(
    r'if\(\$\("historyClientText"\)\)\s*\$\("historyClientText"\)\.textContent=`.*?`;',
    'if($("historyClientText")) $("historyClientText").textContent=`O reajuste da parcela também atualiza o valor da carta. Neste recorte de 18 anos, a evolução do salário mínimo ficou acima do INCC-M.`;',
    text,
    count=1,
    flags=re.S,
)

# Remove microexplicações de base que repetem o que o bloco já mostra.
text = text.replace(
    '<small>Base no fim de 2007. A partir de 2008 são aplicados os reajustes históricos de cada caminho.</small>',
    '',
)

# Remove a observação metodológica do rodapé do comparativo para deixar a apresentação limpa.
text = re.sub(
    r'<p class="incc-history-note">.*?</p>',
    '',
    text,
    count=1,
    flags=re.S,
)

# Subtítulo mais direto no comparativo de 18 anos.
text = text.replace(
    'Como a mesma parcela teria evoluído pelo INCC-M e pela evolução do salário mínimo.',
    'A mesma parcela seguindo dois reajustes históricos.',
    1,
)

# Resumo objetivo dos 18 anos: só os três números pedidos.
text = re.sub(
    r'\s*<div class="history-rate-summary" id="historyRateSummary">.*?</div>\s*</div>',
    '',
    text,
    count=1,
    flags=re.S,
)
rate_summary = '''
      <div class="history-rate-summary" id="historyRateSummary">
        <div class="history-rate-card salary-total">
          <span>💰 Salário no período</span>
          <strong>+299,47%</strong>
        </div>
        <div class="history-rate-card salary-average">
          <span>💰 Média do salário</span>
          <strong>8,00% a.a.</strong>
        </div>
        <div class="history-rate-card incc-average">
          <span>🏗️ Média do INCC-M</span>
          <strong>6,96% a.a.</strong>
        </div>
      </div>
'''
anchor = '      <div class="incc-history-grid parcel-history-grid">'
if 'id="historyRateSummary"' not in text and anchor in text:
    text = text.replace(anchor, rate_summary + '\n' + anchor, 1)

marker = '/* global-readable-v2 */'
css = r'''

/* global-readable-v2 */
/* Tipografia geral mais legível sem aumentar demais a altura do site. */
.hero-mini-note{font-size:10.5px!important;line-height:1.25!important}
.hero p{font-size:13px!important;line-height:1.3!important}
.tag{font-size:12px!important}
.field label{font-size:12px!important}
.field small{font-size:12px!important;line-height:1.3!important}
.compact-grid .field label{font-size:11px!important}
.compact-projection small{font-size:11px!important;line-height:1.25!important}
.credit-control label{font-size:11.5px!important}
.credit-chip{font-size:11.5px!important}
.triple-btn{font-size:12px!important}
#insuranceBtn{font-size:11.5px!important}
.result .kicker{font-size:11.5px!important}
.result .sub{font-size:11.5px!important;line-height:1.3!important}

.comparison-head h2{font-size:20px!important}
.comparison-head p{font-size:11px!important;line-height:1.3!important}
.comparison-badge{font-size:10px!important;padding:6px 8px!important}
.comparison-reference-label{font-size:9.5px!important}
.comparison-mode-btn{font-size:11px!important}
.finance-control label{font-size:10.5px!important;line-height:1.2!important}
.finance-field-hint{font-size:10px!important;line-height:1.3!important}
.finance-reference-note{font-size:10.5px!important;line-height:1.35!important}
.finance-system-wrap span{font-size:10px!important}
.finance-system-btn{font-size:11px!important}

.compare-paired-head{font-size:11px!important}
.compare-cell span{font-size:9.5px!important;line-height:1.2!important}
.compare-cell strong{font-size:12.5px!important;line-height:1.12!important}
.compare-cost-question span{font-size:10px!important}
.compare-cost-question strong{font-size:16px!important}

.proj2-row span{font-size:10px!important;line-height:1.2!important}
.proj2-row strong{font-size:11.5px!important}
.proj2-note,.projection-note,.mode-note{font-size:10.5px!important;line-height:1.35!important}

.rent-investment-period span{font-size:9.5px!important}
.rent-investment-period strong{font-size:11px!important}
.rent-investment-metric span{font-size:9.2px!important;min-height:0!important}
.rent-investment-metric strong{font-size:12.5px!important}
.rent-investment-result span{font-size:10px!important}
.rent-investment-result small{font-size:9.5px!important;line-height:1.3!important}
.rent-investment-note{font-size:9.5px!important;line-height:1.35!important}
.rent-timeline-summary-copy b{font-size:11px!important}
.rent-timeline-summary-copy small{font-size:9.5px!important;line-height:1.3!important}
.rent-timeline-summary-action{font-size:9.5px!important}
.rent-first-contribution span{font-size:9px!important}
.rent-first-contribution strong{font-size:12px!important}
.rent-first-contribution small{font-size:9px!important;line-height:1.3!important}
.rent-year-label{font-size:10px!important}
.rent-year-main b{font-size:10.5px!important}
.rent-year-main small{font-size:9px!important}
.rent-year-status{font-size:9px!important}
.rent-year-metric span{font-size:8.8px!important}
.rent-year-metric b{font-size:10.5px!important}
.rent-month-row{font-size:9px!important}

.parcel-history-base span,
.parcel-credit-projection span{font-size:9.2px!important;line-height:1.2!important}
.parcel-history-base strong{font-size:15px!important}
.parcel-history-grid .incc-history-card span{font-size:9.5px!important;line-height:1.2!important}
.parcel-history-grid .incc-history-card strong{font-size:20px!important}
.parcel-history-grid .incc-history-card small{font-size:9px!important;line-height:1.25!important}
.parcel-credit-projection strong{font-size:20px!important}
.parcel-credit-projection small{font-size:9px!important;line-height:1.3!important}
.parcel-history-explanation strong{font-size:11px!important;line-height:1.4!important}
.incc-money-summary span{font-size:9px!important}
.incc-money-summary strong{font-size:20px!important}
.incc-money-summary small{font-size:9px!important;line-height:1.3!important}
.incc-history-details>summary{font-size:12px!important;padding:11px!important}

.history-rate-summary{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:6px;
  margin-top:7px;
}
.history-rate-card{
  min-width:0;
  padding:8px 5px;
  border:1px solid #e4e7ec;
  border-radius:11px;
  background:#fff;
  text-align:center;
}
.history-rate-card span{
  display:block;
  min-height:25px;
  color:#667085;
  font-size:9px;
  line-height:1.15;
  font-weight:900;
}
.history-rate-card strong{
  display:block;
  margin-top:3px;
  color:#101828;
  font-size:15px;
  line-height:1;
  font-weight:950;
  white-space:nowrap;
}
.history-rate-card.salary-total,
.history-rate-card.salary-average{background:#f6fef9;border-color:#abefc6}
.history-rate-card.salary-total strong,
.history-rate-card.salary-average strong{color:#067647}
.history-rate-card.incc-average{background:#fffaf5;border-color:#fed7aa}
.history-rate-card.incc-average strong{color:#b54708}

/* Tabela: aproximadamente +2 px, com a porcentagem bem mais visível. */
.parcel-history-table thead th,
.incc-history-table thead th{font-size:9.2px!important;height:34px!important;padding:8px 3px!important}
.parcel-history-table tbody td,
.incc-history-table tbody td{font-size:10.5px!important;line-height:1.12!important;padding:7px 3px!important}
.parcel-history-value-sub,
.incc-history-value-sub{font-size:8.8px!important;line-height:1.05!important;margin-top:3px!important;font-weight:900!important;color:#667085!important}
.winner-badge{font-size:8.7px!important;min-width:70px!important;padding:5px 6px!important}

/* Evita excesso de espaço ao aumentar as fontes. */
.compare-cell{padding-top:7px!important;padding-bottom:7px!important}
.rent-investment-metric{padding:7px!important}
'''

# Remove a versão anterior da camada global e grava a nova.
text = re.sub(r'/\* global-readable-v1 \*/.*?(?=</style>)', '', text, count=1, flags=re.S)
text = re.sub(r'/\* global-readable-v2 \*/.*?(?=</style>)', '', text, count=1, flags=re.S)
text = text.replace('</style>', css + '\n</style>', 1)

index_path.write_text(text, encoding='utf-8')

# Força o PWA a buscar esta versão nova.
sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v11', sw)
    sw_path.write_text(sw, encoding='utf-8')
