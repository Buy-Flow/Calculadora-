from pathlib import Path
import re

path = Path('calculadora/index.html')
text = path.read_text(encoding='utf-8')

# Substitui o comparativo fixo por uma simulação dinâmica usando a parcela atual
# da calculadora como mesma base para salário mínimo e INCC-M, em 18 anos.
section_start = text.find('    <section class="card incc-salary-section section" id="inccSalarySection">')
section_end = text.find('    <section class="card rent-investment-section section" id="rentInvestmentSection">', section_start)

new_section = '''    <section class="card incc-salary-section section" id="inccSalarySection">
      <div class="comparison-head parcel-history-head">
        <div>
          <h2>Parcela <em>x</em> salário mínimo</h2>
          <p>Como a mesma parcela teria evoluído pelo INCC-M e pela evolução do salário mínimo.</p>
        </div>
        <span class="comparison-badge">18 anos • 2008–2025</span>
      </div>

      <div class="parcel-history-base">
        <div>
          <span>Carta de crédito usada na simulação</span>
          <strong id="historyCreditBase">R$ 0,00</strong>
        </div>
        <div>
          <span>Mesma parcela inicial nos dois caminhos</span>
          <strong id="historyParcelBase">R$ 0,00</strong>
        </div>
        <small>Base no fim de 2007. A partir de 2008 são aplicados os reajustes históricos de cada caminho.</small>
      </div>

      <div class="incc-history-grid parcel-history-grid">
        <div class="incc-history-card salary">
          <span>💰 Pela evolução do salário mínimo</span>
          <strong id="historySalaryEnd">R$ 0,00</strong>
          <small id="historySalaryMeta">—</small>
        </div>
        <div class="incc-history-card incc">
          <span>🏗️ Parcela corrigida pelo INCC-M</span>
          <strong id="historyInccEnd">R$ 0,00</strong>
          <small id="historyInccMeta">—</small>
        </div>
      </div>

      <div class="parcel-credit-projection">
        <span>🏗️ A carta de crédito, seguindo o mesmo INCC-M</span>
        <strong id="historyCreditEnd">R$ 0,00</strong>
        <small id="historyCreditMeta">—</small>
      </div>

      <div class="incc-money-summary parcel-history-diff">
        <span>Diferença no fim dos 18 anos</span>
        <strong id="historyDiff">R$ 0,00</strong>
        <small id="historyDiffMeta">—</small>
      </div>

      <div class="incc-client-argument parcel-history-explanation">
        <strong id="historyClientText">—</strong>
      </div>

      <details class="incc-history-details">
        <summary>Ver evolução dos últimos 18 anos</summary>
        <div class="incc-history-table-wrap">
          <table class="incc-history-table parcel-history-table">
            <thead><tr><th>Ano</th><th>💰 Salário</th><th>🏗️ Parcela</th><th>Subiu mais</th></tr></thead>
            <tbody id="history18Body"></tbody>
          </table>
        </div>
      </details>

      <p class="incc-history-note"><strong>* Comparação normalizada:</strong> o valor da coluna “Salário” não é o salário mínimo oficial daquele ano. Os dois caminhos começam exatamente na mesma parcela exibida pela calculadora. Um acompanha a evolução proporcional do salário mínimo; o outro, o INCC-M histórico. A carta é projetada pelo mesmo INCC-M apenas para visualizar a valorização proporcional. Desempenho passado não garante reajustes futuros.</p>
    </section>

'''

if section_start != -1 and section_end != -1:
    text = text[:section_start] + new_section + text[section_end:]

