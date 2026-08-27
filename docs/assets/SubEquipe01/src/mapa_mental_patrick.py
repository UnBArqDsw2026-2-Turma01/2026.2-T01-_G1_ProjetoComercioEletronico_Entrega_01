# -*- coding: utf-8 -*-
"""
Gerador do Mapa Mental do G1_ProjetoComercioEletronico.

Autor: Patrick Anderson Carvalho dos Santos - Subequipe 01
Saida: ../MapaMental_Patrick.svg

Uso:  python3 mapa_mental_patrick.py
"""

import html
import os

FONT = "Helvetica,Arial,sans-serif"
VGAP = 13.0         # respiro vertical entre nos irmaos
BRANCH_GAP = 26.0   # respiro extra entre ramos de primeiro nivel
GAP = 42.0          # espacamento horizontal entre colunas
COLW = {1: 196, 2: 182, 3: 214}
PAD_X, PAD_Y = 40, 96
WRAP = {1: 20, 2: 22, 3: 26}
FS = {1: 12.5, 2: 11.5, 3: 11}

# paleta: (borda, preenchimento nivel 1, preenchimento nivel 2+)
PALETTE = {
    "atores":    ("#2f6fb0", "#dceafa", "#eef5fd"),
    "jornada":   ("#1f8a5f", "#d8f2e6", "#edfaf3"),
    "conta":     ("#7a52c7", "#e6ddf8", "#f3eefc"),
    "confianca": ("#c2560f", "#fbe3d2", "#fdf1e9"),
    "rnf":       ("#b0851c", "#faeecd", "#fdf7e8"),
    "riscos":    ("#b8324a", "#fbdde3", "#fdeef1"),
}


def N(name, *children):
    return {"name": name, "children": list(children)}


LEFT = [
    dict(key="atores", node=N("Atores e Papéis",
        N("Comprador"), N("Vendedor autônomo"), N("Loja oficial"),
        N("Plataforma intermediária"), N("Operadora de pagamento"),
        N("Transportadora"), N("Atendimento e mediação"))),
    dict(key="jornada", node=N("Jornada de Compra",
        N("Descoberta", N("Busca por termo"), N("Filtros facetados"), N("Ordenação")),
        N("Decisão", N("Ficha do produto"), N("Frete e prazo por CEP"),
          N("Reputação do vendedor"), N("Avaliações e perguntas")),
        N("Transação", N("Carrinho por vendedor"), N("Endereço de entrega"),
          N("Meio de pagamento"), N("Confirmação do pedido")),
        N("Pós-venda", N("Acompanhamento"), N("Avaliação da compra"),
          N("Devolução e reembolso"), N("Mediação de disputa")))),
    dict(key="conta", node=N("Conta e Acesso",
        N("Cadastro"), N("Autenticação"), N("Endereços salvos"),
        N("Meios de pagamento salvos"))),
]

RIGHT = [
    dict(key="confianca", node=N("Pontos de Confiança",
        N("Antes de pagar", N("Selo de loja oficial"), N("Reputação do vendedor"),
          N("Nota e volume de avaliações")),
        N("No ato de pagar", N("Intermediação do pagamento"),
          N("Mascaramento do cartão"), N("Confirmação do valor")),
        N("Depois de pagar", N("Código de rastreio"), N("Prazo prometido"),
          N("Canal de reclamação"), N("Reembolso")))),
    dict(key="rnf", node=N("Qualidades (RNF)",
        N("Segurança", N("Integridade"), N("Confidencialidade"), N("Disponibilidade")),
        N("Usabilidade"), N("Desempenho"), N("Confiabilidade"))),
    dict(key="riscos", node=N("Riscos do Domínio",
        N("Anúncio fraudulento"), N("Estorno indevido"),
        N("Abandono de carrinho"), N("Vazamento de dados pessoais"))),
]

CENTER = "G1_ProjetoComercioEletronico"


