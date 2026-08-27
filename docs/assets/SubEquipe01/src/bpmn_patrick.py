# -*- coding: utf-8 -*-
"""
Gerador dos modelos BPMN 2.0 da Subequipe 01.

Autor: Patrick Anderson Carvalho dos Santos
Saídas: ../BPMN_Checkout_Patrick.svg
        ../BPMN_PublicacaoAnuncio_Patrick.svg

Elementos implementados: pool (aberta e colapsada), raias, eventos de início,
intermediários, de borda e de fim (simples, mensagem, temporizador, erro e
terminação), tarefas de usuário e de serviço, subprocesso colapsado, gateways
exclusivo e paralelo, objeto e depósito de dados, anotação de texto, fluxo de
sequência (normal, condicional e padrão), fluxo de mensagem e associação.

Uso:  python3 bpmn_patrick.py
"""

import html
import os

FONT = "Helvetica,Arial,sans-serif"
INK = "#1c2530"
MSG = "#3f4c5a"

LANE_FILL = ["#f7f9fc", "#fdfaf4", "#f6fbf8", "#fbf7fc"]
POOL_BAND = "#e8edf4"
TASK_FILL = {"user": "#eaf2fd", "service": "#eafaf1", "none": "#ffffff"}
TASK_LINE = {"user": "#2f6fb0", "service": "#1f8a5f", "none": INK}


def esc(t):
    return html.escape(t)


def txt(x, y, s, size=12, weight="400", anchor="middle", fill=INK, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}"{extra}>{esc(s)}</text>')


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


# --------------------------------------------------------------- primitivas --
def pool(x, y, w, h, name, lanes=None, collapsed=False, note=""):
    band = 34
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" stroke="{INK}" '
           f'stroke-width="1.8" rx="3"/>']
    if lanes:
        ly = y
        for i, (lname, lh) in enumerate(lanes):
            out.append(f'<rect x="{x + band}" y="{ly}" width="{w - band}" height="{lh}" '
                       f'fill="{LANE_FILL[i % len(LANE_FILL)]}" stroke="{INK}" '
                       f'stroke-width="1.2"/>')
            out.append(f'<rect x="{x + band}" y="{ly}" width="26" height="{lh}" '
                       f'fill="#ffffff" stroke="{INK}" stroke-width="1.2"/>')
            lcx, lcy = x + band + 13, ly + lh / 2.0
            lfs = min(10.5, max(7.5, (lh - 14) / (0.62 * max(len(lname), 1))))
            out.append(txt(lcx, lcy + lfs * 0.34, lname, round(lfs, 1), "600",
                           extra=f' transform="rotate(-90 {lcx:.1f} {lcy:.1f})"'))
            ly += lh
    out.append(f'<rect x="{x}" y="{y}" width="{band}" height="{h}" fill="{POOL_BAND}" '
               f'stroke="{INK}" stroke-width="1.8"/>')
    cx, cy = x + band / 2.0, y + h / 2.0
    fs = min(12.5, max(8.5, (h - 16) / (0.62 * max(len(name), 1))))
    out.append(txt(cx, cy + fs * 0.34, name, round(fs, 1), "700",
                   extra=f' transform="rotate(-90 {cx:.1f} {cy:.1f})"'))
    if collapsed and note:
        out.append(txt(x + w / 2.0, y + h / 2.0 + 4, note, 11.5, "400", fill="#5b6570"))
    return "".join(out)


def _marker(kind, x, y):
    if kind == "user":
        return (f'<circle cx="{x + 7:.1f}" cy="{y + 7:.1f}" r="3.6" fill="none" '
                f'stroke="{INK}" stroke-width="1.3"/>'
                f'<path d="M {x + 1:.1f},{y + 16:.1f} a 6.2,6.2 0 0 1 12.4,0" fill="none" '
                f'stroke="{INK}" stroke-width="1.3"/>')
    if kind == "service":
        return (f'<circle cx="{x + 7:.1f}" cy="{y + 9:.1f}" r="6" fill="none" '
                f'stroke="{INK}" stroke-width="1.3"/>'
                f'<circle cx="{x + 7:.1f}" cy="{y + 9:.1f}" r="2.2" fill="none" '
                f'stroke="{INK}" stroke-width="1.3"/>')
    return ""


