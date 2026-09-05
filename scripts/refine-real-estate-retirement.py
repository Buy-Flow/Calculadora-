from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Restaura o ponto-base caso esta versão já tenha sido aplicada em execução anterior.
text = re.sub(
    r'\n?<!-- real-estate-retirement-apollo-v2:start -->.*?<!-- real-estate-retirement-apollo-v2:end -->\n?',
    '\n    <div class="ai-impact-grid" id="aiImpactGrid"></div>\n',
    text,
    flags=re.S,
)
text = re.sub(
    r'\n?/\* real-estate-retirement-apollo-v2:start \*/.*?/\* real-estate-retirement-apollo-v2:end \*/\n?',
    '\n',
    text,
    flags=re.S,
)

base = '    <div class="ai-impact-grid" id="aiImpactGrid"></div>'
replacement = '''
<!-- real-estate-retirement-apollo-v2:start -->
    <div class="ai-apollo-plan-head">
      <span>📋 Planejamento</span>
      <small>resumo do cenário em tempo real</small>
    </div>
    <div class="ai-impact-grid" id="aiImpactGrid"></div>
    <div class="ai-outcome-grid" id="aiOutcomeGrid"></div>
<!-- real-estate-retirement-apollo-v2:end -->'''
if base in text:
    text = text.replace(base, replacement, 1)

# Substitui apenas a função de resumo, preservando todo o restante da aposentadoria imobiliária.
start = text.find('  function buildImpact(sc){')
end = text.find('\n  function buildSnowball(sc){', start)
if start != -1 and end != -1:
    new_function = r'''  function buildImpact(sc){
    const items=sc.items;
    const creditTotal=items.reduce((s,p)=>s+p.credit,0);
    const creditReleased=items.reduce((s,p)=>s+p.creditAtCont,0);
    const purchaseTotal=items.reduce((s,p)=>s+p.purchaseValue,0);
    const initialParcel=items.reduce((s,p)=>s+p.beforeParcel,0);
    const postParcel=items.reduce((s,p)=>s+p.afterParcel,0);
    const initialRent=items.reduce((s,p)=>s+p.initialRent,0);
    const finalValue=items.reduce((s,p)=>s+p.finalValue,0);
    const finalRent=items.reduce((s,p)=>s+p.finalRent,0);
    const avgCoverage=items.length?items.reduce((s,p)=>s+p.coverage,0)/items.length:0;
    const pocket=items.reduce((s,p)=>s+p.outOfPocket,0);
    const rentPct=sc.rentYield*100;
    const reajustePct=sc.creditGrowth*100;

    $ai('aiImpactGrid').innerHTML=[
      metric('🏠','Cotas',String(items.length),'um imóvel planejado por cota',false),
      metric('💳','Crédito inicial',compactMoney(creditTotal),'soma das cartas deste cenário',false),
      metric('🔓','Crédito liberado planejado',compactMoney(creditReleased),'estimativa das cartas na contemplação',false),
      metric('🧾','Parcelas iniciais',money(initialParcel)+'/mês','antes das contemplações',false),
      metric('💰','Aluguel previsto',`${rentPct.toLocaleString('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2})}% a.m.`,`${money(initialRent)}/mês quando todos estiverem locados`,false),
      metric('📈','Reajuste usado',`${reajustePct.toLocaleString('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2})}% a.a.`,'premissa editável do cenário',false)
    ].join('');

    const outcome=$ai('aiOutcomeGrid');
    if(outcome){
      outcome.innerHTML=[
        metric('🔑','Valor dos imóveis na compra',compactMoney(purchaseTotal),'após a premissa de custos/documentação',false),
        metric('💵','Aluguel inicial',money(initialRent)+'/mês','renda estimada após as aquisições',false),
        metric('🧱','Patrimônio projetado',compactMoney(finalValue),`ao fim de ${Math.round(sc.horizonYears)} anos`,true),
        metric('🌱','Renda passiva final',money(finalRent)+'/mês','aluguel mensal no fim do horizonte',true),
        metric('📊','Cobertura média',`${(avgCoverage*100).toLocaleString('pt-BR',{maximumFractionDigits:0})}%`,'aluguel ÷ parcela pós-contemplação',false),
        metric('👛','Complemento estimado',money(pocket)+'/mês',`parcelas pós estimadas: ${money(postParcel)}/mês`,false)
      ].join('');
    }

    $ai('aiHighlight').innerHTML=`Com este cenário, você começa com <b>${items.length} ${items.length===1?'cota':'cotas'}</b> e <b>${money(creditTotal)}</b> em crédito. Depois das contemplações, o planejamento projeta cerca de <b>${money(purchaseTotal)}</b> convertidos em imóveis. Ao final de <b>${Math.round(sc.horizonYears)} anos</b>, o patrimônio projetado é de <b>${money(finalValue)}</b>, com renda mensal estimada de <b>${money(finalRent)}</b>.`;
  }
'''
    text = text[:start] + new_function.rstrip() + '\n' + text[end:]

css = r'''
/* real-estate-retirement-apollo-v2:start */
.ai-apollo-plan-head{
  margin-top:10px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:8px;
  padding:0 2px;
}
.ai-apollo-plan-head span{
  color:#101828;
  font-size:12px;
  line-height:1;
  font-weight:950;
}
.ai-apollo-plan-head small{
  color:#98a2b3;
  font-size:7.5px;
  line-height:1;
  font-weight:800;
}
.ai-outcome-grid{
  margin-top:7px;
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:6px;
}
.ai-outcome-grid .ai-impact-card{
  min-height:72px;
}
.ai-retirement .ai-impact-grid{
  margin-top:6px;
}
@media (max-width:360px){
  .ai-apollo-plan-head small{font-size:7px}
  .ai-impact-card b{font-size:15px}
}
/* real-estate-retirement-apollo-v2:end */
'''
text = text.replace('</style>', css + '\n</style>', 1)

index_path.write_text(text, encoding='utf-8')

# Renova o cache do PWA para a nova versão chegar também ao app instalado.
sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    match = re.search(r'calculadora-ademicon-pwa-v(\d+)', sw)
    if match:
        version = int(match.group(1)) + 1
        sw = re.sub(r'calculadora-ademicon-pwa-v\d+', f'calculadora-ademicon-pwa-v{version}', sw)
    sw_path.write_text(sw, encoding='utf-8')