def wrap(text, limit):
    words, lines, cur = text.split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if len(cand) <= limit or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def measure(node, level):
    node["lines"] = wrap(node["name"], WRAP[level])
    node["fs"] = FS[level]
    node["level"] = level
    node["w"] = max(90.0, min(COLW[level],
                              max(len(l) for l in node["lines"]) * node["fs"] * 0.62 + 26))
    node["h"] = len(node["lines"]) * (node["fs"] + 3.5) + 16
    for c in node["children"]:
        measure(c, level + 1)


class Slots:
    """Cursor vertical que reserva espaco proporcional a altura de cada folha."""

    def __init__(self):
        self.y = 0.0

    def take(self, h):
        cy = self.y + h / 2.0
        self.y += h + VGAP
        return cy


def assign_y(node, slots):
    if not node["children"]:
        node["cy"] = slots.take(node["h"])
    else:
        for c in node["children"]:
            assign_y(c, slots)
        node["cy"] = (node["children"][0]["cy"] + node["children"][-1]["cy"]) / 2.0
    return node["cy"]


def assign_x(node, side, cols):
    lvl = node["level"]
    if side == "right":
        node["x"] = cols[lvl]
    else:
        node["x"] = cols[lvl] - node["w"]
    for c in node["children"]:
        assign_x(c, side, cols)


def walk(node, out):
    out.append(node)
    for c in node["children"]:
        walk(c, out)


def esc(t):
    return html.escape(t)


def pill(n, colors):
    border, fill1, fill2 = colors
    fill = fill1 if n["level"] == 1 else fill2
    sw = 2.0 if n["level"] == 1 else 1.3
    y = n["cy"] - n["h"] / 2.0
    r = n["h"] / 2.0
    out = [f'<rect x="{n["x"]:.1f}" y="{y:.1f}" width="{n["w"]:.1f}" height="{n["h"]:.1f}" '
           f'rx="{r:.1f}" fill="{fill}" stroke="{border}" stroke-width="{sw}" '
           f'filter="url(#soft)"/>']
    weight = "700" if n["level"] == 1 else ("600" if n["level"] == 2 else "400")
    y0 = n["cy"] - (len(n["lines"]) - 1) * (n["fs"] + 3.5) / 2.0 + n["fs"] * 0.36
    for i, ln in enumerate(n["lines"]):
        out.append(f'<text x="{n["x"] + n["w"] / 2.0:.1f}" y="{y0 + i * (n["fs"] + 3.5):.1f}" '
                   f'text-anchor="middle" font-family="{FONT}" font-size="{n["fs"]}" '
                   f'font-weight="{weight}" fill="#1c2530">{esc(ln)}</text>')
    return "".join(out)


def curve(p, c, side, color, width):
    if side == "right":
        x1, x2 = p["x"] + p["w"], c["x"]
    else:
        x1, x2 = p["x"], c["x"] + c["w"]
    y1, y2 = p["cy"], c["cy"]
    mx = (x1 + x2) / 2.0
    return (f'<path d="M {x1:.1f},{y1:.1f} C {mx:.1f},{y1:.1f} {mx:.1f},{y2:.1f} '
            f'{x2:.1f},{y2:.1f}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" opacity="0.85"/>')


