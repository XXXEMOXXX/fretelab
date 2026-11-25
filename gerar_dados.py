"""Gera dados 100% FICTÍCIOS para o demo FreteLab (seed fixa, reproduzível)."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(2026)
OUT = Path(__file__).parent / "dados"
OUT.mkdir(exist_ok=True)

HUBS = {
    "H01": ("Polo Norte", "Aurora do Vale"), "H02": ("Polo Sul", "Rio Claro do Sul"),
    "H03": ("Porto Seco", "Serra Alta"), "H04": ("Entreposto Leste", "Vila Nova do Leste"),
    "H05": ("Centro Oeste", "Campo Largo"), "H06": ("Hub Litoral", "Praia Dourada"),
    "H07": ("Hub Planalto", "Monte Verde"), "H08": ("Terminal Rio Doce", "Barra do Rio"),
}
PERFIS = {  # perfil: (ordem de tamanho, R$ por km)
    "Utilitário": (1, 2.10), "VUC": (2, 2.80), "Toco": (3, 3.60),
    "Truck": (4, 4.70), "Carreta": (5, 6.20),
}
CLIENTES = ["Cliente A", "Cliente B", "Cliente C"]

codes = list(HUBS)
dist = {}
for a in codes:
    for b in codes:
        if a < b:
            dist[(a, b)] = dist[(b, a)] = random.randint(60, 900)

# 1) tabela de fretes (rota x perfil)
tabela = {}
rows = []
for (o, d), km in sorted(dist.items()):
    for perfil, (_, rkm) in PERFIS.items():
        valor = round(km * rkm * random.uniform(0.95, 1.05) + 120, 2)
        tabela[(o, d, perfil)] = valor
        rows.append([o, HUBS[o][0], d, HUBS[d][0], km, perfil, valor])
with open(OUT / "tabela_fretes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["origem", "origem_nome", "destino", "destino_nome", "km", "perfil", "valor_tabela"])
    w.writerows(rows)

# 2) viagens do período, com divergências plantadas
viagens = []
inicio = date(2026, 3, 1)
for i in range(1, 241):
    o, d = random.sample(codes, 2)
    perfil = random.choice(list(PERFIS))
    valor = tabela[(o, d, perfil)]
    erro = ""
    r = random.random()
    if r < 0.07:
        valor = round(valor * random.choice([0.9, 1.12, 1.25]), 2); erro = "valor"
    elif r < 0.10:
        perfil_ant = perfil
        perfil = random.choice([p for p in PERFIS if p != perfil_ant])  # cobrou perfil diferente do tabelado
        erro = "perfil"
    elif r < 0.12:
        d = "H99"; erro = "rota"  # rota sem tabela: destino inexistente
    id_viagem = f"V{i:05d}" if random.random() > 0.03 else ""
    viagens.append({
        "id_viagem": id_viagem, "data": (inicio + timedelta(days=random.randint(0, 14))).isoformat(),
        "cliente": random.choice(CLIENTES), "origem": o, "destino": d, "perfil": perfil,
        "valor_cobrado": valor, "_erro_plantado": erro,
    })
with open(OUT / "viagens.csv", "w", newline="", encoding="utf-8") as f:
    campos = [c for c in viagens[0] if not c.startswith("_")]  # gabarito dos erros não vai pro CSV
    w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
    w.writeheader(); w.writerows(viagens)
print(f"{len(rows)} linhas de tabela, {len(viagens)} viagens")
