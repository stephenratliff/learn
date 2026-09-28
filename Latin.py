#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LATINA · Grammar Studio - Enhanced Edition
===========================================
Color-coded, all-inclusive Latin grammar guide with memorization engine.

Based on latin_grammar_studio.py structure - now with:
 - Concise Grammar Guide (Overview, Nouns 5 declensions, Adjectives, Pronouns, Verbs 4 conjugations, Irregulars, Reference)
 - Color-coded tables (cases + tenses)
 - STUDY: Flashcards (spaced repetition), Type-in Drill, Interactive Worksheet, Memory Aids

Run: python3 latin_grammar_studio_enhanced.py
Needs: Python 3.8+ with Tkinter only. No external packages.
Macrons can be typed or ignored - toggle in app.
"""
import html
import json
import os
import random
import unicodedata
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox

# ─── THEME (same palette as original) ───────────────────────────────────────
BG, PANEL, PANEL2 = "#11131b", "#1a1d2a", "#232739"
ROW_A, ROW_B, HEAD_BG, BORDER = "#1c1f2d", "#171a26", "#0d0f16", "#333955"
FG, DIM, GOLD, GREEN, RED = "#efe6d0", "#8e93ad", "#e0b458", "#6fcf8f", "#ff6b7d"

CASE_COL = ["#f2c94c", "#4fd1b5", "#5fa8ff", "#ff7a7a", "#c58af9", "#9bdc6a"]
TCOL = {"pres": "#f2c94c", "impf": "#4fd1b5", "fut": "#5fa8ff",
        "perf": "#ff7a7a", "plup": "#c58af9", "fpf": "#9bdc6a"}

SERIF, SANS = "Georgia", "Helvetica Neue"
F_TITLE = (SERIF, 30, "bold")
F_H1 = (SERIF, 22, "bold")
F_H2 = (SERIF, 16, "bold")
F_BODY = (SERIF, 14)
F_BOLD = (SERIF, 14, "bold")
F_SMALL = (SANS, 11)
F_NAV = (SANS, 13)
F_BTN = (SANS, 12, "bold")

# ─── LATIN CORE DATA ────────────────────────────────────────────────────────
CASES = ["Nominative", "Genitive", "Dative", "Accusative", "Ablative", "Vocative"]
CASE_ABBR = ["Nom.", "Gen.", "Dat.", "Acc.", "Abl.", "Voc."]
CASE_USE = [
    ("Nominative", "who/what (does it)", "Subject; predicate", "puella cantat — the girl sings"),
    ("Genitive", "whose / of what", "Possession, 'of'", "liber puellae — girl's book"),
    ("Dative", "to / for whom", "Indirect object", "puellae librum dat — gives book to girl"),
    ("Accusative", "whom / what", "Direct object; motion toward", "puellam videt — sees girl"),
    ("Ablative", "by / with / from / in", "Means, agent, separation, place", "cum puellā — with girl"),
    ("Vocative", "O …!", "Direct address", "puella! — O girl!"),
]

def _n(key, group, title, gender, word, meaning, stem, sg, pl, ov=None, note=""):
    return dict(key=key, group=group, title=title, gender=gender, word=word,
                meaning=meaning, stem=stem, sg=sg, pl=pl, ov=ov or {}, note=note)

NOUNS = [
    _n("1", "1st Decl", "1st Declension", "mostly feminine", "puella", "girl", "puell",
       ["a", "ae", "ae", "am", "ā", "a"], ["ae", "ārum", "īs", "ās", "īs", "ae"],
       note="Gen sg -ae. Masculine exceptions: nauta, agricola, poēta. Dea/fīlia: deābus, fīliābus."),
    _n("2m", "2nd Decl", "2nd Decl. masc. -us", "masculine", "dominus", "master", "domin",
       ["us", "ī", "ō", "um", "ō", "e"], ["ī", "ōrum", "īs", "ōs", "īs", "ī"],
       note="Only decl. with distinct vocative sg: -e, -ius→-ī (fīlī). -er nouns: puer, puerī; ager, agrī."),
    _n("2n", "2nd Decl", "2nd Decl. neuter -um", "neuter", "bellum", "war", "bell",
       ["um", "ī", "ō", "um", "ō", "um"], ["a", "ōrum", "īs", "a", "īs", "a"],
       note="Neuter rule: Nom=Acc=Voc, pl -a. Same for 3rd/4th neuter."),
    _n("3c", "3rd Decl", "3rd Decl. cons. stem (m./f.)", "m./f.", "rēx", "king", "rēg",
       ["", "is", "ī", "em", "e", ""], ["ēs", "um", "ibus", "ēs", "ibus", "ēs"],
       ov={("sg",0):("rēx",""), ("sg",5):("rēx","")}, note="Find stem from gen sg: rēgis → rēg-. Nom irregular."),
    _n("3n", "3rd Decl", "3rd Decl. cons. stem (n.)", "neuter", "corpus", "body", "corpor",
       ["", "is", "ī", "", "e", ""], ["a", "um", "ibus", "a", "ibus", "a"],
       ov={("sg",0):("corpus",""),("sg",3):("corpus",""),("sg",5):("corpus","")}, note="Neuter: nom=acc=voc."),
    _n("3i", "3rd Decl", "3rd Decl. i-stem (m./f.)", "m./f.", "cīvis", "citizen", "cīv",
       ["is", "is", "ī", "em", "e", "is"], ["ēs", "ium", "ibus", "ēs", "ibus", "ēs"],
       note="i-stems: gen pl -ium. Includes parisyllabic (cīvis, hostis) and 2-consonant stems (urbs, mōns)."),
    _n("3in", "3rd Decl", "3rd Decl. i-stem (n.)", "neuter", "mare", "sea", "mar",
       ["e", "is", "ī", "e", "ī", "e"], ["ia", "ium", "ibus", "ia", "ibus", "ia"],
       note="Neuters in -e, -al, -ar: abl sg -ī, nom/acc pl -ia."),
    _n("4m", "4th Decl", "4th Decl. masc. -us", "masc. (some fem.)", "manus", "hand", "man",
       ["us", "ūs", "uī", "um", "ū", "us"], ["ūs", "uum", "ibus", "ūs", "ibus", "ūs"],
       note="Gen sg -ūs. Feminine: manus, domus (domī = at home)."),
    _n("4n", "4th Decl", "4th Decl. neuter -ū", "neuter", "cornū", "horn", "corn",
       ["ū", "ūs", "ū", "ū", "ū", "ū"], ["ua", "uum", "ibus", "ua", "ibus", "ua"],
       note="Only 4-5 nouns: cornū, genū, verū."),
    _n("5", "5th Decl", "5th Declension", "feminine (diēs m./f.)", "rēs", "thing", "r",
       ["ēs", "eī", "eī", "em", "ē", "ēs"], ["ēs", "ērum", "ēbus", "ēs", "ēbus", "ēs"],
       note="Gen sg -eī (-ēī after vowel). Full plural only rēs, diēs."),
]

def noun_forms(d):
    return {num: [d["ov"].get((num,i),(d["stem"],e)) for i,e in enumerate(d[num])] for num in ("sg","pl")}

ADJECTIVES = [
    {
        "title": "1st/2nd Declension: bonus, -a, -um (good)",
        "type": "bonus-type",
        "table": [
            ["", "Masc sg", "Fem sg", "Neut sg"],
            ["Nom", "bonus", "bona", "bonum"],
            ["Gen", "bonī", "bonae", "bonī"],
            ["Dat", "bonō", "bonae", "bonō"],
            ["Acc", "bonum", "bonam", "bonum"],
            ["Abl", "bonō", "bonā", "bonō"],
            ["Voc", "bone", "bona", "bonum"],
            ["", "Masc pl", "Fem pl", "Neut pl"],
            ["Nom", "bonī", "bonae", "bona"],
            ["Gen", "bonōrum", "bonārum", "bonōrum"],
        ],
        "note": "Like puella + dominus/bellum. pulcher, pulchra, pulchrum keeps -er: pulchrī."
    },
    {
        "title": "3rd Declension: fortis, forte (brave) & ācer, ācris, ācre (sharp)",
        "type": "3rd decl adj",
        "table": [
            ["", "M/F sg", "N sg", "M/F pl", "N pl"],
            ["Nom", "fortis / ācer", "forte / ācre", "fortēs / ācrēs", "fortia / ācria"],
            ["Gen", "fortis", "fortis", "fortium", "fortium"],
            ["Dat", "fortī", "fortī", "fortibus", "fortibus"],
            ["Acc", "fortem / ācrem", "forte / ācre", "fortēs / ācrīs", "fortia / ācria"],
            ["Abl", "fortī", "fortī", "fortibus", "fortibus"],
        ],
        "note": "i-stem adjectives: abl sg -ī, gen pl -ium, neut pl -ia."
    },
]

PRONOUNS = [
    {"title": "Personal: ego, tū, nōs, vōs", "forms": [["","sg","pl"],["1st Nom","ego","nōs"],["Gen","meī/mē","nostrī/nostrum"],["Dat","mihi","nōbīs"],["Acc","mē","nōs"],["Abl","mē","nōbīs"],["2nd Nom","tū","vōs"],["Gen","tuī","vestrī/vestrum"],["Dat","tibi","vōbīs"]]},
    {"title": "Demonstrative: is, ea, id (he/she/it, that) & hic, ille", "forms": [["","M","F","N"],["is Nom sg","is","ea","id"],["Gen sg","eius (all genders)"],["Dat sg","eī"],["hic Nom sg","hic","haec","hoc"],["ille Nom sg","ille","illa","illud"]]},
    {"title": "Relative: quī, quae, quod (who/which)", "forms": [["","M sg","F sg","N sg","M pl","F pl","N pl"],["Nom","quī","quae","quod","quī","quae","quae"],["Gen","cuius","cuius","cuius","quōrum","quārum","quōrum"],["Dat","cui","cui","cui","quibus","quibus","quibus"],["Acc","quem","quam","quod","quōs","quās","quae"]]},
]

VERBS = [
    {
        "key": "amo",
        "label": "1st Conjugation: amō, amāre, amāvī, amātum (to love)",
        "conj": "1st",
        "pres_stem": "amā",
        "perf_stem": "amāv",
        "tables": {
            "Present Active": ["amō","amās","amat","amāmus","amātis","amant"],
            "Imperfect Active": ["amābam","amābās","amābat","amābāmus","amābātis","amābant"],
            "Future Active": ["amābō","amābis","amābit","amābimus","amābitis","amābunt"],
            "Perfect Active": ["amāvī","amāvistī","amāvit","amāvimus","amāvistis","amāvērunt"],
            "Pluperfect Active": ["amāveram","amāverās","amāverat","amāverāmus","amāverātis","amāverant"],
            "Future Perfect Active": ["amāverō","amāveris","amāverit","amāverimus","amāveritis","amāverint"],
            "Present Passive": ["amor","amāris","amātur","amāmur","amāminī","amantur"],
        }
    },
    {
        "key": "moneo",
        "label": "2nd Conjugation: moneō, monēre, monuī, monitum (to warn)",
        "conj": "2nd",
        "pres_stem": "monē",
        "perf_stem": "monu",
        "tables": {
            "Present Active": ["moneō","monēs","monet","monēmus","monētis","monent"],
            "Imperfect Active": ["monēbam","monēbās","monēbat","monēbāmus","monēbātis","monēbant"],
            "Future Active": ["monēbō","monēbis","monēbit","monēbimus","monēbitis","monēbunt"],
            "Perfect Active": ["monuī","monuistī","monuit","monuimus","monuistis","monuērunt"],
            "Present Passive": ["moneor","monēris","monētur","monēmur","monēminī","monentur"],
        }
    },
    {
        "key": "rego",
        "label": "3rd Conjugation: regō, regere, rēxī, rēctum (to rule)",
        "conj": "3rd",
        "pres_stem": "reg",
        "perf_stem": "rēx",
        "tables": {
            "Present Active": ["regō","regis","regit","regimus","regitis","regunt"],
            "Imperfect Active": ["regēbam","regēbās","regēbat","regēbāmus","regēbātis","regēbant"],
            "Future Active": ["regam","regēs","reget","regēmus","regētis","regent"],
            "Perfect Active": ["rēxī","rēxistī","rēxit","rēximus","rēxistis","rēxērunt"],
        }
    },
    {
        "key": "capio",
        "label": "3rd-io: capiō, capere, cēpī, captum (to take)",
        "conj": "3rd-io",
        "pres_stem": "capi",
        "perf_stem": "cēp",
        "tables": {
            "Present Active": ["capiō","capis","capit","capimus","capitis","capiunt"],
            "Imperfect Active": ["capiēbam","capiēbās","capiēbat","capiēbāmus","capiēbātis","capiēbant"],
            "Future Active": ["capiam","capiēs","capiet","capiēmus","capiētis","capient"],
        }
    },
    {
        "key": "audio",
        "label": "4th Conjugation: audiō, audīre, audīvī, audītum (to hear)",
        "conj": "4th",
        "pres_stem": "audī",
        "perf_stem": "audīv",
        "tables": {
            "Present Active": ["audiō","audīs","audit","audīmus","audītis","audiunt"],
            "Imperfect Active": ["audiēbam","audiēbās","audiēbat","audiēbāmus","audiēbātis","audiēbant"],
            "Future Active": ["audiam","audiēs","audiet","audiēmus","audiētis","audient"],
            "Perfect Active": ["audīvī","audīvistī","audīvit","audīvimus","audīvistis","audīvērunt"],
        }
    },
]

IRREGULAR = [
    {
        "label": "sum, esse, fuī, futūrum (to be)",
        "tables": {
            "Present": ["sum","es","est","sumus","estis","sunt"],
            "Imperfect": ["eram","erās","erat","erāmus","erātis","erant"],
            "Future": ["erō","eris","erit","erimus","eritis","erunt"],
            "Perfect": ["fuī","fuistī","fuit","fuimus","fuistis","fuērunt"],
            "Present Subjunctive": ["sim","sīs","sit","sīmus","sītis","sint"],
            "Infinitive": ["esse","fuisse","futūrum esse"],
        }
    },
    {
        "label": "possum, posse, potuī (to be able)",
        "tables": {
            "Present": ["possum","potes","potest","possumus","potestis","possunt"],
            "Imperfect": ["poteram","poterās","poterat","poterāmus","poterātis","poterant"],
        }
    },
    {
        "label": "ferō, ferre, tulī, lātum (to carry, bear)",
        "tables": {
            "Present Active": ["ferō","fers","fert","ferimus","fertis","ferunt"],
            "Present Passive": ["feror","ferris","fertur","ferimur","feriminī","feruntur"],
        }
    },
]

PERS_LABELS = ["1st sg. (I)", "2nd sg. (you)", "3rd sg. (he/she/it)", "1st pl. (we)", "2nd pl. (you all)", "3rd pl. (they)"]

# ─── HELPERS ────────────────────────────────────────────────────────────────
def strip_macrons(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower().replace("j","i").strip()

def normalize(s: str, ignore: bool) -> str:
    s = s.strip()
    if ignore:
        return strip_macrons(s)
    return s.lower().strip()

def label(parent, text, **kw):
    kw.setdefault("bg", kw.get("bg", BG))
    kw.setdefault("fg", FG)
    return tk.Label(parent, text=text, **kw)

def save_progress(prog):
    try:
        with open(os.path.join(os.path.expanduser("~"), ".latina_progress.json"), "w", encoding="utf-8") as f:
            json.dump(prog, f)
    except: pass

def load_progress():
    try:
        with open(os.path.join(os.path.expanduser("~"), ".latina_progress.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def build_cards():
    cards = []
    # nouns
    for n in NOUNS:
        forms = noun_forms(n)
        for num in ("sg","pl"):
            for i, case in enumerate(CASE_ABBR):
                stem, end = forms[num][i]
                full = stem+end
                if not full: continue
                q = f"{n['word']} ({n['meaning']}) — {case} {num}"
                cards.append(dict(q=q, a=full, type="noun", key=n["key"], group=n["group"], hint=f"{n['title']} | {n['stem']}+{n[num][i]}"))
                cards.append(dict(q=f"{full} — what case?", a=f"{case} {num} of {n['word']}", type="reverse", key=n["key"]))
    # verbs
    for v in VERBS:
        for tense, forms in v["tables"].items():
            for idx, form in enumerate(forms[:6]):
                if not form: continue
                q = f"{v['key']} — {tense} — {PERS_LABELS[idx]}"
                cards.append(dict(q=q, a=form, type="verb", key=v["key"], group=tense, hint=v["label"]))
    # irregulars
    for irr in IRREGULAR:
        for tense, forms in irr["tables"].items():
            for idx, form in enumerate(forms[:6]):
                if not form: continue
                pers = PERS_LABELS[idx] if idx < len(PERS_LABELS) else ""
                q = f"{irr['label'].split(',')[0]} — {tense} {pers}"
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
def decl_table(parent, noun):
    forms = noun_forms(noun)
    wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    wrap.pack(fill="x", pady=8)
    # header
    header = tk.Frame(wrap, bg=HEAD_BG)
    header.pack(fill="x")
    label(header, f"{noun['title']} — {noun['word']}, {noun['sg'][1]} ({noun['meaning']})", font=F_H2, fg=GOLD, bg=HEAD_BG).pack(side="left", padx=12, pady=8)
    label(header, f"{noun['gender']} · stem {noun['stem']}-", font=F_SMALL, fg=DIM, bg=HEAD_BG).pack(side="right", padx=12)

    grid = tk.Frame(wrap, bg=PANEL)
    grid.pack(fill="x", padx=1, pady=1)
    # column headers
    for col, txt in enumerate(["", "Singular", "Plural"]):
        l = tk.Label(grid, text=txt, font=F_BOLD, fg=DIM, bg=ROW_B, bd=0, padx=10, pady=6)
        l.grid(row=0, column=col, sticky="ew", padx=1, pady=1)
    grid.columnconfigure(1, weight=1)
    grid.columnconfigure(2, weight=1)

    for i, case in enumerate(CASES):
        abbr = CASE_ABBR[i]
        # case label with color
        case_frame = tk.Frame(grid, bg=ROW_A if i%2==0 else ROW_B)
        case_frame.grid(row=i+1, column=0, sticky="nsew", padx=1, pady=1)
        col = CASE_COL[i]
        tk.Frame(case_frame, bg=col, width=4).pack(side="left", fill="y")
        tk.Label(case_frame, text=f"{abbr}\n{case[:3]}", font=F_SMALL, fg=FG, bg=case_frame["bg"], justify="left", padx=8, pady=4).pack(side="left")

        for num_idx, num in enumerate(("sg","pl")):
            stem, end = forms[num][i]
            cell_bg = ROW_A if i%2==0 else ROW_B
            cell = tk.Frame(grid, bg=cell_bg)
            cell.grid(row=i+1, column=num_idx+1, sticky="ew", padx=1, pady=1)
            full = stem+end
            if not full:
                full = "—"
            # show stem+ending in two colors
            tk.Label(cell, text=stem, font=F_BODY, fg=DIM, bg=cell_bg).pack(side="left", padx=(12,0), pady=6)
            tk.Label(cell, text=end, font=F_BOLD, fg=GOLD, bg=cell_bg).pack(side="left", pady=6)
            tk.Label(cell, text=f"  {full}", font=F_BODY, fg=FG, bg=cell_bg).pack(side="left", padx=8)
    # note
    if noun["note"]:
        label(wrap, f"Note: {noun['note']}", font=F_SMALL, fg=DIM, bg=PANEL, wraplength=900, justify="left", anchor="w").pack(fill="x", padx=12, pady=6)

def verb_table(parent, verb):
    wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    wrap.pack(fill="x", pady=8)
    header = tk.Frame(wrap, bg=HEAD_BG)
    header.pack(fill="x")
    label(header, verb["label"], font=F_H2, fg=GOLD, bg=HEAD_BG).pack(side="left", padx=12, pady=8)
    label(header, f"{verb['conj']} conj. | stem {verb['pres_stem']}- / perf {verb['perf_stem']}-", font=F_SMALL, fg=DIM, bg=HEAD_BG).pack(side="right", padx=12)

    for tense, forms in verb["tables"].items():
        # tense header with color
        tcol = "#888"
        for k,v in TCOL.items():
            if k in tense.lower()[:4]:
                tcol = v
                break
        tframe = tk.Frame(wrap, bg=PANEL)
        tframe.pack(fill="x", padx=8, pady=(10,2))
        tk.Frame(tframe, bg=tcol, width=4).pack(side="left", fill="y", padx=(0,8))
        label(tframe, tense, font=F_BOLD, fg=tcol, bg=PANEL).pack(side="left")

        grid = tk.Frame(wrap, bg=PANEL)
        grid.pack(fill="x", padx=12, pady=2)
        for idx, form in enumerate(forms):
            r = idx // 3
            c = idx % 3
            cell = tk.Frame(grid, bg=ROW_A if r%2==0 else ROW_B, bd=1, relief="flat")
            cell.grid(row=r, column=c, sticky="ew", padx=2, pady=2)
            grid.columnconfigure(c, weight=1)
            pers = PERS_LABELS[idx] if idx < len(PERS_LABELS) else f"form {idx+1}"
            label(cell, pers, font=F_SMALL, fg=DIM, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(4,0))
            label(cell, form, font=F_BODY, fg=FG, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(0,6))

# ─── PAGES ──────────────────────────────────────────────────────────────────
def page_overview(parent):
    tk.Label(parent, text="LATINA", font=F_TITLE, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(20,4))
    tk.Label(parent, text="A color-coded map of Latin grammar — built for active recall.", font=(SERIF, 14, "italic"), fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,20))

    # case overview
    card = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    card.pack(fill="x", padx=20, pady=8)
    tk.Label(card, text="The 6 Cases — color code", font=F_H2, fg=GOLD, bg=PANEL).pack(anchor="w", padx=12, pady=8)
    for i, (case, who, use, ex) in enumerate(CASE_USE):
        row = tk.Frame(card, bg=ROW_A if i%2==0 else ROW_B)
        row.pack(fill="x", padx=1, pady=1)
        tk.Frame(row, bg=CASE_COL[i], width=5).pack(side="left", fill="y")
        tk.Label(row, text=CASE_ABBR[i], font=F_BOLD, fg=CASE_COL[i], bg=row["bg"], width=6).pack(side="left", padx=8, pady=8)
        tk.Label(row, text=f"{case} — {who}", font=F_BODY, fg=FG, bg=row["bg"]).pack(side="left")
        tk.Label(row, text=f"· {use} · {ex}", font=F_SMALL, fg=DIM, bg=row["bg"], wraplength=500, justify="left").pack(side="left", padx=12)

    # 5 decl + 4 conj quick
    for title, txt in [
        ("5 Declensions in 20 seconds", "1st (-a, f): puella. 2nd (-us/-um, m/n): dominus, bellum. 3rd (various, m/f/n): rēx, corpus, cīvis, mare — find stem from gen sg. 4th (-us/-ū, m/n): manus, cornū. 5th (-ēs, f): rēs, diēs. Neuter rule: Nom=Acc=Voc, pl -a / -ia / -ua."),
        ("4 Conjugations + esse", "1st ā: amō, amāre. 2nd ē: moneō, monēre. 3rd e: regō, regere (short e). 3rd-io: capiō, capere (i). 4th ī: audiō, audīre. Principal parts: present, infinitive, perfect, supine. All tenses built from present stem vs perfect stem. sum is irregular but everywhere."),
        ("Why color?", "Gold = ending to memorize. Dim = stem. Case colors on left border match flashcards. Tense colors: Yellow Pres, Teal Impf, Blue Fut, Red Perf, Purple Plup, Green Fut-Perf."),
    ]:
        c = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        c.pack(fill="x", padx=20, pady=6)
        tk.Label(c, text=title, font=F_H2, fg=GOLD, bg=PANEL).pack(anchor="w", padx=12, pady=(8,2))
        tk.Label(c, text=txt, font=F_BODY, fg=FG, bg=PANEL, wraplength=900, justify="left").pack(anchor="w", padx=12, pady=(0,10))

def page_nouns(parent):
    tk.Label(parent, text="Nouns — 5 Declensions", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    tk.Label(parent, text="Endings are gold. Stem is dim. Left bar = case color. Tap any declension below.", font=F_SMALL, fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,10))
    for n in NOUNS:
        decl_table(parent, n)

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
                tk.Label(r, text=cell, font=F_BODY if "Nom" not in cell and "Gen" not in cell else F_BOLD, fg=FG, bg=ROW_A, width=18, padx=6, pady=4, bd=1, relief="flat").pack(side="left", padx=1)
        tk.Label(wrap, text=adj["note"], font=F_SMALL, fg=DIM, bg=PANEL, wraplength=900, justify="left").pack(anchor="w", padx=12, pady=6)

def page_pronouns(parent):
    tk.Label(parent, text="Pronouns", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
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
    tk.Label(parent, text="Verbs — 4 Conjugations", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    tk.Label(parent, text="Present stem = infectum (present, imperfect, future). Perfect stem = perfectum (perfect, pluperfect, fut-perf). Passive uses -r endings.", font=F_SMALL, fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,10))
    for v in VERBS:
        verb_table(parent, v)

def page_irregular(parent):
    tk.Label(parent, text="Irregular Verbs — the ones you can't escape", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    for irr in IRREGULAR:
        wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        wrap.pack(fill="x", padx=20, pady=8)
        tk.Label(wrap, text=irr["label"], font=F_H2, fg=GOLD, bg=HEAD_BG).pack(fill="x", padx=12, pady=8)
        for tense, forms in irr["tables"].items():
            tframe = tk.Frame(wrap, bg=PANEL)
            tframe.pack(fill="x", padx=12, pady=4)
            tk.Label(tframe, text=tense, font=F_BOLD, fg=TCOL.get(tense.lower()[:4], FG), bg=PANEL).pack(anchor="w")
            grid = tk.Frame(wrap, bg=PANEL)
            grid.pack(fill="x", padx=12, pady=2)
            for idx, form in enumerate(forms):
                if idx >= len(PERS_LABELS) and tense != "Infinitive": continue
                cell = tk.Frame(grid, bg=ROW_A, bd=1, relief="flat")
                cell.grid(row=idx//3, column=idx%3, sticky="ew", padx=2, pady=2)
                grid.columnconfigure(idx%3, weight=1)
                pers = PERS_LABELS[idx] if idx < len(PERS_LABELS) else ""
                if pers: tk.Label(cell, text=pers, font=F_SMALL, fg=DIM, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(4,0))
                tk.Label(cell, text=form, font=F_BODY, fg=FG, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(0,6))

def page_reference(parent):
    tk.Label(parent, text="Reference — Endings Cheat Sheet", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    ref = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    ref.pack(fill="x", padx=20, pady=8)
    txt = """
