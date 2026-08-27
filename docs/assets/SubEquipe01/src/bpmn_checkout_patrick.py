# -*- coding: utf-8 -*-
"""
Gerador do modelo BPMN 2.0 do fluxo de carrinho, endereco e checkout,
levantado por engenharia reversa.

Autor: Patrick Anderson Carvalho dos Santos - Subequipe 01
Saida: ../BPMN_Checkout_Patrick.svg

Recursos da notacao usados: pools, pool colapsada, evento de inicio e de fim,
tarefas de usuario e de servico, gateways exclusivos, fluxo de sequencia,
fluxo de mensagem e anotacao de texto.

Uso:  python3 bpmn_checkout_patrick.py
"""

import html
import os

W, H = 1760, 800
FONT = "Helvetica,Arial,sans-serif"
INK = "#1f2933"

# ---------------------------------------------------------------- pools -----
POOLS = [
    dict(name="Comprador",                     x=40, y=56,  w=1680, h=308),
    dict(name="G1_ProjetoComercioEletronico",  x=40, y=384, w=1680, h=246),
    dict(name="Vendedor",                      x=40, y=650, w=1680, h=64,
         collapsed=True),
]

# --------------------------------------------------------------- tarefas ----
# icon: "user" (tarefa de usuario) | "service" (tarefa de servico)
TASKS = {
    "T1": dict(cx=250,  cy=230, w=150, h=68, icon="user",
               lines=["Adicionar item", "ao carrinho"]),
    "T2": dict(cx=440,  cy=230, w=150, h=68, icon="user",
               lines=["Revisar itens", "do carrinho"]),
    "T3": dict(cx=610,  cy=320, w=170, h=64, icon="user",
               lines=["Cadastrar endereco", "de entrega"]),
    "T4": dict(cx=790,  cy=230, w=160, h=68, icon="user",
               lines=["Informar meio", "de pagamento"]),
    "T5": dict(cx=960,  cy=120, w=160, h=64, icon="user",
               lines=["Corrigir o campo", "apontado"]),
    "T6": dict(cx=1130, cy=230, w=150, h=68, icon="user",
               lines=["Confirmar", "a compra"]),
    "P1": dict(cx=265,  cy=507, w=170, h=68, icon="service",
               lines=["Agrupar itens", "por vendedor"]),
    "P2": dict(cx=470,  cy=507, w=180, h=68, icon="service",
               lines=["Calcular frete e", "prazo por CEP"]),
    "P3": dict(cx=690,  cy=507, w=170, h=68, icon="service",
               lines=["Validar endereco", "informado"]),
    "P4": dict(cx=910,  cy=507, w=180, h=68, icon="service",
               lines=["Validar dados", "na submissao"]),
    "P5": dict(cx=1130, cy=507, w=150, h=68, icon="service",
               lines=["Registrar", "o pedido"]),
    "P6": dict(cx=1330, cy=507, w=160, h=68, icon="service",
               lines=["Notificar", "o vendedor"]),
}

# --------------------------------------------------------------- eventos ----
EVENTS = {
    "S1": dict(cx=120,  cy=230, kind="start", label="Decidiu comprar"),
    "E1": dict(cx=1300, cy=230, kind="end",   label="Pedido confirmado"),
    "S2": dict(cx=145,  cy=507, kind="start", label="Carrinho aberto"),
    "E2": dict(cx=1470, cy=507, kind="end",   label="Pedido registrado"),
}

# -------------------------------------------------------------- gateways ----
GATEWAYS = {
    "G1": dict(cx=610, cy=230, pos="above", label="Endereco de\nentrega definido?"),
    "G2": dict(cx=960, cy=230, pos="below", label="Dados do\nformulario validos?"),
}

