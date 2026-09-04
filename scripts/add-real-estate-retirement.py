from pathlib import Path
import re

index_path = Path("calculadora/index.html")
text = index_path.read_text(encoding="utf-8")

text = re.sub(
    r'\n?<!-- real-estate-retirement-v1:start -->.*?<!-- real-estate-retirement-v1:end -->\n?',
    '\n',
    text,
    flags=re.S,
)
text = re.sub(
    r'\n?/\* real-estate-retirement-v1:start \*/.*?/\* real-estate-retirement-v1:end \*/\n?',
    '\n',
    text,
    flags=re.S,
)
text = re.sub(
    r'\n?/\* real-estate-retirement-v1-js:start \*/.*?/\* real-estate-retirement-v1-js:end \*/\n?',
    '\n',
    text,
    flags=re.S,
)

html = r'''
<!-- real-estate-retirement-v1:start -->
<div class="ai-retirement-wrap" id="realEstateRetirementWrap">
  <section class="card section ai-retirement" id="realEstateRetirementSection" aria-labelledby="aiRetirementTitle">
    <div class="ai-retirement-head">
      <div>
        <div class="ai-retirement-eyebrow">🏘️ Planejamento patrimonial</div>
        <h2 id="aiRetirementTitle">Aposentadoria Imobiliária</h2>
        <p>Transforme cartas em imóveis, aluguel e patrimônio ao longo do tempo.</p>
      </div>
      <span class="ai-retirement-badge">Imóveis</span>
    </div>

    <details class="ai-assumptions" id="aiAssumptions">
      <summary>
        <span>Premissas do cenário</span>
        <small>editar</small>
      </summary>
      <div class="ai-assumption-grid">
        <label>
          <span>Imóveis / cotas</span>
          <input id="aiPropertyCount" type="number" min="1" max="10" step="1" value="2">
        </label>
        <label>
          <span>Horizonte (anos)</span>
          <input id="aiHorizonYears" type="number" min="1" max="40" step="1" value="18">
        </label>
        <label>
          <span>Valorização imóvel % a.a.</span>
          <input id="aiPropertyGrowth" type="number" min="-20" max="30" step="0.01" value="4.82">
        </label>
        <label>
          <span>Aluguel mensal %</span>
          <input id="aiRentYield" type="number" min="0" max="5" step="0.01" value="0.60">
        </label>
        <label>
          <span>Documentação / custos %</span>
          <input id="aiDocsPct" type="number" min="0" max="20" step="0.01" value="3.00">
        </label>
        <label>
          <span>Reajuste crédito % a.a.</span>
          <input id="aiCreditGrowth" type="number" min="-20" max="30" step="0.01" value="6.00">
        </label>
      </div>
      <button class="ai-sync-main" id="aiSyncMain" type="button">↻ Usar valores atuais da simulação</button>
      <p class="ai-assumption-note">Premissas editáveis para cenário ilustrativo. Não representam garantia de valorização, aluguel ou contemplação.</p>
    </details>

    <div class="ai-impact-grid" id="aiImpactGrid"></div>
    <div class="ai-highlight" id="aiHighlight"></div>

    <div class="ai-section-title">
      <div>
        <strong>Efeito bola de neve</strong>
        <small>quanto o aluguel ajuda a carregar as parcelas</small>
      </div>
    </div>
    <div class="ai-snowball" id="aiSnowball"></div>

    <div class="ai-section-title">
      <div>
        <strong>Projeção ao longo do tempo</strong>
        <small>patrimônio e renda mensal de aluguel</small>
      </div>
    </div>
    <div class="ai-chart-card">
      <div class="ai-chart-legend">
        <span><i class="ai-dot ai-dot-house"></i> Patrimônio</span>
        <span><i class="ai-dot ai-dot-rent"></i> Aluguel mensal</span>
      </div>
      <div id="aiProjectionChart" class="ai-chart"></div>
      <small class="ai-chart-note">As duas curvas usam escalas independentes para facilitar a leitura.</small>
    </div>

    <div class="ai-section-title">
      <div>
        <strong>Planejamento resumido</strong>
        <small>um imóvel por cota</small>
      </div>
    </div>
    <div class="ai-summary-strip" id="aiSummaryStrip"></div>

    <div class="ai-section-title">
      <div>
        <strong>Planejamento detalhado</strong>
        <small>contemplação, compra, aluguel e patrimônio</small>
      </div>
    </div>
    <div class="ai-timeline" id="aiTimeline"></div>

    <div class="ai-retirement-disclaimer">
      Simulação ilustrativa. Contemplação, reajustes, valorização do imóvel, aluguel, custos e disponibilidade do bem podem variar. Não representa garantia de rentabilidade ou contemplação.
    </div>
  </section>
</div>
<!-- real-estate-retirement-v1:end -->
'''

