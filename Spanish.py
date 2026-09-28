#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESPAÑOL · Grammar Studio - Enhanced Edition
============================================
Color-coded, all-inclusive Spanish grammar guide with memorization engine.
Converted from Latin/Greek/French Studios — same fancy dark GUI, fully debugged.

GUIDE   Overview · Alphabet & Pronunciation · Nouns & Articles · Adjectives · Pronouns · Verbs · Irregular Verbs · Reference
STUDY   Flashcards (spaced repetition) · Type-in Drill · Worksheet · Memory Aids

Run: python3 Spanish-Grammar-Studio-Enhanced.py
Needs: Python 3.8+ with Tkinter only.
"""

import html
import json
import os
import random
import unicodedata
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox

# ─── THEME (same as previous Studios) ───────────────────────────────────────
BG, PANEL, PANEL2 = "#11131b", "#1a1d2a", "#232739"
ROW_A, ROW_B, HEAD_BG, BORDER = "#1c1f2d", "#171a26", "#0d0f16", "#333955"
FG, DIM, GOLD, GREEN, RED = "#efe6d0", "#8e93ad", "#e0b458", "#6fcf8f", "#ff6b7d"

CASE_COL = ["#5fa8ff", "#ff8ab8", "#4fd1b5", "#f2c94c", "#c58af9", "#9bdc6a"]
TCOL = {
    "pres": "#f2c94c",   # presente
    "pret": "#ff7a7a",   # pretérito
    "impf": "#4fd1b5",   # imperfecto
    "fut": "#5fa8ff",    # futuro
    "cond": "#9bdc6a",   # condicional
    "subj": "#ffb74d",   # subjuntivo
    "imp": "#ff8ab8",    # imperativo
    "perf": "#c58af9",   # perfecto
}

SERIF, SANS = "Georgia", "Helvetica Neue"
F_TITLE = (SERIF, 30, "bold")
F_H1 = (SERIF, 22, "bold")
F_H2 = (SERIF, 16, "bold")
F_BODY = (SERIF, 14)
F_BOLD = (SERIF, 14, "bold")
F_SMALL = (SANS, 11)
F_NAV = (SANS, 13)
F_BTN = (SANS, 12, "bold")

# ─── SPANISH CORE DATA ──────────────────────────────────────────────────────
GENDER_USE = [
    ("Masculino", "el / un", "Masc nouns -o, -e, -ma, consonant", "el gato negro — the black cat (m)"),
    ("Femenino", "la / una", "Fem nouns -a, -ción, -sión, -dad", "la casa blanca — the white house (f)"),
    ("Plural", "los / las", "Plural -s or -es", "los gatos negros / las casas blancas"),
]

PERS = ["yo (I)", "tú (you)", "él/ella/usted (he/she/you formal)", "nosotros (we)", "vosotros (you pl Spain)", "ellos/ellas/ustedes (they)"]
PERS_SHORT = ["yo", "tú", "él/ella/Ud.", "nosotros", "vosotros", "ellos/Uds."]

def _n(key, group, title, gender, word, meaning, art_sg, art_pl, plural, note=""):
    return dict(key=key, group=group, title=title, gender=gender, word=word,
                meaning=meaning, art_sg=art_sg, art_pl=art_pl, plural=plural, note=note)

NOUNS = [
    _n("m_gato", "Masc -o", "Masc. -o: gato", "masculine", "gato", "cat", "el", "los", "gatos",
       note="Most -o masc: el gato, el libro, el perro. Exception: la mano (f)."),
    _n("f_casa", "Fém -a", "Fém. -a: casa", "feminine", "casa", "house", "la", "las", "casas",
       note="Most -a fém: la casa, la mesa, la silla. Exception: el día, el mapa (m)."),
    _n("m_arbol", "Masc - consonante", "Masc. cons: árbol", "masculine", "árbol", "tree", "el", "los", "árboles",
       note="Cons ending → -es pl: árbol→árboles, pared→paredes, lápiz→lápices (z→c)."),
    _n("f_cancion", "Fém -ción", "Fém. -ción: canción", "feminine", "canción", "song", "la", "las", "canciones",
       note="All -ción, -sión, -dad, -tad fém: la canción, la ciudad, la universidad."),
    _n("m_problema", "Masc -ma griego", "Masc. griego -ma: problema", "masculine", "problema", "problem", "el", "los", "problemas",
       note="Greek -ma masc: el problema, el sistema, el tema, el programa, el idioma."),
    _n("m_lapiz", "Masc -z → -ces", "Masc. -z: lápiz", "masculine", "lápiz", "pencil", "el", "los", "lápices",
       note="-z → -ces pl and accent shift: lápiz→lápices, voz→voces, luz→luces."),
    _n("f_mano", "Fém irregular -o", "Fém. irregular -o: mano", "feminine", "mano", "hand", "la", "las", "manos",
       note="Irregular fem in -o: la mano, la foto (fotografía), la moto (motocicleta)."),
    _n("f_agua", "Fém - agua with el", "Fém. agua (takes el)", "feminine", "agua", "water", "el", "las", "aguas",
       note="Fem starting with stressed a- takes el in sg: el agua, el águila (but fem! las aguas frías)."),
]

ADJECTIVES = [
    {
        "title": "Regular: -o/-a: negro, blanca (black/white)",
        "type": "regular",
        "table": [
            ["", "Masc sg", "Fém sg", "Masc pl", "Fém pl"],
            ["negro (black)", "negro", "negra", "negros", "negras"],
            ["blanco (white)", "blanco", "blanca", "blancos", "blancas"],
            ["pequeño (small)", "pequeño", "pequeña", "pequeños", "pequeñas"],
            ["alto (tall)", "alto", "alta", "altos", "altas"],
        ],
        "note": "Rule: -o → -a (fém), -os (m pl), -as (f pl). Must agree with noun."
    },
    {
        "title": "Consonant / -e: same for m/f sg, -es pl",
        "type": "consonant",
        "table": [
            ["", "Masc sg", "Fém sg", "Masc pl", "Fém pl"],
            ["fácil (easy)", "fácil", "fácil", "fáciles", "fáciles"],
            ["difícil (difficult)", "difícil", "difícil", "difíciles", "difíciles"],
            ["grande (big)", "grande", "grande", "grandes", "grandes"],
            ["inteligente", "inteligente", "inteligente", "inteligentes", "inteligentes"],
            ["español", "español", "española", "españoles", "españolas"],
        ],
        "note": "-e and consonant: same m/f sg, pl -es. Except -or, -án, -ón, -és add -a for fém: español→española."
    },
    {
        "title": "Position & Short forms: buen/mal/gran + comparison",
        "type": "position",
        "table": [
            ["", "Before vowel/masc", "Normal", "Meaning change"],
            ["bueno (good)", "buen amigo", "amigo bueno", "buen = short before masc sg noun"],
            ["malo (bad)", "mal día", "día malo", "mal = short"],
            ["grande (big/great)", "gran idea", "idea grande", "gran = great, grande = big"],
            ["Comparison", "alto", "más alto que", "el más alto / altísimo"],
            ["Irregular comp", "bueno", "mejor que", "el mejor / óptimo"],
            ["Irregular comp", "malo", "peor que", "el peor / pésimo"],
        ],
        "note": "BAGS in Spanish too: bueno/malo/gran go before noun (shortened). Most adj AFTER noun. Superlative: -ísimo or más...que / el más..."
    },
]

PRONOUNS = [
    {"title": "Articles: definido, indefinido, neutro", "forms": [
        ["", "Masc sg", "Fém sg", "Masc pl", "Fém pl"],
        ["Definido (the)", "el", "la", "los", "las"],
        ["Indefinido (a/some)", "un", "una", "unos", "unas"],
        ["Neutro lo", "lo (lo bueno = what is good)", "—", "—", "—"],
        ["Contracción", "al (a+el)", "del (de+el)", "—", "—"],
    ]},
    {"title": "Personal Pronouns — sujeto, objeto directo/indirecto, reflexivo", "forms": [
        ["", "Sujeto", "OD (lo/la/los)", "OI (le/les)", "Reflexivo"],
        ["yo", "yo", "me", "me", "me"],
        ["tú", "tú", "te", "te", "te"],
        ["él/ella/Ud.", "él/ella/Ud.", "lo/la", "le", "se"],
        ["nosotros", "nosotros", "nos", "nos", "nos"],
        ["vosotros", "vosotros", "os", "os", "os"],
        ["ellos/Uds.", "ellos/Uds.", "los/las", "les", "se"],
    ]},
    {"title": "Posesivo, Demostrativo, Relativo", "forms": [
        ["", "Masc sg", "Fém sg", "Pl", "Note"],
        ["mi (my)", "mi", "mi", "mis", "mi libro, mis libros"],
        ["tu (your)", "tu", "tu", "tus", "tu casa"],
        ["su (his/her/your)", "su", "su", "sus", "su libro (his/your)"],
        ["este (this)", "este", "esta", "estos/estas", "este libro (near me)"],
        ["ese (that)", "ese", "esa", "esos/esas", "ese libro (near you)"],
        ["aquel (that over there)", "aquel", "aquella", "aquellos/aquellas", "aquel libro (far)"],
        ["que (that/who)", "que", "que", "que", "el libro que leo"],
        ["quien (who)", "quien", "quien", "quienes", "la persona con quien hablo"],
    ]},
]

VERBS = [
    {
        "key": "hablar",
        "label": "1er grupo -AR: hablar (to speak) — most common!",
        "conj": "1er grupo -AR",
        "tables": {
            "Presente": ["hablo", "hablas", "habla", "hablamos", "habláis", "hablan"],
            "Imperfecto": ["hablaba", "hablabas", "hablaba", "hablábamos", "hablabais", "hablaban"],
            "Pretérito": ["hablé", "hablaste", "habló", "hablamos", "hablasteis", "hablaron"],
            "Futuro": ["hablaré", "hablarás", "hablará", "hablaremos", "hablaréis", "hablarán"],
            "Condicional": ["hablaría", "hablarías", "hablaría", "hablaríamos", "hablaríais", "hablarían"],
            "Subjuntivo presente": ["hable", "hables", "hable", "hablemos", "habléis", "hablen"],
            "Imperativo": ["—", "habla!", "—", "hablemos!", "hablad!", "—"],
        }
    },
    {
        "key": "comer",
        "label": "2º grupo -ER: comer (to eat)",
        "conj": "2º grupo -ER",
        "tables": {
            "Presente": ["como", "comes", "come", "comemos", "coméis", "comen"],
            "Imperfecto": ["comía", "comías", "comía", "comíamos", "comíais", "comían"],
            "Pretérito": ["comí", "comiste", "comió", "comimos", "comisteis", "comieron"],
            "Futuro": ["comeré", "comerás", "comerá", "comeremos", "comeréis", "comerán"],
            "Subjuntivo presente": ["coma", "comas", "coma", "comamos", "comáis", "coman"],
        }
    },
    {
        "key": "vivir",
        "label": "3er grupo -IR: vivir (to live)",
        "conj": "3er grupo -IR",
        "tables": {
            "Presente": ["vivo", "vives", "vive", "vivimos", "vivís", "viven"],
            "Imperfecto": ["vivía", "vivías", "vivía", "vivíamos", "vivíais", "vivían"],
            "Pretérito": ["viví", "viviste", "vivió", "vivimos", "vivisteis", "vivieron"],
            "Futuro": ["viviré", "vivirás", "vivirá", "viviremos", "viviréis", "vivirán"],
            "Subjuntivo presente": ["viva", "vivas", "viva", "vivamos", "viváis", "vivan"],
        }
    },
]

IRREGULAR = [
    {
        "label": "ser (to be - identity) vs estar (to be - state/location)",
        "tables": {
            "ser Presente": ["soy", "eres", "es", "somos", "sois", "son"],
            "estar Presente": ["estoy", "estás", "está", "estamos", "estáis", "están"],
            "ser Imperfecto": ["era", "eras", "era", "éramos", "erais", "eran"],
            "estar Imperfecto": ["estaba", "estabas", "estaba", "estábamos", "estabais", "estaban"],
            "ser Pretérito": ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"],
            "estar Pretérito": ["estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron"],
            "ser Futuro": ["seré", "serás", "será", "seremos", "seréis", "serán"],
            "estar Futuro": ["estaré", "estarás", "estará", "estaremos", "estaréis", "estarán"],
            "ser Subjuntivo": ["sea", "seas", "sea", "seamos", "seáis", "sean"],
            "estar Subjuntivo": ["esté", "estés", "esté", "estemos", "estéis", "estén"],
        }
    },
    {
        "label": "tener (to have), haber (auxiliary), ir (to go)",
        "tables": {
            "tener Presente": ["tengo", "tienes", "tiene", "tenemos", "tenéis", "tienen"],
            "haber Presente": ["he", "has", "ha", "hemos", "habéis", "han"],
            "ir Presente": ["voy", "vas", "va", "vamos", "vais", "van"],
            "tener Pretérito": ["tuve", "tuviste", "tuvo", "tuvimos", "tuvisteis", "tuvieron"],
            "haber Pretérito": ["hube", "hubiste", "hubo", "hubimos", "hubisteis", "hubieron"],
            "ir Pretérito": ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"],
            "tener Futuro": ["tendré", "tendrás", "tendrá", "tendremos", "tendréis", "tendrán"],
            "ir Futuro": ["iré", "irás", "irá", "iremos", "iréis", "irán"],
            "Perfecto (haber + -ado/-ido)": ["he hablado", "has hablado", "ha hablado", "hemos hablado", "habéis hablado", "han hablado"],
        }
    },
    {
        "label": "hacer, poder, querer, venir — go verbs & stem changers",
        "tables": {
            "hacer Presente": ["hago", "haces", "hace", "hacemos", "hacéis", "hacen"],
            "poder Presente": ["puedo", "puedes", "puede", "podemos", "podéis", "pueden"],
            "querer Presente": ["quiero", "quieres", "quiere", "queremos", "queréis", "quieren"],
            "venir Presente": ["vengo", "vienes", "viene", "venimos", "venís", "vienen"],
            "hacer Pretérito": ["hice", "hiciste", "hizo", "hicimos", "hicisteis", "hicieron"],
            "poder Pretérito": ["pude", "pudiste", "pudo", "pudimos", "pudisteis", "pudieron"],
            "querer Futuro": ["querré", "querrás", "querrá", "querremos", "querréis", "querrán"],
        }
    },
]

# ─── HELPERS ────────────────────────────────────────────────────────────────
def strip_accents(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower().strip()

def normalize(s: str, ignore: bool) -> str:
    s = s.strip()
    if ignore:
        return strip_accents(s)
    return s.lower().strip()

def label(parent, text, **kw):
    kw.setdefault("bg", kw.get("bg", BG))
    kw.setdefault("fg", FG)
    return tk.Label(parent, text=text, **kw)

def save_progress(prog):
    try:
        with open(os.path.join(os.path.expanduser("~"), ".espanol_progress.json"), "w", encoding="utf-8") as f:
            json.dump(prog, f)
    except:
        pass

def load_progress():
    try:
        with open(os.path.join(os.path.expanduser("~"), ".espanol_progress.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def build_cards():
    cards = []
    for n in NOUNS:
        cards.append(dict(q=f"Gender of '{n['word']}' ({n['meaning']})?", a=n["gender"], type="noun", key=n["key"], group=n["group"], hint=f"{n['art_sg']} {n['word']} → {n['art_pl']} {n['plural']} — {n['note']}"))
        cards.append(dict(q=f"Plural of '{n['word']}'? ({n['art_sg']} {n['word']})", a=n["plural"], type="noun", key=n["key"], group="Plural", hint=n["note"]))
    for v in VERBS:
        for tense, forms in v["tables"].items():
            for idx, form in enumerate(forms[:6]):
                if not form or form.startswith("—"):
                    continue
                clean = form.split("/")[0].strip()
                q = f"{v['key']} — {tense} — {PERS[idx]}"
                cards.append(dict(q=q, a=clean, type="verb", key=v["key"], group=tense, hint=v["label"]))
    for irr in IRREGULAR:
        for tense, forms in irr["tables"].items():
            for idx, form in enumerate(forms[:6]):
                if not form or form.startswith("—"):
                    continue
                if "/" in form:
                    form = form.split("/")[0].strip()
                pers = PERS[idx] if idx < len(PERS) else ""
                base = irr["label"].split()[0]
                q = f"{base} — {tense} {pers}"
                cards.append(dict(q=q, a=form, type="irr", hint=irr["label"]))
    return cards

# ─── SCROLLABLE FRAME ───────────────────────────────────────────────────────
class Scroll(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BG, **kw)
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0, bd=0)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")
        self.inner = tk.Frame(self.canvas, bg=BG)
        self.win = self.canvas.create_window((0,0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.win, width=e.width))

def scrolled(builder):
    def wrapper(parent):
        s = Scroll(parent)
        builder(s.inner)
        return s
    return wrapper

# ─── TABLE WIDGETS ──────────────────────────────────────────────────────────
def noun_table(parent, noun):
    wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    wrap.pack(fill="x", pady=8)
    header = tk.Frame(wrap, bg=HEAD_BG)
    header.pack(fill="x")
    label(header, f"{noun['title']} — {noun['word']} ({noun['meaning']})", font=F_H2, fg=GOLD, bg=HEAD_BG).pack(side="left", padx=12, pady=8)
    label(header, f"{noun['gender']} · {noun['art_sg']} {noun['word']} → {noun['art_pl']} {noun['plural']}", font=F_SMALL, fg=DIM, bg=HEAD_BG).pack(side="right", padx=12)

    grid = tk.Frame(wrap, bg=PANEL)
    grid.pack(fill="x", padx=1, pady=1)
    headers = ["", "Singular", "Plural"]
    for col, txt in enumerate(headers):
        l = tk.Label(grid, text=txt, font=F_BOLD, fg=DIM, bg=ROW_B, bd=0, padx=10, pady=6)
        l.grid(row=0, column=col, sticky="ew", padx=1, pady=1)
    grid.columnconfigure(1, weight=1)
    grid.columnconfigure(2, weight=1)

    for i, (lbl, sg, pl) in enumerate([
        ("Definido (the)", f"{noun['art_sg']} {noun['word']}", f"{noun['art_pl']} {noun['plural']}"),
        ("Indefinido (a/some)", f"{'un' if noun['gender']=='masculine' else 'una'} {noun['word']}", f"{'unos' if noun['gender']=='masculine' else 'unas'} {noun['plural']}"),
        ("Con preposición", f"del {noun['word']} (de+el)", f"a los {noun['plural']}"),
    ]):
        bg = ROW_A if i%2==0 else ROW_B
        tk.Label(grid, text=lbl, font=F_BOLD, fg=FG, bg=bg, padx=10, pady=6).grid(row=i+1, column=0, sticky="ew", padx=1, pady=1)
        tk.Label(grid, text=sg, font=F_BODY, fg=GOLD, bg=bg, padx=10, pady=6).grid(row=i+1, column=1, sticky="ew", padx=1, pady=1)
        tk.Label(grid, text=pl, font=F_BODY, fg=GOLD, bg=bg, padx=10, pady=6).grid(row=i+1, column=2, sticky="ew", padx=1, pady=1)

    if noun["note"]:
        label(wrap, f"Note: {noun['note']}", font=F_SMALL, fg=DIM, bg=PANEL, wraplength=900, justify="left", anchor="w").pack(fill="x", padx=12, pady=6)

def verb_table(parent, verb):
    wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    wrap.pack(fill="x", pady=8)
    header = tk.Frame(wrap, bg=HEAD_BG)
    header.pack(fill="x")
    label(header, verb["label"], font=F_H2, fg=GOLD, bg=HEAD_BG).pack(side="left", padx=12, pady=8)
    label(header, verb["conj"], font=F_SMALL, fg=DIM, bg=HEAD_BG).pack(side="right", padx=12)

    for tense, forms in verb["tables"].items():
        tcol = GOLD
        tl = tense.lower()
        if "presente" in tl: tcol = TCOL["pres"]
        elif "pretérito" in tl or "pretérito" in tl: tcol = TCOL["pret"]
        elif "imperfecto" in tl: tcol = TCOL["impf"]
        elif "futuro" in tl: tcol = TCOL["fut"]
        elif "condicional" in tl: tcol = TCOL["cond"]
        elif "subjuntivo" in tl: tcol = TCOL["subj"]
        elif "imperativo" in tl: tcol = TCOL["imp"]

        tframe = tk.Frame(wrap, bg=PANEL)
        tframe.pack(fill="x", padx=8, pady=(10,2))
        tk.Frame(tframe, bg=tcol, width=4).pack(side="left", fill="y", padx=(0,8))
        label(tframe, tense, font=F_BOLD, fg=tcol, bg=PANEL).pack(side="left")

        grid = tk.Frame(wrap, bg=PANEL)
        grid.pack(fill="x", padx=12, pady=2)
        for idx, form in enumerate(forms):
            if idx >= 6: continue
            r = idx // 3
            c = idx % 3
            if form.startswith("—"): continue
            cell = tk.Frame(grid, bg=ROW_A if r%2==0 else ROW_B, bd=1, relief="flat")
            cell.grid(row=r, column=c, sticky="ew", padx=2, pady=2)
            grid.columnconfigure(c, weight=1)
            pers = PERS_SHORT[idx]
            label(cell, pers, font=F_SMALL, fg=DIM, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(4,0))
            label(cell, form, font=F_BODY, fg=FG, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(0,6))

# ─── PAGES ──────────────────────────────────────────────────────────────────
def page_overview(parent):
    tk.Label(parent, text="ESPAÑOL", font=F_TITLE, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(20,4))
    tk.Label(parent, text="Spanish Studio — gender, articles & verb tenses color-coded.", font=(SERIF, 14, "italic"), fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,20))

    card_wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    card_wrap.pack(fill="x", padx=20, pady=8)
    tk.Label(card_wrap, text="Género y Número — color code", font=F_H2, fg=GOLD, bg=PANEL).pack(anchor="w", padx=12, pady=8)
    for i, (gender, art, rule, ex) in enumerate(GENDER_USE):
        row = tk.Frame(card_wrap, bg=ROW_A if i%2==0 else ROW_B)
        row.pack(fill="x", padx=1, pady=1)
        tk.Frame(row, bg=CASE_COL[i], width=5).pack(side="left", fill="y")
        tk.Label(row, text=["Masc.","Fém.","Pl."][i], font=F_BOLD, fg=CASE_COL[i], bg=row["bg"], width=6).pack(side="left", padx=8, pady=8)
        tk.Label(row, text=f"{gender} — {art}", font=F_BODY, fg=FG, bg=row["bg"]).pack(side="left")
        tk.Label(row, text=f"· {rule} · {ex}", font=F_SMALL, fg=DIM, bg=row["bg"], wraplength=500, justify="left").pack(side="left", padx=12)

    for title, txt in [
        ("Español en 20 segundos", "No hay declinaciones como en latín. Sustantivos tienen género (masculino/femenino) + número. Artículos: el/la/los/las (the), un/una/unos/unas (a/some). Adjetivos concuerdan: negro/negra/negros/negras. Verbos: 3 grupos -AR (hablar, 50%), -ER (comer), -IR (vivir). Dos verbos para 'to be': ser (identidad) vs estar (estado/lugar). Pretérito vs Imperfecto: acción completa vs habitual."),
        ("Tiempos clave", "Presente (hablo), Pretérito (hablé = I spoke once), Imperfecto (hablaba = used to speak / was speaking), Futuro (hablaré = will), Condicional (hablaría = would), Subjuntivo (que hable = that I speak), Perfecto (he hablado = have spoken), Imperativo (¡habla!)."),
        ("Por qué colores?", "Azul = Masculino, Rosa = Femenino, Verde = Plural. Verbos: Amarillo Presente, Rojo Pretérito, Turquesa Imperfecto, Azul Futuro, Verde Condicional, Naranja Subjuntivo — mismos colores en guía, flashcards, worksheet."),
        ("Pronunciación básica", "J = /x/ fuerte: Juan /xwan/. LL = /ʝ/ o /ʎ/: calle. Ñ = /ɲ/: niño. RR = vibrante: perro vs pero. B/V = /b/ (betacismo). H muda. Tilde: el acento indica sílaba tónica: árbol, canción, fácil. Interrogación y exclamación: ¿Qué? ¡Hola!"),
    ]:
        c = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        c.pack(fill="x", padx=20, pady=6)
        tk.Label(c, text=title, font=F_H2, fg=GOLD, bg=PANEL).pack(anchor="w", padx=12, pady=(8,2))
        tk.Label(c, text=txt, font=F_BODY, fg=FG, bg=PANEL, wraplength=900, justify="left").pack(anchor="w", padx=12, pady=(0,10))

def page_alphabet(parent):
    tk.Label(parent, text="Alfabeto y Pronunciación", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    wrap.pack(fill="x", padx=20, pady=8)
    txt = """
