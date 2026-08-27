# -*- coding: utf-8 -*-
"""
Gerador do SIG (Softgoal Interdependency Graph) de Segurança do checkout,
na notação do NFR Framework (CHUNG et al., 2000).

Autor: Patrick Anderson Carvalho dos Santos - Subequipe 01
Saída: ../SIG_Seguranca_Patrick.svg

Uso:  python3 sig_seguranca_patrick.py
"""

import html
import os

W, H = 2120, 1240
FONT = "Helvetica,Arial,sans-serif"

CLOUD = ("M 22.5,56 C 10.1,56 0,46.7 0,35.2 C 0,25.6 7.1,17.5 16.7,15.2 "
         "C 18.6,6.4 27,0 37,0 C 44.6,0 51.4,3.7 55.2,9.4 "
         "C 58.2,7.6 61.8,6.5 65.6,6.5 C 75.6,6.5 83.9,13.6 85.3,22.9 "
         "C 93.7,25.1 100,32.4 100,41.1 C 100,49.3 94.4,56 86.2,56 Z")

# estilo por categoria: (borda, preenchimento, espessura, tracejado)
STYLE = {
    "root":   ("#1e3f78", "#d9e7fa", 2.6, ""),
    "sec":    ("#2c5aa0", "#eef4fd", 1.9, ""),
    "impact": ("#b26a00", "#fdf3e3", 1.9, ""),
    "oper":   ("#1b7f3b", "#e9f8ef", 4.2, ""),
    "claim":  ("#6b7280", "#f5f6f8", 1.7, ' stroke-dasharray="9 6"'),
}

LABEL = {
    "sat":  ("✓",  "#1b7f3b", "satisfeito"),
    "wsat": ("W⁺", "#1b7f3b", "fracamente satisfeito"),
    "wden": ("W⁻", "#b3261e", "fracamente negado"),
    "conf": ("↯",  "#b26a00", "conflito"),
}

NODES = {
    "N1": dict(cx=720,  cy=150, w=250, h=118, kind="root", label="wsat",
               title="Segurança", topic="[Checkout]"),
    "N2": dict(cx=400,  cy=340, w=246, h=110, kind="sec", label="wsat",
               title="Confidencialidade", topic="[Dados do Comprador]"),
    "N3": dict(cx=1040, cy=340, w=214, h=110, kind="sec", label="sat",
               title="Integridade", topic="[Pedido]"),
    "N4": dict(cx=180,  cy=530, w=224, h=104, kind="sec", label="wsat",
               title="Confidencialidade", topic="[Endereço]"),
    "N5": dict(cx=520,  cy=530, w=238, h=104, kind="sec", label="sat",
               title="Confidencialidade", topic="[Meio de Pagamento]"),
    "N6": dict(cx=880,  cy=530, w=230, h=104, kind="sec", label="sat",
               title="Validade", topic="[Dados do Formulário]"),
    "N7": dict(cx=1220, cy=530, w=214, h=104, kind="sec", label="sat",
               title="Autenticidade", topic="[Comprador]"),
    "M1": dict(cx=1880, cy=300, w=230, h=106, kind="impact", label="wden",
               title="Tempo de Resposta", topic="[Checkout]"),
    "M2": dict(cx=1880, cy=460, w=230, h=106, kind="impact", label="conf",
               title="Facilidade de Uso", topic="[Checkout]"),
    "M3": dict(cx=1880, cy=620, w=230, h=106, kind="impact", label="sat",
               title="Acessibilidade", topic="[Formulário]"),
    "O1": dict(cx=150,  cy=790, w=232, h=108, kind="oper",
               text="Contexto de retorno como token opaco"),
    "O2": dict(cx=420,  cy=790, w=232, h=108, kind="oper",
               text="Tokenizar o meio de pagamento"),
    "O3": dict(cx=690,  cy=790, w=212, h=108, kind="oper",
               text="Validar no servidor"),
    "O4": dict(cx=940,  cy=790, w=228, h=108, kind="oper",
               text="Validar no cliente ao perder o foco"),
    "O6": dict(cx=1190, cy=790, w=232, h=108, kind="oper",
               text="Declarar obrigatoriedade com required"),
    "O5": dict(cx=1430, cy=790, w=228, h=108, kind="oper",
               text="Reautenticar antes de confirmar"),
    "C1": dict(cx=300,  cy=655, w=250, h=104, kind="claim",
               text="Claim: dados de entrega trafegam em parâmetro de URL entre subdomínios — T03 e T04"),
    "C2": dict(cx=1180, cy=1010, w=272, h=104, kind="claim",
               text="Claim: reautenticar apenas quando o meio de pagamento é novo limita a fricção a parte das compras"),
}