anchor = '<div class="toast" id="toast">'
if anchor in text:
    text = text.replace(anchor, html + '\n' + anchor, 1)
else:
    text = text.replace('</body>', html + '\n</body>', 1)

css = r'''
/* real-estate-retirement-v1:start */
.ai-retirement-wrap{max-width:530px;margin:0 auto;padding:0 10px 18px}
.ai-retirement{padding:11px;overflow:hidden}
.ai-retirement-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}
.ai-retirement-eyebrow{color:#b42318;font-size:9px;font-weight:900;text-transform:uppercase;letter-spacing:.35px;margin-bottom:3px}
.ai-retirement-head h2{margin:0;font-size:19px;line-height:1.02;letter-spacing:-.35px}
.ai-retirement-head p{margin:4px 0 0;color:#667085;font-size:9.5px;line-height:1.3;font-weight:700}
.ai-retirement-badge{flex:0 0 auto;padding:5px 8px;border-radius:999px;background:#fff1f2;color:#c8161d;font-size:9px;font-weight:900}
.ai-assumptions{margin-top:9px;border:1px solid #e4e7ec;border-radius:14px;background:#fbfcfd;overflow:hidden}
.ai-assumptions summary{list-style:none;cursor:pointer;min-height:40px;padding:9px 10px;display:flex;align-items:center;justify-content:space-between;gap:8px;color:#344054;font-size:11px;font-weight:900}
.ai-assumptions summary::-webkit-details-marker{display:none}
.ai-assumptions summary small{color:#b42318;font-size:9px;font-weight:900}
.ai-assumption-grid{padding:0 9px 9px;display:grid;grid-template-columns:1fr 1fr;gap:6px}
.ai-assumption-grid label{border:1px solid #eaecf0;background:#fff;border-radius:11px;padding:7px 8px}
.ai-assumption-grid label span{display:block;color:#667085;font-size:8px;line-height:1.15;font-weight:900;text-transform:uppercase;letter-spacing:.2px;margin-bottom:4px}
.ai-assumption-grid input{width:100%;border:0;outline:0;background:transparent;color:#101828;padding:0;font-size:14px;font-weight:950}
.ai-sync-main{margin:0 9px 7px;width:calc(100% - 18px);min-height:34px;border:1px solid #fecaca;border-radius:11px;background:#fff5f5;color:#b42318;font-size:9.5px;font-weight:900}
.ai-assumption-note{margin:0;padding:0 10px 10px;color:#98a2b3;font-size:8px;line-height:1.3}
.ai-impact-grid{margin-top:9px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}
.ai-impact-card{min-height:68px;padding:8px;border:1px solid #eaecf0;border-radius:13px;background:#fff}
.ai-impact-card strong{display:block;color:#667085;font-size:8px;line-height:1.15;text-transform:uppercase;letter-spacing:.18px;font-weight:900}
.ai-impact-card b{display:block;margin-top:5px;color:#101828;font-size:16px;line-height:1;letter-spacing:-.3px}
.ai-impact-card small{display:block;margin-top:4px;color:#98a2b3;font-size:7.5px;line-height:1.2;font-weight:700}
.ai-impact-card.emphasis{background:linear-gradient(145deg,#fff5f5,#fff);border-color:#fecaca}
.ai-impact-card.emphasis b{color:#c8161d}
.ai-highlight{margin-top:7px;padding:10px;border-radius:14px;background:linear-gradient(145deg,#101828,#1d2939);color:#fff;font-size:10.5px;line-height:1.35;font-weight:800}
.ai-highlight b{color:#fda4af}
.ai-section-title{margin-top:13px;display:flex;align-items:flex-end;justify-content:space-between}
.ai-section-title strong{display:block;font-size:12px;color:#101828}
.ai-section-title small{display:block;margin-top:2px;color:#98a2b3;font-size:8px;font-weight:700}
.ai-snowball{margin-top:6px;padding:9px;border:1px solid #e4e7ec;border-radius:14px;background:#fbfcfd}
.ai-snow-stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}
.ai-snow-stat{padding:7px;border-radius:10px;background:#fff;border:1px solid #eaecf0}
.ai-snow-stat span{display:block;color:#667085;font-size:7.5px;font-weight:900;text-transform:uppercase}
.ai-snow-stat b{display:block;margin-top:3px;color:#101828;font-size:13px}
.ai-progress{margin-top:8px;height:10px;border-radius:999px;background:#eaecf0;overflow:hidden}
.ai-progress>i{display:block;height:100%;width:0;border-radius:999px;background:linear-gradient(90deg,#16a34a,#22c55e);transition:width .22s ease}
.ai-progress-copy{margin-top:5px;display:flex;align-items:center;justify-content:space-between;gap:6px;color:#667085;font-size:8px;font-weight:800}
.ai-progress-copy b{color:#067647}
.ai-chart-card{margin-top:6px;padding:8px;border:1px solid #e4e7ec;border-radius:14px;background:#fff}
.ai-chart-legend{display:flex;gap:10px;align-items:center;color:#667085;font-size:8px;font-weight:800}
.ai-dot{display:inline-block;width:7px;height:7px;border-radius:999px;margin-right:3px;vertical-align:middle}
.ai-dot-house{background:#c8161d}.ai-dot-rent{background:#16a34a}
.ai-chart{margin-top:6px;min-height:154px}.ai-chart svg{display:block;width:100%;height:auto}
.ai-chart-note{display:block;margin-top:2px;color:#98a2b3;font-size:7px;line-height:1.2}
.ai-summary-strip{margin-top:6px;display:flex;gap:7px;overflow-x:auto;padding-bottom:2px;scrollbar-width:none;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch}
.ai-summary-strip::-webkit-scrollbar{display:none}
.ai-summary-card{flex:0 0 210px;padding:9px;border:1px solid #e4e7ec;border-radius:14px;background:#fff}
.ai-summary-card-head{display:flex;align-items:center;justify-content:space-between;gap:6px}
.ai-summary-card-head strong{font-size:11px;color:#101828}.ai-summary-card-head span{padding:3px 6px;border-radius:999px;background:#ecfdf3;color:#067647;font-size:7.5px;font-weight:900}
.ai-summary-grid{margin-top:6px;display:grid;grid-template-columns:1fr 1fr;gap:5px}
.ai-summary-grid div{padding:5px 6px;border-radius:9px;background:#f9fafb}
.ai-summary-grid span{display:block;color:#98a2b3;font-size:6.8px;text-transform:uppercase;font-weight:900}
.ai-summary-grid b{display:block;margin-top:2px;color:#344054;font-size:9px}
.ai-timeline{position:relative;margin-top:7px;padding-left:22px}
.ai-timeline::before{content:"";position:absolute;left:7px;top:6px;bottom:8px;width:2px;border-radius:999px;background:#e4e7ec}
.ai-property{position:relative;margin-bottom:8px}.ai-property::before{content:"";position:absolute;left:-20px;top:15px;width:9px;height:9px;border-radius:999px;background:#16a34a;border:3px solid #fff;box-shadow:0 0 0 2px #16a34a}
.ai-property details{border:1px solid #d1fadf;border-radius:14px;background:#fff;overflow:hidden}
.ai-property summary{list-style:none;cursor:pointer;padding:9px 10px;display:flex;align-items:center;justify-content:space-between;gap:8px}
.ai-property summary::-webkit-details-marker{display:none}
.ai-property-title strong{display:block;color:#101828;font-size:11px}.ai-property-title small{display:block;margin-top:2px;color:#667085;font-size:8px}
.ai-property-summary-value{color:#067647;font-size:9px;font-weight:950;text-align:right}
.ai-property-body{padding:0 9px 9px}
.ai-property-controls{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:7px}
.ai-property-controls label{padding:6px 7px;border:1px solid #eaecf0;border-radius:10px;background:#fbfcfd}
.ai-property-controls span{display:block;color:#98a2b3;font-size:7px;text-transform:uppercase;font-weight:900;margin-bottom:3px}
.ai-property-controls input{width:100%;border:0;outline:0;padding:0;background:transparent;color:#101828;font-size:12px;font-weight:950}
.ai-year-strip{display:flex;gap:5px;overflow-x:auto;padding:1px 0 7px;scrollbar-width:none;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch}
.ai-year-strip::-webkit-scrollbar{display:none}
.ai-year-chip{flex:0 0 auto;min-width:34px;height:29px;padding:0 7px;border:1px solid #e4e7ec;border-radius:999px;background:#fff;color:#475467;font-size:9px;font-weight:900}
.ai-year-chip.active{background:#fff1f2;color:#c8161d;border-color:#fecaca}
.ai-property-copy{padding:8px;border-radius:10px;background:#f9fafb;color:#475467;font-size:9px;line-height:1.45;font-weight:700}.ai-property-copy b{color:#101828}
.ai-property-metrics{margin-top:7px;display:grid;grid-template-columns:1fr 1fr;gap:5px}
.ai-property-metric{padding:6px;border:1px solid #eaecf0;border-radius:9px;background:#fff}
.ai-property-metric span{display:block;color:#98a2b3;font-size:6.7px;text-transform:uppercase;font-weight:900}.ai-property-metric b{display:block;margin-top:2px;color:#344054;font-size:9px}
.ai-retirement-disclaimer{margin-top:10px;padding:8px 9px;border-radius:10px;background:#f9fafb;color:#98a2b3;font-size:7.5px;line-height:1.35}
@media (min-width:520px){.ai-impact-grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media (prefers-reduced-motion:reduce){.ai-progress>i{transition:none!important}}
/* real-estate-retirement-v1:end */
'''
text = text.replace('</style>', css + '\n</style>', 1)