def task(cx, cy, text, kind="user", w=176, h=72, subprocess=False):
    x, y = cx - w / 2.0, cy - h / 2.0
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="10" '
           f'fill="{TASK_FILL[kind]}" stroke="{TASK_LINE[kind]}" stroke-width="1.9" '
           f'filter="url(#soft)"/>', _marker(kind, x + 7, y + 7)]
    lines = wrap(text, 22)
    y0 = cy - (len(lines) - 1) * 8 + (8 if not subprocess else 3)
    for i, ln in enumerate(lines):
        out.append(txt(cx, y0 + i * 16, ln, 12.5, "600"))
    if subprocess:
        out.append(f'<rect x="{cx - 8:.1f}" y="{y + h - 20:.1f}" width="16" height="16" '
                   f'fill="#ffffff" stroke="{INK}" stroke-width="1.3"/>'
                   f'<path d="M {cx - 4:.1f},{y + h - 12:.1f} h 8 M {cx:.1f},'
                   f'{y + h - 16:.1f} v 8" stroke="{INK}" stroke-width="1.3"/>')
    return "".join(out)


def _event_glyph(etype, cx, cy, filled=False):
    c = "#ffffff" if not filled else INK
    s = INK
    if etype == "message":
        return (f'<rect x="{cx - 8:.1f}" y="{cy - 6:.1f}" width="16" height="12" '
                f'fill="{c}" stroke="{s}" stroke-width="1.4"/>'
                f'<path d="M {cx - 8:.1f},{cy - 6:.1f} L {cx:.1f},{cy + 1:.1f} '
                f'L {cx + 8:.1f},{cy - 6:.1f}" fill="none" stroke="{s}" stroke-width="1.4"/>')
    if etype == "timer":
        return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8.5" fill="{c}" stroke="{s}" '
                f'stroke-width="1.4"/>'
                f'<path d="M {cx:.1f},{cy - 5:.1f} V {cy:.1f} L {cx + 4:.1f},{cy + 3:.1f}" '
                f'fill="none" stroke="{s}" stroke-width="1.4"/>')
    if etype == "error":
        return (f'<path d="M {cx - 8:.1f},{cy + 7:.1f} L {cx - 2:.1f},{cy - 4:.1f} '
                f'L {cx + 2:.1f},{cy + 2:.1f} L {cx + 8:.1f},{cy - 7:.1f}" fill="none" '
                f'stroke="{s}" stroke-width="2"/>')
    if etype == "terminate":
        return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="{INK}"/>'
    return ""


def event(cx, cy, kind="start", etype="none", label="", boundary=False, r=19):
    out = []
    if kind == "end":
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="#ffffff" '
                   f'stroke="{INK}" stroke-width="4"/>')
    elif kind == "intermediate":
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="#ffffff" '
                   f'stroke="{INK}" stroke-width="1.6"/>')
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r - 4}" fill="none" '
                   f'stroke="{INK}" stroke-width="1.6"/>')
    elif boundary:
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="#ffffff" '
                   f'stroke="{INK}" stroke-width="1.6"/>')
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r - 4}" fill="none" '
                   f'stroke="{INK}" stroke-width="1.6"/>')
    else:
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="#ffffff" '
                   f'stroke="{INK}" stroke-width="1.8"/>')
    out.append(_event_glyph(etype, cx, cy))
    if label:
        for i, ln in enumerate(wrap(label, 15)):
            out.append(txt(cx, cy + r + 15 + i * 13, ln, 10.5, "400", fill="#5b6570"))
    return "".join(out)


def gateway(cx, cy, gtype="xor", label="", pos="above", s=27):
    pts = f'{cx},{cy - s} {cx + s},{cy} {cx},{cy + s} {cx - s},{cy}'
    out = [f'<polygon points="{pts}" fill="#fffdf0" stroke="#b0851c" stroke-width="1.9" '
           f'filter="url(#soft)"/>']
    if gtype == "xor":
        out.append(f'<path d="M {cx - 8},{cy - 8} L {cx + 8},{cy + 8} M {cx + 8},{cy - 8} '
                   f'L {cx - 8},{cy + 8}" stroke="{INK}" stroke-width="2.3" fill="none"/>')
    elif gtype == "and":
        out.append(f'<path d="M {cx - 10},{cy} H {cx + 10} M {cx},{cy - 10} V {cy + 10}" '
                   f'stroke="{INK}" stroke-width="2.3" fill="none"/>')
    if label:
        lines = wrap(label, 18)
        y0 = cy - s - 16 - (len(lines) - 1) * 12 if pos == "above" else cy + s + 20
        for i, ln in enumerate(lines):
            out.append(txt(cx, y0 + i * 12, ln, 10.5, "600", fill="#5b6570"))
    return "".join(out)