# ------------------------------------------------- fluxos de sequencia ------
# cada item: lista de pontos (polilinha) e rotulo opcional
SEQ = [
    ([(139, 230), (175, 230)], ""),
    ([(325, 230), (365, 230)], ""),
    ([(515, 230), (582, 230)], ""),
    ([(610, 258), (610, 288)], "nao"),
    ([(695, 320), (790, 320), (790, 264)], ""),
    ([(638, 230), (710, 230)], "sim"),
    ([(870, 230), (932, 230)], ""),
    ([(960, 202), (960, 152)], "nao"),
    ([(880, 120), (740, 120), (740, 196)], ""),
    ([(988, 230), (1055, 230)], "sim"),
    ([(1205, 230), (1281, 230)], ""),
    ([(164, 507), (180, 507)], ""),
    ([(335, 507), (380, 507)], ""),
    ([(560, 507), (605, 507)], ""),
    ([(775, 507), (820, 507)], ""),
    ([(1000, 507), (1055, 507)], ""),
    ([(1205, 507), (1250, 507)], ""),
    ([(1410, 507), (1451, 507)], ""),
]

# --------------------------------------------------- fluxos de mensagem -----
MSG = [
    ([(250, 264), (250, 473)], "itens selecionados"),
    ([(470, 473), (440, 264)], "frete e prazo"),
    ([(610, 352), (690, 473)], "CEP e endereco"),
    ([(850, 264), (880, 473)], "dados do pagamento"),
    ([(990, 473), (1010, 152)], "erro por campo"),
    ([(1130, 264), (1130, 473)], "confirmacao"),
    ([(1330, 541), (1330, 650)], "pedido a preparar"),
]

# ------------------------------------------------------------- anotacao -----
ANNOT = dict(x=640, y=556, w=252, h=54, anchor=(892, 583), target=(910, 541),
             lines=["Validar no servidor: ++ Integridade [Pedido]",
                    "e - Tempo de Resposta [Checkout] - ver SIG"])


def esc(t):
    return html.escape(t)


def txt(x, y, s, size=12, weight="400", anchor="middle", fill=INK):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(s)}</text>')


def pool(p):
    band = 36
    out = [f'<rect x="{p["x"]}" y="{p["y"]}" width="{p["w"]}" height="{p["h"]}" '
           f'fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>',
           f'<rect x="{p["x"]}" y="{p["y"]}" width="{band}" height="{p["h"]}" '
           f'fill="#eef1f5" stroke="{INK}" stroke-width="1.8"/>']
    cx, cy = p["x"] + band / 2.0, p["y"] + p["h"] / 2.0
    out.append(f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" '
               f'font-family="{FONT}" font-size="13" font-weight="700" fill="{INK}" '
               f'transform="rotate(-90 {cx:.1f} {cy:.1f})">{esc(p["name"])}</text>')
    if p.get("collapsed"):
        out.append(txt(p["x"] + p["w"] / 2.0, p["y"] + p["h"] / 2.0 + 4,
                       "pool colapsada - processo do vendedor fora do escopo deste recorte",
                       size=12, fill="#5b6570"))
    return "".join(out)


def icon(kind, x, y):
    """Marcador do tipo de tarefa, no canto superior esquerdo."""
    if kind == "user":
        return (f'<circle cx="{x + 7:.1f}" cy="{y + 7:.1f}" r="3.6" fill="none" '
                f'stroke="{INK}" stroke-width="1.3"/>'
                f'<path d="M {x + 1:.1f},{y + 16:.1f} a 6.2,6.2 0 0 1 12.4,0" fill="none" '
                f'stroke="{INK}" stroke-width="1.3"/>')
    return (f'<circle cx="{x + 7:.1f}" cy="{y + 9:.1f}" r="6" fill="none" '
            f'stroke="{INK}" stroke-width="1.3"/>'
            f'<circle cx="{x + 7:.1f}" cy="{y + 9:.1f}" r="2.2" fill="none" '
            f'stroke="{INK}" stroke-width="1.3"/>')


def task(t):
    x, y = t["cx"] - t["w"] / 2.0, t["cy"] - t["h"] / 2.0
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{t["w"]}" height="{t["h"]}" rx="9" '
           f'fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>',
           icon(t["icon"], x + 6, y + 6)]
    n = len(t["lines"])
    y0 = t["cy"] - (n - 1) * 8 + 8
    for i, ln in enumerate(t["lines"]):
        out.append(txt(t["cx"], y0 + i * 16, ln, size=12.5, weight="600"))
    return "".join(out)