js = r'''
/* real-estate-retirement-v1-js:start */
(function(){
  const root = document.getElementById('realEstateRetirementSection');
  if(!root) return;
  const $ai = id => document.getElementById(id);
  const state = {properties:[],lastMainCredit:null};

  const money = value => (Number(value)||0).toLocaleString('pt-BR',{style:'currency',currency:'BRL',maximumFractionDigits:2});
  const compactMoney = value => {
    const n = Number(value)||0;
    if(Math.abs(n)>=1000000) return `R$ ${(n/1000000).toLocaleString('pt-BR',{maximumFractionDigits:2})} mi`;
    if(Math.abs(n)>=1000) return `R$ ${(n/1000).toLocaleString('pt-BR',{maximumFractionDigits:1})} mil`;
    return money(n);
  };
  const num = value => {
    if(typeof value==='number') return Number.isFinite(value)?value:0;
    const raw=String(value??'').trim();
    if(!raw) return 0;
    if(raw.includes(',')&&raw.includes('.')) return Number(raw.replace(/\./g,'').replace(',','.'))||0;
    if(raw.includes(',')) return Number(raw.replace(',','.'))||0;
    return Number(raw.replace(/[^\d.-]/g,''))||0;
  };
  const clamp=(v,min,max)=>Math.min(Math.max(Number(v)||0,min),max);

  function isImoveis(){
    try{if(typeof active!=='undefined') return active==='imoveis'}catch(_){}
    const selected=document.querySelector('.seg.active');
    return !!selected&&/im[oó]veis/i.test(selected.textContent||'');
  }
  function mainCredit(){return Math.max(num(document.getElementById('credit')?.value),0)}
  function mainMonths(){return Math.max(parseInt(document.getElementById('months')?.value||'220',10)||220,1)}
  function mainFeePct(){
    const direct=num(document.getElementById('fee')?.value);
    if(direct) return direct;
    try{if(typeof presets!=='undefined'&&typeof active!=='undefined'&&presets[active]) return Number(presets[active].fee)||0}catch(_){}
    return 24.2;
  }
  function mainReservePct(){return Math.max(num(document.getElementById('reserve')?.value),0)}
  function mainAnnualAdjustment(){
    try{if(typeof presets!=='undefined'&&typeof active!=='undefined'&&presets[active]) return Number(presets[active].historicalRate)||6}catch(_){}
    return 6;
  }
  function currentContemplationMonth(){
    try{if(typeof projectionContemplationMonth==='function') return Math.max(Number(projectionContemplationMonth())||1,1)}catch(_){}
    const raw=Math.max(parseInt(document.getElementById('projectionContemplation')?.value||'1',10)||1,1);
    try{if(typeof projectionMode!=='undefined'&&projectionMode==='year') return raw*12}catch(_){}
    return raw;
  }
  function reducedSelected(){
    const reducedBtn=document.getElementById('reducedBtn');
    if(reducedBtn) return reducedBtn.classList.contains('active');
    try{if(typeof currentMode!=='undefined') return currentMode==='reduced'}catch(_){}
    return true;
  }

  function syncAssumptionsFromMain(forceProperties){
    const months=mainMonths();
    $ai('aiHorizonYears').value=String(Math.max(Math.ceil(months/12),1));
    $ai('aiCreditGrowth').value=Number(mainAnnualAdjustment()).toFixed(2);
    const credit=mainCredit(), cont=Math.min(currentContemplationMonth(),months);
    if(forceProperties||state.properties.length===0){
      const count=clamp(parseInt($ai('aiPropertyCount').value||'2',10),1,10);
      state.properties=Array.from({length:count},()=>({credit,manualCredit:false,contMonth:cont}));
    }else if(state.lastMainCredit!==credit){
      state.properties.forEach(p=>{if(!p.manualCredit)p.credit=credit});
    }
    state.lastMainCredit=credit;
  }

  function ensurePropertyCount(){
    const count=clamp(parseInt($ai('aiPropertyCount').value||'2',10),1,10);
    $ai('aiPropertyCount').value=String(count);
    const credit=mainCredit(),cont=Math.min(currentContemplationMonth(),mainMonths());
    while(state.properties.length<count) state.properties.push({credit,manualCredit:false,contMonth:cont});
    if(state.properties.length>count) state.properties.length=count;
  }

  function scenario(){
    const months=mainMonths();
    const horizonYears=clamp(num($ai('aiHorizonYears').value),1,40);
    const growth=clamp(num($ai('aiPropertyGrowth').value),-20,30)/100;
    const rentYield=clamp(num($ai('aiRentYield').value),0,5)/100;
    const docs=clamp(num($ai('aiDocsPct').value),0,20)/100;
    const creditGrowth=clamp(num($ai('aiCreditGrowth').value),-20,30)/100;
    const fee=mainFeePct()/100,reserve=mainReservePct()/100;
    const beforeFundFactor=reducedSelected()?.5:1;
    const items=state.properties.map((p,index)=>{
      const credit=Math.max(Number(p.credit)||0,0);
      const contMonth=clamp(Math.round(Number(p.contMonth)||1),1,months);
      const annualSteps=Math.max(Math.floor((contMonth-1)/12),0);
      const creditAtCont=credit*Math.pow(1+creditGrowth,annualSteps);
      const purchaseValue=Math.max(creditAtCont*(1-docs),0);
      const initialRent=purchaseValue*rentYield;
      const beforeParcel=credit*(beforeFundFactor+fee+reserve)/months;
      const afterParcel=creditAtCont*(1+fee+reserve)/months;
      const coverage=afterParcel>0?initialRent/afterParcel:0;
      const outOfPocket=Math.max(afterParcel-initialRent,0),surplus=Math.max(initialRent-afterParcel,0);
      const purchaseYear=contMonth/12,yearsAfterPurchase=Math.max(horizonYears-purchaseYear,0);
      const finalValue=purchaseValue*Math.pow(1+growth,yearsAfterPurchase);
      const finalRent=finalValue*rentYield;
      return {index:index+1,credit,contMonth,creditAtCont,purchaseValue,initialRent,beforeParcel,afterParcel,coverage,outOfPocket,surplus,purchaseYear,yearsAfterPurchase,finalValue,finalRent};
    });
    return {months,horizonYears,growth,rentYield,docs,creditGrowth,fee,reserve,beforeFundFactor,items};
  }

  function metric(icon,label,value,sub,emphasis){
    return `<div class="ai-impact-card${emphasis?' emphasis':''}"><strong>${icon} ${label}</strong><b>${value}</b><small>${sub}</small></div>`;
  }

  function buildImpact(sc){
    const items=sc.items;
    const creditTotal=items.reduce((s,p)=>s+p.credit,0),purchaseTotal=items.reduce((s,p)=>s+p.purchaseValue,0);
    const initialRent=items.reduce((s,p)=>s+p.initialRent,0),finalValue=items.reduce((s,p)=>s+p.finalValue,0),finalRent=items.reduce((s,p)=>s+p.finalRent,0);
    const avgCoverage=items.length?items.reduce((s,p)=>s+p.coverage,0)/items.length:0,pocket=items.reduce((s,p)=>s+p.outOfPocket,0);
    $ai('aiImpactGrid').innerHTML=[
      metric('🏠','Imóveis planejados',String(items.length),'cotas neste cenário',false),
      metric('💳','Crédito contratado',compactMoney(creditTotal),'soma das cartas',false),
      metric('🔑','Capital em imóveis',compactMoney(purchaseTotal),'após custos de compra',false),
      metric('🧱','Patrimônio projetado',compactMoney(finalValue),`ao fim de ${Math.round(sc.horizonYears)} anos`,true),
      metric('💰','Aluguel inicial',money(initialRent)+'/mês','quando todos estiverem locados',false),
      metric('🌱','Renda passiva final',money(finalRent)+'/mês','cenário projetado',true),
      metric('📊','Cobertura média',`${(avgCoverage*100).toLocaleString('pt-BR',{maximumFractionDigits:0})}%`,'aluguel ÷ parcela pós',false),
      metric('👛','Complemento estimado',money(pocket)+'/mês','logo após as contemplações',false)
    ].join('');
    $ai('aiHighlight').innerHTML=`Com este cenário, você projeta <b>${items.length} ${items.length===1?'imóvel':'imóveis'}</b>, patrimônio de <b>${money(finalValue)}</b> e renda mensal de <b>${money(finalRent)}</b> ao final de <b>${Math.round(sc.horizonYears)} anos</b>.`;
  }

  function buildSnowball(sc){
    if(!sc.items.length){$ai('aiSnowball').innerHTML='';return}
    const referenceMonth=Math.max(...sc.items.map(p=>p.contMonth));
    let parcel=0,rent=0;
    sc.items.forEach(p=>{
      const elapsedYears=Math.max((referenceMonth-p.contMonth)/12,0);
      const propertyNow=p.purchaseValue*Math.pow(1+sc.growth,elapsedYears);
      rent+=propertyNow*sc.rentYield;
      if(referenceMonth<=sc.months) parcel+=p.afterParcel;
    });
    const coverage=parcel>0?rent/parcel:(rent>0?1:0),pocket=Math.max(parcel-rent,0),surplus=Math.max(rent-parcel,0),pct=Math.max(coverage*100,0);
    $ai('aiSnowball').innerHTML=`<div class="ai-snow-stats">
      <div class="ai-snow-stat"><span>Parcelas ativas</span><b>${money(parcel)}</b></div>
      <div class="ai-snow-stat"><span>Aluguel total</span><b>${money(rent)}</b></div>
      <div class="ai-snow-stat"><span>Diferença do bolso</span><b>${money(pocket)}</b></div>
      <div class="ai-snow-stat"><span>Sobra estimada</span><b>${money(surplus)}</b></div>
    </div><div class="ai-progress"><i style="width:${Math.min(pct,100)}%"></i></div>
    <div class="ai-progress-copy"><span>Aluguel cobrindo as parcelas</span><b>${pct.toLocaleString('pt-BR',{maximumFractionDigits:0})}%</b></div>
    ${surplus>0?`<div class="ai-progress-copy"><span>Aluguel supera as parcelas neste cenário</span><b>+ ${money(surplus)}/mês</b></div>`:''}`;
  }

  function chartSeries(sc){
    const years=[],maxYear=Math.max(Math.round(sc.horizonYears),1);
    for(let y=0;y<=maxYear;y++){
      let patrimony=0,rent=0;
      sc.items.forEach(p=>{
        const month=y*12;
        if(month<p.contMonth)return;
        const elapsed=Math.max(y-p.purchaseYear,0),value=p.purchaseValue*Math.pow(1+sc.growth,elapsed);
        patrimony+=value;rent+=value*sc.rentYield;
      });
      years.push({y,patrimony,rent});
    }
    return years;
  }
  function svgPath(points,key,max,w,h,top){
    if(!points.length||max<=0)return'';
    return points.map((p,i)=>{
      const x=8+(points.length===1?0:i*(w-16)/(points.length-1)),y=top+h-((p[key]||0)/max)*h;
      return `${i?'L':'M'}${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');
  }
  function buildChart(sc){
    const data=chartSeries(sc),w=330,top1=18,h1=58,top2=98,h2=38;
    const maxP=Math.max(...data.map(d=>d.patrimony),1),maxR=Math.max(...data.map(d=>d.rent),1);
    const pathP=svgPath(data,'patrimony',maxP,w,h1,top1),pathR=svgPath(data,'rent',maxR,w,h2,top2);
    const milestoneYears=sc.items.map(p=>Math.max(Math.round(p.purchaseYear),0));
    const ticks=[0,Math.round(sc.horizonYears/2),Math.round(sc.horizonYears)].filter((v,i,a)=>a.indexOf(v)===i).map(y=>{
      const idx=Math.min(Math.max(y,0),data.length-1),x=8+(data.length===1?0:idx*(w-16)/(data.length-1));
      return `<text x="${x}" y="151" text-anchor="middle" font-size="7" fill="#98a2b3">${y}a</text>`;
    }).join('');
    const marks=milestoneYears.map((y,i)=>{
      const idx=Math.min(Math.max(y,0),data.length-1),x=8+(data.length===1?0:idx*(w-16)/(data.length-1));
      return `<line x1="${x}" x2="${x}" y1="12" y2="140" stroke="#d0d5dd" stroke-dasharray="2 3"/><circle cx="${x}" cy="12" r="3.2" fill="#16a34a"/><text x="${x+4}" y="14" font-size="6.5" fill="#667085">I${i+1}</text>`;
    }).join('');
    $ai('aiProjectionChart').innerHTML=`<svg viewBox="0 0 ${w} 158" role="img" aria-label="Projeção de patrimônio e aluguel">
      <rect x="0" y="0" width="${w}" height="158" rx="10" fill="#fbfcfd"/>
      <text x="8" y="12" font-size="7" font-weight="800" fill="#667085">Patrimônio · ${compactMoney(maxP)}</text>
      <path d="${pathP}" fill="none" stroke="#c8161d" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="8" y="92" font-size="7" font-weight="800" fill="#667085">Aluguel mensal · ${money(maxR)}</text>
      <path d="${pathR}" fill="none" stroke="#16a34a" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
      ${marks}${ticks}</svg>`;
  }

  function labelCont(month){if(month<=1)return'1º mês';return `${Math.max(Math.round(month/12),1)}º ano`}
  function buildSummary(sc){
    $ai('aiSummaryStrip').innerHTML=sc.items.map(p=>`<article class="ai-summary-card">
      <div class="ai-summary-card-head"><strong>${p.index}º imóvel</strong><span>${labelCont(p.contMonth)}</span></div>
      <div class="ai-summary-grid">
        <div><span>Carta</span><b>${compactMoney(p.credit)}</b></div>
        <div><span>Crédito na contemplação</span><b>${compactMoney(p.creditAtCont)}</b></div>
        <div><span>Valor para compra</span><b>${compactMoney(p.purchaseValue)}</b></div>
        <div><span>Aluguel inicial</span><b>${money(p.initialRent)}</b></div>
        <div><span>Valor final</span><b>${compactMoney(p.finalValue)}</b></div>
        <div><span>Aluguel final</span><b>${money(p.finalRent)}</b></div>
      </div></article>`).join('');
  }
  function buildYearChips(p,idx,sc){
    const horizon=Math.max(Math.ceil(Math.min(sc.horizonYears,sc.months/12)),1);
    let html=`<button type="button" class="ai-year-chip${p.contMonth===1?' active':''}" data-ai-property="${idx}" data-ai-month="1">1º m</button>`;
    for(let y=1;y<=horizon;y++){
      const month=Math.min(y*12,sc.months);
      html+=`<button type="button" class="ai-year-chip${p.contMonth===month?' active':''}" data-ai-property="${idx}" data-ai-month="${month}">${y}º</button>`;
    }
    return html;
  }
  function buildTimeline(sc){
    $ai('aiTimeline').innerHTML=sc.items.map((p,idx)=>{
      const coveragePct=p.coverage*100;
      const phrase=`No <b>${labelCont(p.contMonth)}</b>, a carta estimada de <b>${money(p.creditAtCont)}</b> gera um valor aproximado para compra de <b>${money(p.purchaseValue)}</b> após os custos informados. Com aluguel estimado de <b>${money(p.initialRent)}/mês</b>, o aluguel cobriria <b>${coveragePct.toLocaleString('pt-BR',{maximumFractionDigits:0})}%</b> da parcela pós estimada. Ao fim da projeção, este imóvel poderia atingir <b>${money(p.finalValue)}</b> e gerar <b>${money(p.finalRent)}/mês</b> de aluguel.`;
      return `<div class="ai-property"><details ${idx===0?'open':''}><summary>
        <div class="ai-property-title"><strong>${p.index}º imóvel</strong><small>${labelCont(p.contMonth)} · ${compactMoney(p.credit)}</small></div>
        <div class="ai-property-summary-value">${compactMoney(p.finalValue)}<br>${money(p.finalRent)}/mês</div>
      </summary><div class="ai-property-body">
        <div class="ai-property-controls">
          <label><span>Valor da carta</span><input type="number" min="0" step="1000" value="${Math.round(p.credit)}" data-ai-credit="${idx}"></label>
          <label><span>Contemplação</span><input type="text" value="${labelCont(p.contMonth)}" readonly tabindex="-1"></label>
        </div>
        <div class="ai-year-strip">${buildYearChips(p,idx,sc)}</div>
        <div class="ai-property-copy">${phrase}</div>
        <div class="ai-property-metrics">
          <div class="ai-property-metric"><span>Parcela antes</span><b>${money(p.beforeParcel)}</b></div>
          <div class="ai-property-metric"><span>Parcela pós estimada</span><b>${money(p.afterParcel)}</b></div>
          <div class="ai-property-metric"><span>Complemento do bolso</span><b>${money(p.outOfPocket)}</b></div>
          <div class="ai-property-metric"><span>Sobra de aluguel</span><b>${money(p.surplus)}</b></div>
        </div></div></details></div>`;
    }).join('');
    root.querySelectorAll('[data-ai-credit]').forEach(input=>{
      input.addEventListener('change',()=>{
        const idx=parseInt(input.getAttribute('data-ai-credit'),10);
        if(!state.properties[idx])return;
        state.properties[idx].credit=Math.max(num(input.value),0);state.properties[idx].manualCredit=true;render();
      });
    });
    root.querySelectorAll('[data-ai-month]').forEach(button=>{
      button.addEventListener('click',event=>{
        event.preventDefault();event.stopPropagation();
        const idx=parseInt(button.getAttribute('data-ai-property'),10),month=parseInt(button.getAttribute('data-ai-month'),10);
        if(!state.properties[idx])return;
        state.properties[idx].contMonth=clamp(month,1,mainMonths());render();
      });
    });
  }

  function updateNav(){
    const panel=document.querySelector('.floating-nav-list');
    if(!panel)return;
    let btn=panel.querySelector('[data-nav-target="#realEstateRetirementSection"]');
    if(!btn){
      btn=document.createElement('button');
      btn.className='floating-nav-item ai-retirement-nav';btn.type='button';btn.setAttribute('data-nav-target','#realEstateRetirementSection');
      btn.innerHTML='<span class="floating-nav-item-icon">🏘️</span><span class="floating-nav-item-copy"><strong>Aposentadoria imobiliária</strong></span>';
      panel.appendChild(btn);
      btn.addEventListener('click',()=>{
        const target=document.getElementById('realEstateRetirementSection'),navPanel=document.getElementById('floatingNavPanel'),navTrigger=document.getElementById('floatingNavTrigger');
        if(navPanel){navPanel.classList.remove('open');navPanel.setAttribute('aria-hidden','true')}
        if(navTrigger){navTrigger.classList.remove('open');navTrigger.setAttribute('aria-expanded','false')}
        if(target)requestAnimationFrame(()=>target.scrollIntoView({behavior:'smooth',block:'start'}));
      });
    }
    btn.style.display=isImoveis()?'':'none';
  }

  function render(){
    const visible=isImoveis(),wrap=document.getElementById('realEstateRetirementWrap');
    if(wrap)wrap.style.display=visible?'':'none';
    updateNav();if(!visible)return;
    ensurePropertyCount();
    const sc=scenario();buildImpact(sc);buildSnowball(sc);buildChart(sc);buildSummary(sc);buildTimeline(sc);
  }

  ['aiPropertyCount','aiHorizonYears','aiPropertyGrowth','aiRentYield','aiDocsPct','aiCreditGrowth'].forEach(id=>{
    $ai(id)?.addEventListener('input',()=>{if(id==='aiPropertyCount')ensurePropertyCount();render()});
    $ai(id)?.addEventListener('change',render);
  });
  $ai('aiSyncMain')?.addEventListener('click',()=>{syncAssumptionsFromMain(true);render()});
  document.addEventListener('click',event=>{
    const target=event.target;
    if(target&&target.closest&&target.closest('#realEstateRetirementSection'))return;
    if(target&&target.closest&&target.closest('.seg, #reducedBtn, #fullBtn, #projectionNumberBtn, #projectionMonthBtn, #projectionYearBtn')){
      setTimeout(()=>{syncAssumptionsFromMain(false);render()},80);
    }
  },true);
  ['credit','months','fee','reserve','projectionContemplation'].forEach(id=>{
    const el=document.getElementById(id);if(!el)return;
    el.addEventListener('input',()=>setTimeout(()=>{syncAssumptionsFromMain(false);render()},0));
    el.addEventListener('change',()=>setTimeout(()=>{syncAssumptionsFromMain(false);render()},0));
  });
  window.addEventListener('resize',()=>setTimeout(()=>buildChart(scenario()),80),{passive:true});
  syncAssumptionsFromMain(true);render();setTimeout(render,250);
})();
/* real-estate-retirement-v1-js:end */
'''
text = text.replace('</body>', '<script>\n' + js + '\n</script>\n</body>', 1)

index_path.write_text(text, encoding="utf-8")

sw_path = Path("calculadora/service-worker.js")
if sw_path.exists():
    sw = sw_path.read_text(encoding="utf-8")
    sw = re.sub(r'calculadora-ademicon-pwa-v\d+', 'calculadora-ademicon-pwa-v31', sw)
    sw_path.write_text(sw, encoding="utf-8")