Alfabeto: a b c d e f g h i j k l m n ñ o p q r s t u v w x y z + ch, ll (ya no oficiales)

Vocales: a /a/, e /e/, i /i/, o /o/, u /u/ — siempre puras, nunca diptongadas como en inglés.
Consonantes:
b/v = /b/ (betacismo): beber /beber/, votar /botar/ — b fuerte al inicio, suave entre vocales.
c: ca /ka/ casa, ce/ci /θe/ (España) o /se/ (LatAm): cena /θena/~/sena/
g: ga /ga/ gato, ge/gi /xe/~/he/: gente /xente/
j: /x/ fuerte: Juan /xwan/, trabajo /trabaxo/
h muda: hombre /ombre/, hablar /ablar/
ll: /ʝ/ ~ /dʒ/ ~ /ʎ/: calle /kaʝe/
ñ: /ɲ/: niño /niɲo/, año /aɲo/
r: suave /ɾ/ pero, fuerte /r/ perro, inicial /r/ Ramón
rr: siempre fuerte /r/: perro, arriba
y: /ʝ/ y /i/: yo /ʝo/, y (and) /i/
z: /θ/ España, /s/ LatAm: zapato /θapato/~/sapato/

Acento ortográfico:
- Palabras agudas (última sílaba): tilde si terminan en vocal, n, s: canción, sofá, inglés
- Llanas (penúltima): tilde si NO terminan en vocal, n, s: árbol, fácil, lápiz
- Esdrújulas siempre con tilde: pájaro, teléfono, sábado
- Interrogativos/exclamativos siempre tilde: qué, quién, dónde, cuándo, cómo