def event(e):
    r = 19
    if e["kind"] == "start":
        body = (f'<circle cx="{e["cx"]}" cy="{e["cy"]}" r="{r}" fill="#ffffff" '
                f'stroke="{INK}" stroke-width="1.8"/>')
    else:
        body = (f'<circle cx="{e["cx"]}" cy="{e["cy"]}" r="{r}" fill="#ffffff" '
                f'stroke="{INK}" stroke-width="4"/>')
    return body + txt(e["cx"], e["cy"] + r + 16, e["label"], size=11, fill="#5b6570")


def gateway(g):
    s = 28
    pts = f'{g["cx"]},{g["cy"] - s} {g["cx"] + s},{g["cy"]} {g["cx"]},{g["cy"] + s} {g["cx"] - s},{g["cy"]}'
    out = [f'<polygon points="{pts}" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>',
           f'<path d="M {g["cx"] - 8},{g["cy"] - 8} L {g["cx"] + 8},{g["cy"] + 8} '
           f'M {g["cx"] + 8},{g["cy"] - 8} L {g["cx"] - 8},{g["cy"] + 8}" '
           f'stroke="{INK}" stroke-width="2.2" fill="none"/>']
    lines = g["label"].split("\n")
    if g.get("pos", "above") == "below":
        y0 = g["cy"] + s + 20
    else:
        y0 = g["cy"] - s - 18 - (len(lines) - 1) * 13
    for i, ln in enumerate(lines):
        out.append(txt(g["cx"], y0 + i * 13, ln, size=10.5, fill="#5b6570"))
    return "".join(out)


def polyline(points, stroke, width, dash, marker):
    d = " ".join(f'{"M" if i == 0 else "L"} {x:.1f},{y:.1f}'
                 for i, (x, y) in enumerate(points))
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}"'
            f'{da} marker-end="url(#{marker})"/>')


def seq_flow(points, label):
    out = [polyline(points, INK, 1.8, None, "seqArrow")]
    if label:
        (x1, y1), (x2, y2) = points[0], points[1]
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        off = -8 if abs(y2 - y1) > abs(x2 - x1) else -7
        out.append(f'<rect x="{mx + off - 14:.1f}" y="{my - 19:.1f}" width="30" '
                   f'height="16" rx="3" fill="#ffffff"/>')
        out.append(txt(mx + off, my - 7, label, size=11, weight="700"))
    return "".join(out)


def msg_flow(points, label):
    x1, y1 = points[0]
    out = [f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="4" fill="#ffffff" '
           f'stroke="{INK}" stroke-width="1.4"/>',
           polyline(points, "#3f4c5a", 1.5, "7 5", "msgArrow")]
    if label:
        x2, y2 = points[-1]
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        w = 7.0 * len(label)
        out.append(f'<rect x="{mx - w / 2:.1f}" y="{my - 10:.1f}" width="{w:.1f}" '
                   f'height="17" rx="3" fill="#ffffff" stroke="#c3cad3" stroke-width="0.9"/>')
        out.append(txt(mx, my + 3, label, size=10.5, fill="#3f4c5a"))
    return "".join(out)


def annotation(a):
    out = [f'<path d="M {a["x"] + 12},{a["y"]} L {a["x"]},{a["y"]} L {a["x"]},'
           f'{a["y"] + a["h"]} L {a["x"] + 12},{a["y"] + a["h"]}" fill="none" '
           f'stroke="{INK}" stroke-width="1.6"/>']
    for i, ln in enumerate(a["lines"]):
        out.append(txt(a["x"] + 14, a["y"] + 22 + i * 15, ln, size=11,
                       anchor="start", fill="#3f4c5a"))
    out.append(f'<line x1="{a["anchor"][0]}" y1="{a["anchor"][1]}" '
               f'x2="{a["target"][0]}" y2="{a["target"][1]}" stroke="{INK}" '
               f'stroke-width="1.3" stroke-dasharray="4 4"/>')
    return "".join(out)