Noun endings (bare):
1st: -a, -ae, -ae, -am, -ā, -a | -ae, -ārum, -īs, -ās, -īs, -ae
2nd m: -us, -ī, -ō, -um, -ō, -e | -ī, -ōrum, -īs, -ōs, -īs, -ī
2nd n: -um, -ī, -ō, -um, -ō, -um | -a, -ōrum, -īs, -a, -īs, -a
3rd cons m/f: -, -is, -ī, -em, -e, - | -ēs, -um, -ibus, -ēs, -ibus, -ēs
3rd cons n: -, -is, -ī, -, -e, - | -a, -um, -ibus, -a, -ibus, -a
3rd i m/f: -is, -is, -ī, -em, -e, -is | -ēs, -ium, -ibus, -ēs, -ibus, -ēs
3rd i n: -e, -is, -ī, -e, -ī, -e | -ia, -ium, -ibus, -ia, -ibus, -ia
4th m: -us, -ūs, -uī, -um, -ū, -us | -ūs, -uum, -ibus, -ūs, -ibus, -ūs
4th n: -ū, -ūs, -ū, -ū, -ū, -ū | -ua, -uum, -ibus, -ua, -ibus, -ua
5th: -ēs, -eī, -eī, -em, -ē, -ēs | -ēs, -ērum, -ēbus, -ēs, -ēbus, -ēs

