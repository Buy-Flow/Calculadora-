from pathlib import Path

path = Path('calculadora/index.html')
text = path.read_text(encoding='utf-8')

SECTION_ID = 'inccSalarySection'

css = r'''

/* incc-salary-history-v1 */
.incc-salary-section{padding:11px;overflow:hidden}
.incc-history-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px}
.incc-history-card{padding:9px;border:1px solid #eaecf0;border-radius:11px;background:#fff}
.incc-history-card.salary{background:#ecfdf3;border-color:#abefc6}
.incc-history-card.incc{background:#fff7ed;border-color:#fed7aa}
.incc-history-card span{display:block;color:#667085;font-size:7px;line-height:1.1;font-weight:900;text-transform:uppercase}
.incc-history-card strong{display:block;margin-top:3px;color:#101828;font-size:17px;line-height:1;font-weight:950}
.incc-history-card.salary strong{color:#067647}
.incc-history-card.incc strong{color:#b54708}
.incc-history-card small{display:block;margin-top:3px;color:#667085;font-size:7.3px;line-height:1.2;font-weight:750}
.incc-bars{margin-top:8px;padding:9px;border-radius:11px;background:#f8fafc;border:1px solid #eaecf0}
.incc-bar-row+ .incc-bar-row{margin-top:7px}
.incc-bar-head{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px;color:#475467;font-size:8px;font-weight:900}
.incc-bar-track{height:8px;border-radius:999px;background:#e9edf2;overflow:hidden}
.incc-bar-fill{height:100%;border-radius:999px}
.incc-bar-fill.salary{width:100%;background:#079455}
.incc-bar-fill.incc{width:67.5%;background:#f79009}
.incc-client-argument{margin-top:8px;padding:10px;border-radius:12px;background:linear-gradient(145deg,#101b2d,#172438);color:#fff}
.incc-client-argument span{display:block;color:#c8d0dd;font-size:7px;font-weight:900;text-transform:uppercase;letter-spacing:.25px}
.incc-client-argument strong{display:block;margin-top:4px;font-size:11px;line-height:1.35;font-weight:850}
.incc-history-details{margin-top:8px;border:1px solid #eaecf0;border-radius:10px;background:#fff;overflow:hidden}
.incc-history-details>summary{list-style:none;display:flex;align-items:center;justify-content:space-between;gap:8px;padding:9px;cursor:pointer;color:#344054;font-size:9px;font-weight:900}
.incc-history-details>summary::-webkit-details-marker{display:none}
.incc-history-details>summary:after{content:'⌄';font-size:16px;line-height:1;color:#667085;transition:transform .18s ease}
.incc-history-details[open]>summary:after{transform:rotate(180deg)}
.incc-history-table-wrap{max-height:310px;overflow:auto;border-top:1px solid #eef0f3}
.incc-history-table{width:100%;border-collapse:collapse;font-size:7.4px}
.incc-history-table th{position:sticky;top:0;background:#f8fafc;color:#667085;text-align:left;padding:7px 6px;font-size:6.8px;text-transform:uppercase;letter-spacing:.2px}
.incc-history-table td{padding:6px;border-top:1px solid #f0f1f3;color:#475467;font-weight:750}
.incc-history-table td:nth-child(2),.incc-history-table td:nth-child(3){text-align:right}
.incc-history-table td:last-child{text-align:right;font-weight:900}
.incc-history-table .salary-win{color:#067647}
.incc-history-table .incc-win{color:#b54708}
.incc-history-note{margin:7px 1px 0;color:#667085;font-size:7px;line-height:1.3;font-weight:700}
'''