css_marker = '/* parcel-salary-history-18y-v1 */'
css = r'''

/* parcel-salary-history-18y-v1 */
.parcel-history-head{align-items:center}
.parcel-history-head .comparison-badge{white-space:nowrap}
.parcel-history-base{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:6px;
  padding:8px;
  border:1px solid #e4e7ec;
  border-radius:12px;
  background:#f8fafc;
}
.parcel-history-base>div{
  min-width:0;
  padding:7px 8px;
  border:1px solid #eaecf0;
  border-radius:10px;
  background:#fff;
}
.parcel-history-base span,
.parcel-credit-projection span{
  display:block;
  color:#667085;
  font-size:7.2px;
  line-height:1.15;
  font-weight:900;
  text-transform:uppercase;
}
.parcel-history-base strong{
  display:block;
  margin-top:3px;
  color:#101828;
  font-size:13px;
  line-height:1.05;
  font-weight:950;
}
.parcel-history-base>small{
  grid-column:1/-1;
  display:block;
  color:#667085;
  font-size:7.3px;
  line-height:1.25;
  font-weight:750;
  padding:0 2px;
}
.parcel-history-grid{margin-top:7px}
.parcel-history-grid .incc-history-card strong{font-size:18px}
.parcel-credit-projection{
  margin-top:7px;
  padding:9px 10px;
  border:1px solid #fed7aa;
  border-radius:12px;
  background:#fff7ed;
}
.parcel-credit-projection strong{
  display:block;
  margin-top:2px;
  color:#b54708;
  font-size:18px;
  line-height:1.05;
  font-weight:950;
}
.parcel-credit-projection small{
  display:block;
  margin-top:3px;
  color:#7a2e0e;
  font-size:7.5px;
  line-height:1.25;
  font-weight:800;
}
.parcel-history-diff{margin-top:7px}
.parcel-history-explanation{margin-top:7px!important}
.parcel-history-explanation strong{font-size:9.6px!important;line-height:1.4!important}
.parcel-history-table-wrap,
.incc-history-table-wrap{
  position:relative;
  max-height:390px;
  overflow-y:auto!important;
  overflow-x:hidden!important;
  padding:0 6px 6px!important;
  background:#f8fafc!important;
}
.parcel-history-table,
.incc-history-table{
  width:100%!important;
  min-width:0!important;
  table-layout:fixed!important;
  border-collapse:separate!important;
  border-spacing:0 5px!important;
  margin:0!important;
}
.parcel-history-table thead th,
.incc-history-table thead th{
  position:sticky!important;
  top:0!important;
  z-index:9!important;
  height:31px;
  padding:8px 3px!important;
  background:#eef2f6!important;
  color:#475467!important;
  border:0!important;
  box-shadow:0 2px 5px rgba(16,24,40,.10);
  text-align:center!important;
  vertical-align:middle!important;
  font-size:7.2px!important;
  line-height:1!important;
  font-weight:950!important;
  text-transform:uppercase;
  white-space:nowrap;
}
.parcel-history-table th:nth-child(1){width:13%!important}
.parcel-history-table th:nth-child(2){width:27%!important}
.parcel-history-table th:nth-child(3){width:27%!important}
.parcel-history-table th:nth-child(4){width:33%!important}
.parcel-history-table tbody tr{background:#fff;box-shadow:0 1px 2px rgba(16,24,40,.04)}
.parcel-history-table tbody td{
  padding:7px 3px!important;
  border-top:1px solid #eaecf0!important;
  border-bottom:1px solid #eaecf0!important;
  color:#475467;
  font-size:8.5px!important;
  line-height:1.08!important;
  font-weight:900;
  text-align:center!important;
  vertical-align:middle!important;
  white-space:nowrap;
}
.parcel-history-table tbody td:first-child{
  border-left:1px solid #eaecf0!important;
  border-radius:9px 0 0 9px;
  color:#344054;
}
.parcel-history-table tbody td:last-child{
  border-right:1px solid #eaecf0!important;
  border-radius:0 9px 9px 0;
}
.parcel-history-table tr.latest-year td{background:#f6fef9}
.parcel-history-value-sub{
  display:block;
  margin-top:2px;
  color:#98a2b3;
  font-size:6.7px;
  line-height:1;
  font-weight:800;
}
.winner-cell{text-align:center!important;white-space:nowrap}
.winner-badge{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  min-width:64px;
  padding:4px 5px;
  border-radius:999px;
  font-size:7px;
  line-height:1;
  font-weight:950;
  white-space:nowrap;
}
.winner-badge.salary{background:#ecfdf3;color:#067647;border:1px solid #abefc6}
.winner-badge.incc{background:#fff7ed;color:#b54708;border:1px solid #fed7aa}
'''
if css_marker not in text:
    text = text.replace('</style>', css + '\n</style>', 1)

