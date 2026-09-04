from pathlib import Path
import re

index_path = Path('calculadora/index.html')
text = index_path.read_text(encoding='utf-8')

# Torna os textos do bloco dinâmicos conforme o índice do segmento.
text = text.replace(
    '<p>Como a mesma parcela teria evoluído pelo INCC-M e pela evolução do salário mínimo.</p>',
    '<p id="historyIndexIntro">Como a mesma parcela teria evoluído pelo índice do segmento e pela evolução do salário mínimo.</p>'
)
text = text.replace(
    '<span>🏗️ Parcela corrigida pelo INCC-M</span>',
    '<span id="historyIndexParcelLabel">📊 Parcela corrigida pelo índice do segmento</span>'
)
text = text.replace(
    '<span>🏗️ A carta de crédito, seguindo o mesmo INCC-M</span>',
    '<span id="historyCreditIndexLabel">📊 A carta de crédito, seguindo o mesmo índice</span>'
)
text = text.replace(
    '<p class="incc-history-note"><strong>* Comparação normalizada:</strong> o valor da coluna “Salário” não é o salário mínimo oficial daquele ano. Os dois caminhos começam exatamente na mesma parcela exibida pela calculadora. Um acompanha a evolução proporcional do salário mínimo; o outro, o INCC-M histórico. A carta é projetada pelo mesmo INCC-M apenas para visualizar a valorização proporcional. Desempenho passado não garante reajustes futuros.</p>',
    '<p class="incc-history-note" id="historyIndexNote"><strong>* Comparação normalizada:</strong> os dois caminhos começam exatamente na mesma parcela exibida pela calculadora. Um acompanha a evolução proporcional do salário mínimo; o outro, o índice histórico do segmento. Desempenho passado não garante reajustes futuros.</p>'
)

# Histórico oficial anual do IBGE para INPC e IPCA. INCC-M mantém a série já usada no site.
index_data = r'''
const PARCEL_INDEX_HISTORY_INPC_18Y = {
  2008:6.48, 2009:4.11, 2010:6.47, 2011:6.08, 2012:6.20, 2013:5.56,
  2014:6.23, 2015:11.28, 2016:6.58, 2017:2.07, 2018:3.43, 2019:4.48,
  2020:5.45, 2021:10.16, 2022:5.93, 2023:3.71, 2024:4.77, 2025:3.90
};
const PARCEL_INDEX_HISTORY_IPCA_18Y = {
  2008:5.90, 2009:4.31, 2010:5.91, 2011:6.50, 2012:5.84, 2013:5.91,
  2014:6.41, 2015:10.67, 2016:6.29, 2017:2.95, 2018:3.75, 2019:4.31,
  2020:4.52, 2021:10.06, 2022:5.79, 2023:4.62, 2024:4.83, 2025:4.26
};
'''

marker = 'const PARCEL_INDEX_HISTORY_INPC_18Y = {'
if marker not in text:
    anchor = 'function historyPctBR(value){'
    if anchor in text:
        text = text.replace(anchor, index_data + '\n' + anchor, 1)

