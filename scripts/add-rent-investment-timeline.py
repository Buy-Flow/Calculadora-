from pathlib import Path

path = Path("calculadora/index.html")
text = path.read_text(encoding="utf-8")

if "rent-investment-timeline-v1" in text:
    print("Timeline já instalada; nada a fazer.")
    raise SystemExit(0)

css = r'''
/* rent-investment-timeline-v1 */
.rent-investment-timeline{
  margin-top:8px;
  border:1px solid #e4e7ec;
  border-radius:12px;
  background:#fff;
  overflow:hidden;
}
.rent-investment-timeline>summary{
  list-style:none;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  padding:10px;
  cursor:pointer;
  user-select:none;
}
.rent-investment-timeline>summary::-webkit-details-marker{display:none}
.rent-investment-timeline>summary::after{
  content:"⌄";
  flex:0 0 auto;
  color:#667085;
  font-size:18px;
  line-height:1;
  font-weight:900;
  transition:transform .18s ease;
}
.rent-investment-timeline[open]>summary::after{transform:rotate(180deg)}
.rent-timeline-summary-copy{min-width:0}
.rent-timeline-summary-copy b{display:block;color:#101828;font-size:11px;line-height:1.15;font-weight:950}
.rent-timeline-summary-copy small{display:block;margin-top:2px;color:#667085;font-size:8px;line-height:1.2;font-weight:750}
.rent-timeline-summary-action{flex:0 0 auto;margin-left:auto;color:#b42318;font-size:8px;line-height:1;font-weight:900;white-space:nowrap}
.rent-timeline-body{padding:0 8px 8px;border-top:1px solid #f0f1f3}
.rent-first-contribution{margin-top:8px;padding:9px 10px;border-radius:10px;background:#f2f4f7}
.rent-first-contribution.positive{background:#ecfdf3;border:1px solid #abefc6}
.rent-first-contribution.none{background:#f9fafb;border:1px solid #eaecf0}
.rent-first-contribution span{display:block;color:#667085;font-size:7.5px;line-height:1.1;font-weight:900;text-transform:uppercase}
.rent-first-contribution strong{display:block;margin-top:3px;color:#101828;font-size:12px;line-height:1.15;font-weight:950}
.rent-first-contribution.positive strong{color:#067647}
.rent-first-contribution small{display:block;margin-top:3px;color:#667085;font-size:7.5px;line-height:1.25;font-weight:750}
.rent-year-list{display:grid;gap:6px;margin-top:8px}
.rent-year{border:1px solid #eaecf0;border-radius:10px;overflow:hidden;background:#fff}
.rent-year>summary{list-style:none;display:grid;grid-template-columns:48px minmax(0,1fr) auto;align-items:center;gap:7px;min-height:46px;padding:7px 8px;cursor:pointer}
.rent-year>summary::-webkit-details-marker{display:none}
.rent-year-label{color:#475467;font-size:9px;line-height:1.1;font-weight:950}
.rent-year-main{min-width:0}
.rent-year-main b{display:block;color:#101828;font-size:10px;line-height:1.15;font-weight:950}
.rent-year-main small{display:block;margin-top:2px;color:#667085;font-size:7.2px;line-height:1.2;font-weight:750}
.rent-year-status{padding:5px 7px;border-radius:999px;background:#ecfdf3;color:#067647;font-size:7.2px;line-height:1;font-weight:950;white-space:nowrap}
.rent-year.no-contribution .rent-year-status{background:#f2f4f7;color:#667085}
.rent-year-metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:5px;padding:7px 8px;border-top:1px solid #f0f1f3;background:#fafbfc}
.rent-year-metric{min-width:0;padding:6px;border-radius:8px;background:#fff;border:1px solid #eef0f3}
.rent-year-metric span{display:block;color:#667085;font-size:6.6px;line-height:1.15;font-weight:900;text-transform:uppercase}
.rent-year-metric b{display:block;margin-top:2px;color:#101828;font-size:8.2px;line-height:1.1;font-weight:950;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rent-month-list{padding:0 8px 8px;background:#fafbfc}
.rent-month-row{display:grid;grid-template-columns:38px minmax(0,1fr) minmax(0,1fr);gap:6px;align-items:center;padding:7px 0;border-top:1px solid #eef0f3}
.rent-month-number{color:#475467;font-size:8px;line-height:1.1;font-weight:950}
.rent-month-cell{min-width:0}
.rent-month-cell span{display:block;color:#667085;font-size:6.5px;line-height:1.1;font-weight:850;text-transform:uppercase}
.rent-month-cell b{display:block;margin-top:2px;color:#101828;font-size:8.3px;line-height:1.1;font-weight:950;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rent-month-cell b.positive{color:#067647}
.rent-month-cell b.negative{color:#b42318}
.rent-month-context{grid-column:2 / -1;margin-top:-2px;color:#667085;font-size:6.6px;line-height:1.25;font-weight:700}
'''

