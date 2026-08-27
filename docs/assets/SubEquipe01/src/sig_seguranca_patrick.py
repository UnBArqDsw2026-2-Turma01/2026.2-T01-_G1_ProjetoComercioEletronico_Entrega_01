# -*- coding: utf-8 -*-
"""
Gerador do SIG (Softgoal Interdependency Graph) de Seguranca do checkout,
na notacao do NFR Framework (CHUNG et al., 2000).

Autor: Patrick Anderson Carvalho dos Santos - Subequipe 01
Saida: ../SIG_Seguranca_Patrick.svg

O artefato e gerado por codigo de proposito: o SVG resultante e texto
versionado, e qualquer alteracao do grafo aparece como diff no commit.

Uso:  python3 sig_seguranca_patrick.py
"""

import html
import os

W, H = 1620, 950

# Silhueta de nuvem normalizada em uma caixa 100 x 56.
CLOUD = ("M 22.5,56 C 10.1,56 0,46.7 0,35.2 C 0,25.6 7.1,17.5 16.7,15.2 "
         "C 18.6,6.4 27,0 37,0 C 44.6,0 51.4,3.7 55.2,9.4 "
         "C 58.2,7.6 61.8,6.5 65.6,6.5 C 75.6,6.5 83.9,13.6 85.3,22.9 "
         "C 93.7,25.1 100,32.4 100,41.1 C 100,49.3 94.4,56 86.2,56 Z")

# Rotulos de avaliacao propagados no grafo.
LABEL = {
    "sat":  ("✓",  "#1b7f3b"),   # satisfeito
    "wsat": ("W⁺", "#1b7f3b"),   # fracamente satisfeito
    "wden": ("W⁻", "#b3261e"),   # fracamente negado
    "den":  ("✗",  "#b3261e"),   # negado
    "conf": ("↯",  "#b26a00"),   # conflito
}

# kind: soft = softgoal (borda fina) | oper = operacionalizacao (borda grossa)
#       claim = claim softgoal (borda tracejada)
NODES = {
    # --- softgoals de seguranca ----------------------------------------
    "N1":  dict(cx=800,  cy=118, w=240, h=112, kind="soft",
                lines=["Seguranca", "[Checkout]"], label="wsat"),
    "N2":  dict(cx=360,  cy=268, w=232, h=104, kind="soft",
                lines=["Confidencialidade", "[Dados do Comprador]"], label="wsat"),
    "N3":  dict(cx=820,  cy=268, w=200, h=104, kind="soft",
                lines=["Integridade", "[Pedido]"], label="sat"),
    "N4":  dict(cx=170,  cy=430, w=210, h=100, kind="soft",
                lines=["Confidencialidade", "[Endereco]"], label="wsat"),
    "N5":  dict(cx=500,  cy=430, w=224, h=100, kind="soft",
                lines=["Confidencialidade", "[Meio de Pagamento]"], label="sat"),
    "N6":  dict(cx=780,  cy=430, w=216, h=100, kind="soft",
                lines=["Validade", "[Dados do Formulario]"], label="sat"),
    "N7":  dict(cx=1060, cy=430, w=200, h=100, kind="soft",
                lines=["Autenticidade", "[Comprador]"], label="sat"),
    # --- softgoals nao-seguranca, atingidos por correlacao --------------
    "N8":  dict(cx=1420, cy=268, w=216, h=100, kind="soft",
                lines=["Tempo de Resposta", "[Checkout]"], label="wden"),
    "N9":  dict(cx=1420, cy=430, w=216, h=100, kind="soft",
                lines=["Facilidade de Uso", "[Checkout]"], label="conf"),
    "N10": dict(cx=1420, cy=830, w=216, h=100, kind="soft",
                lines=["Acessibilidade", "[Formulario]"], label="sat"),
    # --- operacionalizacoes --------------------------------------------
    "O1":  dict(cx=150,  cy=650, w=232, h=104, kind="oper",
                lines=["Contexto de retorno", "como token opaco"]),
    "O2":  dict(cx=470,  cy=650, w=232, h=104, kind="oper",
                lines=["Tokenizar o meio", "de pagamento"]),
    "O3":  dict(cx=760,  cy=650, w=200, h=104, kind="oper",
                lines=["Validar no", "servidor"]),
    "O4":  dict(cx=1040, cy=650, w=232, h=104, kind="oper",
                lines=["Validar no cliente", "ao perder o foco"]),
    "O5":  dict(cx=1420, cy=650, w=232, h=104, kind="oper",
                lines=["Reautenticar antes", "de confirmar"]),
    "O6":  dict(cx=900,  cy=830, w=248, h=104, kind="oper",
                lines=["Declarar obrigatoriedade", "com atributo required"]),
    # --- claim softgoals ------------------------------------------------
    "C1":  dict(cx=330,  cy=546, w=252, h=90, kind="claim",
                lines=["Claim: dados de entrega trafegam em",
                       "parametro de URL entre subdominios",
                       "- transicoes T03 e T04"]),
    "C2":  dict(cx=1080, cy=546, w=268, h=90, kind="claim",
                lines=["Claim: reautenticar apenas quando o",
                       "meio de pagamento e novo limita a",
                       "friccao a parte das compras"]),
}