def data_object(cx, cy, label, w=44, h=56):
    x, y = cx - w / 2.0, cy - h / 2.0
    f = 13
    out = [f'<path d="M {x},{y} H {x + w - f} L {x + w},{y + f} V {y + h} H {x} Z" '
           f'fill="#ffffff" stroke="{INK}" stroke-width="1.5"/>',
           f'<path d="M {x + w - f},{y} V {y + f} H {x + w}" fill="none" stroke="{INK}" '
           f'stroke-width="1.5"/>']
    for i, ln in enumerate(wrap(label, 14)):
        out.append(txt(cx, y + h + 14 + i * 12, ln, 10.5, "400", fill="#5b6570"))
    return "".join(out)


def data_store(cx, cy, label, w=56, h=46):
    x, y = cx - w / 2.0, cy - h / 2.0
    out = [f'<path d="M {x},{y + 7} V {y + h - 7} A {w / 2},7 0 0 0 {x + w},{y + h - 7} '
           f'V {y + 7}" fill="#ffffff" stroke="{INK}" stroke-width="1.5"/>',
           f'<ellipse cx="{cx}" cy="{y + 7}" rx="{w / 2}" ry="7" fill="#ffffff" '
           f'stroke="{INK}" stroke-width="1.5"/>',
           f'<path d="M {x},{y + 15} A {w / 2},7 0 0 0 {x + w},{y + 15}" fill="none" '
           f'stroke="{INK}" stroke-width="1.1"/>']
    for i, ln in enumerate(wrap(label, 14)):
        out.append(txt(cx, y + h + 14 + i * 12, ln, 10.5, "400", fill="#5b6570"))
    return "".join(out)


def annotation(x, y, w, h, lines, target):
    out = [f'<path d="M {x + 12},{y} L {x},{y} L {x},{y + h} L {x + 12},{y + h}" '
           f'fill="none" stroke="{INK}" stroke-width="1.6"/>']
    for i, ln in enumerate(lines):
        out.append(txt(x + 14, y + 20 + i * 15, ln, 11, "400", anchor="start", fill=MSG))
    sx = x + w if target[0] > x + w / 2 else x
    out.append(f'<line x1="{sx}" y1="{y + h / 2:.1f}" x2="{target[0]}" y2="{target[1]}" '
               f'stroke="{INK}" stroke-width="1.2" stroke-dasharray="4 4"/>')
    return "".join(out)


def _path(points):
    return " ".join(f'{"M" if i == 0 else "L"} {x:.1f},{y:.1f}'
                    for i, (x, y) in enumerate(points))


def seq(points, label="", style="normal", lpos=0):
    out = [f'<path d="{_path(points)}" fill="none" stroke="{INK}" stroke-width="1.9" '
           f'stroke-linejoin="round" marker-end="url(#seqA)"/>']
    if style == "conditional":
        x, y = points[0]
        nx, ny = points[1]
        dx, dy = nx - x, ny - y
        n = max((dx ** 2 + dy ** 2) ** 0.5, 1)
        ux, uy = dx / n, dy / n
        px, py = -uy, ux
        c = (x + ux * 9, y + uy * 9)
        out.append(f'<polygon points="{x:.1f},{y:.1f} {c[0] - px * 5:.1f},{c[1] - py * 5:.1f} '
                   f'{x + ux * 18:.1f},{y + uy * 18:.1f} {c[0] + px * 5:.1f},'
                   f'{c[1] + py * 5:.1f}" fill="#ffffff" stroke="{INK}" stroke-width="1.4"/>')
    if label:
        a, b = points[lpos], points[lpos + 1]
        mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
        vertical = abs(b[1] - a[1]) > abs(b[0] - a[0])
        mx += 20 if vertical else 0
        my += -9 if not vertical else 0
        w = 7.4 * len(label) + 10
        out.append(f'<rect x="{mx - w / 2:.1f}" y="{my - 12:.1f}" width="{w:.1f}" height="17" '
                   f'rx="4" fill="#ffffff"/>')
        out.append(txt(mx, my + 1, label, 11, "700"))
    return "".join(out)