DECOMP = [("N1", ["N2", "N3"]), ("N2", ["N4", "N5"]), ("N3", ["N6", "N7"])]

# contribuições internas: (origem, destino, rótulo, posição do rótulo)
CONTRIB = [
    ("O1", "N4", "+",  0.50),
    ("O2", "N5", "++", 0.50),
    ("O3", "N6", "++", 0.50),
    ("O4", "N6", "+",  0.50),
    ("O6", "N6", "+",  0.32),
    ("O5", "N7", "++", 0.50),
]

# correlações roteadas em ortogonal: (origem, destino, rótulo, faixa, canal, desvio y no destino)
CORREL = [
    ("O3", "M1", "-",  880, 1580,   0),
    ("O4", "M2", "+",  902, 1602, -16),
    ("O5", "M2", "--", 924, 1624,  16),
    ("O6", "M3", "++", 946, 1646,   0),
]

# claims: (claim, ponto de ancoragem no grafo)
CLAIMS = [("C1", (167, 660)), ("C2", (1500, 924))]

PANEL = dict(x=1700, y=196, w=360, h=536,
             title="Softgoals impactados por correlação")


def esc(t):
    return html.escape(t)


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


def box(n):
    return n["cx"] - n["w"] / 2.0, n["cy"] - n["h"] / 2.0, n["w"], n["h"]


def cloud(n):
    x, y, w, h = box(n)
    stroke, fill, sw, dash = STYLE[n["kind"]]
    return (f'<path d="{CLOUD}" transform="translate({x:.1f},{y:.1f}) '
            f'scale({w / 100.0:.4f},{h / 56.0:.4f})" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" vector-effect="non-scaling-stroke"{dash} '
            f'filter="url(#soft)"/>')


def node_text(n):
    stroke = STYLE[n["kind"]][0]
    out = []
    if "title" in n:
        lines = [(n["title"], 13.5, "700"), (n["topic"], 12, "400")]
        sym, col, _ = LABEL[n["label"]]
        total = 2 * 17 + 16
        y0 = n["cy"] - total / 2.0 + 13
        for i, (t, fs, fw) in enumerate(lines):
            out.append(f'<text x="{n["cx"]:.1f}" y="{y0 + i * 17:.1f}" text-anchor="middle" '
                       f'font-family="{FONT}" font-size="{fs}" font-weight="{fw}" '
                       f'fill="#1c2530">{esc(t)}</text>')
        out.append(f'<text x="{n["cx"]:.1f}" y="{y0 + 2 * 17 + 5:.1f}" text-anchor="middle" '
                   f'font-family="{FONT}" font-size="15" font-weight="700" '
                   f'fill="{col}">{sym}</text>')
    else:
        claim = n["kind"] == "claim"
        fs = 10.5 if claim else 12.5
        lines = wrap(n["text"], 32 if claim else 20)
        lh = fs + 3.5
        y0 = n["cy"] - (len(lines) - 1) * lh / 2.0 + fs * 0.35
        for i, ln in enumerate(lines):
            out.append(f'<text x="{n["cx"]:.1f}" y="{y0 + i * lh:.1f}" text-anchor="middle" '
                       f'font-family="{FONT}" font-size="{fs}" '
                       f'font-weight="{"400" if claim else "600"}" '
                       f'fill="{"#4a5560" if claim else "#1c2530"}">{esc(ln)}</text>')
    return "".join(out)


def anchor(n, toward_y):
    _, y, _, h = box(n)
    return (n["cx"], y + h * 0.9) if toward_y > n["cy"] else (n["cx"], y + h * 0.1)