# (origem, destino, rotulo de contribuicao, estilo)
LINKS = [
    # (origem, destino, rotulo, estilo, posicao do rotulo ao longo da aresta)
    ("O1", "N4",  "+",  "contrib", 0.50),
    ("O2", "N5",  "++", "contrib", 0.50),
    ("O3", "N6",  "++", "contrib", 0.50),
    ("O3", "N8",  "-",  "correl",  0.72),
    ("O4", "N6",  "+",  "contrib", 0.50),
    ("O4", "N9",  "+",  "correl",  0.62),
    ("O5", "N7",  "++", "contrib", 0.28),
    ("O5", "N9",  "--", "correl",  0.50),
    ("O6", "N6",  "+",  "contrib", 0.25),
    ("O6", "N10", "++", "contrib", 0.50),
]

# Claims justificam LIGACOES, nao nos: (claim, origem_da_ligacao, destino_da_ligacao)
CLAIM_LINKS = [
    ("C1", "O1", "N4"),
    ("C2", "O5", "N9"),
]

# Decomposicoes AND: (pai, [filhos])
DECOMP = [
    ("N1", ["N2", "N3"]),
    ("N2", ["N4", "N5"]),
    ("N3", ["N6", "N7"]),
]

STROKE = {"soft": 1.7, "oper": 4.2, "claim": 1.7}
FILL = {"soft": "#ffffff", "oper": "#ffffff", "claim": "#f7f8fa"}
FONT = "Helvetica,Arial,sans-serif"


def box(n):
    """Caixa (x, y, w, h) que circunscreve a nuvem."""
    return n["cx"] - n["w"] / 2.0, n["cy"] - n["h"] / 2.0, n["w"], n["h"]


def cloud(n):
    x, y, w, h = box(n)
    dash = ' stroke-dasharray="9 6"' if n["kind"] == "claim" else ""
    return (f'<path d="{CLOUD}" transform="translate({x:.1f},{y:.1f}) '
            f'scale({w / 100.0:.4f},{h / 56.0:.4f})" fill="{FILL[n["kind"]]}" '
            f'stroke="#1f2933" stroke-width="{STROKE[n["kind"]]}" '
            f'vector-effect="non-scaling-stroke"{dash}/>')


def node_text(n):
    lines = n["lines"]
    size = 13 if n["kind"] != "claim" else 10.5
    lh = size + 3.5
    has_label = "label" in n
    total = len(lines) * lh + (15 if has_label else 0)
    y0 = n["cy"] - total / 2.0 + size
    out = []
    for i, ln in enumerate(lines):
        weight = "600" if i == 0 and n["kind"] != "claim" else "400"
        out.append(f'<text x="{n["cx"]}" y="{y0 + i * lh:.1f}" text-anchor="middle" '
                   f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
                   f'fill="#1f2933">{html.escape(ln)}</text>')
    if has_label:
        sym, col = LABEL[n["label"]]
        out.append(f'<text x="{n["cx"]}" y="{y0 + len(lines) * lh + 9:.1f}" '
                   f'text-anchor="middle" font-family="{FONT}" font-size="15" '
                   f'font-weight="700" fill="{col}">{sym}</text>')
    return "".join(out)


def anchor(n, toward_y):
    """Ponto de saida/entrada na nuvem: base se o alvo esta abaixo, topo se acima."""
    _, y, _, h = box(n)
    return (n["cx"], y + h * 0.92) if toward_y > n["cy"] else (n["cx"], y + h * 0.08)


def endpoints(a_id, b_id):
    a, b = NODES[a_id], NODES[b_id]
    return anchor(a, b["cy"]), anchor(b, a["cy"])


def link_line(a_id, b_id, style):
    (x1, y1), (x2, y2) = endpoints(a_id, b_id)
    if style == "correl":
        stroke, mk = '#b3261e', 'arrowRed'
    else:
        stroke, mk = '#1f2933', 'arrow'
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="1.8" marker-end="url(#{mk})"/>')


def link_label(a_id, b_id, lab, style, t=0.5):
    (x1, y1), (x2, y2) = endpoints(a_id, b_id)
    mx, my = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
    col = "#b3261e" if style == "correl" else "#1b7f3b"
    w = 38 if len(lab) > 1 else 32
    return (f'<rect x="{mx - w / 2:.1f}" y="{my - 12:.1f}" width="{w}" height="21" rx="5" '
            f'fill="#ffffff" stroke="{col}" stroke-width="1.3"/>'
            f'<text x="{mx:.1f}" y="{my + 3:.1f}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="13" font-weight="700" fill="{col}">'
            f'{html.escape(lab)}</text>')


def claim_line(c_id, a_id, b_id):
    """Liga o claim ao PONTO MEDIO da ligacao que ele justifica."""
    (x1, y1), (x2, y2) = endpoints(a_id, b_id)
    mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    c = NODES[c_id]
    cx0, cy0, cw, _ = box(c)
    sx = cx0 + cw if mx > c["cx"] else cx0
    return (f'<line x1="{sx:.1f}" y1="{c["cy"]:.1f}" x2="{mx:.1f}" y2="{my:.1f}" '
            f'stroke="#6b7280" stroke-width="1.5" stroke-dasharray="7 5"/>')