def msg(points, label=""):
    x1, y1 = points[0]
    out = [f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="4.2" fill="#ffffff" stroke="{MSG}" '
           f'stroke-width="1.4"/>',
           f'<path d="{_path(points)}" fill="none" stroke="{MSG}" stroke-width="1.5" '
           f'stroke-dasharray="8 5" marker-end="url(#msgA)"/>']
    if label:
        x2, y2 = points[-1]
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        w = 6.6 * len(label) + 14
        out.append(f'<rect x="{mx - w / 2:.1f}" y="{my - 11:.1f}" width="{w:.1f}" height="18" '
                   f'rx="4" fill="#ffffff" stroke="#ccd4dd" stroke-width="0.9"/>')
        out.append(txt(mx, my + 2, label, 10.5, "400", fill=MSG))
    return "".join(out)


def assoc(points):
    return (f'<path d="{_path(points)}" fill="none" stroke="{MSG}" stroke-width="1.2" '
            f'stroke-dasharray="4 4" marker-end="url(#assocA)"/>')


def legend(x, y, w, items, h=112):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#fbfcfd" '
           f'stroke="#ccd4dd" stroke-width="1.3"/>',
           txt(x + 20, y + 26, "Legenda", 13, "700", anchor="start")]
    cur, row = x + 22, y + 52
    for kind, label in items:
        if kind == "seq":
            out.append(f'<line x1="{cur}" y1="{row}" x2="{cur + 38}" y2="{row}" '
                       f'stroke="{INK}" stroke-width="1.9" marker-end="url(#seqA)"/>')
            cur += 46
        elif kind == "msg":
            out.append(f'<circle cx="{cur}" cy="{row}" r="4.2" fill="#ffffff" stroke="{MSG}" '
                       f'stroke-width="1.4"/>')
            out.append(f'<line x1="{cur}" y1="{row}" x2="{cur + 38}" y2="{row}" stroke="{MSG}" '
                       f'stroke-width="1.5" stroke-dasharray="8 5" marker-end="url(#msgA)"/>')
            cur += 46
        elif kind in ("xor", "and"):
            out.append(gateway(cur + 14, row, kind, "", s=13))
            cur += 34
        elif kind in ("user", "service"):
            out.append(f'<rect x="{cur}" y="{row - 13}" width="32" height="26" rx="6" '
                       f'fill="{TASK_FILL[kind]}" stroke="{TASK_LINE[kind]}" '
                       f'stroke-width="1.6"/>')
            out.append(_marker(kind, cur + 9, row - 9.5))
            cur += 40
        elif kind == "sub":
            out.append(f'<rect x="{cur}" y="{row - 13}" width="32" height="26" rx="6" '
                       f'fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
            out.append(f'<rect x="{cur + 10.5}" y="{row - 5.5}" width="11" height="11" '
                       f'fill="#ffffff" stroke="{INK}" stroke-width="1.1"/>')
            out.append(f'<path d="M {cur + 13.5},{row} h 5 M {cur + 16},{row - 2.5} v 5" '
                       f'stroke="{INK}" stroke-width="1.1"/>')
            cur += 40
        elif kind in ("message", "timer", "error", "terminate"):
            out.append(event(cur + 15, row, "end" if kind in ("error", "terminate") else "start",
                             kind, "", r=14))
            cur += 38
        elif kind == "data":
            out.append(data_object(cur + 12, row, "", w=22, h=28))
            cur += 30
        elif kind == "store":
            out.append(data_store(cur + 14, row, "", w=28, h=24))
            cur += 36
        elif kind == "annot":
            out.append(f'<path d="M {cur + 10},{row - 12} L {cur},{row - 12} L {cur},'
                       f'{row + 12} L {cur + 10},{row + 12}" fill="none" stroke="{INK}" '
                       f'stroke-width="1.5"/>')
            cur += 20
        out.append(txt(cur + 8, row + 4, label, 11.5, "400", anchor="start", fill=MSG))
        cur += 7.1 * len(label) + 34
        if cur > x + w - 200:
            cur, row = x + 22, row + 32
    return "".join(out)


def svg(w, h, title, subtitle, body):
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
        f'height="{h}" role="img" aria-label="{esc(title)}">',
        '<defs>'
        f'<marker id="seqA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/></marker>'
        '<marker id="msgA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" '
        f'markerHeight="9" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10" fill="none" stroke="{MSG}" stroke-width="1.4"/></marker>'
        '<marker id="assocA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
        f'markerHeight="8" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10" fill="none" stroke="{MSG}" stroke-width="1.2"/></marker>'
        '<filter id="soft" x="-15%" y="-30%" width="130%" height="160%">'
        '<feDropShadow dx="0" dy="1.3" stdDeviation="1.8" flood-color="#0d1b2a" '
        'flood-opacity="0.11"/></filter>'
        '</defs>',
        f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
        txt(w / 2.0, 34, title, 19, "700"),
        txt(w / 2.0, 58, subtitle, 12.5, "400", fill="#5b6570"),
        body, '</svg>'])