def build():
    # 1) medidas e posicoes verticais, lado a lado
    for side in (LEFT, RIGHT):
        for br in side:
            measure(br["node"], 1)
    slots_l, slots_r = Slots(), Slots()
    for br in LEFT:
        assign_y(br["node"], slots_l)
        slots_l.y += BRANCH_GAP
    for br in RIGHT:
        assign_y(br["node"], slots_r)
        slots_r.y += BRANCH_GAP

    hl, hr = slots_l.y, slots_r.y
    height = max(hl, hr) + PAD_Y + 60
    # centraliza verticalmente o lado mais curto
    off_l = (max(hl, hr) - hl) / 2.0 + PAD_Y
    off_r = (max(hl, hr) - hr) / 2.0 + PAD_Y
    def shift(node, dy):
        node["cy"] += dy
        for c in node["children"]:
            shift(c, dy)
    for br in LEFT:
        shift(br["node"], off_l)
    for br in RIGHT:
        shift(br["node"], off_r)

    # 2) colunas horizontais
    left_cols = {1: 0.0, 2: 0.0, 3: 0.0}
    right_cols = {1: 0.0, 2: 0.0, 3: 0.0}
    center_half = 116.0
    right_cols[1] = center_half + 96
    right_cols[2] = right_cols[1] + COLW[1] + GAP
    right_cols[3] = right_cols[2] + COLW[2] + GAP
    left_cols[1] = -(center_half + 96)
    left_cols[2] = left_cols[1] - COLW[1] - GAP
    left_cols[3] = left_cols[2] - COLW[2] - GAP

    for br in LEFT:
        assign_x(br["node"], "left", left_cols)
    for br in RIGHT:
        assign_x(br["node"], "right", right_cols)

    nodes = []
    for br in LEFT + RIGHT:
        walk(br["node"], nodes)
    min_x = min(n["x"] for n in nodes)
    max_x = max(n["x"] + n["w"] for n in nodes)
    shift_x = PAD_X - min_x
    for n in nodes:
        n["x"] += shift_x
    width = max_x - min_x + 2 * PAD_X
    cx = shift_x  # posicao 0 original == centro

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" '
             f'width="{width:.0f}" height="{height:.0f}" role="img" '
             f'aria-label="Mapa mental do G1_ProjetoComercioEletronico">',
             '<defs>'
             '<filter id="soft" x="-20%" y="-40%" width="140%" height="180%">'
             '<feDropShadow dx="0" dy="1.2" stdDeviation="1.6" flood-color="#0d1b2a" '
             'flood-opacity="0.13"/></filter>'
             '<radialGradient id="core" cx="38%" cy="32%">'
             '<stop offset="0%" stop-color="#4f7fd0"/>'
             '<stop offset="100%" stop-color="#1e3f78"/></radialGradient>'
             '</defs>',
             f'<rect width="{width:.0f}" height="{height:.0f}" fill="#ffffff"/>',
             f'<text x="{width / 2:.0f}" y="44" text-anchor="middle" font-family="{FONT}" '
             f'font-size="19" font-weight="700" fill="#1c2530">'
             f'Mapa Mental - G1_ProjetoComercioEletronico</text>',
             f'<text x="{width / 2:.0f}" y="68" text-anchor="middle" font-family="{FONT}" '
             f'font-size="12.5" fill="#5b6570">'
             f'O sistema visto pelos pontos em que o comprador precisa confiar</text>']

    cy = height / 2.0
    # 3) conexoes
    for side_name, side in (("left", LEFT), ("right", RIGHT)):
        for br in side:
            border = PALETTE[br["key"]][0]
            root = br["node"]
            x_root = root["x"] if side_name == "right" else root["x"] + root["w"]
            k = 1 if side_name == "right" else -1
            parts.append(f'<path d="M {cx + k * center_half:.1f},{cy:.1f} '
                         f'C {cx + k * (center_half + 60):.1f},{cy:.1f} '
                         f'{x_root - k * 60:.1f},{root["cy"]:.1f} {x_root:.1f},{root["cy"]:.1f}" '
                         f'fill="none" stroke="{border}" stroke-width="3.2" '
                         f'stroke-linecap="round" opacity="0.9"/>')
            stack = [root]
            while stack:
                p = stack.pop()
                for c in p["children"]:
                    parts.append(curve(p, c, side_name, border,
                                       2.4 if c["level"] == 2 else 1.5))
                    stack.append(c)

    # 4) nucleo
    parts.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{center_half:.0f}" ry="52" '
                 f'fill="url(#core)" stroke="#122a52" stroke-width="2"/>')
    for i, ln in enumerate(["G1_Projeto", "ComercioEletronico"]):
        parts.append(f'<text x="{cx:.1f}" y="{cy - 6 + i * 19:.1f}" text-anchor="middle" '
                     f'font-family="{FONT}" font-size="14" font-weight="700" '
                     f'fill="#ffffff">{esc(ln)}</text>')

    # 5) nos
    for side in (LEFT, RIGHT):
        for br in side:
            colors = PALETTE[br["key"]]
            ns = []
            walk(br["node"], ns)
            for n in ns:
                parts.append(pill(n, colors))

    parts.append('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    out = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "MapaMental_Patrick.svg"))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(build())
    print("gerado:", out)