def pill(mx, my, lab, positive):
    col = "#1b7f3b" if positive else "#b3261e"
    w = 40 if len(lab) > 1 else 32
    return (f'<rect x="{mx - w / 2:.1f}" y="{my - 12:.1f}" width="{w}" height="22" rx="6" '
            f'fill="#ffffff" stroke="{col}" stroke-width="1.4"/>'
            f'<text x="{mx:.1f}" y="{my + 4:.1f}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="13.5" font-weight="700" fill="{col}">{esc(lab)}</text>')


def build():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
         f'height="{H}" role="img" aria-label="SIG de Segurança do checkout na notação do '
         f'NFR Framework">',
         '<defs>'
         '<marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
         'markerHeight="7" orient="auto-start-reverse">'
         '<path d="M 0 0 L 10 5 L 0 10 z" fill="#2c5aa0"/></marker>'
         '<marker id="arwR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
         'markerHeight="7" orient="auto-start-reverse">'
         '<path d="M 0 0 L 10 5 L 0 10 z" fill="#b3261e"/></marker>'
         '<marker id="arwG" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
         'markerHeight="7" orient="auto-start-reverse">'
         '<path d="M 0 0 L 10 5 L 0 10 z" fill="#1b7f3b"/></marker>'
         '<filter id="soft" x="-15%" y="-30%" width="130%" height="160%">'
         '<feDropShadow dx="0" dy="1.4" stdDeviation="2" flood-color="#0d1b2a" '
         'flood-opacity="0.12"/></filter>'
         '</defs>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="{W // 2}" y="40" text-anchor="middle" font-family="{FONT}" '
         'font-size="19" font-weight="700" fill="#1c2530">'
         'SIG de Segurança do Checkout — G1_ProjetoComercioEletronico</text>',
         f'<text x="{W // 2}" y="64" text-anchor="middle" font-family="{FONT}" '
         'font-size="12.5" fill="#5b6570">'
         'Notação do NFR Framework — Chung, Nixon, Yu e Mylopoulos (2000)</text>']

    # painel dos softgoals impactados
    p.append(f'<rect x="{PANEL["x"]}" y="{PANEL["y"]}" width="{PANEL["w"]}" '
             f'height="{PANEL["h"]}" rx="14" fill="#fffaf2" stroke="#e3c9a0" '
             f'stroke-width="1.5" stroke-dasharray="8 5"/>')
    p.append(f'<text x="{PANEL["x"] + PANEL["w"] / 2:.0f}" y="{PANEL["y"] + 26}" '
             f'text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" '
             f'fill="#8a5a12">{esc(PANEL["title"])}</text>')

    # decomposições AND
    for parent, children in DECOMP:
        par = NODES[parent]
        px, py = anchor(par, par["cy"] + 10000)
        for cid in children:
            cx, cy = anchor(NODES[cid], par["cy"])
            p.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{px:.1f}" y2="{py:.1f}" '
                     f'stroke="#2c5aa0" stroke-width="2" marker-end="url(#arw)"/>')
        p.append(f'<path d="M {px - 50},{py + 40:.1f} A 50,50 0 0 1 {px + 50},{py + 40:.1f}" '
                 f'fill="none" stroke="#2c5aa0" stroke-width="1.8"/>')
        p.append(f'<text x="{px:.1f}" y="{py + 32:.1f}" text-anchor="middle" '
                 f'font-family="{FONT}" font-size="11" font-weight="700" '
                 f'fill="#2c5aa0">AND</text>')

    # contribuições
    for a, b, lab, t in CONTRIB:
        (x1, y1), (x2, y2) = anchor(NODES[a], NODES[b]["cy"]), anchor(NODES[b], NODES[a]["cy"])
        p.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="#1b7f3b" stroke-width="2" marker-end="url(#arwG)"/>')

    # correlações, roteadas em ortogonal por faixa e canal
    for a, b, lab, lane, chan, dy in CORREL:
        src = NODES[a]
        dst = NODES[b]
        sx = src["cx"]
        sy = src["cy"] + src["h"] * 0.4
        ty = dst["cy"] + dy
        tx = dst["cx"] - dst["w"] / 2.0
        pos = lab.startswith("+")
        col = "#1b7f3b" if pos else "#b3261e"
        mk = "arwG" if pos else "arwR"
        d = (f'M {sx:.1f},{sy:.1f} L {sx:.1f},{lane} L {chan},{lane} '
             f'L {chan},{ty:.1f} L {tx:.1f},{ty:.1f}')
        p.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2" '
                 f'stroke-linejoin="round" marker-end="url(#{mk})"/>')

    # claims
    for cid, (ax, ay) in CLAIMS:
        c = NODES[cid]
        cx0, cy0, cw, ch = box(c)
        sx = cx0 + cw if ax > c["cx"] else cx0
        sy = c["cy"] - 12 if ax > c["cx"] else c["cy"]
        p.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ax}" y2="{ay}" stroke="#8b93a0" '
                 f'stroke-width="1.6" stroke-dasharray="7 5"/>')

    # nuvens e textos
    for n in NODES.values():
        p.append(cloud(n))
        p.append(node_text(n))

    # rótulos das contribuições, por cima das nuvens
    for a, b, lab, t in CONTRIB:
        (x1, y1), (x2, y2) = anchor(NODES[a], NODES[b]["cy"]), anchor(NODES[b], NODES[a]["cy"])
        p.append(pill(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, lab, lab.startswith("+")))
    for a, b, lab, lane, chan, dy in CORREL:
        p.append(pill(chan, (lane + NODES[b]["cy"] + dy) / 2.0, lab, lab.startswith("+")))

    p.append(legend())
    p.append('</svg>')
    return "\n".join(p)