# =========================================================== diagrama 1 ======
def diagrama_checkout():
    W, H = 1960, 1130
    b = []
    b.append(pool(40, 80, 1880, 310, "Comprador"))
    b.append(pool(40, 410, 1880, 500, "G1_ProjetoComercioEletronico",
                  lanes=[("Catálogo e Carrinho", 200), ("Entrega", 150), ("Pagamentos", 150)]))
    b.append(pool(40, 926, 1880, 74, "Vendedor", collapsed=True,
                  note="pool colapsada — o processo interno do vendedor está fora deste recorte"))

    # --- raia do comprador
    b.append(seq([(149, 230), (182, 230)]))
    b.append(seq([(358, 230), (382, 230)]))
    b.append(seq([(558, 230), (613, 230)]))
    b.append(seq([(640, 257), (640, 299)], "Não", "conditional"))
    b.append(seq([(728, 335), (830, 335), (830, 266)]))
    b.append(seq([(667, 230), (742, 230)], "Sim", "conditional"))
    b.append(seq([(918, 230), (983, 230)]))
    b.append(seq([(1010, 203), (1010, 166)], "Não", "conditional"))
    b.append(seq([(922, 130), (860, 130), (860, 194)]))
    b.append(seq([(1037, 230), (1102, 230)], "Sim", "conditional"))
    b.append(seq([(1278, 230), (1351, 230)]))
    b.append(seq([(890, 266), (890, 298), (1050, 298), (1050, 311)]))

    # --- raia da plataforma
    b.append(seq([(169, 490), (192, 490)]))
    b.append(seq([(368, 490), (385, 490), (385, 685), (402, 685)]))
    b.append(seq([(578, 685), (602, 685)]))
    b.append(seq([(778, 685), (785, 685), (785, 835), (792, 835)]))
    b.append(seq([(968, 835), (992, 835)]))
    b.append(seq([(1168, 835), (1205, 835), (1205, 685), (1223, 685)]))
    b.append(seq([(1250, 658), (1250, 490), (1292, 490)]))
    b.append(seq([(1277, 685), (1292, 685)]))
    b.append(seq([(1468, 490), (1590, 490), (1590, 658)]))
    b.append(seq([(1468, 685), (1563, 685)]))
    b.append(seq([(1617, 685), (1671, 685)]))
    b.append(seq([(1140, 871), (1140, 890), (1180, 890), (1180, 835), (1231, 835)]))

    # --- fluxos de mensagem
    b.append(msg([(250, 266), (250, 350), (150, 350), (150, 471)], "Itens selecionados"))
    b.append(msg([(480, 649), (480, 266)], "Frete e prazo"))
    b.append(msg([(660, 371), (660, 649)], "CEP e endereço"))
    b.append(msg([(860, 266), (860, 799)], "Dados do pagamento"))
    b.append(msg([(940, 799), (940, 166)], "Erro por campo"))
    b.append(msg([(1160, 266), (1160, 799)], "Confirmação"))
    b.append(msg([(1380, 721), (1380, 926)], "Pedido a preparar"))

    # --- associações de dados
    b.append(assoc([(368, 490), (532, 490)]))
    b.append(assoc([(1424, 526), (1516, 545)]))

    # --- tarefas, eventos e gateways
    b.append(task(270, 230, "Adicionar item ao carrinho"))
    b.append(task(470, 230, "Revisar itens do carrinho"))
    b.append(task(640, 335, "Cadastrar endereço de entrega"))
    b.append(task(830, 230, "Informar meio de pagamento"))
    b.append(task(1010, 130, "Corrigir o campo apontado"))
    b.append(task(1190, 230, "Confirmar a compra"))
    b.append(task(280, 490, "Agrupar itens por vendedor", "service"))
    b.append(task(490, 685, "Calcular frete e prazo por CEP", "service"))
    b.append(task(690, 685, "Validar endereço informado", "service"))
    b.append(task(880, 835, "Validar dados do formulário", "none", subprocess=True))
    b.append(task(1080, 835, "Autorizar pagamento", "service"))
    b.append(task(1380, 490, "Registrar o pedido", "service"))
    b.append(task(1380, 685, "Notificar o vendedor", "service"))

    b.append(data_store(560, 490, "Catálogo"))
    b.append(data_object(1540, 556, "Pedido"))

    b.append(gateway(640, 230, "xor", "Endereço de entrega definido?"))
    b.append(gateway(1010, 230, "xor", "Dados válidos?", pos="below"))
    b.append(gateway(1250, 685, "and"))
    b.append(gateway(1590, 685, "and"))

    b.append(event(130, 230, "start", "none", "Decidiu comprar"))
    b.append(event(1370, 230, "end", "none", "Pedido confirmado"))
    b.append(event(1050, 330, "end", "terminate", "Checkout expirado"))
    b.append(event(890, 266, "start", "timer", "", boundary=True, r=15))
    b.append(event(150, 490, "start", "message", "Carrinho aberto"))
    b.append(event(1690, 685, "end", "none", "Pedido registrado"))
    b.append(event(1250, 835, "end", "error", "Pagamento recusado"))
    b.append(event(1140, 871, "start", "error", "", boundary=True, r=15))

    b.append(annotation(560, 770, 220, 50,
                        ["Validação só na submissão (RN-B06):",
                         "++ Integridade / − Tempo de Resposta"], (792, 835)))
    b.append(annotation(1200, 302, 236, 46,
                        ["Evento não observado —", "inferido a partir do domínio"],
                        (1069, 330)))

    b.append(legend(40, 1012, 1880, [
        ("seq", "fluxo de sequência"), ("msg", "fluxo de mensagem"),
        ("xor", "gateway exclusivo"), ("and", "gateway paralelo"),
        ("user", "tarefa de usuário"), ("service", "tarefa de serviço"),
        ("sub", "subprocesso colapsado"), ("message", "evento de mensagem"),
        ("timer", "evento temporizador"), ("error", "evento de erro"),
        ("terminate", "terminação"), ("data", "objeto de dados"),
        ("store", "depósito de dados"), ("annot", "anotação de texto"),
    ], h=100))

    return svg(W, H, "BPMN — Carrinho, endereço e checkout do G1_ProjetoComercioEletronico",
               "Fluxo recuperado por engenharia reversa da interface — notação BPMN 2.0 (OMG, 2011)",
               "\n".join(b))