Signos: ¿? ¡! al inicio y final: ¿Cómo estás? ¡Hola!

Pretérito vs Imperfecto (CRITICAL):
Pretérito (acción completa): Ayer hablé con Juan (once), Comí a las 2 (finished)
Imperfecto (hábito/fondo): Cuando era niño, jugaba (used to), Hacía sol cuando salí (was sunny)
"""
    tk.Label(wrap, text=txt.strip(), font=F_BODY, fg=FG, bg=PANEL, justify="left", wraplength=850).pack(padx=12, pady=10)

def page_nouns(parent):
    tk.Label(parent, text="Sustantivos y Artículos", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    tk.Label(parent, text="Oro = artículo + terminación. Aprende sustantivo CON artículo: el gato, no solo gato.", font=F_SMALL, fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,10))
    for n in NOUNS:
        noun_table(parent, n)

def page_adjectives(parent):
    tk.Label(parent, text="Adjetivos", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    for adj in ADJECTIVES:
        wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        wrap.pack(fill="x", padx=20, pady=8)
        tk.Label(wrap, text=adj["title"], font=F_H2, fg=GOLD, bg=HEAD_BG).pack(fill="x", padx=12, pady=8)
        for row in adj["table"]:
            r = tk.Frame(wrap, bg=PANEL)
            r.pack(fill="x", padx=8, pady=1)
            for cell in row:
                tk.Label(r, text=cell, font=F_BODY, fg=FG, bg=ROW_A, width=22, padx=6, pady=4, bd=1, relief="flat").pack(side="left", padx=1)
        tk.Label(wrap, text=adj["note"], font=F_SMALL, fg=DIM, bg=PANEL, wraplength=900, justify="left").pack(anchor="w", padx=12, pady=6)

def page_pronouns(parent):
    tk.Label(parent, text="Pronombres y Artículos", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    for pr in PRONOUNS:
        wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        wrap.pack(fill="x", padx=20, pady=8)
        tk.Label(wrap, text=pr["title"], font=F_H2, fg=GOLD, bg=HEAD_BG).pack(fill="x", padx=12, pady=8)
        for row in pr["forms"]:
            r = tk.Frame(wrap, bg=PANEL)
            r.pack(fill="x", padx=8, pady=1)
            for cell in row:
                tk.Label(r, text=cell, font=F_BODY, fg=FG, bg=ROW_A, width=20, padx=6, pady=4, bd=1, relief="flat").pack(side="left", padx=1)

def page_verbs(parent):
    tk.Label(parent, text="Verbos — 3 Conjugaciones", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    tk.Label(parent, text="Amarillo Presente, Turquesa Imperfecto, Rojo Pretérito, Azul Futuro, Verde Condicional, Naranja Subjuntivo.", font=F_SMALL, fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,10))
    for v in VERBS:
        verb_table(parent, v)

def page_irregular(parent):
    tk.Label(parent, text="Verbos Irregulares — ser/estar/haber/ir/hacer", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    tk.Label(parent, text="¡Ser y estar son diferentes! Ser = identidad, Estar = estado/lugar.", font=F_SMALL, fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,10))
    for irr in IRREGULAR:
        wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        wrap.pack(fill="x", padx=20, pady=8)
        tk.Label(wrap, text=irr["label"], font=F_H2, fg=GOLD, bg=HEAD_BG).pack(fill="x", padx=12, pady=8)
        for tense, forms in irr["tables"].items():
            tframe = tk.Frame(wrap, bg=PANEL)
            tframe.pack(fill="x", padx=12, pady=4)
            tcol = GOLD
            tl = tense.lower()
            if "presente" in tl: tcol = TCOL["pres"]
            elif "pretérito" in tl: tcol = TCOL["pret"]
            elif "imperfecto" in tl: tcol = TCOL["impf"]
            elif "futuro" in tl: tcol = TCOL["fut"]
            elif "condicional" in tl: tcol = TCOL["cond"]
            elif "subjuntivo" in tl: tcol = TCOL["subj"]
            tk.Label(tframe, text=tense, font=F_BOLD, fg=tcol, bg=PANEL).pack(anchor="w")
            grid = tk.Frame(wrap, bg=PANEL)
            grid.pack(fill="x", padx=12, pady=2)
            for idx, form in enumerate(forms):
                if idx >= len(PERS_SHORT): continue
                if form.startswith("—"): continue
                cell = tk.Frame(grid, bg=ROW_A, bd=1, relief="flat")
                cell.grid(row=idx//3, column=idx%3, sticky="ew", padx=2, pady=2)
                grid.columnconfigure(idx%3, weight=1)
                tk.Label(cell, text=PERS_SHORT[idx], font=F_SMALL, fg=DIM, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(4,0))
                tk.Label(cell, text=form, font=F_BODY, fg=FG, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(0,6))

def page_reference(parent):
    tk.Label(parent, text="Referencia — Chuleta", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    ref = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    ref.pack(fill="x", padx=20, pady=8)
    txt = """