html = r'''

    <section class="card incc-salary-section section" id="inccSalarySection">
      <div class="comparison-head">
        <div>
          <h2>INCC-M <em>x</em> salário mínimo</h2>
          <p>Uma referência histórica para entender o reajuste da carta.</p>
        </div>
        <span class="comparison-badge">2006–2025</span>
      </div>

      <div class="incc-history-grid">
        <div class="incc-history-card salary">
          <span>Salário mínimo subiu mais</span>
          <strong>15 de 20 anos</strong>
          <small>Acumulado aproximado: +406% • média composta: 8,44% a.a.</small>
        </div>
        <div class="incc-history-card incc">
          <span>INCC-M subiu mais</span>
          <strong>5 de 20 anos</strong>
          <small>Acumulado aproximado: +274% • média composta: 6,82% a.a.</small>
        </div>
      </div>

      <div class="incc-bars" aria-label="Comparação do crescimento acumulado entre salário mínimo e INCC-M">
        <div class="incc-bar-row">
          <div class="incc-bar-head"><span>💰 Salário mínimo</span><strong>+406%</strong></div>
          <div class="incc-bar-track"><div class="incc-bar-fill salary"></div></div>
        </div>
        <div class="incc-bar-row">
          <div class="incc-bar-head"><span>🏗️ INCC-M</span><strong>+274%</strong></div>
          <div class="incc-bar-track"><div class="incc-bar-fill incc"></div></div>
        </div>
      </div>

      <div class="incc-client-argument">
        <span>Argumento para apresentar ao cliente</span>
        <strong>“O reajuste não aumenta só a parcela: ele também atualiza o valor da sua carta. E, olhando os últimos 20 anos, o salário mínimo subiu mais que o INCC-M em 15 deles. No acumulado, foram cerca de 406% contra 274% do INCC-M.”</strong>
      </div>

      <details class="incc-history-details">
        <summary>Ver histórico ano a ano</summary>
        <div class="incc-history-table-wrap">
          <table class="incc-history-table">
            <thead><tr><th>Ano</th><th>INCC-M</th><th>Salário</th><th>Subiu mais</th></tr></thead>
            <tbody>
              <tr><td>2006</td><td>5,05%</td><td>16,67%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2007</td><td>6,03%</td><td>8,57%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2008</td><td>11,97%</td><td>9,21%</td><td class="incc-win">INCC</td></tr>
              <tr><td>2009</td><td>3,21%</td><td>12,05%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2010</td><td>7,57%</td><td>9,68%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2011</td><td>7,58%</td><td>6,86%</td><td class="incc-win">INCC</td></tr>
              <tr><td>2012</td><td>7,25%</td><td>14,13%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2013</td><td>8,07%</td><td>9,00%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2014</td><td>6,74%</td><td>6,78%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2015</td><td>7,22%</td><td>8,84%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2016</td><td>6,34%</td><td>11,68%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2017</td><td>4,03%</td><td>6,48%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2018</td><td>3,97%</td><td>1,81%</td><td class="incc-win">INCC</td></tr>
              <tr><td>2019</td><td>4,13%</td><td>4,61%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2020</td><td>8,68%</td><td>4,71%</td><td class="incc-win">INCC</td></tr>
              <tr><td>2021</td><td>14,03%</td><td>5,26%</td><td class="incc-win">INCC</td></tr>
              <tr><td>2022</td><td>9,41%</td><td>10,18%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2023</td><td>3,32%</td><td>8,91%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2024</td><td>6,34%</td><td>6,97%</td><td class="salary-win">Salário</td></tr>
              <tr><td>2025</td><td>6,10%</td><td>7,51%</td><td class="salary-win">Salário</td></tr>
            </tbody>
          </table>
        </div>
      </details>

      <p class="incc-history-note">Referência histórica usando INCC-M e salário mínimo. Desempenho passado não garante reajustes futuros e a renda individual de cada cliente pode seguir uma trajetória diferente.</p>
    </section>
'''

if SECTION_ID not in text:
    if '</style>' not in text:
        raise SystemExit('style marker not found')
    text = text.replace('</style>', css + '\n</style>', 1)

    marker = '    <section class="card rent-investment-section section" id="rentInvestmentSection">'
    if marker not in text:
        raise SystemExit('rent investment section marker not found')
    text = text.replace(marker, html + '\n' + marker, 1)

    js_marker = '  const section = $("rentInvestmentSection");\n  if(!section) return;'
    js_replacement = '  const inccSalarySection = $("inccSalarySection");\n  if(inccSalarySection) inccSalarySection.style.display = active === "imoveis" ? "" : "none";\n\n' + js_marker
    if js_marker not in text:
        raise SystemExit('render marker not found')
    text = text.replace(js_marker, js_replacement, 1)

path.write_text(text, encoding='utf-8')