Verb endings:
Active: -ō, -s, -t, -mus, -tis, -nt
Passive: -or, -ris, -tur, -mur, -minī, -ntur
Imperfect: -bam, -bās, -bat, -bāmus, -bātis, -bant (1st/2nd); -ēbam (3rd/4th)
Future: -bō, -bis, -bit (1st/2nd); -am, -ēs, -et (3rd/4th)
Perfect: -ī, -istī, -it, -imus, -istis, -ērunt
Pluperfect: -eram etc. Future Perfect: -erō etc.
Imperatives: -ā, -āte (1st); -ē, -ēte (2nd); -e, -ite (3rd); -ī, -īte (4th)
Infinitives: -āre, -ēre, -ere, -īre | Perfect -isse, Passive -ārī, -ērī, -ī, -īrī
"""
    tk.Label(ref, text=txt.strip(), font=("Courier New", 12), fg=FG, bg=PANEL, justify="left", anchor="w").pack(fill="x", padx=12, pady=10)

def page_memory(parent):
    tk.Label(parent, text="Memory Aids", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    aids = [
        ("1st Declension Chant", "a, ae, ae, am, ā, a — ae, ārum, īs, ās, īs, ae\nSing it to 'Twinkle Twinkle'. Feminine, mostly."),
        ("2nd Declension Masc", "us, ī, ō, um, ō, e — ī, ōrum, īs, ōs, īs, ī\nVocative -e! Domine! Brute!"),
        ("Neuter Rule", "Neuter rule: Nom = Acc = Voc. Always. And plural ends in -a. bellum, bella; corpus, corpora; mare, maria; cornū, cornua."),
        ("3rd Decl Trick", "Find genitive: rēx, rēgis → stem rēg-. i-stem if gen pl -ium. Two consonants at end? Probably i-stem (urbs, mōns)."),
        ("Verb Ladder", "Present stem: amā- → amō, amābam, amābō\nPerfect stem: amāv- → amāvī, amāveram, amāverō\nPassive: add -r: amor, amābar, amābor"),
        ("esse is essential", "sum, es, est, sumus, estis, sunt\nImperfect: eram, erās, erat... Future: erō, eris, erit... Perfect: fuī, fuistī, fuit... Subj: sim, sīs, sit..."),
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
        tk.Checkbutton(top, text="Ignore macrons", variable=self.opt_var, bg=HEAD_BG, fg=DIM, selectcolor=PANEL2, activebackground=HEAD_BG, command=self.toggle_ignore).pack(side="right", padx=8)

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
        # simple spaced: good cards go to end, bad cards reappear soon
        if good:
            # push further
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
        tk.Label(top, text="Worksheet — Fill the endings", font=F_H2, fg=GOLD, bg=HEAD_BG).pack(side="left", padx=16, pady=12)
        tk.Label(top, text="Type endings or full forms. Gold = to memorize.", font=F_SMALL, fg=DIM, bg=HEAD_BG).pack(side="left", padx=12)

        self.scroll = Scroll(self)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=12)

        self.entries = []  # list of (entry, expected)

        def section(title):
            tk.Label(self.scroll.inner, text=title, font=F_H2, fg=GOLD, bg=BG).pack(anchor="w", pady=(20,6))

        def make_decl_block(noun):
            section(f"{noun['title']} — {noun['word']} ({noun['meaning']})")
            forms = noun_forms(noun)
            grid = tk.Frame(self.scroll.inner, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
            grid.pack(fill="x", pady=4)
            # headers
            hdr = tk.Frame(grid, bg=HEAD_BG)
            hdr.pack(fill="x")
            for txt in ["Case", "Singular (stem+ending)", "Plural"]:
                tk.Label(hdr, text=txt, font=F_SMALL, fg=DIM, bg=HEAD_BG, width=24).pack(side="left", padx=8, pady=6)
            for i, case in enumerate(CASES):
                row = tk.Frame(grid, bg=ROW_A if i%2==0 else ROW_B)
                row.pack(fill="x", padx=1, pady=1)
                tk.Frame(row, bg=CASE_COL[i], width=4).pack(side="left", fill="y")
                tk.Label(row, text=CASE_ABBR[i], font=F_BOLD, fg=CASE_COL[i], bg=row["bg"], width=6).pack(side="left", padx=8, pady=8)
                for num_idx, num in enumerate(("sg","pl")):
                    stem, end = forms[num][i]
                    full = stem+end
                    cell = tk.Frame(row, bg=row["bg"])
                    cell.pack(side="left", fill="x", expand=True, padx=8, pady=4)
                    e = tk.Entry(cell, font=F_BODY, bg=PANEL2, fg=FG, relief="flat", bd=0, width=18)
                    e.pack(side="left", ipady=4, padx=4)
                    tk.Label(cell, text=f"→ {full}", font=F_SMALL, fg=DIM, bg=row["bg"]).pack(side="left", padx=6)
                    self.entries.append((e, full, full))

        # Build 3 representative blocks for worksheet (not all 10 to keep printable)
        for key in ["1","2m","3c"]:
            n = next(x for x in NOUNS if x["key"]==key)
            make_decl_block(n)

        # Verb worksheet
        section("Verbs — Conjugation Drill")
        for v in VERBS[:3]:
            wrap = tk.Frame(self.scroll.inner, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
            wrap.pack(fill="x", pady=6)
            tk.Label(wrap, text=v["label"], font=F_BOLD, fg=GOLD, bg=HEAD_BG).pack(fill="x", padx=12, pady=6)
            for tense in ["Present Active","Imperfect Active","Perfect Active"]:
                if tense not in v["tables"]: continue
                t = tk.Frame(wrap, bg=PANEL)
                t.pack(fill="x", padx=12, pady=4)
                tk.Label(t, text=tense, font=F_SMALL, fg=TCOL.get(tense.lower()[:4], FG), bg=PANEL).pack(anchor="w")
                grid = tk.Frame(wrap, bg=PANEL)
                grid.pack(fill="x", padx=12, pady=2)
                for idx, form in enumerate(v["tables"][tense]):
                    cell = tk.Frame(grid, bg=ROW_A, bd=1, relief="flat")
                    cell.grid(row=idx//3, column=idx%3, sticky="ew", padx=2, pady=2)
                    grid.columnconfigure(idx%3, weight=1)
                    tk.Label(cell, text=PERS_LABELS[idx], font=F_SMALL, fg=DIM, bg=cell["bg"]).pack(anchor="w", padx=6, pady=(4,0))
                    e = tk.Entry(cell, font=F_BODY, bg=PANEL2, fg=FG, relief="flat", bd=0)
                    e.pack(fill="x", padx=6, pady=(2,6), ipady=4)
                    self.entries.append((e, form, form))

        # controls
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=20, pady=10)
        tk.Label(ctrl, text="Tip: Leave blank to show answer key after grading.", font=F_SMALL, fg=DIM, bg=BG).pack(side="left")
        def grade():
            correct=0; total=0
            for entry, expected, full in self.entries:
                user = entry.get().strip()
                total+=1
                if not user:
                    entry.config(bg=PANEL2); continue
                if normalize(user, self.app.opts.get("ignore",True)) == normalize(expected, self.app.opts.get("ignore",True)) or normalize(user, self.app.opts.get("ignore",True)) in normalize(full, self.app.opts.get("ignore",True)):
                    correct+=1; entry.config(bg="#1a2e1f")
                else:
                    entry.config(bg="#2e1a1a")
            messagebox.showinfo("Result", f"Score: {correct}/{total} (blank = not counted as wrong)\n\nGreen = correct, Red = check ending.\n\nMacrons ignored if toggle on.")
        def clear_all():
            for e,_,_ in self.entries:
                e.delete(0, tk.END); e.config(bg=PANEL2)
        def export_html():
            # simple export similar to original
            path = os.path.join(os.path.expanduser("~"), "latin_worksheet.html")
            # build minimal
            html_rows = []
            for entry, expected, full in self.entries[:60]:
                html_rows.append(f"<tr><td><span class='b'></span></td><td>{html.escape(full)}</td></tr>")
            page = f"<!doctype html><meta charset='utf-8'><title>Latin Worksheet</title><style>body{{font:16px Georgia;margin:40px}} table{{border-collapse:collapse}} td{{border:1px solid #bbb;padding:8px 14px}} .b{{display:inline-block;min-width:90px;border-bottom:1px solid #000}}</style><h1>Latin Worksheet</h1><table>{''.join(html_rows)}</table>"
            try:
                with open(path,"w",encoding="utf-8") as f: f.write(page)
                webbrowser.open("file://"+path)
            except Exception as e:
                messagebox.showerror("Export failed", str(e))

        for txt,cmd in [("Grade ✓", grade), ("Clear", clear_all), ("Export HTML", export_html)]:
            b = tk.Label(ctrl, text=txt, bg=GOLD if "Grade" in txt else PANEL2, fg=BG if "Grade" in txt else FG, font=F_BTN, padx=16, pady=8, cursor="hand2")
            b.pack(side="right", padx=6)
            b.bind("<Button-1>", lambda e, c=cmd: c())

# ─── APP SHELL (same nav as original) ───────────────────────────────────────
NAV = [("GUIDE", None),
       ("Overview", lambda p, a: scrolled(page_overview)(p)),
       ("Nouns", lambda p, a: scrolled(page_nouns)(p)),
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

ICONS = {"Overview":"✦","Nouns":"Ⅰ","Adjectives":"Ⅱ","Pronouns":"Ⅲ","Verbs":"Ⅳ","Irregular Verbs":"Ⅴ","Reference":"§","Flashcards":"◈","Type-in Drill":"⌨","Worksheet":"✎","Memory Aids":"♪"}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Latina · Grammar Studio — Enhanced")
        self.geometry("1280x860")
        self.minsize(1100, 720)
        self.configure(bg=BG)
        self.opts = {"ignore": True}
        self.prog = load_progress()
        self.cards = build_cards()
        self.pages, self.cur, self.navbtns = {}, None, {}

        head = tk.Frame(self, bg=HEAD_BG)
        head.pack(fill="x")
        label(head, "LATINA", fg=GOLD, font=F_TITLE, bg=HEAD_BG).pack(side="left", padx=(24,12), pady=(12,8))
        label(head, "Grammar Studio  ·  Enhanced · declensions & conjugations · color-coded", fg=DIM, font=(SERIF, 14, "italic"), bg=HEAD_BG).pack(side="left", pady=(20,0))

        self.strip = tk.Canvas(self, height=4, bg=BG, highlightthickness=0)
        self.strip.pack(fill="x")
        self.strip.bind("<Configure>", self._strip)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)
        side = tk.Frame(body, bg=HEAD_BG, width=220)
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

        self.foot = label(self, "Tip: macrons ignored by default — toggle Ignore macrons in study modes to drill vowel length. Space=show, 1=again, 3=good.", fg=DIM, font=F_SMALL, bg=HEAD_BG, anchor="w", padx=18, pady=5)
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