ARTÍCULOS:
Definido: el (m), la (f), los (m pl), las (f pl) = the
Indefinido: un (m), una (f), unos (m pl), unas (f pl) = a/some
Contracciones: al (a+el), del (de+el)
Neutro: lo + adj = lo bueno, lo importante = what is good/important

SUSTANTIVOS:
Regular: -o masc (gato), -a fem (casa) — but la mano (f), el día/mapa (m)
Cons → -es pl: árbol→árboles, pared→paredes, lápiz→lápices (z→c)
-és/-án/-ón/-or + -a fem: español→española, actor→actriz

ADJETIVOS:
-o/-a: negro/negra/negros/negras — must agree!
-e / consonante: same m/f sg: grande/grande, fácil/fácil → pl -es: grandes, fáciles
Posición: usually AFTER noun: casa blanca, coche rojo. Before: buen/mal/gran + meaning change.
Comparación: más...que, menos...que, tan...como. Irregular: bueno→mejor, malo→peor, grande→mayor, pequeño→menor.
Superlativo: -ísimo: buenísimo, altísimo, facilísimo OR el más...: el más alto, el mejor

VERBOS -AR/-ER/-IR ENDINGS:
Presente:
 -AR: -o, -as, -a, -amos, -áis, -an (hablo, hablas, habla...)
 -ER: -o, -es, -e, -emos, -éis, -en (como, comes, come...)
 -IR: -o, -es, -e, -imos, -ís, -en (vivo, vives, vive, vivimos...)