new_function = r'''function renderParcelSalaryHistory18Y({baseParcel=0,credit=0}={}){
  const section=$("inccSalarySection");
  if(!section) return;

  // A comparação agora existe em todos os segmentos.
  section.style.display = "";

  const parcel=Math.max(Number(baseParcel)||0,0);
  const baseCredit=Math.max(Number(credit)||0,0);
  if(parcel<=0) return;

  const configuredIndex = String(presets?.[active]?.index || "INCC").toUpperCase();
  const indexKey = configuredIndex.includes("INPC")
    ? "INPC"
    : configuredIndex.includes("IPCA")
      ? "IPCA"
      : "INCC-M";
  const indexLabel = indexKey;
  const indexIcon = indexKey === "INCC-M" ? "🏗️" : "📊";

  const salaryBase=380;
  const salaryEndOfficial=1518;
  const salaryFactor=salaryEndOfficial/salaryBase;
  let indexFactor=1;
  const rows=[];

  const rateFor = item => {
    if(indexKey === "INPC") return Number(PARCEL_INDEX_HISTORY_INPC_18Y[item.year]) || 0;
    if(indexKey === "IPCA") return Number(PARCEL_INDEX_HISTORY_IPCA_18Y[item.year]) || 0;
    return Number(item.incc) || 0;
  };

  PARCEL_HISTORY_18Y.forEach(item=>{
    const indexRate = rateFor(item);
    indexFactor *= (1 + indexRate/100);
    const salaryIndexed = parcel * (item.minWage/salaryBase);
    const indexedParcel = parcel * indexFactor;
    const salaryWins = item.salaryPct > indexRate;
    rows.push({
      ...item,
      indexRate,
      salaryIndexed,
      indexedParcel,
      winner:salaryWins ? 'salary' : 'incc',
      winnerLabel:salaryWins ? '💰 Salário' : `${indexIcon} ${indexLabel}`
    });
  });

  const salaryEnd=parcel*salaryFactor;
  const indexEnd=parcel*indexFactor;
  const creditEnd=baseCredit*indexFactor;
  const diff=salaryEnd-indexEnd;
  const diffPct=indexEnd>0 ? (diff/indexEnd)*100 : 0;
  const salaryGrowth=(salaryFactor-1)*100;
  const indexGrowth=(indexFactor-1)*100;
  const salaryCagr=(Math.pow(salaryFactor,1/18)-1)*100;
  const indexCagr=(Math.pow(indexFactor,1/18)-1)*100;

  if($("historyIndexIntro")) $("historyIndexIntro").textContent=`Como a mesma parcela teria evoluído pelo ${indexLabel} e pela evolução do salário mínimo.`;
  if($("historyIndexParcelLabel")) $("historyIndexParcelLabel").textContent=`${indexIcon} Parcela corrigida pelo ${indexLabel}`;
  if($("historyCreditIndexLabel")) $("historyCreditIndexLabel").textContent=`${indexIcon} A carta de crédito, seguindo o mesmo ${indexLabel}`;

  if($("historyCreditBase")) $("historyCreditBase").textContent=money(baseCredit);
  if($("historyParcelBase")) $("historyParcelBase").textContent=money(parcel);
  if($("historySalaryEnd")) $("historySalaryEnd").textContent=money(salaryEnd);
  if($("historyInccEnd")) $("historyInccEnd").textContent=money(indexEnd);
  if($("historyCreditEnd")) $("historyCreditEnd").textContent=money(creditEnd);
  if($("historyDiff")) $("historyDiff").textContent=`${money(Math.abs(diff))} ${diff>=0?'a favor do salário':`a favor do ${indexLabel}`}`;

  if($("historySalaryMeta")) $("historySalaryMeta").textContent=`+${historyPctBR(salaryGrowth)} no período • média ${historyPctBR(salaryCagr)} a.a.`;
  if($("historyInccMeta")) $("historyInccMeta").textContent=`+${historyPctBR(indexGrowth)} no período • média ${historyPctBR(indexCagr)} a.a.`;
  if($("historyCreditMeta")) $("historyCreditMeta").textContent=`A carta de ${money(baseCredit)} chegaria a aproximadamente ${money(creditEnd)} aplicando o ${indexLabel} histórico do período.`;
  if($("historyDiffMeta")) $("historyDiffMeta").textContent=`Partindo da mesma parcela de ${money(parcel)}, a evolução do salário termina ${historyPctBR(Math.abs(diffPct))} ${diff>=0?'acima':'abaixo'} da parcela corrigida pelo ${indexLabel}.`;
  if($("historyClientText")) $("historyClientText").textContent=`Imagine esta mesma carta de ${money(baseCredit)} com uma parcela inicial de ${money(parcel)} há 18 anos. Corrigindo a parcela pelo ${indexLabel} histórico, ela chegaria hoje a cerca de ${money(indexEnd)}. Usando exatamente a mesma parcela inicial, mas acompanhando a evolução do salário mínimo, o equivalente chegaria a ${money(salaryEnd)}. Os dois caminhos começam iguais para mostrar, de forma proporcional, qual cresceu mais no período.`;
  if($("historyIndexNote")) $("historyIndexNote").innerHTML=`<strong>* Comparação normalizada:</strong> o valor da coluna “Salário” não é o salário mínimo oficial daquele ano. Os dois caminhos começam exatamente na mesma parcela exibida pela calculadora. Um acompanha a evolução proporcional do salário mínimo; o outro, o ${indexLabel} histórico. A carta é projetada pelo mesmo ${indexLabel} apenas para visualizar a valorização proporcional. Desempenho passado não garante reajustes futuros.`;

  const body=$("history18Body");
  if(body){
    body.innerHTML=rows.map((row,index)=>`
      <tr class="${index===rows.length-1?'latest-year':''}">
        <td>${row.year}</td>
        <td>${money(row.salaryIndexed)}<span class="parcel-history-value-sub">+${historyPctBR(row.salaryPct)}</span></td>
        <td>${money(row.indexedParcel)}<span class="parcel-history-value-sub">${indexLabel} ${historyPctBR(row.indexRate)}</span></td>
        <td class="winner-cell"><span class="winner-badge ${row.winner}">${row.winnerLabel}</span></td>
      </tr>`).join('');
  }
}
'''

start = text.find('function renderParcelSalaryHistory18Y(')
end = text.find('\nfunction renderRentInvestmentComparison(', start)
if start != -1 and end != -1:
    text = text[:start] + new_function.rstrip() + '\n' + text[end:]

# Atualiza o cache do PWA sem depender de um número fixo.
sw_path = Path('calculadora/service-worker.js')
if sw_path.exists():
    sw = sw_path.read_text(encoding='utf-8')
    match = re.search(r'calculadora-ademicon-pwa-v(\d+)', sw)
    if match:
        version = int(match.group(1)) + 1
        sw = re.sub(r'calculadora-ademicon-pwa-v\d+', f'calculadora-ademicon-pwa-v{version}', sw)
    sw_path.write_text(sw, encoding='utf-8')

index_path.write_text(text, encoding='utf-8')