def legend():
    x, y, w, h = 40, 1096, 1180, 112
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#fbfcfd" '
           f'stroke="#ccd4dd" stroke-width="1.3"/>',
           f'<text x="{x + 20}" y="{y + 26}" font-family="{FONT}" font-size="13" '
           f'font-weight="700" fill="#1c2530">Legenda</text>']
    shapes = [("sec", "Softgoal NFR — Tipo [Tópico]"), ("oper", "Operacionalização"),
              ("claim", "Claim — justificativa da ligação")]
    cur = x + 20
    for kind, label in shapes:
        stroke, fill, sw, dash = STYLE[kind]
        out.append(f'<path d="{CLOUD}" transform="translate({cur},{y + 42}) scale(0.46,0.34)" '
                   f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
                   f'vector-effect="non-scaling-stroke"{dash}/>')
        out.append(f'<text x="{cur + 60}" y="{y + 55}" font-family="{FONT}" font-size="11.5" '
                   f'fill="#3f4c5a">{esc(label)}</text>')
        cur += 60 + 7.0 * len(label) + 40
    rows = [("#2c5aa0", "arw", "Decomposição AND"),
            ("#1b7f3b", "arwG", "Contribuição positiva — ++ MAKE, + HELP"),
            ("#b3261e", "arwR", "Correlação negativa — − HURT, −− BREAK")]
    cur = x + 20
    for col, mk, label in rows:
        out.append(f'<line x1="{cur}" y1="{y + 88}" x2="{cur + 38}" y2="{y + 88}" '
                   f'stroke="{col}" stroke-width="2" marker-end="url(#{mk})"/>')
        out.append(f'<text x="{cur + 48}" y="{y + 92}" font-family="{FONT}" font-size="11.5" '
                   f'fill="#3f4c5a">{esc(label)}</text>')
        cur += 48 + 6.6 * len(label) + 40
    cur = x + w - 20
    items = list(LABEL.items())[::-1]
    for key, (sym, col, name) in items:
        txt = f'{sym}  {name}'
        cur -= 6.4 * len(name) + 40
        out.append(f'<text x="{cur}" y="{y + 26}" font-family="{FONT}" font-size="12" '
                   f'font-weight="700" fill="{col}">{sym}</text>')
        out.append(f'<text x="{cur + 18}" y="{y + 26}" font-family="{FONT}" font-size="10.5" '
                   f'fill="#5b6570">{esc(name)}</text>')
    return "".join(out)


if __name__ == "__main__":
    out = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "SIG_Seguranca_Patrick.svg"))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(build())
    print("gerado:", out)