Imperfecto:
 -AR: -aba, -abas, -aba, -ábamos, -abais, -aban
 -ER/-IR: -ía, -ías, -ía, -íamos, -íais, -ían

Pretérito (indefinido):
 -AR: -é, -aste, -ó, -amos, -asteis, -aron (hablé, hablaste...)
 -ER/-IR: -í, -iste, -ió, -imos, -isteis, -ieron (comí, comiste, comió...)

Futuro: infinitive + -é, -ás, -á, -emos, -éis, -án (hablaré, comeré, viviré)

Ser vs Estar (CRITICAL):
Ser = identity, origin, profession, time, material: Soy español, Es de madera, Son las tres, Es médico
Estar = location, state, emotion, temporary: Estoy en casa, Estoy cansado, Está roto, Está en la mesa
Ser: soy, eres, es, somos, sois, son | Estar: estoy, estás, está, estamos, estáis, están

Haber vs Tener:
Haber = auxiliary for perfecto: he, has, ha, hemos, habéis, han + hablado/comido/vivido
Tener = to have (possession): tengo, tienes, tiene...
Hay = there is/are (impersonal haber): Hay un libro, Hay muchos.

Pronombres objeto: me/te/lo/la/nos/os/los/las + le/les (indirect) + se (reflexivo)
Orden: Me lo da (gives it to me), Se lo digo (I tell it to him), ¡Dámelo! (give it to me!)
Negación: no + verbo: No hablo, No tengo nada, No veo a nadie, Nunca como.

