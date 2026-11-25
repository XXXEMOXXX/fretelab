"""Gera tabela/index.html (página única, sem servidor) a partir de dados/tabela_fretes.csv."""
import csv
import json
from pathlib import Path

BASE = Path(__file__).parent
with open(BASE / "dados" / "tabela_fretes.csv", encoding="utf-8") as f:
    dados = [{"o": r["origem_nome"], "d": r["destino_nome"], "km": int(r["km"]),
              "p": r["perfil"], "v": float(r["valor_tabela"])} for r in csv.DictReader(f)]

HTML = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FreteLab · Tabela de fretes</title>
<style>
:root{--bg:#f6f7f9;--card:#fff;--tx:#1b1f24;--mut:#6a737d;--ac:#d1242f;--bd:#e1e4e8}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0e1013;--card:#171a1f;--tx:#e8eaed;--mut:#8b949e;--ac:#ff5a64;--bd:#2a2f36}}
:root[data-theme=dark]{--bg:#0e1013;--card:#171a1f;--tx:#e8eaed;--mut:#8b949e;--ac:#ff5a64;--bd:#2a2f36}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.5 system-ui,sans-serif}
main{max-width:980px;margin:0 auto;padding:20px 16px 48px}
header{display:flex;justify-content:space-between;align-items:center;gap:12px}
h1{font-size:22px;margin:0}h1 span{color:var(--ac)}
button{background:var(--card);color:var(--tx);border:1px solid var(--bd);border-radius:8px;padding:6px 12px;cursor:pointer}
.sub{color:var(--mut);margin:4px 0 16px}
.filtros{display:grid;grid-template-columns:2fr 1fr 1fr;gap:10px;margin-bottom:14px}
input,select{width:100%;padding:10px;border:1px solid var(--bd);border-radius:8px;background:var(--card);color:var(--tx);font:inherit}
.card{background:var(--card);border:1px solid var(--bd);border-radius:12px;overflow:hidden}
table{width:100%;border-collapse:collapse}th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--bd)}
th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);cursor:pointer;user-select:none}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
tr:last-child td{border-bottom:0}.tag{font-size:12px;padding:2px 8px;border-radius:99px;border:1px solid var(--bd);color:var(--mut)}
.cont{color:var(--mut);margin:10px 2px;font-size:13px}
@media(max-width:640px){.filtros{grid-template-columns:1fr}th:nth-child(3),td:nth-child(3){display:none}}
</style></head><body><main>
<header><h1>Frete<span>Lab</span> · Tabela de fretes</h1><button id="tema">Tema</button></header>
<p class="sub">Demo com dados fictícios. Busque por origem/destino e filtre por perfil de veículo.</p>
<div class="filtros">
 <input id="q" placeholder="Buscar origem ou destino…" aria-label="Buscar">
 <select id="perfil" aria-label="Perfil"><option value="">Todos os perfis</option></select>
 <select id="ordem" aria-label="Ordenar"><option value="v">Menor valor</option><option value="-v">Maior valor</option><option value="km">Menor distância</option></select>
</div>
<div class="card"><table><thead><tr><th>Origem</th><th>Destino</th><th class="n">Km</th><th>Perfil</th><th class="n">Valor (R$)</th></tr></thead><tbody id="corpo"></tbody></table></div>
<p class="cont" id="cont"></p>
</main>
<script>
const DADOS=__DADOS__;
const $=id=>document.getElementById(id);
[...new Set(DADOS.map(x=>x.p))].forEach(p=>$('perfil').add(new Option(p,p)));
const brl=n=>n.toLocaleString('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2});
function render(){
  const q=$('q').value.trim().toLowerCase(),p=$('perfil').value,o=$('ordem').value;
  let r=DADOS.filter(x=>(!p||x.p===p)&&(!q||(x.o+' '+x.d).toLowerCase().includes(q)));
  r.sort((a,b)=>o==='km'?a.km-b.km:o==='-v'?b.v-a.v:a.v-b.v);
  $('corpo').innerHTML=r.slice(0,200).map(x=>`<tr><td>${x.o}</td><td>${x.d}</td><td class="n">${x.km}</td><td><span class="tag">${x.p}</span></td><td class="n">${brl(x.v)}</td></tr>`).join('');
  $('cont').textContent=`${r.length} de ${DADOS.length} tarifas`+(r.length>200?' (mostrando 200)':'');
}
['q','perfil','ordem'].forEach(i=>$(i).addEventListener('input',render));
$('tema').onclick=()=>{const d=document.documentElement,c=d.dataset.theme||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');d.dataset.theme=c==='dark'?'light':'dark'};
render();
</script></body></html>"""
out = BASE / "tabela"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(HTML.replace("__DADOS__", json.dumps(dados, ensure_ascii=False)), encoding="utf-8")
print("tabela/index.html:", len(dados), "tarifas")