def legend():
    x, y, w, h = 40, 726, 1680, 58
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#fafbfc" '
           f'stroke="#c3cad3" stroke-width="1.2"/>']
    cy = y + h / 2.0
    cur = x + 24
    items = [
        ("seq",   "fluxo de sequencia - dentro da pool"),
        ("msg",   "fluxo de mensagem - entre pools"),
        ("gw",    "gateway exclusivo"),
        ("user",  "tarefa de usuario"),
        ("serv",  "tarefa de servico"),
        ("annot", "anotacao de texto"),
    ]
    for kind, label in items:
        if kind == "seq":
            out.append(polyline([(cur, cy), (cur + 40, cy)], INK, 1.8, None, "seqArrow"))
            cur += 48
        elif kind == "msg":
            out.append(f'<circle cx="{cur}" cy="{cy}" r="4" fill="#ffffff" '
                       f'stroke="{INK}" stroke-width="1.4"/>')
            out.append(polyline([(cur, cy), (cur + 40, cy)], "#3f4c5a", 1.5, "7 5", "msgArrow"))
            cur += 48
        elif kind == "gw":
            out.append(f'<polygon points="{cur + 14},{cy - 13} {cur + 27},{cy} '
                       f'{cur + 14},{cy + 13} {cur + 1},{cy}" fill="#ffffff" '
                       f'stroke="{INK}" stroke-width="1.6"/>')
            out.append(f'<path d="M {cur + 9},{cy - 5} L {cur + 19},{cy + 5} '
                       f'M {cur + 19},{cy - 5} L {cur + 9},{cy + 5}" stroke="{INK}" '
                       f'stroke-width="1.8"/>')
            cur += 34
        elif kind in ("user", "serv"):
            out.append(f'<rect x="{cur}" y="{cy - 13}" width="30" height="26" rx="5" '
                       f'fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
            out.append(icon("user" if kind == "user" else "service", cur + 3, cy - 11))
            cur += 38
        else:
            out.append(f'<path d="M {cur + 10},{cy - 12} L {cur},{cy - 12} L {cur},'
                       f'{cy + 12} L {cur + 10},{cy + 12}" fill="none" stroke="{INK}" '
                       f'stroke-width="1.5"/>')
            cur += 18
        out.append(txt(cur + 6, cy + 4, label, size=11.5, anchor="start", fill="#3f4c5a"))
        cur += 7.6 * len(label) + 34
    return "".join(out)


def build():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
         f'height="{H}" role="img" aria-label="Modelo BPMN do fluxo de carrinho, '
         f'endereco e checkout">',
         '<defs>',
         f'<marker id="seqArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
         f'markerHeight="7" orient="auto-start-reverse">'
         f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/></marker>',
         '<marker id="msgArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" '
         'markerHeight="9" orient="auto-start-reverse">'
         '<path d="M 0 0 L 10 5 L 0 10" fill="none" stroke="#3f4c5a" '
         'stroke-width="1.4"/></marker>',
         '</defs>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         txt(W / 2.0, 32, "BPMN - Fluxo de carrinho, endereco e entrada de checkout "
             "- G1_ProjetoComercioEletronico", size=17, weight="700")]
    for pl in POOLS:
        p.append(pool(pl))
    for pts, lab in SEQ:
        p.append(seq_flow(pts, lab))
    for pts, lab in MSG:
        p.append(msg_flow(pts, lab))
    for t in TASKS.values():
        p.append(task(t))
    for e in EVENTS.values():
        p.append(event(e))
    for g in GATEWAYS.values():
        p.append(gateway(g))
    p.append(annotation(ANNOT))
    p.append(legend())
    p.append('</svg>')
    return "\n".join(p)


if __name__ == "__main__":
    out = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "BPMN_Checkout_Patrick.svg"))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(build())
    print("gerado:", out)