Preguntas: ¿Qué? ¿Quién? ¿Dónde? ¿Cuándo? ¿Cómo? ¿Por qué? ¿Cuánto?
"""
    tk.Label(ref, text=txt.strip(), font=("Courier New", 11), fg=FG, bg=PANEL, justify="left", anchor="w").pack(fill="x", padx=12, pady=10)

def page_memory(parent):
    tk.Label(parent, text="Memory Aids", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    aids = [
        ("Género: el/la Trick", "Aprende SIEMPRE con artículo: el gato, la casa, el problema (¡masc!), la mano (¡fem!). Reglas: -ción/-sión/-dad/-tad/-tud siempre fem: canción, ciudad, virtud. -ma griego masc: problema, sistema, tema, programa, idioma, clima."),
        ("Plural Chant", "Un gato → dos gatos | Un árbol → dos árboles (-es) | Un lápiz → dos lápices (z→c + tilde) | El agua → las aguas (fem but el in sg). Di 3x en voz alta."),
        ("Adjetivo Concordancia", "El gato negro, La casa negra, Los gatos negros, Las casas negras. -o→-a, -os→-as. Para -e/cons: fácil→fáciles, grande→grandes. ¡El adjetivo SIEMPRE concuerda con el sustantivo!"),
        ("Ser vs Estar – DOCTOR vs PLACE", "Ser = DOCTOR: Description, Origin, Characteristic, Time, Occupation, Relation. Estar = PLACE: Position, Location, Action (progressive), Condition, Emotion. Soy español (origin), Estoy en Madrid (location), Soy alto (characteristic), Estoy cansado (condition)."),
        ("Presente -AR Chant", "Hablo, hablas, habla, hablamos, habláis, hablan — -o, -as, -a, -amos, -áis, -an. Canta la canción de Despacito con conjugaciones."),
        ("Pretérito vs Imperfecto", "Pretérito = foto (acción completa): Ayer comí paella, Llegué a las 8. Imperfecto = película (fondo/hábito): Cuando era niño, comía mucho, Hacía sol cuando salí. ¡Clave para sonar nativo!"),
        ("Irregulares Clave – Tener", "Tener: tengo, tienes, tiene, tenemos, tenéis, tienen — go verb (g). Pretérito: tuve, tuviste, tuvo... Futuro: tendré. Usos: tener hambre/sed/frío/calor/miedo/sueño/años — ¡no estar!"),
        ("Go Verbs & Stem Changers", "Go verbs: tengo, vengo, salgo, pongo, hago, traigo, digo, oigo. e→ie: quiero, quieres, quiere, queremos (o→nosotros/vosotros no cambia), queréis, quieren. o→ue: puedo, duermo, juego. e→i: pido, pides, pide."),
        ("Subjuntivo Trigger", "¡Que + subjuntivo después de querer, necesitar, es importante que, ojalá, para que, sin que, antes de que! Quiero que vengas, Es necesario que hables, Ojalá que llueva. Presente: hable, hables, hable, hablemos, habléis, hablen."),
    ]
    for title, txt in aids:
        c = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        c.pack(fill="x", padx=20, pady=6)
        tk.Label(c, text=title, font=F_H2, fg=GOLD, bg=PANEL).pack(anchor="w", padx=12, pady=(8,2))
        tk.Label(c, text=txt, font=F_BODY, fg=FG, bg=PANEL, wraplength=850, justify="left").pack(anchor="w", padx=12, pady=(0,10))

# ─── STUDY PAGES ────────────────────────────────────────────────────────────
class StudyPage(tk.Frame):
    def __init__(self, parent, app, mode="flash"):
        super().__init__(parent, bg=BG)
        self.app = app
        self.mode = mode
        self.cards = app.cards[:]
        random.shuffle(self.cards)
        self.idx = 0
        self.score = 0
        self.total = 0
        self.current = None
        self.showing = False

        top = tk.Frame(self, bg=HEAD_BG, height=56)
        top.pack(fill="x")
        tk.Label(top, text="Flashcards" if mode=="flash" else "Type-in Drill", font=F_H2, fg=GOLD, bg=HEAD_BG).pack(side="left", padx=16, pady=12)
        self.score_lbl = tk.Label(top, text="0/0", font=F_SMALL, fg=DIM, bg=HEAD_BG)
        self.score_lbl.pack(side="right", padx=16)
        self.opt_var = tk.BooleanVar(value=app.opts.get("ignore", True))
        tk.Checkbutton(top, text="Ignore accents", variable=self.opt_var, bg=HEAD_BG, fg=DIM, selectcolor=PANEL2, activebackground=HEAD_BG, command=self.toggle_ignore).pack(side="right", padx=8)

        self.q_frame = tk.Frame(self, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        self.q_frame.pack(fill="x", padx=20, pady=20)

        self.q_lbl = tk.Label(self.q_frame, text="", font=(SERIF, 22), fg=FG, bg=PANEL, wraplength=800, justify="left")
        self.q_lbl.pack(anchor="w", padx=20, pady=(20,8))
        self.hint_lbl = tk.Label(self.q_frame, text="", font=F_SMALL, fg=DIM, bg=PANEL, wraplength=800, justify="left")
        self.hint_lbl.pack(anchor="w", padx=20, pady=(0,8))
        self.a_lbl = tk.Label(self.q_frame, text="", font=(SERIF, 20, "bold"), fg=GOLD, bg=PANEL)
        self.a_lbl.pack(anchor="w", padx=20, pady=(0,20))

        if mode == "flash":
            btn_row = tk.Frame(self, bg=BG)
            btn_row.pack(fill="x", padx=20, pady=10)
            for txt, col, cmd in [("Show / Hide (Space)", PANEL2, self.flip), ("Again (1)", "#ff6b7d", lambda: self.rate(False)), ("Good (3)", "#6fcf8f", lambda: self.rate(True)), ("Next →", GOLD, self.next_card)]:
                b = tk.Label(btn_row, text=txt, bg=col, fg=FG if col!=GOLD else BG, font=F_BTN, padx=16, pady=10, cursor="hand2", bd=0)
                b.pack(side="left", padx=6)
                b.bind("<Button-1>", lambda e, c=cmd: c())
        else:
            entry_row = tk.Frame(self, bg=BG)
            entry_row.pack(fill="x", padx=20, pady=10)
            self.entry = tk.Entry(entry_row, font=(SERIF, 18), bg=PANEL2, fg=FG, insertbackground=FG, relief="flat", bd=0)
            self.entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0,10))
            self.entry.bind("<Return>", lambda e: self.check())
            b = tk.Label(entry_row, text="Check (Enter)", bg=GOLD, fg=BG, font=F_BTN, padx=18, pady=10, cursor="hand2")
            b.pack(side="left")
            b.bind("<Button-1>", lambda e: self.check())
            self.feedback = tk.Label(self, text="", font=F_BODY, fg=FG, bg=BG)
            self.feedback.pack(anchor="w", padx=20, pady=6)

        self.next_card()

    def toggle_ignore(self):
        self.app.opts["ignore"] = self.opt_var.get()

    def next_card(self):
        if not self.cards:
            self.q_lbl.config(text="No cards!"); return
        self.current = self.cards[self.idx % len(self.cards)]
        self.idx += 1
        self.showing = False
        self.q_lbl.config(text=self.current["q"])
        self.hint_lbl.config(text=self.current.get("hint",""))
        self.a_lbl.config(text="")
        if hasattr(self, "entry"):
            self.entry.delete(0, tk.END)
            self.entry.focus()
            self.feedback.config(text="")
        self.score_lbl.config(text=f"{self.score}/{self.total}")

    def flip(self):
        if not self.current: return
        self.showing = not self.showing
        self.a_lbl.config(text=self.current["a"] if self.showing else "")

    def rate(self, good):
        self.total += 1
        if good: self.score += 1
        if good:
            self.cards.append(self.current)
        else:
            self.cards.insert(min(5, len(self.cards)), self.current)
        self.next_card()

    def check(self):
        if not self.current: return
        user = self.entry.get()
        if not user: return
        exp = self.current["a"]
        ok = normalize(user, self.app.opts.get("ignore", True)) == normalize(exp, self.app.opts.get("ignore", True))
        self.total += 1
        if ok:
            self.score += 1
            self.feedback.config(text=f"✓ Correct! {exp}", fg=GREEN)
        else:
            self.feedback.config(text=f"✗ Expected {exp} — you typed {user}", fg=RED)
        self.score_lbl.config(text=f"{self.score}/{self.total}")
        self.after(1200, self.next_card)

    def on_key(self, e):
        if e.keysym == "space" and self.mode=="flash":
            self.flip()
        elif e.keysym in ("1","2"):
            self.rate(False)
        elif e.keysym in ("3","4"):
            self.rate(True)
        elif e.keysym == "Right":
            self.next_card()

class WorksheetPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        top = tk.Frame(self, bg=HEAD_BG)
        top.pack(fill="x")
        tk.Label(top, text="Worksheet — Fill the endings (Spanish)", font=F_H2, fg=GOLD, bg=HEAD_BG).pack(side="left", padx=16, pady=12)
        tk.Label(top, text="Type Spanish. Gold = to memorize. Accents matter!", font=F_SMALL, fg=DIM, bg=HEAD_BG).pack(side="left", padx=12)

        self.scroll = Scroll(self)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=12)

        self.entries = []

        def section(title):
            tk.Label(self.scroll.inner, text=title, font=F_H2, fg=GOLD, bg=BG).pack(anchor="w", pady=(20,6))

        def make_noun_block(noun):
            section(f"{noun['title']} — {noun['word']} ({noun['meaning']})")
            grid = tk.Frame(self.scroll.inner, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
            grid.pack(fill="x", pady=4)
            hdr = tk.Frame(grid, bg=HEAD_BG)
            hdr.pack(fill="x")
            for txt in ["Forma", "Singular", "Plural"]:
                tk.Label(hdr, text=txt, font=F_SMALL, fg=DIM, bg=HEAD_BG, width=24).pack(side="left", padx=8, pady=6)
            for i, (lbl, sg, pl) in enumerate([
                ("Con artículo definido", f"{noun['art_sg']} {noun['word']}", f"{noun['art_pl']} {noun['plural']}"),
                ("Indefinido", f"{'un' if noun['gender']=='masculine' else 'una'} {noun['word']}", f"{'unos' if noun['gender']=='masculine' else 'unas'} {noun['plural']}"),
            ]):
                row = tk.Frame(grid, bg=ROW_A if i%2==0 else ROW_B)
                row.pack(fill="x", padx=1, pady=1)
                tk.Label(row, text=lbl, font=F_BOLD, fg=FG, bg=row["bg"], width=20).pack(side="left", padx=8, pady=8)
                for form in [sg, pl]:
                    cell = tk.Frame(row, bg=row["bg"])
                    cell.pack(side="left", fill="x", expand=True, padx=8, pady=4)
                    e = tk.Entry(cell, font=F_BODY, bg=PANEL2, fg=FG, relief="flat", bd=0, width=18)
                    e.pack(side="left", ipady=4, padx=4)
                    tk.Label(cell, text=f"→ {form}", font=F_SMALL, fg=DIM, bg=row["bg"]).pack(side="left", padx=6)
                    self.entries.append((e, form, form))

        for key in ["m_gato", "f_casa", "m_lapiz"]:
            n = next(x for x in NOUNS if x["key"]==key)
            make_noun_block(n)

        section("Verbos — Conjugación")
        for v in VERBS[:2]:
            wrap = tk.Frame(self.scroll.inner, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
            wrap.pack(fill="x", pady=6)
            tk.Label(wrap, text=v["label"], font=F_BOLD, fg=GOLD, bg=HEAD_BG).pack(fill="x", padx=12, pady=6)
            for tense in ["Presente", "Pretérito", "Futuro"]:
                if tense not in v["tables"]: continue
                t = tk.Frame(wrap, bg=PANEL)
                t.pack(fill="x", padx=12, pady=4)
                tk.Label(t, text=tense, font=F_SMALL, fg=GOLD, bg=PANEL).pack(anchor="w")
                grid = tk.Frame(wrap, bg=PANEL)
                grid.pack(fill="x", padx=12, pady=2)
                for idx, form in enumerate(v["tables"][tense]):
                    if form.startswith("—"): continue
                    cell = tk.Frame(grid, bg=ROW_A, bd=1, relief="flat")
                    cell.grid(row=idx//3, column=idx%3, sticky="ew", padx=2, pady=2)
                    grid.columnconfigure(idx%3, weight=1)
                    tk.Label(cell, text=PERS_SHORT[idx], font=F_SMALL, fg=DIM, bg=cell["bg"]).pack(anchor="w", padx=6, pady=(4,0))
                    e = tk.Entry(cell, font=F_BODY, bg=PANEL2, fg=FG, relief="flat", bd=0)
                    e.pack(fill="x", padx=6, pady=(2,6), ipady=4)
                    self.entries.append((e, form, form))

        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=20, pady=10)
        tk.Label(ctrl, text="Blank = not counted. Toggle Ignore accents to allow a/á same.", font=F_SMALL, fg=DIM, bg=BG).pack(side="left")
        def grade():
            correct=0; total=0
            for entry, expected, full in self.entries:
                user = entry.get().strip()
                total+=1
                if not user:
                    entry.config(bg=PANEL2); continue
                if normalize(user, self.app.opts.get("ignore",True)) == normalize(expected, self.app.opts.get("ignore",True)):
                    correct+=1; entry.config(bg="#1a2e1f")
                else:
                    entry.config(bg="#2e1a1a")
            messagebox.showinfo("Result", f"Score: {correct}/{total}\nGreen=correct, Red=check.")
        def clear_all():
            for e,_,_ in self.entries:
                e.delete(0, tk.END); e.config(bg=PANEL2)
        def export_html():
            path = os.path.join(os.path.expanduser("~"), "spanish_worksheet.html")
            html_rows = []
            for entry, expected, full in self.entries[:60]:
                html_rows.append(f"<tr><td><span class='b'></span></td><td>{html.escape(full)}</td></tr>")
            page = f"<!doctype html><meta charset='utf-8'><title>Spanish Worksheet</title><style>body{{font:16px Georgia;margin:40px}} table{{border-collapse:collapse}} td{{border:1px solid #bbb;padding:8px 14px}} .b{{display:inline-block;min-width:90px;border-bottom:1px solid #000}}</style><h1>Spanish Worksheet</h1><table>{''.join(html_rows)}</table>"
            try:
                with open(path,"w",encoding="utf-8") as f: f.write(page)
                webbrowser.open("file://"+path)
            except Exception as e:
                messagebox.showerror("Export failed", str(e))

        for txt,cmd in [("Grade ✓", grade), ("Clear", clear_all), ("Export HTML", export_html)]:
            b = tk.Label(ctrl, text=txt, bg=GOLD if "Grade" in txt else PANEL2, fg=BG if "Grade" in txt else FG, font=F_BTN, padx=16, pady=8, cursor="hand2")
            b.pack(side="right", padx=6)
            b.bind("<Button-1>", lambda e, c=cmd: c())

# ─── APP SHELL ──────────────────────────────────────────────────────────────
NAV = [("GUIDE", None),
       ("Overview", lambda p, a: scrolled(page_overview)(p)),
       ("Alphabet", lambda p, a: scrolled(page_alphabet)(p)),
       ("Nouns & Articles", lambda p, a: scrolled(page_nouns)(p)),
       ("Adjectives", lambda p, a: scrolled(page_adjectives)(p)),
       ("Pronouns", lambda p, a: scrolled(page_pronouns)(p)),
       ("Verbs", lambda p, a: scrolled(page_verbs)(p)),
       ("Irregular Verbs", lambda p, a: scrolled(page_irregular)(p)),
       ("Reference", lambda p, a: scrolled(page_reference)(p)),
       ("STUDY", None),
       ("Flashcards", lambda p, a: StudyPage(p, a, "flash")),
       ("Type-in Drill", lambda p, a: StudyPage(p, a, "type")),
       ("Worksheet", lambda p, a: WorksheetPage(p, a)),
       ("Memory Aids", lambda p, a: scrolled(page_memory)(p))]

ICONS = {"Overview":"✦","Alphabet":"ñ","Nouns & Articles":"Ⅰ","Adjectives":"Ⅱ","Pronouns":"Ⅲ","Verbs":"Ⅳ","Irregular Verbs":"Ⅴ","Reference":"§","Flashcards":"◈","Type-in Drill":"⌨","Worksheet":"✎","Memory Aids":"♪"}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Español · Grammar Studio — Enhanced (Spanish)")
        self.geometry("1280x860")
        self.minsize(1100, 720)
        self.configure(bg=BG)
        self.opts = {"ignore": True}
        self.prog = load_progress()
        self.cards = build_cards()
        self.pages, self.cur, self.navbtns = {}, None, {}

        head = tk.Frame(self, bg=HEAD_BG)
        head.pack(fill="x")
        label(head, "ESPAÑOL", fg=GOLD, font=F_TITLE, bg=HEAD_BG).pack(side="left", padx=(24,12), pady=(12,8))
        label(head, "Grammar Studio — Spanish · gender & conjugation · color-coded", fg=DIM, font=(SERIF, 14, "italic"), bg=HEAD_BG).pack(side="left", pady=(20,0))

        self.strip = tk.Canvas(self, height=4, bg=BG, highlightthickness=0)
        self.strip.pack(fill="x")
        self.strip.bind("<Configure>", self._strip)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)
        side = tk.Frame(body, bg=HEAD_BG, width=230)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        self.content = tk.Frame(body, bg=BG)
        self.content.pack(side="left", fill="both", expand=True, padx=(22,14), pady=(16,10))

        for name, builder in NAV:
            if builder is None:
                label(side, name, fg=DIM, font=(SANS, 10, "bold"), bg=HEAD_BG).pack(anchor="w", padx=20, pady=(18,4))
                continue
            b = tk.Label(side, text=f"  {ICONS.get(name,'·')}   {name}", anchor="w", fg=FG, bg=HEAD_BG, font=F_NAV, padx=14, pady=9, cursor="hand2")
            b.pack(fill="x")
            b.bind("<Button-1>", lambda e, n=name: self.show(n))
            b.bind("<Enter>", lambda e, n=name: self.navbtns[n].config(bg=PANEL2) if n != self.cur else None)
            b.bind("<Leave>", lambda e, n=name: self.navbtns[n].config(bg=HEAD_BG) if n != self.cur else None)
            self.navbtns[name] = b

        self.foot = label(self, "Tip: Ignore accents toggle in study modes. Space=show, 1=again, 3=good, → next. Learn nouns WITH el/la.", fg=DIM, font=F_SMALL, bg=HEAD_BG, anchor="w", padx=18, pady=5)
        self.foot.pack(fill="x", side="bottom")

        self.bind_all("<MouseWheel>", self._wheel)
        self.bind_all("<Button-4>", self._wheel)
        self.bind_all("<Button-5>", self._wheel)
        self.bind("<Key>", self._key)
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.show("Overview")

    def _strip(self, e):
        self.strip.delete("all")
        w = e.width / 6
        for i,c in enumerate(CASE_COL):
            self.strip.create_rectangle(i*w,0,(i+1)*w+1,4,fill=c,width=0)

    def show(self, name):
        if self.cur:
            self.pages[self.cur].pack_forget()
            self.navbtns[self.cur].config(bg=HEAD_BG, fg=FG)
        if name not in self.pages:
            builder = dict(NAV)[name]
            self.pages[name] = builder(self.content, self)
        self.pages[name].pack(fill="both", expand=True)
        self.navbtns[name].config(bg=PANEL2, fg=GOLD)
        self.cur = name

    def _wheel(self, e):
        w = self.winfo_containing(e.x_root, e.y_root)
        while w is not None:
            if isinstance(w, Scroll):
                if w.inner.winfo_reqheight() > w.canvas.winfo_height():
                    d = -1 if getattr(e,"num",0)==4 else 1 if getattr(e,"num",0)==5 else -e.delta if abs(e.delta)<30 else -int(e.delta/120)
                    w.canvas.yview_scroll(d,"units")
                return
            w = w.master

    def _key(self, e):
        try:
            if isinstance(self.focus_get(), (tk.Entry, ttk.Combobox)): return
        except: return
        page = self.pages.get(self.cur)
        if hasattr(page, "on_key"): page.on_key(e)

    def _close(self):
        save_progress(self.prog)
        self.destroy()

if __name__ == "__main__":
    App().mainloop()