# =========================================================== diagrama 2 ======
def diagrama_anuncio():
    W, H = 1880, 920
    b = []
    b.append(pool(40, 80, 1800, 300, "Vendedor"))
    b.append(pool(40, 400, 1800, 300, "G1_ProjetoComercioEletronico",
                  lanes=[("Anúncios", 150), ("Catálogo", 150)]))
    b.append(pool(40, 716, 1800, 74, "Comprador", collapsed=True,
                  note="pool colapsada — a descoberta do anúncio pelo comprador é outro recorte"))

    # --- raia do vendedor
    b.append(seq([(139, 225), (172, 225)]))
    b.append(seq([(348, 225), (403, 225)]))
    b.append(seq([(430, 252), (430, 294)], "Outros", "conditional"))
    b.append(seq([(457, 225), (512, 225)], "Produtos", "conditional"))
    b.append(seq([(688, 225), (743, 225)]))
    b.append(seq([(770, 198), (770, 156), (842, 156)], "Não", "conditional"))
    b.append(seq([(797, 225), (842, 225)], "Sim", "conditional"))
    b.append(seq([(1018, 156), (1150, 156), (1150, 189)]))
    b.append(seq([(1018, 225), (1062, 225)]))
    b.append(seq([(1238, 225), (1272, 225)]))
    b.append(seq([(1448, 225), (1482, 225)]))
    b.append(seq([(1658, 225), (1711, 225)]))
    b.append(seq([(1448, 330), (1570, 330), (1570, 261)]))

    # --- raia da plataforma
    b.append(seq([(169, 475), (182, 475)]))
    b.append(seq([(358, 475), (370, 475), (370, 625), (382, 625)]))
    b.append(seq([(558, 625), (620, 625), (620, 475), (682, 475)]))
    b.append(seq([(858, 475), (963, 475)]))
    b.append(seq([(1017, 475), (1112, 475)], "Sim", "conditional"))
    b.append(seq([(990, 502), (990, 601)], "Não", "conditional"))
    b.append(seq([(1288, 475), (1381, 475)]))

    # --- fluxos de mensagem
    b.append(msg([(240, 261), (240, 330), (150, 330), (150, 456)], "Domínio escolhido"))
    b.append(msg([(540, 589), (540, 261)], "Sugestões do catálogo"))
    b.append(msg([(1540, 261), (1540, 372), (770, 372), (770, 439)], "Anúncio submetido"))
    b.append(msg([(1009, 620), (1040, 620), (1040, 390), (1360, 390), (1360, 366)],
                 "Erro no anúncio"))
    b.append(msg([(1270, 511), (1270, 560), (1400, 560), (1400, 716)], "Anúncio disponível"))

    b.append(assoc([(270, 511), (270, 592)]))
    b.append(assoc([(1200, 511), (1200, 600)]))

    # --- elementos
    b.append(task(260, 225, "Escolher o que anunciar"))
    b.append(task(430, 330, "Veículos, imóveis e serviços", "none", subprocess=True))
    b.append(task(600, 225, "Buscar produto no catálogo"))
    b.append(task(930, 156, "Descrever o produto do zero"))
    b.append(task(930, 225, "Selecionar item do catálogo"))
    b.append(task(1150, 225, "Definir preço e estoque"))
    b.append(task(1360, 225, "Enviar fotos do produto"))
    b.append(task(1570, 225, "Publicar o anúncio"))
    b.append(task(1360, 330, "Corrigir dados do anúncio"))

    b.append(task(270, 475, "Criar rascunho do anúncio", "service"))
    b.append(task(470, 625, "Sugerir itens do catálogo", "service"))
    b.append(task(770, 475, "Validar dados do anúncio", "none", subprocess=True))
    b.append(task(1200, 475, "Publicar no catálogo", "service"))

    b.append(data_object(270, 620, "Rascunho"))
    b.append(data_store(1200, 625, "Catálogo"))

    b.append(gateway(430, 225, "xor", "Tipo de anúncio?"))
    b.append(gateway(770, 225, "xor", "Encontrou no catálogo?", pos="below"))
    b.append(gateway(990, 475, "xor", "Dados completos?"))

    b.append(event(120, 225, "start", "none", "Decidiu vender"))
    b.append(event(1730, 225, "end", "none", "Anúncio publicado"))
    b.append(event(150, 475, "start", "message", "Rascunho solicitado"))
    b.append(event(990, 620, "intermediate", "message", "Devolve o erro"))
    b.append(event(1400, 475, "end", "none", "Anúncio no ar"))

    b.append(annotation(700, 552, 260, 56,
                        ["O rascunho é criado assim que o domínio é",
                         "escolhido, antes de qualquer dado do produto;",
                         "o identificador viaja na URL — observado"], (270, 511)))

    b.append(legend(40, 800, 1800, [
        ("seq", "fluxo de sequência"), ("msg", "fluxo de mensagem"),
        ("xor", "gateway exclusivo"), ("user", "tarefa de usuário"),
        ("service", "tarefa de serviço"), ("sub", "subprocesso colapsado"),
        ("message", "evento de mensagem"), ("data", "objeto de dados"),
        ("store", "depósito de dados"), ("annot", "anotação de texto"),
    ], h=100))

    return svg(W, H, "BPMN — Publicação de anúncio pelo vendedor",
               "Fluxo recuperado por engenharia reversa da interface — notação BPMN 2.0 (OMG, 2011)",
               "\n".join(b))


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    for nome, fn in (("BPMN_Checkout_Patrick.svg", diagrama_checkout),
                     ("BPMN_PublicacaoAnuncio_Patrick.svg", diagrama_anuncio)):
        out = os.path.normpath(os.path.join(base, "..", nome))
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(fn())
        print("gerado:", out)