js_marker = '/* parcel-salary-history-18y-js-v1 */'
js = r'''

/* parcel-salary-history-18y-js-v1 */
const PARCEL_HISTORY_18Y = [
  {year:2008,incc:11.97,salaryPct:9.21,minWage:415},
  {year:2009,incc:3.21,salaryPct:12.05,minWage:465},
  {year:2010,incc:7.57,salaryPct:9.68,minWage:510},
  {year:2011,incc:7.58,salaryPct:6.86,minWage:545},
  {year:2012,incc:7.25,salaryPct:14.13,minWage:622},
  {year:2013,incc:8.07,salaryPct:9.00,minWage:678},
  {year:2014,incc:6.74,salaryPct:6.78,minWage:724},
  {year:2015,incc:7.22,salaryPct:8.84,minWage:788},
  {year:2016,incc:6.34,salaryPct:11.68,minWage:880},
  {year:2017,incc:4.03,salaryPct:6.48,minWage:937},
  {year:2018,incc:3.97,salaryPct:1.81,minWage:954},
  {year:2019,incc:4.13,salaryPct:4.61,minWage:998},
  {year:2020,incc:8.68,salaryPct:4.71,minWage:1045},
  {year:2021,incc:14.03,salaryPct:5.26,minWage:1100},
  {year:2022,incc:9.41,salaryPct:10.18,minWage:1212},
  {year:2023,incc:3.32,salaryPct:8.91,minWage:1320},
  {year:2024,incc:6.34,salaryPct:6.97,minWage:1412},
  {year:2025,incc:6.10,salaryPct:7.51,minWage:1518}
];

function historyPctBR(value){
  return `${(Number(value)||0).toLocaleString('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2})}%`;
}

function renderParcelSalaryHistory18Y({baseParcel=0,credit=0}={}){
  const section=$("inccSalarySection");
  if(!section) return;
  section.style.display = active === "imoveis" ? "" : "none";
  if(active !== "imoveis") return;

  const parcel=Math.max(Number(baseParcel)||0,0);
  const baseCredit=Math.max(Number(credit)||0,0);
  if(parcel<=0) return;

  const salaryBase=380;
  const salaryEndOfficial=1518;
  const salaryFactor=salaryEndOfficial/salaryBase;
  let inccFactor=1;
  const rows=[];

  PARCEL_HISTORY_18Y.forEach(item=>{
    inccFactor *= (1 + item.incc/100);
    const salaryIndexed = parcel * (item.minWage/salaryBase);
    const inccParcel = parcel * inccFactor;
    const salaryWins = item.salaryPct > item.incc;
    rows.push({
      ...item,
      salaryIndexed,
      inccParcel,
      winner:salaryWins ? 'salary' : 'incc',
      winnerLabel:salaryWins ? '💰 Salário' : '🏗️ INCC-M'
    });
  });

  const salaryEnd=parcel*salaryFactor;
  const inccEnd=parcel*inccFactor;
  const creditEnd=baseCredit*inccFactor;
  const diff=salaryEnd-inccEnd;
  const diffPct=inccEnd>0 ? (diff/inccEnd)*100 : 0;
  const salaryGrowth=(salaryFactor-1)*100;
  const inccGrowth=(inccFactor-1)*100;
  const salaryCagr=(Math.pow(salaryFactor,1/18)-1)*100;
  const inccCagr=(Math.pow(inccFactor,1/18)-1)*100;

  if($("historyCreditBase")) $("historyCreditBase").textContent=money(baseCredit);
  if($("historyParcelBase")) $("historyParcelBase").textContent=money(parcel);
  if($("historySalaryEnd")) $("historySalaryEnd").textContent=money(salaryEnd);
  if($("historyInccEnd")) $("historyInccEnd").textContent=money(inccEnd);
  if($("historyCreditEnd")) $("historyCreditEnd").textContent=money(creditEnd);
  if($("historyDiff")) $("historyDiff").textContent=`${money(Math.abs(diff))} ${diff>=0?'a favor do salário':'a favor do INCC'}`;

  if($("historySalaryMeta")) $("historySalaryMeta").textContent=`+${historyPctBR(salaryGrowth)} no período • média ${historyPctBR(salaryCagr)} a.a.`;
  if($("historyInccMeta")) $("historyInccMeta").textContent=`+${historyPctBR(inccGrowth)} no período • média ${historyPctBR(inccCagr)} a.a.`;
  if($("historyCreditMeta")) $("historyCreditMeta").textContent=`A carta de ${money(baseCredit)} chegaria a aproximadamente ${money(creditEnd)} aplicando o INCC-M histórico do período.`;
  if($("historyDiffMeta")) $("historyDiffMeta").textContent=`Partindo da mesma parcela de ${money(parcel)}, a evolução do salário termina ${historyPctBR(Math.abs(diffPct))} ${diff>=0?'acima':'abaixo'} da parcela corrigida pelo INCC-M.`;
  if($("historyClientText")) $("historyClientText").textContent=`Imagine esta mesma carta de ${money(baseCredit)} com uma parcela inicial de ${money(parcel)} há 18 anos. Corrigindo a parcela pelo INCC-M histórico, ela chegaria hoje a cerca de ${money(inccEnd)}. Usando exatamente a mesma parcela inicial, mas acompanhando a evolução do salário mínimo, o equivalente chegaria a ${money(salaryEnd)}. Assim a comparação fica proporcional: os dois começam iguais, e a gente vê qual índice cresceu mais ao longo do tempo.`;

  const body=$("history18Body");
  if(body){
    body.innerHTML=rows.map((row,index)=>`
      <tr class="${index===rows.length-1?'latest-year':''}">
        <td>${row.year}</td>
        <td>${money(row.salaryIndexed)}<span class="parcel-history-value-sub">+${historyPctBR(row.salaryPct)}</span></td>
        <td>${money(row.inccParcel)}<span class="parcel-history-value-sub">INCC ${historyPctBR(row.incc)}</span></td>
        <td class="winner-cell"><span class="winner-badge ${row.winner}">${row.winnerLabel}</span></td>
      </tr>`).join('');
  }
}
'''

if js_marker not in text:
    anchor = 'function renderRentInvestmentComparison({' 
    if anchor in text:
        text = text.replace(anchor, js + '\n\n' + anchor, 1)

call_marker = '// parcel-salary-history-18y-call'
if call_marker not in text:
    target = '''  const reducedDisplayed = reduced + insuranceBefore;\n  const fullDisplayed = full + insuranceBefore;'''
    replacement = target + '''\n\n  // parcel-salary-history-18y-call\n  renderParcelSalaryHistory18Y({\n    baseParcel: currentMode === "reduced" ? reducedDisplayed : fullDisplayed,\n    credit\n  });'''
    if target in text:
        text = text.replace(target, replacement, 1)

# Renova o cache do PWA para a nova simulação aparecer também no app instalado.
sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v9', sw)
    sw_path.write_text(sw, encoding='utf-8')

path.write_text(text, encoding='utf-8')