html = r'''
      <details class="rent-investment-timeline" id="rentInvestmentTimeline">
        <summary>
          <span class="rent-timeline-summary-copy">
            <b>Evolução dos aportes</b>
            <small id="rentInvestmentTimelineSummary">Veja quando começa a sobrar e quanto é aplicado em cada ano.</small>
          </span>
          <em class="rent-timeline-summary-action">Ver ano a ano</em>
        </summary>
        <div class="rent-timeline-body">
          <div class="rent-first-contribution none" id="rentFirstContribution">
            <span>Primeiro aporte</span>
            <strong>Aguardando cálculo</strong>
            <small>A linha do tempo usa a mesma comparação mensal acima.</small>
          </div>
          <div class="rent-year-list" id="rentYearList"></div>
        </div>
      </details>

'''

js = r'''
function buildRentInvestmentTimelineData({financingPayments=[],consortiumPayments=[],rentMonthly=0,rentUntilMonth=null,months=0,annualRatePct=CURRENT_SELIC_ANNUAL_RATE}={}){
  const horizon=Math.max(Math.floor(Number(months)||0),0);
  const rent=Math.max(Number(rentMonthly)||0,0);
  const requestedRentEnd=Number(rentUntilMonth);
  const rentEndExclusive=Number.isFinite(requestedRentEnd)?Math.max(Math.floor(requestedRentEnd),1):horizon+1;
  const annualRate=Math.max(Number(annualRatePct)||0,0)/100;
  const monthlyRate=annualRate>0?Math.pow(1+annualRate,1/12)-1:0;
  let balance=0,cumulativeContributions=0,firstPositiveMonth=null,currentYear=null;
  const years=[];
  for(let index=0;index<horizon;index++){
    const month=index+1,yearNumber=Math.floor(index/12)+1;
    if(!currentYear||currentYear.year!==yearNumber){currentYear={year:yearNumber,startMonth:month,endMonth:month,contributions:0,shortfall:0,positiveMonths:0,months:[]};years.push(currentYear)}
    const financing=Math.max(Number(financingPayments[index])||0,0);
    const consortium=Math.max(Number(consortiumPayments[index])||0,0);
    const rentForMonth=month<rentEndExclusive?rent:0;
    const combined=consortium+rentForMonth;
    const difference=financing-combined;
    const contribution=difference>0?difference:0;
    const shortfall=difference<0?Math.abs(difference):0;
    balance*=(1+monthlyRate);
    if(contribution>0){if(firstPositiveMonth===null)firstPositiveMonth=month;balance+=contribution;cumulativeContributions+=contribution;currentYear.contributions+=contribution;currentYear.positiveMonths+=1}else if(shortfall>0){currentYear.shortfall+=shortfall}
    currentYear.endMonth=month;
    currentYear.months.push({month,financing,combined,difference,contribution,shortfall,balance});
    currentYear.endBalance=balance;
    currentYear.cumulativeContributions=cumulativeContributions;
    currentYear.cumulativeEarnings=Math.max(balance-cumulativeContributions,0);
  }
  return {firstPositiveMonth,years,endBalance:balance,cumulativeContributions};
}
function renderRentInvestmentTimeline({financingPayments=[],consortiumPayments=[],rentMonthly=0,rentUntilMonth=null,months=0,annualRatePct=CURRENT_SELIC_ANNUAL_RATE}={}){
  const summary=$("rentInvestmentTimelineSummary"),firstBox=$("rentFirstContribution"),yearList=$("rentYearList");
  if(!summary||!firstBox||!yearList)return;
  const data=buildRentInvestmentTimelineData({financingPayments,consortiumPayments,rentMonthly,rentUntilMonth,months,annualRatePct});
  const firstMonth=data.firstPositiveMonth;
  if(firstMonth!==null){
    const firstYear=Math.ceil(firstMonth/12);
    const firstRow=data.years.flatMap(year=>year.months).find(row=>row.month===firstMonth);
    summary.textContent=`Primeiro aporte no ${firstMonth}º mês • ${firstYear}º ano.`;
    firstBox.classList.remove("none");firstBox.classList.add("positive");
    firstBox.innerHTML=`<span>Primeiro aporte</span><strong>${firstMonth}º mês • ${firstYear}º ano</strong><small>Sobra de ${money(firstRow?.contribution||0)} nesse mês. A partir daí, só os meses com diferença positiva viram aporte.</small>`;
  }else{
    summary.textContent="Nenhum mês gerou sobra positiva para investir.";
    firstBox.classList.remove("positive");firstBox.classList.add("none");
    firstBox.innerHTML=`<span>Primeiro aporte</span><strong>Não houve aporte no período</strong><small>Consórcio + aluguel não ficou abaixo do financiamento em nenhum mês.</small>`;
  }
  yearList.innerHTML=data.years.map(year=>{
    const hasContribution=year.contributions>0;
    const statusText=hasContribution?`${year.positiveMonths} ${year.positiveMonths===1?"mês":"meses"} com aporte`:"Sem aporte";
    const mainText=hasContribution?`${money(year.contributions)} aplicados`:"Não houve sobra para investir";
    const secondaryText=hasContribution?`Meses ${year.startMonth}–${year.endMonth}`:(year.shortfall>0?`Déficit no ano: ${money(year.shortfall)}`:`Meses ${year.startMonth}–${year.endMonth}`);
    const monthRows=year.months.map(row=>{
      const diffClass=row.difference>0?"positive":(row.difference<0?"negative":"");
      const diffText=row.difference>0?`+ ${money(row.difference)}`:(row.difference<0?`- ${money(Math.abs(row.difference))}`:money(0));
      const contributionText=row.contribution>0?money(row.contribution):"Sem aporte";
      return `<div class="rent-month-row"><div class="rent-month-number">Mês ${row.month}</div><div class="rent-month-cell"><span>Diferença</span><b class="${diffClass}">${diffText}</b></div><div class="rent-month-cell"><span>Aplicado</span><b class="${row.contribution>0?"positive":""}">${contributionText}</b></div><div class="rent-month-context">Financiamento ${money(row.financing)} • Consórcio + aluguel ${money(row.combined)}</div></div>`;
    }).join("");
    return `<details class="rent-year${hasContribution?"":" no-contribution"}"><summary><span class="rent-year-label">${year.year}º ano</span><span class="rent-year-main"><b>${mainText}</b><small>${secondaryText}</small></span><span class="rent-year-status">${statusText}</span></summary><div class="rent-year-metrics"><div class="rent-year-metric"><span>Aplicado no ano</span><b>${money(year.contributions)}</b></div><div class="rent-year-metric"><span>Rendimento acumulado</span><b>${money(year.cumulativeEarnings||0)}</b></div><div class="rent-year-metric"><span>Saldo no Tesouro</span><b>${money(year.endBalance||0)}</b></div></div><div class="rent-month-list">${monthRows}</div></details>`;
  }).join("");
}
'''

if "</style>" not in text: raise RuntimeError("Não encontrei </style>")
text=text.replace("</style>",css+"\n</style>",1)
html_anchor='      <div class="rent-investment-note" id="rentInvestmentNote">'
if html_anchor not in text: raise RuntimeError("Não encontrei o ponto de inserção do HTML")
text=text.replace(html_anchor,html+html_anchor,1)
js_anchor="function renderRentInvestmentComparison({"
if js_anchor not in text: raise RuntimeError("Não encontrei renderRentInvestmentComparison")
text=text.replace(js_anchor,js+"\n"+js_anchor,1)
call_anchor='  $("rentInvestmentPeriod").textContent ='
if call_anchor not in text: raise RuntimeError("Não encontrei o ponto de renderização da linha do tempo")
call=r'''  renderRentInvestmentTimeline({
    financingPayments:financePayments,
    consortiumPayments,
    rentMonthly:rent,
    rentUntilMonth:selectedContemplationMonth,
    months:horizon,
    annualRatePct:annualRate
  });

'''
text=text.replace(call_anchor,call+call_anchor,1)
path.write_text(text,encoding="utf-8")
print("Linha do tempo de aportes instalada.")
