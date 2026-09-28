#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRANÇAIS · Grammar Studio - Enhanced Edition
============================================
Color-coded, all-inclusive French grammar guide with memorization engine.
Converted from Latin & Greek Studios — same fancy dark GUI, fully debugged.

GUIDE   Overview · Alphabet & Pronunciation · Nouns & Articles · Adjectives · Pronouns · Verbs · Irregular Verbs · Reference
STUDY   Flashcards (spaced repetition) · Type-in Drill · Worksheet · Memory Aids

Run: python3 French-Grammar-Studio-Enhanced.py
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

# ─── THEME (same as Latin/Greek Enhanced) ───────────────────────────────────
BG, PANEL, PANEL2 = "#11131b", "#1a1d2a", "#232739"
ROW_A, ROW_B, HEAD_BG, BORDER = "#1c1f2d", "#171a26", "#0d0f16", "#333955"
FG, DIM, GOLD, GREEN, RED = "#efe6d0", "#8e93ad", "#e0b458", "#6fcf8f", "#ff6b7d"

CASE_COL = ["#5fa8ff", "#ff8ab8", "#4fd1b5", "#f2c94c", "#c58af9", "#9bdc6a"]  # repurposed for gender/case
TCOL = {
    "pres": "#f2c94c",   # présent - yellow
    "impf": "#4fd1b5",   # imparfait - teal
    "fut": "#5fa8ff",    # futur - blue
    "pc": "#ff7a7a",     # passé composé - red
    "ps": "#c58af9",     # passé simple - purple
    "cond": "#9bdc6a",   # conditionnel - green
    "subj": "#ffb74d",   # subjonctif - orange
    "imp": "#ff8ab8",    # impératif - pink
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

# ─── FRENCH CORE DATA ───────────────────────────────────────────────────────
# French has no Latin-style declensions, but we keep 6-color system for gender/number + pronouns
GENDERS = ["Masculin", "Féminin", "Pluriel"]
GENDER_ABBR = ["Masc.", "Fém.", "Plur."]
GENDER_USE = [
    ("Masculin", "le / un", "Masculine nouns, adjectives in -∅", "le chat noir — the black cat (m)"),
    ("Féminin", "la / une", "Feminine nouns, adjectives in -e", "la maison blanche — the white house (f)"),
    ("Pluriel", "les / des", "Plural -s (usually silent), x for -eau/-al", "les chevaux noirs — the black horses"),
]

PERS = ["je (I)", "tu (you)", "il/elle (he/she)", "nous (we)", "vous (you pl/formal)", "ils/elles (they)"]
PERS_SHORT = ["je", "tu", "il/elle", "nous", "vous", "ils/elles"]

def _n(key, group, title, gender, word, meaning, art_sg, art_pl, plural, note=""):
    return dict(key=key, group=group, title=title, gender=gender, word=word,
                meaning=meaning, art_sg=art_sg, art_pl=art_pl, plural=plural, note=note)

NOUNS = [
    _n("m_chat", "Masc - regular", "Masc. regular - chat", "masculine", "chat", "cat", "le", "les", "chats",
       note="Most masc: -∅ → -s pl. le chat / les chats. -e? le livre (masc despite -e)."),
    _n("f_maison", "Fém - regular", "Fém. regular - maison", "feminine", "maison", "house", "la", "les", "maisons",
       note="Most fém: -e, -ion, -ure. la maison / les maisons."),
    _n("m_livre", "Masc - e ending", "Masc. tricky -e: livre", "masculine", "livre", "book", "le", "les", "livres",
       note="le livre is masc despite -e! Learn gender with article: le/un vs la/une."),
    _n("f_table", "Fém - e ending", "Fém. -e: table", "feminine", "table", "table", "la", "les", "tables",
       note="la table — regular fem."),
    _n("m_cheval", "Masc -al → -aux", "Masc. irregular pl -al → -aux", "masculine", "cheval", "horse", "le", "les", "chevaux",
       note="7 in -al: cheval → chevaux, journal → journaux, hôpital → hôpitaux. Most -al regular: festival → festivals."),
    _n("m_bateau", "Masc -eau → -eaux", "Masc. -eau → -eaux", "masculine", "bateau", "boat", "le", "les", "bateaux",
       note="All -eau, -eu, -au → -x: bateau→bateaux, jeu→jeux, chapeau→chapeaux. -ou: 7 in -oux: bijou, caillou, chou, genou, hibou, joujou, pou."),
    _n("f_eau", "Fém -eau", "Fém. eau (f but -eau)", "feminine", "eau", "water", "l'", "les", "eaux",
       note="l'eau (fém!) — elision before vowel: le/la → l'. l'ami, l'eau, l'école."),
    _n("m_ami", "Masc - vowel", "Masc. elision - ami", "masculine", "ami", "friend", "l'", "les", "amis",
       note="Elision: le/la → l' before vowel/h muet: l'ami, l'homme (h muet), but le héros (h aspiré, no elision)."),
]

ADJECTIVES = [
    {
        "title": "Regular: noir, -e, -s, -es (black)",
        "type": "regular",
        "table": [
            ["", "Masc sg", "Fém sg", "Masc pl", "Fém pl"],
            ["noir", "noir", "noire", "noirs", "noires"],
            ["petit (small)", "petit", "petite", "petits", "petites"],
            ["grand (big)", "grand", "grande", "grands", "grandes"],
            ["français (French)", "français", "française", "français", "françaises"],
        ],
        "note": "Rule: Masc + -e = Fém, + -s = Pl, Fém pl -es. Spoken: noir /nwaʁ/ = noire /nwaʁ/ same, but petit/petite different."
    },
    {
        "title": "Irregular: beau, nouveau, vieux + position",
        "type": "irregular",
        "table": [
            ["", "Masc sg", "Masc before vowel", "Fém sg", "Masc pl", "Fém pl"],
            ["beau (beautiful)", "beau", "bel", "belle", "beaux", "belles"],
            ["nouveau (new)", "nouveau", "nouvel", "nouvelle", "nouveaux", "nouvelles"],
            ["vieux (old)", "vieux", "vieil", "vieille", "vieux", "vieilles"],
            ["bon (good)", "bon", "bon", "bonne", "bons", "bonnes"],
        ],
        "note": "BAGS: Beauty, Age, Goodness, Size go BEFORE noun: un grand homme vs un homme grand (big man vs tall man). Most adj AFTER."
    },
    {
        "title": "Comparison: plus...que, superlative",
        "type": "comparison",
        "table": [
            ["", "Positive", "Comparative", "Superlative"],
            ["grand", "grand", "plus grand que", "le plus grand"],
            ["bon", "bon", "meilleur que", "le meilleur"],
            ["mauvais", "mauvais", "pire / plus mauvais que", "le pire / le plus mauvais"],
            ["petit", "petit", "plus petit / moindre que", "le plus petit / le moindre"],
        ],
        "note": "Adverbs: bien → mieux → le mieux. beaucoup → plus → le plus. Superlative with le/la/les + plus/moins."
    },
]

PRONOUNS = [
    {"title": "Articles: défini, indéfini, partitif", "forms": [
        ["", "Masc sg", "Fém sg", "Pluriel"],
        ["Défini (the)", "le / l'", "la / l'", "les"],
        ["Indéfini (a/some)", "un", "une", "des"],
        ["Partitif (some)", "du (de+le)", "de la / de l'", "des"],
        ["Négation", "de / d'", "de / d'", "de / d'"],
        ["Ex: Je veux", "du pain (some bread)", "de l'eau", "des pommes"],
    ]},
    {"title": "Personal Pronouns — subject, direct, indirect, disjunctive", "forms": [
        ["", "Sujet", "COD (le/la/les)", "COI (lui/leur)", "Tonique (moi)"],
        ["je", "je", "me", "me", "moi"],
        ["tu", "tu", "te", "te", "toi"],
        ["il/elle", "il/elle", "le/la", "lui", "lui/elle"],
        ["nous", "nous", "nous", "nous", "nous"],
        ["vous", "vous", "vous", "vous", "vous"],
        ["ils/elles", "ils/elles", "les", "leur", "eux/elles"],
    ]},
    {"title": "Possessive & Demonstrative & Relative", "forms": [
        ["", "Masc sg", "Fém sg", "Pl"],
        ["mon (my)", "mon", "ma (mon before vowel)", "mes"],
        ["ton (your)", "ton", "ta", "tes"],
        ["son (his/her)", "son", "sa", "ses"],
        ["ce (this/that)", "ce / cet (+vowel)", "cette", "ces"],
        ["qui (who/that subj)", "qui", "qui", "qui"],
        ["que (whom/that obj)", "que / qu'", "que", "que"],
        ["où / dont", "où (where)", "dont (whose/of which)", "lequel/laquelle"],
    ]},
]

VERBS = [
    {
        "key": "parler",
        "label": "1er groupe -ER: parler (to speak) — 90% of verbs!",
        "conj": "1er groupe",
        "tables": {
            "Présent": ["parle", "parles", "parle", "parlons", "parlez", "parlent"],
            "Imparfait": ["parlais", "parlais", "parlait", "parlions", "parliez", "parlaient"],
            "Futur simple": ["parlerai", "parleras", "parlera", "parlerons", "parlerez", "parleront"],
            "Passé composé": ["ai parlé", "as parlé", "a parlé", "avons parlé", "avez parlé", "ont parlé"],
            "Conditionnel": ["parlerais", "parlerais", "parlerait", "parlerions", "parleriez", "parleraient"],
            "Subjonctif présent": ["parle", "parles", "parle", "parlions", "parliez", "parlent"],
            "Impératif": ["—", "parle!", "—", "parlons!", "parlez!", "—"],
        }
    },
    {
        "key": "finir",
        "label": "2e groupe -IR (type finir): finir (to finish)",
        "conj": "2e groupe",
        "tables": {
            "Présent": ["finis", "finis", "finit", "finissons", "finissez", "finissent"],
            "Imparfait": ["finissais", "finissais", "finissait", "finissions", "finissiez", "finissaient"],
            "Futur simple": ["finirai", "finiras", "finira", "finirons", "finirez", "finiront"],
            "Passé composé": ["ai fini", "as fini", "a fini", "avons fini", "avez fini", "ont fini"],
            "Subjonctif présent": ["finisse", "finisses", "finisse", "finissions", "finissiez", "finissent"],
        }
    },
    {
        "key": "vendre",
        "label": "3e groupe -RE: vendre (to sell) + -IR type dormir/partir",
        "conj": "3e groupe",
        "tables": {
            "Présent (vendre)": ["vends", "vends", "vend", "vendons", "vendez", "vendent"],
            "Présent (dormir)": ["dors", "dors", "dort", "dormons", "dormez", "dorment"],
            "Présent (partir)": ["pars", "pars", "part", "partons", "partez", "partent"],
            "Imparfait": ["vendais", "vendais", "vendait", "vendions", "vendiez", "vendaient"],
            "Futur simple": ["vendrai", "vendras", "vendra", "vendrons", "vendrez", "vendront"],
        }
    },
]

IRREGULAR = [
    {
        "label": "être (to be) — most irregular, auxiliary",
        "tables": {
            "Présent": ["suis", "es", "est", "sommes", "êtes", "sont"],
            "Imparfait": ["étais", "étais", "était", "étions", "étiez", "étaient"],
            "Futur simple": ["serai", "seras", "sera", "serons", "serez", "seront"],
            "Passé composé": ["ai été", "as été", "a été", "avons été", "avez été", "ont été"],
            "Subjonctif présent": ["sois", "sois", "soit", "soyons", "soyez", "soient"],
            "Conditionnel": ["serais", "serais", "serait", "serions", "seriez", "seraient"],
            "Impératif": ["—", "sois!", "—", "soyons!", "soyez!", "—"],
        }
    },
    {
        "label": "avoir (to have) — auxiliary for most passé composé",
        "tables": {
            "Présent": ["ai", "as", "a", "avons", "avez", "ont"],
            "Imparfait": ["avais", "avais", "avait", "avions", "aviez", "avaient"],
            "Futur simple": ["aurai", "auras", "aura", "aurons", "aurez", "auront"],
            "Passé composé": ["ai eu", "as eu", "a eu", "avons eu", "avez eu", "ont eu"],
            "Subjonctif présent": ["aie", "aies", "ait", "ayons", "ayez", "aient"],
            "Conditionnel": ["aurais", "aurais", "aurait", "aurions", "auriez", "auraient"],
        }
    },
    {
        "label": "aller (to go) — -er but irregular + Y: all-/aill-/va-",
        "tables": {
            "Présent": ["vais", "vas", "va", "allons", "allez", "vont"],
            "Imparfait": ["allais", "allais", "allait", "allions", "alliez", "allaient"],
            "Futur simple": ["irai", "iras", "ira", "irons", "irez", "iront"],
            "Passé composé": ["suis allé(e)", "es allé(e)", "est allé(e)", "sommes allé(e)s", "êtes allé(e)s", "sont allé(e)s"],
            "Subjonctif présent": ["aille", "ailles", "aille", "allions", "alliez", "aillent"],
        }
    },
    {
        "label": "faire (to do/make) — fait, faisons, font + fass-",
        "tables": {
            "Présent": ["fais", "fais", "fait", "faisons", "faites", "font"],
            "Imparfait": ["faisais", "faisais", "faisait", "faisions", "faisiez", "faisaient"],
            "Futur simple": ["ferai", "feras", "fera", "ferons", "ferez", "feront"],
            "Subjonctif présent": ["fasse", "fasses", "fasse", "fassions", "fassiez", "fassent"],
        }
    },
    {
        "label": "prendre, venir, pouvoir, vouloir — big 3rd group",
        "tables": {
            "prendre Présent": ["prends", "prends", "prend", "prenons", "prenez", "prennent"],
            "venir Présent": ["viens", "viens", "vient", "venons", "venez", "viennent"],
            "pouvoir Présent": ["peux/puis", "peux", "peut", "pouvons", "pouvez", "peuvent"],
            "vouloir Présent": ["veux", "veux", "veut", "voulons", "voulez", "veulent"],
            "pouvoir Futur": ["pourrai", "pourras", "pourra", "pourrons", "pourrez", "pourront"],
            "vouloir Futur": ["voudrai", "voudras", "voudra", "voudrons", "voudrez", "voudront"],
        }
    },
]

PERS_LABELS = PERS

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
        with open(os.path.join(os.path.expanduser("~"), ".francais_progress.json"), "w", encoding="utf-8") as f:
            json.dump(prog, f)
    except:
        pass

def load_progress():
    try:
        with open(os.path.join(os.path.expanduser("~"), ".francais_progress.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def build_cards():
    cards = []
    for n in NOUNS:
        # gender
        cards.append(dict(q=f"Gender of '{n['word']}' ({n['meaning']})?", a=n["gender"], type="noun", key=n["key"], group=n["group"], hint=f"{n['art_sg']} {n['word']} → {n['art_pl']} {n['plural']} — {n['note']}"))
        # plural
        cards.append(dict(q=f"Plural of '{n['word']}'? ({n['art_sg']} {n['word']})", a=n["plural"], type="noun", key=n["key"], group="Pluriel", hint=n["note"]))
    for v in VERBS:
        for tense, forms in v["tables"].items():
            for idx, form in enumerate(forms[:6]):
                if not form or form.startswith("—"):
                    continue
                clean = form.split("→")[-1].strip().split("/")[0].strip()
                # strip auxiliary for passé composé to just participle? keep full
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
                base_verb = irr["label"].split()[0]
                q = f"{base_verb} — {tense} {pers}"
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
    headers = ["", "Singulier", "Pluriel"]
    for col, txt in enumerate(headers):
        l = tk.Label(grid, text=txt, font=F_BOLD, fg=DIM, bg=ROW_B, bd=0, padx=10, pady=6)
        l.grid(row=0, column=col, sticky="ew", padx=1, pady=1)
    grid.columnconfigure(1, weight=1)
    grid.columnconfigure(2, weight=1)

    # Row for article + noun
    for i, (case_lbl, sg, pl) in enumerate([("Défini", f"{noun['art_sg']} {noun['word']}", f"{noun['art_pl']} {noun['plural']}"),
                                            ("Indéfini", f"{'un' if noun['gender']=='masculine' else 'une'} {noun['word']}", f"des {noun['plural']}"),
                                            ("Partitif", f"{'du' if noun['gender']=='masculine' else 'de la'} {noun['word']}", f"des {noun['plural']}")]):
        bg = ROW_A if i%2==0 else ROW_B
        tk.Label(grid, text=case_lbl, font=F_BOLD, fg=FG, bg=bg, padx=10, pady=6).grid(row=i+1, column=0, sticky="ew", padx=1, pady=1)
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
        if "présent" in tl: tcol = TCOL["pres"]
        elif "imparfait" in tl: tcol = TCOL["impf"]
        elif "futur" in tl: tcol = TCOL["fut"]
        elif "passé" in tl and "composé" in tl: tcol = TCOL["pc"]
        elif "conditionnel" in tl: tcol = TCOL["cond"]
        elif "subjonctif" in tl: tcol = TCOL["subj"]
        elif "impératif" in tl: tcol = TCOL["imp"]

        tframe = tk.Frame(wrap, bg=PANEL)
        tframe.pack(fill="x", padx=8, pady=(10,2))
        tk.Frame(tframe, bg=tcol, width=4).pack(side="left", fill="y", padx=(0,8))
        label(tframe, tense, font=F_BOLD, fg=tcol, bg=PANEL).pack(side="left")

        grid = tk.Frame(wrap, bg=PANEL)
        grid.pack(fill="x", padx=12, pady=2)
        for idx, form in enumerate(forms):
            if idx >= 6:
                continue
            r = idx // 3
            c = idx % 3
            if form.startswith("—"):
                continue
            cell = tk.Frame(grid, bg=ROW_A if r%2==0 else ROW_B, bd=1, relief="flat")
            cell.grid(row=r, column=c, sticky="ew", padx=2, pady=2)
            grid.columnconfigure(c, weight=1)
            pers = PERS_SHORT[idx]
            label(cell, pers, font=F_SMALL, fg=DIM, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(4,0))
            label(cell, form, font=F_BODY, fg=FG, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(0,6))

# ─── PAGES ──────────────────────────────────────────────────────────────────
def page_overview(parent):
    tk.Label(parent, text="FRANÇAIS", font=F_TITLE, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(20,4))
    tk.Label(parent, text="French Studio — color-coded gender, articles & verb tenses.", font=(SERIF, 14, "italic"), fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,20))

    card_wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    card_wrap.pack(fill="x", padx=20, pady=8)
    tk.Label(card_wrap, text="Gender & Number — color code", font=F_H2, fg=GOLD, bg=PANEL).pack(anchor="w", padx=12, pady=8)
    for i, (gender, art, adj, ex) in enumerate(GENDER_USE):
        row = tk.Frame(card_wrap, bg=ROW_A if i%2==0 else ROW_B)
        row.pack(fill="x", padx=1, pady=1)
        tk.Frame(row, bg=CASE_COL[i], width=5).pack(side="left", fill="y")
        tk.Label(row, text=GENDER_ABBR[i], font=F_BOLD, fg=CASE_COL[i], bg=row["bg"], width=6).pack(side="left", padx=8, pady=8)
        tk.Label(row, text=f"{gender} — {art}", font=F_BODY, fg=FG, bg=row["bg"]).pack(side="left")
        tk.Label(row, text=f"· {adj} · {ex}", font=F_SMALL, fg=DIM, bg=row["bg"], wraplength=500, justify="left").pack(side="left", padx=12)

    for title, txt in [
        ("French in 20 seconds", "No Latin declensions! Nouns have gender (masculine/feminine) + number. Articles carry the work: le/la/les (the), un/une/des (a/some), du/de la/des (some). Adjectives agree: noir (m), noire (f), noirs (m pl), noires (f pl). Verbs: 3 groups: -er (parler, 90%), -ir (finir, with -iss-), -re (vendre) + huge irregular list. 2 auxiliaries: avoir (most) and être (movement/reflexive)."),
        ("Tenses you need", "Présent (je parle), Imparfait (je parlais = was speaking / used to), Futur simple (je parlerai = will), Passé composé (j'ai parlé = have spoken / spoke), Conditionnel (je parlerais = would), Subjonctif (que je parle = that I speak). Passé simple (je parlai) literary only."),
        ("Why color?", "Blue = Masculin, Pink = Féminin, Teal = Pluriel. Verb colors: Yellow Présent, Teal Imparfait, Blue Futur, Red Passé composé, Green Conditionnel, Orange Subjonctif — same colors in guide, flashcards, worksheet."),
        ("Pronunciation basics", "Final -s, -t, -d, -x usually silent: les chats /le ʃa/, petit /pəti/. Nasals: bon /bɔ̃/, vin /vɛ̃/. Accents: é /e/, è/ê /ɛ/, à/ù distinguish words, ç /s/. Liaison: les‿amis /lezami/, elision: le/la → l' before vowel."),
    ]:
        c = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        c.pack(fill="x", padx=20, pady=6)
        tk.Label(c, text=title, font=F_H2, fg=GOLD, bg=PANEL).pack(anchor="w", padx=12, pady=(8,2))
        tk.Label(c, text=txt, font=F_BODY, fg=FG, bg=PANEL, wraplength=900, justify="left").pack(anchor="w", padx=12, pady=(0,10))

def page_alphabet(parent):
    tk.Label(parent, text="Alphabet & Pronunciation", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    wrap.pack(fill="x", padx=20, pady=8)
    txt = """
Alphabet: a-z same as English + accents: é è ê à â ô î û ù ë ï ü ÿ ç æ œ

Accents:
é acute = /e/ fermé: café /kafe/
è grave = /ɛ/ ouvert: mère /mɛʁ/
ê circonflexe = /ɛ/ souvent long + historical s: fête < feste, hôpital < hospital
à ù = distinguish: à (to) vs a (has), où (where) vs ou (or)
ë ï ü tréma = split: Noël /nɔɛl/, maïs /ma.is/
ç cédille = /s/ before a/o/u: français /fʁɑ̃sɛ/, garçon /gaʁsɔ̃/

Pronunciation:
Final consonants usually silent: petit /pəti/, grand /gʁɑ̃/, temps /tɑ̃/
But C,R,F,L often pronounced: sac /sak/, mer /mɛʁ/, vif /vif/, sel /sɛl/ (CaReFuL)
Nasals: an/en /ɑ̃/ or /ã/, on /ɔ̃/, in/un /ɛ̃/, ein/ain /ɛ̃/
GN = /ɲ/: montagne /mɔ̃taɲ/, ILL = /j/: fille /fij/, CH = /ʃ/: chat /ʃa/
H: h muet (l'homme /lɔm/) vs h aspiré (le héros /lə eʁo/ no liaison/elision)

Liaison: les‿amis /lezami/ (z liaison), nous‿avons /nuzavɔ̃/
Elision: le/la → l' before vowel: l'ami, l'eau, l'école
Enchaînement: il‿a /ila/.

Passé composé: j'ai, tu as, il a, nous avons, vous avez, ils ont + past participle.
Agreement with être: elle est allée (f), ils sont allés (m pl) — extra -e/-s.
"""
    tk.Label(wrap, text=txt.strip(), font=F_BODY, fg=FG, bg=PANEL, justify="left", wraplength=850).pack(padx=12, pady=10)

def page_nouns(parent):
    tk.Label(parent, text="Nouns & Articles", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    tk.Label(parent, text="Gold = article + ending to memorize. Learn noun WITH its article: le chat, not just chat.", font=F_SMALL, fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,10))
    for n in NOUNS:
        noun_table(parent, n)

def page_adjectives(parent):
    tk.Label(parent, text="Adjectives", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    for adj in ADJECTIVES:
        wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        wrap.pack(fill="x", padx=20, pady=8)
        tk.Label(wrap, text=adj["title"], font=F_H2, fg=GOLD, bg=HEAD_BG).pack(fill="x", padx=12, pady=8)
        for row in adj["table"]:
            r = tk.Frame(wrap, bg=PANEL)
            r.pack(fill="x", padx=8, pady=1)
            for cell in row:
                tk.Label(r, text=cell, font=F_BODY, fg=FG, bg=ROW_A, width=20, padx=6, pady=4, bd=1, relief="flat").pack(side="left", padx=1)
        tk.Label(wrap, text=adj["note"], font=F_SMALL, fg=DIM, bg=PANEL, wraplength=900, justify="left").pack(anchor="w", padx=12, pady=6)

def page_pronouns(parent):
    tk.Label(parent, text="Pronouns & Articles", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
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
    tk.Label(parent, text="Verbs — 3 Groups + Auxiliaries", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    tk.Label(parent, text="Yellow Présent, Teal Imparfait, Blue Futur, Red Passé composé, Green Conditionnel, Orange Subjonctif.", font=F_SMALL, fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,10))
    for v in VERBS:
        verb_table(parent, v)

def page_irregular(parent):
    tk.Label(parent, text="Irregular Verbs — the big 5 + modal", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    tk.Label(parent, text="être, avoir, aller, faire are 90% of irregular usage. Master these first.", font=F_SMALL, fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,10))
    for irr in IRREGULAR:
        wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        wrap.pack(fill="x", padx=20, pady=8)
        tk.Label(wrap, text=irr["label"], font=F_H2, fg=GOLD, bg=HEAD_BG).pack(fill="x", padx=12, pady=8)
        for tense, forms in irr["tables"].items():
            tframe = tk.Frame(wrap, bg=PANEL)
            tframe.pack(fill="x", padx=12, pady=4)
            tcol = GOLD
            tl = tense.lower()
            if "présent" in tl: tcol = TCOL["pres"]
            elif "imparfait" in tl: tcol = TCOL["impf"]
            elif "futur" in tl: tcol = TCOL["fut"]
            elif "passé" in tl: tcol = TCOL["pc"]
            elif "conditionnel" in tl: tcol = TCOL["cond"]
            elif "subjonctif" in tl: tcol = TCOL["subj"]
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
    tk.Label(parent, text="Reference — Cheat Sheet", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    ref = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    ref.pack(fill="x", padx=20, pady=8)
    txt = """
FRENCH ARTICLES:
Défini: le (m), la (f), l' (before vowel), les (pl) = the
Indéfini: un (m), une (f), des (pl) = a / some
Partitif: du (m), de la (f), de l' (vowel), des (pl) = some (mass)
Negation: Je veux du pain → Je ne veux pas DE pain (du/des → de/d')

ADJECTIVE AGREEMENT:
Masc sg: petit, grand, français, beau, nouveau, vieux
Fém sg: petite, grande, française, belle, nouvelle, vieille (+ -e)
Masc pl: petits, grands, français, beaux, nouveaux, vieux (+ -s, -eaux, -aux)
Fém pl: petites, grandes, françaises, belles, nouvelles, vieilles (+ -es)
Position: BAGS (Beauty, Age, Goodness, Size) BEFORE noun: un grand homme, un petit chat
Otherwise AFTER: un homme intelligent, une maison blanche.

NOUN PLURALS:
Regular: -s (silent): chat→chats, maison→maisons
-eau/-au/-eu → -x: bateau→bateaux, chapeau→chapeaux, jeu→jeux
-al → -aux (7 common): cheval→chevaux, journal→journaux, hôpital→hôpitaux, animal→animaux, etc.
-ou → -oux (7): bijou, caillou, chou, genou, hibou, joujou, pou → bijoux etc. Others: clou→clous.

VERB ENDINGS:
-er (parler): Présent -e, -es, -e, -ons, -ez, -ent | Imparfait -ais, -ais, -ait, -ions, -iez, -aient | Futur -erai, -eras, -era, -erons, -erez, -eront
-ir (finir): Présent -is, -is, -it, -issons, -issez, -issent | Imparfait -issais...
-re (vendre): Présent -s, -s, -, -ons, -ez, -ent

AUXILIARIES:
avoir: ai, as, a, avons, avez, ont (most verbs)
être: suis, es, est, sommes, êtes, sont (movement: aller, venir, arriver, partir, entrer, sortir, monter, descendre, naître, mourir, rester, tomber + reflexive)
Passé composé with être: agreement! Elle est allée, Ils sont allés, Elles sont allées.

PRONOUN ORDER: me/te/se/nous/vous + le/la/les + lui/leur + y + en
Je te le donne (I give it to you), Il y en a (There are some)

NEGATION: ne...pas (not), ne...jamais (never), ne...rien (nothing), ne...personne (nobody), ne...plus (no more), ne...que (only)
Je ne parle pas, Je ne parle jamais.

QUESTIONS: Est-ce que tu parles? / Parles-tu? / Tu parles? (informal rising)
"""
    tk.Label(ref, text=txt.strip(), font=("Courier New", 11), fg=FG, bg=PANEL, justify="left", anchor="w").pack(fill="x", padx=12, pady=10)

def page_memory(parent):
    tk.Label(parent, text="Memory Aids", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    aids = [
        ("Gender Trick", "Learn noun WITH article: le chat, la maison, l'eau. Never learn chat alone. 60% masc, 40% fem. Endings that are usually fem: -tion, -sion, -ure, -ence, -ance, -euse, -ette, -elle. Masc: -ment, -age, -isme, -eur, -oir, -ail."),
        ("Plural Chant", "Un chat, des chats | Un bateau, des bateaux (-eau→-eaux) | Un cheval, des chevaux (-al→-aux) | Un bijou, des bijoux (7 -oux) — say them aloud 3x."),
        ("Adjective Agreement", "Petit → Petite (add -e), Petits (add -s), Petites (add -es). For beau: beau (m), bel (m before vowel: bel ami), belle (f), beaux, belles. Same for nouveau/nouvel/nouvelle."),
        ("BAGS Before Noun", "Beauty, Age, Goodness, Size BEFORE noun: bon, mauvais, beau, joli, petit, grand, gros, vieux, jeune, nouveau. Un grand homme (great man) vs un homme grand (tall man) — meaning changes!"),
        ("Présent -er", "Parle, parles, parle, parlons, parlez, parlent — -e, -es, -e, -ons, -ez, -ent (ent silent!). Pronounced: /paʁl, paʁl, paʁl, paʁlɔ̃, paʁle, paʁl/."),
        ("Passé composé", "Avoir + past participle: parlé, fini, vendu. With être: allé(e), venu(e), arrivé(e), parti(e). Agreement: Elle est allée, Ils sont allés. Memorize être verbs with Dr & Mrs Vandertramp: Devenir, Revenir, Monter, Rester, Sortir, Venir, Aller, Naître, Descendre, Entrer, Retourner, Tomber, Rentrer, Arriver, Mourir, Partir."),
        ("Être & Avoir", "Être: suis, es, est, sommes, êtes, sont — Imparfait étais, Futur serai, Subj sois. Avoir: ai, as, a, avons, avez, ont — Imparfait avais, Futur aurai, Subj aie. These two are 30% of all verbs you hear."),
        ("Subjonctif Trigger", "Use subjunctive after: il faut que, vouloir que, pour que, bien que, avant que, sans que, que + emotion: je veux que tu viennes, il faut que tu fasses. Present: que je parle, que tu parles, qu'il parle, que nous parlions, que vous parliez, qu'ils parlent."),
        ("Pronoun Order Chant", "Me Te Se Nous Vous — Le La Les — Lui Leur — Y — En. Je te le donne, Il me les a donnés, J'y vais, J'en veux. Place before conjugated verb, or attached to imperative: Donne-le-moi! Donnez-m'en!"),
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
        tk.Label(top, text="Worksheet — Fill the endings (French)", font=F_H2, fg=GOLD, bg=HEAD_BG).pack(side="left", padx=16, pady=12)
        tk.Label(top, text="Type French. Gold = to memorize. Accents matter!", font=F_SMALL, fg=DIM, bg=HEAD_BG).pack(side="left", padx=12)

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
            for txt in ["Forme", "Singulier", "Pluriel"]:
                tk.Label(hdr, text=txt, font=F_SMALL, fg=DIM, bg=HEAD_BG, width=24).pack(side="left", padx=8, pady=6)
            for i, (lbl, sg, pl) in enumerate([
                ("Avec article défini", f"{noun['art_sg']} {noun['word']}", f"{noun['art_pl']} {noun['plural']}"),
                ("Indéfini", f"{'un' if noun['gender']=='masculine' else 'une'} {noun['word']}", f"des {noun['plural']}"),
            ]):
                row = tk.Frame(grid, bg=ROW_A if i%2==0 else ROW_B)
                row.pack(fill="x", padx=1, pady=1)
                tk.Label(row, text=lbl, font=F_BOLD, fg=FG, bg=row["bg"], width=20).pack(side="left", padx=8, pady=8)
                for num_idx, form in enumerate([sg, pl]):
                    cell = tk.Frame(row, bg=row["bg"])
                    cell.pack(side="left", fill="x", expand=True, padx=8, pady=4)
                    e = tk.Entry(cell, font=F_BODY, bg=PANEL2, fg=FG, relief="flat", bd=0, width=18)
                    e.pack(side="left", ipady=4, padx=4)
                    tk.Label(cell, text=f"→ {form}", font=F_SMALL, fg=DIM, bg=row["bg"]).pack(side="left", padx=6)
                    self.entries.append((e, form, form))

        for key in ["m_chat", "f_maison", "m_cheval"]:
            n = next(x for x in NOUNS if x["key"]==key)
            make_noun_block(n)

        section("Verbes — Conjugaison")
        for v in VERBS[:2]:
            wrap = tk.Frame(self.scroll.inner, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
            wrap.pack(fill="x", pady=6)
            tk.Label(wrap, text=v["label"], font=F_BOLD, fg=GOLD, bg=HEAD_BG).pack(fill="x", padx=12, pady=6)
            for tense in ["Présent", "Imparfait", "Futur simple"]:
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
        tk.Label(ctrl, text="Blank = not counted. Toggle Ignore accents to allow e/é/è same.", font=F_SMALL, fg=DIM, bg=BG).pack(side="left")
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
            path = os.path.join(os.path.expanduser("~"), "french_worksheet.html")
            html_rows = []
            for entry, expected, full in self.entries[:60]:
                html_rows.append(f"<tr><td><span class='b'></span></td><td>{html.escape(full)}</td></tr>")
            page = f"<!doctype html><meta charset='utf-8'><title>French Worksheet</title><style>body{{font:16px Georgia;margin:40px}} table{{border-collapse:collapse}} td{{border:1px solid #bbb;padding:8px 14px}} .b{{display:inline-block;min-width:90px;border-bottom:1px solid #000}}</style><h1>French Worksheet</h1><table>{''.join(html_rows)}</table>"
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

ICONS = {"Overview":"✦","Alphabet":"É","Nouns & Articles":"Ⅰ","Adjectives":"Ⅱ","Pronouns":"Ⅲ","Verbs":"Ⅳ","Irregular Verbs":"Ⅴ","Reference":"§","Flashcards":"◈","Type-in Drill":"⌨","Worksheet":"✎","Memory Aids":"♪"}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Français · Grammar Studio — Enhanced (French)")
        self.geometry("1280x860")
        self.minsize(1100, 720)
        self.configure(bg=BG)
        self.opts = {"ignore": True}
        self.prog = load_progress()
        self.cards = build_cards()
        self.pages, self.cur, self.navbtns = {}, None, {}

        head = tk.Frame(self, bg=HEAD_BG)
        head.pack(fill="x")
        label(head, "FRANÇAIS", fg=GOLD, font=F_TITLE, bg=HEAD_BG).pack(side="left", padx=(24,12), pady=(12,8))
        label(head, "Grammar Studio — French · gender & conjugation · color-coded", fg=DIM, font=(SERIF, 14, "italic"), bg=HEAD_BG).pack(side="left", pady=(20,0))

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

        self.foot = label(self, "Tip: Ignore accents toggle in study modes. Space=show, 1=again, 3=good, → next. Learn nouns WITH le/la.", fg=DIM, font=F_SMALL, bg=HEAD_BG, anchor="w", padx=18, pady=5)
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
