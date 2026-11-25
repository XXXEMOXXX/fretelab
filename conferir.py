"""Confere as viagens contra a tabela de fretes e gera o relatório de divergências.

Regras (todas fictícias, só para o demo):
  1. Viagem sem ID não entra no pagamento -> pendência "sem_id".
  2. Rota/perfil sem preço na tabela -> pendência "sem_tabela".
  3. Valor cobrado acima da tabela -> "acima" (cobrar correção).
  4. Valor cobrado abaixo da tabela -> aceito (não se aponta a favor da empresa).
  Tolerância: R$ 0,01.
"""
import csv
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
TOL = 0.01


def carregar_tabela():
    with open(BASE / "dados" / "tabela_fretes.csv", encoding="utf-8") as f:
        return {(r["origem"], r["destino"], r["perfil"]): float(r["valor_tabela"]) for r in csv.DictReader(f)}


def conferir():
    tabela = carregar_tabela()
    achados = []
    with open(BASE / "dados" / "viagens.csv", encoding="utf-8") as f:
        for v in csv.DictReader(f):
            cobrado = float(v["valor_cobrado"])
            ref = tabela.get((v["origem"], v["destino"], v["perfil"]))
            if not v["id_viagem"]:
                tipo, ref_txt = "sem_id", ""
            elif ref is None:
                tipo, ref_txt = "sem_tabela", ""
            elif cobrado - ref > TOL:
                tipo, ref_txt = "acima", ref
            else:
                continue
            achados.append({**v, "tipo": tipo, "valor_tabela": ref_txt,
                            "diferenca": round(cobrado - ref, 2) if ref_txt != "" else ""})
    return achados


def main():
    achados = conferir()
    campos = ["id_viagem", "data", "cliente", "origem", "destino", "perfil",
              "valor_cobrado", "valor_tabela", "diferenca", "tipo"]
    with open(BASE / "relatorio_divergencias.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader(); w.writerows(achados)

    por_tipo = defaultdict(list)
    for a in achados:
        por_tipo[a["tipo"]].append(a)
    titulos = {"acima": "Cobrado acima da tabela", "sem_tabela": "Rota/perfil sem preço na tabela",
               "sem_id": "Viagem sem ID (não paga)"}
    linhas = ["# Relatório de divergências (dados fictícios)\n",
              f"Total de pendências: **{len(achados)}**\n"]
    for tipo, titulo in titulos.items():
        itens = por_tipo.get(tipo, [])
        linhas.append(f"\n## {titulo} ({len(itens)})\n")
        if itens:
            linhas.append("| ID | Data | Cliente | Rota | Perfil | Cobrado | Tabela | Dif. |\n|---|---|---|---|---|---|---|---|")
            for a in itens:
                linhas.append(f"| {a['id_viagem'] or '—'} | {a['data']} | {a['cliente']} | {a['origem']}→{a['destino']} | "
                              f"{a['perfil']} | {float(a['valor_cobrado']):.2f} | {a['valor_tabela'] or '—'} | {a['diferenca'] or '—'} |")
    (BASE / "relatorio_divergencias.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print({t: len(i) for t, i in por_tipo.items()}, "total", len(achados))


if __name__ == "__main__":
    main()