def decomposition(parent_id, child_ids):
    """Liga o pai aos filhos e marca a decomposicao AND com um arco sobre as ligacoes."""
    p = NODES[parent_id]
    px, py = anchor(p, p["cy"] + 10000)
    out = []
    for c_id in child_ids:
        cx, cy = anchor(NODES[c_id], p["cy"])
        out.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{px:.1f}" y2="{py:.1f}" '
                   f'stroke="#1f2933" stroke-width="1.8" marker-end="url(#arrow)"/>')
    r = 46
    out.append(f'<path d="M {px - r},{py + 36:.1f} A {r},{r} 0 0 1 {px + r},{py + 36:.1f}" '
               f'fill="none" stroke="#1f2933" stroke-width="1.6"/>')
    out.append(f'<text x="{px:.1f}" y="{py + 30:.1f}" text-anchor="middle" '
               f'font-family="{FONT}" font-size="11" font-weight="700" '
               f'fill="#1f2933">AND</text>')
    return "".join(out)


def legend():
    x, y, lw, lh = 30, 14, 300, 176
    rows = [
        ("cloud-thin",  "Softgoal NFR - Tipo [Topico]"),
        ("cloud-thick", "Operacionalizacao"),
        ("cloud-dash",  "Claim softgoal - justificativa"),
        ("arrow-black", "Contribuicao / decomposicao AND"),
        ("arrow-red",   "Correlacao negativa"),
    ]
    out = [f'<rect x="{x}" y="{y}" width="{lw}" height="{lh}" rx="8" fill="#ffffff" '
           f'stroke="#c3cad3" stroke-width="1.3"/>',
           f'<text x="{x + 14}" y="{y + 22}" font-family="{FONT}" font-size="13" '
           f'font-weight="700" fill="#1f2933">Legenda</text>']
    for i, (kind, txt) in enumerate(rows):
        ry = y + 44 + i * 25
        if kind.startswith("cloud"):
            sw = 4.2 if kind == "cloud-thick" else 1.7
            dash = ' stroke-dasharray="6 4"' if kind == "cloud-dash" else ""
            out.append(f'<path d="{CLOUD}" transform="translate({x + 14},{ry - 11}) '
                       f'scale(0.42,0.28)" fill="#ffffff" stroke="#1f2933" '
                       f'stroke-width="{sw}" vector-effect="non-scaling-stroke"{dash}/>')
        else:
            col = "#b3261e" if kind == "arrow-red" else "#1f2933"
            mk = "arrowRed" if kind == "arrow-red" else "arrow"
            out.append(f'<line x1="{x + 16}" y1="{ry}" x2="{x + 52}" y2="{ry}" '
                       f'stroke="{col}" stroke-width="1.8" marker-end="url(#{mk})"/>')
        out.append(f'<text x="{x + 66}" y="{ry + 4}" font-family="{FONT}" font-size="11.5" '
                   f'fill="#1f2933">{html.escape(txt)}</text>')
    dx = 0
    for key, name in [("sat", "satisfeito"), ("wsat", "fraco +"), ("wden", "fraco -"),
                      ("den", "negado"), ("conf", "conflito")]:
        sym, col = LABEL[key]
        out.append(f'<text x="{x + 14 + dx}" y="{y + lh - 12}" font-family="{FONT}" '
                   f'font-size="13" font-weight="700" fill="{col}">{sym}</text>')
        out.append(f'<text x="{x + 28 + dx}" y="{y + lh - 12}" font-family="{FONT}" '
                   f'font-size="9.5" fill="#5b6570">{html.escape(name)}</text>')
        dx += 56
    return "".join(out)


def build():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
        f'height="{H}" role="img" aria-label="SIG de Seguranca do checkout na notacao '
        f'do NFR Framework">',
        '<defs>',
        '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#1f2933"/></marker>',
        '<marker id="arrowRed" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#b3261e"/></marker>',
        '</defs>',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        f'<text x="{W // 2}" y="30" text-anchor="middle" font-family="{FONT}" '
        'font-size="17" font-weight="700" fill="#1f2933">'
        'SIG de Seguranca do Checkout - G1_ProjetoComercioEletronico</text>',
    ]
    # 1) ligacoes, 2) nuvens, 3) rotulos das ligacoes por cima das nuvens
    for parent, children in DECOMP:
        parts.append(decomposition(parent, children))
    for a, b, _, style, _t in LINKS:
        parts.append(link_line(a, b, style))
    for c, a, b in CLAIM_LINKS:
        parts.append(claim_line(c, a, b))
    for n in NODES.values():
        parts.append(cloud(n))
        parts.append(node_text(n))
    for a, b, lab, style, t in LINKS:
        parts.append(link_label(a, b, lab, style, t))
    parts.append(legend())
    parts.append('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    out = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "SIG_Seguranca_Patrick.svg"))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(build())
    print("gerado:", out)
