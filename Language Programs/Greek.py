#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HELLENIKA · Grammar Studio - Attic Greek Enhanced Edition (FIXED)
==================================================================
Color-coded, all-inclusive Attic Greek grammar guide with memorization engine.
Converted from Latin-Grammar-Studio-Enhanced.py — same fancy GUI, fully debugged.

GUIDE   Overview · Alphabet & Accents · Nouns · Adjectives · Pronouns · Verbs · Irregular Verbs · Reference
STUDY   Flashcards (spaced repetition) · Type-in Drill · Worksheet · Memory Aids

Run: python3 Attic-Greek-Grammar-Studio-FIXED.py
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

# ─── THEME (same as Latin Enhanced) ─────────────────────────────────────────
BG, PANEL, PANEL2 = "#11131b", "#1a1d2a", "#232739"
ROW_A, ROW_B, HEAD_BG, BORDER = "#1c1f2d", "#171a26", "#0d0f16", "#333955"
FG, DIM, GOLD, GREEN, RED = "#efe6d0", "#8e93ad", "#e0b458", "#6fcf8f", "#ff6b7d"

# Attic Greek: 5 cases
CASE_COL = ["#f2c94c", "#4fd1b5", "#5fa8ff", "#ff7a7a", "#c58af9"]
TCOL = {
    "pres": "#f2c94c",
    "impf": "#4fd1b5",
    "fut": "#5fa8ff",
    "aor": "#ff7a7a",
    "perf": "#c58af9",
    "plup": "#9bdc6a",
    "mid": "#5fa8ff",
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

# ─── GREEK CORE DATA ────────────────────────────────────────────────────────
CASES = ["Nominative", "Genitive", "Dative", "Accusative", "Vocative"]
CASE_ABBR = ["Nom.", "Gen.", "Dat.", "Acc.", "Voc."]
CASE_USE = [
    ("Nominative", "who/what (does it)", "Subject; predicate", "ὁ λόγος καλός ἐστι — the word is good"),
    ("Genitive", "whose / of what", "Possession, separation, source (ablative functions)", "ὁ λόγος τοῦ ἀνθρώπου — the man's word"),
    ("Dative", "to/for/in/by whom", "Indirect object, means, place", "τῷ λόγῳ πιστεύω — I trust in the word"),
    ("Accusative", "whom/what", "Direct object; extent; motion toward", "λέγω τὸν λόγον — I speak the word"),
    ("Vocative", "O …!", "Direct address", "ὦ ἄνθρωπε! — O man!"),
]

PERS = ["1st sg. (I)", "2nd sg. (you)", "3rd sg. (he/she/it)",
        "1st pl. (we)", "2nd pl. (you all)", "3rd pl. (they)"]

def _n(key, group, title, gender, word, meaning, stem, sg, pl, ov=None, note=""):
    return dict(key=key, group=group, title=title, gender=gender, word=word,
                meaning=meaning, stem=stem, sg=sg, pl=pl, ov=ov or {}, note=note)

def noun_forms(d):
    return {num: [d["ov"].get((num, i), (d["stem"], e)) for i, e in enumerate(d[num])]
            for num in ("sg", "pl")}

NOUNS = [
    _n("1f_eta", "1st Decl", "1st Decl. fem. -η (τιμή)", "feminine", "τιμή", "honor", "τιμ",
       ["ή", "ῆς", "ῇ", "ήν", "ή"], ["αί", "ῶν", "αῖς", "άς", "αί"],
       note="η-type: gen -ης, dat -ῃ with iota subscript. Nom pl -αι."),
    _n("1f_alpha", "1st Decl", "1st Decl. fem. short -α (θάλαττα)", "feminine", "θάλαττα", "sea", "θαλαττ",
       ["α", "ης", "ῃ", "αν", "α"], ["αι", "ῶν", "αις", "ας", "αι"],
       note="Short α after ε, ι, ρ: θάλαττα, -ης, -ῃ. Long α elsewhere: χώρα, χώρας."),
    _n("1m_as", "1st Decl", "1st Decl. masc. -ας (νεανίας)", "masculine", "νεανίας", "young man", "νεανί",
       ["ας", "ου", "ᾳ", "αν", "α"], ["αι", "ῶν", "αις", "ας", "αι"],
       note="Masc 1st: nom -ας/-ης, gen -ου from 2nd decl, dat -ᾳ/-ῃ, voc -α/-η."),
    _n("1m_es", "1st Decl", "1st Decl. masc. -ης (πολίτης)", "masculine", "πολίτης", "citizen", "πολίτ",
       ["ης", "ου", "ῃ", "ην", "α"], ["αι", "ῶν", "αις", "ας", "αι"],
       note="πολίτης, gen πολίτου, dat πολίτῃ, acc πολίτην, voc πολῖτα."),
    _n("2m", "2nd Decl", "2nd Decl. masc. -ος (λόγος)", "masculine", "λόγος", "word", "λόγ",
       ["ος", "ου", "ῳ", "ον", "ε"], ["οι", "ων", "οις", "ους", "οι"],
       note="Classic o-decl. Voc -ε: λόγε. Neuter rule: nom=acc=voc."),
    _n("2n", "2nd Decl", "2nd Decl. neut. -ον (δῶρον)", "neuter", "δῶρον", "gift", "δώρ",
       ["ον", "ου", "ῳ", "ον", "ον"], ["α", "ων", "οις", "α", "α"],
       note="Neuter: nom=acc=voc sg -ον, pl -α."),
    _n("3c_k", "3rd Decl", "3rd Decl. cons. -κ (φύλαξ)", "masculine", "φύλαξ", "guard", "φύλακ",
       ["", "ος", "ι", "α", ""], ["ες", "ων", "ξι(ν)", "ας", "ες"],
       ov={("sg",0):("φύλαξ",""), ("sg",4):("φύλαξ","")},
       note="Stem φυλακ-, ξ = κ+ς. Dat pl φυλακσι → φύλαξι(ν)."),
    _n("3c_nt", "3rd Decl", "3rd Decl. -ντ (ἄρχων)", "masculine", "ἄρχων", "ruler", "ἄρχοντ",
       ["", "ος", "ι", "α", ""], ["ες", "ων", "σι(ν)", "ας", "ες"],
       ov={("sg",0):("ἄρχων",""), ("sg",4):("ἄρχων","")},
       note="ντ stems drop τ: ἄρχων < ἄρχοντ+ς. Gen ἄρχοντος."),
    _n("3n_ma", "3rd Decl", "3rd Decl. neut. -μα (σῶμα)", "neuter", "σῶμα", "body", "σώματ",
       ["", "ος", "ι", "", ""], ["α", "ων", "σι(ν)", "α", "α"],
       ov={("sg",0):("σῶμα",""), ("sg",3):("σῶμα",""), ("sg",4):("σῶμα",""),
           ("pl",0):("σώματα",""), ("pl",3):("σώματα",""), ("pl",4):("σώματα","")},
       note="τ stems: nom -μα, gen -ματος. Neuter nom=acc=voc."),
    _n("3i_polis", "3rd Decl", "3rd Decl. i-stem -ις (πόλις)", "feminine", "πόλις", "city", "πόλ",
       ["ις", "εως", "ει", "ιν", "ι"], ["εις", "εων", "εσι(ν)", "εις", "εις"],
       note="Attic mixed: gen πόλεως not *πόλιος. Dat πόλει, acc πόλιν."),
]

ADJECTIVES = [
    {
        "title": "2-1-2 Adjective: ἀγαθός, -ή, -όν (good)",
        "type": "2-1-2",
        "table": [
            ["", "Masc sg", "Fem sg", "Neut sg"],
            ["Nom", "ἀγαθός", "ἀγαθή", "ἀγαθόν"],
            ["Gen", "ἀγαθοῦ", "ἀγαθῆς", "ἀγαθοῦ"],
            ["Dat", "ἀγαθῷ", "ἀγαθῇ", "ἀγαθῷ"],
            ["Acc", "ἀγαθόν", "ἀγαθήν", "ἀγαθόν"],
            ["Voc", "ἀγαθέ", "ἀγαθή", "ἀγαθόν"],
            ["", "Masc pl", "Fem pl", "Neut pl"],
            ["Nom", "ἀγαθοί", "ἀγαθαί", "ἀγαθά"],
            ["Gen", "ἀγαθῶν", "ἀγαθῶν", "ἀγαθῶν"],
        ],
        "note": "Fem like τιμή (η-type), masc/neut like λόγος/δῶρον."
    },
    {
        "title": "3rd Decl Adj: μέγας, μεγάλη, μέγα (great) & Contract",
        "type": "3rd",
        "table": [
            ["", "M sg", "F sg", "N sg"],
            ["Nom", "μέγας", "μεγάλη", "μέγα"],
            ["Gen", "μεγάλου", "μεγάλης", "μεγάλου"],
            ["Nom pl", "μεγάλοι", "μεγάλαι", "μεγάλα"],
        ],
        "note": "Irregular stem μεγα-/μεγάλ-. Also contract adj: τιμῶν, -ῶσα, -ῶν etc."
    },
]

PRONOUNS = [
    {"title": "Article ὁ, ἡ, τό (the) – CRITICAL", "forms": [
        ["", "M sg", "F sg", "N sg", "M pl", "F pl", "N pl"],
        ["Nom", "ὁ", "ἡ", "τό", "οἱ", "αἱ", "τά"],
        ["Gen", "τοῦ", "τῆς", "τοῦ", "τῶν", "τῶν", "τῶν"],
        ["Dat", "τῷ", "τῇ", "τῷ", "τοῖς", "ταῖς", "τοῖς"],
        ["Acc", "τόν", "τήν", "τό", "τούς", "τάς", "τά"],
    ]},
    {"title": "Personal ἐγώ, σύ, ἡμεῖς, ὑμεῖς", "forms": [
        ["", "1sg", "1pl", "2sg", "2pl"],
        ["Nom", "ἐγώ", "ἡμεῖς", "σύ", "ὑμεῖς"],
        ["Gen", "ἐμοῦ/μου", "ἡμῶν", "σοῦ/σου", "ὑμῶν"],
        ["Dat", "ἐμοί/μοι", "ἡμῖν", "σοί/σοι", "ὑμῖν"],
        ["Acc", "ἐμέ/με", "ἡμᾶς", "σέ/σε", "ὑμᾶς"],
    ]},
    {"title": "Demonstrative αὐτός, οὗτος, ἐκεῖνος, ὅς", "forms": [
        ["", "M", "F", "N"],
        ["αὐτός", "αὐτός", "αὐτή", "αὐτό"],
        ["οὗτος", "οὗτος", "αὕτη", "τοῦτο"],
        ["ὅς (who)", "ὅς", "ἥ", "ὅ"],
    ]},
]

VERBS = [
    {
        "key": "luo",
        "label": "ω-verb: λύω, λύσω, ἔλυσα, λέλυκα, λέλυμαι, ἐλύθην (to loose)",
        "conj": "ω-verb",
        "tables": {
            "Present Active": ["λύω", "λύεις", "λύει", "λύομεν", "λύετε", "λύουσι(ν)"],
            "Present Mid/Pass": ["λύομαι", "λύῃ", "λύεται", "λυόμεθα", "λύεσθε", "λύονται"],
            "Imperfect Active": ["ἔλυον", "ἔλυες", "ἔλυε(ν)", "ἐλύομεν", "ἐλύετε", "ἔλυον"],
            "Imperfect Mid/Pass": ["ἐλυόμην", "ἐλύου", "ἐλύετο", "ἐλυόμεθα", "ἐλύεσθε", "ἐλύοντο"],
            "Future Active": ["λύσω", "λύσεις", "λύσει", "λύσομεν", "λύσετε", "λύσουσι(ν)"],
            "Aorist Active": ["ἔλυσα", "ἔλυσας", "ἔλυσε(ν)", "ἐλύσαμεν", "ἐλύσατε", "ἔλυσαν"],
            "Aorist Passive": ["ἐλύθην", "ἐλύθης", "ἐλύθη", "ἐλύθημεν", "ἐλύθητε", "ἐλύθησαν"],
            "Perfect Active": ["λέλυκα", "λέλυκας", "λέλυκε(ν)", "λελύκαμεν", "λελύκατε", "λελύκασι(ν)"],
            "Perfect Mid/Pass": ["λέλυμαι", "λέλυσαι", "λέλυται", "λελύμεθα", "λέλυσθε", "λέλυνται"],
        }
    },
    {
        "key": "timao",
        "label": "Contract -άω: τιμάω → τιμῶ (to honor)",
        "conj": "-άω contract",
        "tables": {
            "Present Active (contracted)": ["τιμῶ", "τιμᾷς", "τιμᾷ", "τιμῶμεν", "τιμᾶτε", "τιμῶσι(ν)"],
            "Present Mid (contracted)": ["τιμῶμαι", "τιμᾷ", "τιμᾶται", "τιμώμεθα", "τιμᾶσθε", "τιμῶνται"],
            "Uncontracted → Contracted": ["τιμάω→τιμῶ", "τιμάεις→τιμᾷς", "τιμάει→τιμᾷ", "τιμάομεν→τιμῶμεν", "τιμάετε→τιμᾶτε", "τιμάουσι→τιμῶσι"],
        }
    },
    {
        "key": "poieo",
        "label": "Contract -έω / -όω: ποιέω → ποιῶ, δηλόω → δηλῶ",
        "conj": "-έω / -όω",
        "tables": {
            "ποιέω → ποιῶ": ["ποιῶ", "ποιεῖς", "ποιεῖ", "ποιοῦμεν", "ποιεῖτε", "ποιοῦσι(ν)"],
            "δηλόω → δηλῶ": ["δηλῶ", "δηλοῖς", "δηλοῖ", "δηλοῦμεν", "δηλοῦτε", "δηλοῦσι(ν)"],
        }
    },
]

IRREGULAR = [
    {
        "label": "εἰμί, ἔσομαι, — to be (suppletive)",
        "tables": {
            "Present": ["εἰμί", "εἶ", "ἐστί(ν)", "ἐσμέν", "ἐστέ", "εἰσί(ν)"],
            "Imperfect": ["ἦ / ἦν", "ἦσθα", "ἦν", "ἦμεν", "ἦτε", "ἦσαν"],
            "Future": ["ἔσομαι", "ἔσῃ", "ἔσται", "ἐσόμεθα", "ἔσεσθε", "ἔσονται"],
            "Subjunctive": ["ὦ", "ᾖς", "ᾖ", "ὦμεν", "ἦτε", "ὦσι(ν)"],
            "Optative": ["εἴην", "εἴης", "εἴη", "εἴημεν", "εἴητε", "εἴησαν"],
            "Infinitive": ["εἶναι", "ἔσεσθαι"],
            "Imperative": ["ἴσθι", "ἔστω", "ἔστε", "ἔστων"],
        }
    },
    {
        "label": "δίδωμι, δώσω, ἔδωκα, δέδωκα, δέδομαι, ἐδόθην (to give) – μι-verb",
        "tables": {
            "Present Active": ["δίδωμι", "δίδως", "δίδωσι(ν)", "δίδομεν", "δίδοτε", "διδόασι(ν)"],
            "Imperfect Active": ["ἐδίδουν", "ἐδίδους", "ἐδίδου", "ἐδίδομεν", "ἐδίδοτε", "ἐδίδοσαν"],
            "Aorist Active": ["ἔδωκα", "ἔδωκας", "ἔδωκε(ν)", "ἔδομεν", "ἔδοτε", "ἔδοσαν"],
            "Perfect Mid": ["δέδομαι", "δέδοσαι", "δέδοται", "δεδόμεθα", "δέδοσθε", "δέδονται"],
            "Aorist Passive": ["ἐδόθην", "ἐδόθης", "ἐδόθη", "ἐδόθημεν", "ἐδόθητε", "ἐδόθησαν"],
        }
    },
    {
        "label": "τίθημι & ἵστημι (μι-verbs)",
        "tables": {
            "τίθημι Pres": ["τίθημι", "τίθης", "τίθησι(ν)", "τίθεμεν", "τίθετε", "τιθέασι(ν)"],
            "ἵστημι Pres": ["ἵστημι", "ἵστης", "ἵστησι(ν)", "ἵσταμεν", "ἵστατε", "ἱστᾶσι(ν)"],
            "τίθημι Aor": ["ἔθηκα", "ἔθηκας", "ἔθηκε(ν)", "ἔθεμεν", "ἔθετε", "ἔθεσαν"],
        }
    },
]

PERS_LABELS = PERS

# ─── HELPERS ────────────────────────────────────────────────────────────────
def strip_accents(s: str) -> str:
    # remove all diacritics + movable nu
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = unicodedata.normalize("NFC", s)
    return s.lower().replace("(ν)", "").replace("ν", "").strip()

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
        with open(os.path.join(os.path.expanduser("~"), ".hellenika_progress.json"), "w", encoding="utf-8") as f:
            json.dump(prog, f)
    except:
        pass

def load_progress():
    try:
        with open(os.path.join(os.path.expanduser("~"), ".hellenika_progress.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def build_cards():
    cards = []
    for n in NOUNS:
        forms = noun_forms(n)
        for num in ("sg", "pl"):
            for i, case in enumerate(CASE_ABBR):
                stem, end = forms[num][i]
                full = stem + end
                # check override
                if (num, i) in n["ov"]:
                    full = n["ov"][(num, i)][0]
                if not full or full == "—":
                    continue
                q = f"{n['word']} ({n['meaning']}) — {case} {num}"
                cards.append(dict(q=q, a=full, type="noun", key=n["key"], group=n["group"], hint=f"{n['title']} | {n['stem']}+{n[num][i]}"))
    for v in VERBS:
        for tense, forms in v["tables"].items():
            for idx, form in enumerate(forms[:6]):
                if not form:
                    continue
                # take first variant before →
                clean = form.split("→")[-1].strip() if "→" in form else form.split("/")[0].strip()
                q = f"{v['key']} — {tense} — {PERS_LABELS[idx]}"
                cards.append(dict(q=q, a=clean, type="verb", key=v["key"], group=tense, hint=v["label"]))
    for irr in IRREGULAR:
        for tense, forms in irr["tables"].items():
            for idx, form in enumerate(forms[:6]):
                if not form:
                    continue
                pers = PERS_LABELS[idx] if idx < len(PERS_LABELS) else ""
                q = f"{irr['label'].split(',')[0]} — {tense} {pers}"
                cards.append(dict(q=q, a=form.split("/")[0].strip(), type="irr", hint=irr["label"]))
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
    header = tk.Frame(wrap, bg=HEAD_BG)
    header.pack(fill="x")
    label(header, f"{noun['title']} — {noun['word']}, {noun['meaning']}", font=F_H2, fg=GOLD, bg=HEAD_BG).pack(side="left", padx=12, pady=8)
    label(header, f"{noun['gender']} · stem {noun['stem']}-", font=F_SMALL, fg=DIM, bg=HEAD_BG).pack(side="right", padx=12)

    grid = tk.Frame(wrap, bg=PANEL)
    grid.pack(fill="x", padx=1, pady=1)
    for col, txt in enumerate(["", "Singular", "Plural"]):
        l = tk.Label(grid, text=txt, font=F_BOLD, fg=DIM, bg=ROW_B, bd=0, padx=10, pady=6)
        l.grid(row=0, column=col, sticky="ew", padx=1, pady=1)
    grid.columnconfigure(1, weight=1)
    grid.columnconfigure(2, weight=1)

    for i, case in enumerate(CASES):
        abbr = CASE_ABBR[i]
        cell_bg = ROW_A if i % 2 == 0 else ROW_B
        case_frame = tk.Frame(grid, bg=cell_bg)
        case_frame.grid(row=i+1, column=0, sticky="nsew", padx=1, pady=1)
        tk.Frame(case_frame, bg=CASE_COL[i], width=4).pack(side="left", fill="y")
        tk.Label(case_frame, text=f"{abbr}\n{case[:3]}", font=F_SMALL, fg=FG, bg=case_frame["bg"], justify="left", padx=8, pady=4).pack(side="left")

        for num_idx, num in enumerate(("sg", "pl")):
            stem, end = forms[num][i]
            override = noun["ov"].get((num, i))
            if override:
                full = override[0]
                stem_display = ""
                end_display = full
                combined = full
            else:
                full = stem + end
                stem_display = stem
                end_display = end
                combined = full
            cell = tk.Frame(grid, bg=cell_bg)
            cell.grid(row=i+1, column=num_idx+1, sticky="ew", padx=1, pady=1)
            if stem_display:
                tk.Label(cell, text=stem_display, font=F_BODY, fg=DIM, bg=cell_bg).pack(side="left", padx=(12,0), pady=6)
                tk.Label(cell, text=end_display, font=F_BOLD, fg=GOLD, bg=cell_bg).pack(side="left", pady=6)
                tk.Label(cell, text=f"  {combined}", font=F_BODY, fg=FG, bg=cell_bg).pack(side="left", padx=8)
            else:
                tk.Label(cell, text=combined, font=F_BOLD, fg=GOLD, bg=cell_bg).pack(side="left", padx=12, pady=6)
    if noun["note"]:
        label(wrap, f"Note: {noun['note']}", font=F_SMALL, fg=DIM, bg=PANEL, wraplength=900, justify="left", anchor="w").pack(fill="x", padx=12, pady=6)

def verb_table(parent, verb):
    wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    wrap.pack(fill="x", pady=8)
    header = tk.Frame(wrap, bg=HEAD_BG)
    header.pack(fill="x")
    label(header, verb["label"], font=F_H2, fg=GOLD, bg=HEAD_BG).pack(side="left", padx=12, pady=8)
    label(header, f"{verb['conj']} | {verb.get('mean','') if 'mean' in verb else ''}", font=F_SMALL, fg=DIM, bg=HEAD_BG).pack(side="right", padx=12)

    for tense, forms in verb["tables"].items():
        # choose color
        tcol = GOLD
        tl = tense.lower()
        if "pres" in tl: tcol = TCOL["pres"]
        elif "impf" in tl or "imperfect" in tl: tcol = TCOL["impf"]
        elif "fut" in tl: tcol = TCOL["fut"]
        elif "aor" in tl: tcol = TCOL["aor"]
        elif "perf" in tl: tcol = TCOL["perf"]
        elif "mid" in tl: tcol = TCOL["mid"]

        tframe = tk.Frame(wrap, bg=PANEL)
        tframe.pack(fill="x", padx=8, pady=(10,2))
        tk.Frame(tframe, bg=tcol, width=4).pack(side="left", fill="y", padx=(0,8))
        label(tframe, tense, font=F_BOLD, fg=tcol, bg=PANEL).pack(side="left")

        grid = tk.Frame(wrap, bg=PANEL)
        grid.pack(fill="x", padx=12, pady=2)
        for idx, form in enumerate(forms):
            if idx >= 6 and "→" not in form:
                continue
            r = idx // 3
            c = idx % 3
            cell = tk.Frame(grid, bg=ROW_A if r%2==0 else ROW_B, bd=1, relief="flat")
            cell.grid(row=r, column=c, sticky="ew", padx=2, pady=2)
            grid.columnconfigure(c, weight=1)
            pers = PERS_LABELS[idx] if idx < len(PERS_LABELS) else f"form {idx+1}"
            if "→" not in form:
                label(cell, pers, font=F_SMALL, fg=DIM, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(4,0))
            label(cell, form, font=F_BODY, fg=FG, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(0,6))

# ─── PAGES ──────────────────────────────────────────────────────────────────
def page_overview(parent):
    tk.Label(parent, text="HELLENIKA", font=F_TITLE, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(20,4))
    tk.Label(parent, text="Attic Greek — color-coded case & tense map, converted from Latin Studio.", font=(SERIF, 14, "italic"), fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,20))

    card_wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    card_wrap.pack(fill="x", padx=20, pady=8)
    tk.Label(card_wrap, text="The 5 Cases — color code (Attic has no Ablative)", font=F_H2, fg=GOLD, bg=PANEL).pack(anchor="w", padx=12, pady=8)
    for i, (case, who, use, ex) in enumerate(CASE_USE):
        row = tk.Frame(card_wrap, bg=ROW_A if i%2==0 else ROW_B)
        row.pack(fill="x", padx=1, pady=1)
        tk.Frame(row, bg=CASE_COL[i], width=5).pack(side="left", fill="y")
        tk.Label(row, text=CASE_ABBR[i], font=F_BOLD, fg=CASE_COL[i], bg=row["bg"], width=6).pack(side="left", padx=8, pady=8)
        tk.Label(row, text=f"{case} — {who}", font=F_BODY, fg=FG, bg=row["bg"]).pack(side="left")
        tk.Label(row, text=f"· {use} · {ex}", font=F_SMALL, fg=DIM, bg=row["bg"], wraplength=500, justify="left").pack(side="left", padx=12)

    for title, txt in [
        ("3 Declensions in 20 seconds", "1st (-α/-η, f & -ας/-ης m): τιμή, θάλαττα, νεανίας, πολίτης. 2nd (-ος m, -ον n): λόγος, δῶρον. 3rd (consonant stems m/f/n): φύλαξ (φυλακ-), ἄρχων (ἄρχοντ-), σῶμα (σωματ-), πόλις. Find stem from gen sg: φύλακος → φυλακ-."),
        ("Verbs: ω-verbs, contract, μι-verbs + εἰμί", "6 principal parts: present λύω, future λύσω, aorist ἔλυσα, perfect act λέλυκα, perfect mid λέλυμαι, aorist pass ἐλύθην. Voices: Active, Middle (for oneself), Passive (shared forms except fut/aor). Contract: τιμάω→τιμῶ (α+ω=ω), ποιέω→ποιῶ, δηλόω→δηλῶ. μι-verbs: δίδωμι, τίθημι, ἵστημι with -μι endings."),
        ("Why color?", "Gold = ending to memorize. Dim = stem. Case colors on left border match flashcards. Tense colors: Yellow Pres, Teal Impf, Blue Fut, Red Aor, Purple Perf, Green Plup."),
        ("Alphabet & breathing", "24 letters: α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ/ς τ υ φ χ ψ ω. Rough ῾ = h- (ὁ=ho), smooth ᾿. Iota subscript ᾳ ῃ ῳ. Movable ν: λέγουσι(ν) before vowel. Accent recessive in verbs, persistent in nouns."),
    ]:
        c = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        c.pack(fill="x", padx=20, pady=6)
        tk.Label(c, text=title, font=F_H2, fg=GOLD, bg=PANEL).pack(anchor="w", padx=12, pady=(8,2))
        tk.Label(c, text=txt, font=F_BODY, fg=FG, bg=PANEL, wraplength=900, justify="left").pack(anchor="w", padx=12, pady=(0,10))

def page_alphabet(parent):
    tk.Label(parent, text="Alphabet & Accents", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    wrap.pack(fill="x", padx=20, pady=8)
    txt = """
α alpha a, β beta b, γ gamma g (ng before κγχξ), δ delta d, ε epsilon e (short),
ζ zeta zd/sd, η eta ē (long), θ theta th, ι iota i, κ kappa k, λ lambda l,
μ mu m, ν nu n, ξ xi x (=ks), ο omicron o (short), π pi p, ρ rho r (rough ῥ = rh),
σ/ς sigma s, τ tau t, υ upsilon y/u, φ phi ph, χ chi kh, ψ psi ps (=bs), ω omega ō (long).

Breathings: rough ῾ = h- : ὁ = ho, ἡ = hē. Smooth ᾿ = no h. Over initial ρ always rough: ῥήτωρ rhētōr.
Iota subscript: ᾳ ῃ ῳ = long αηω + iota (was pronounced earlier).
Accents: acute ´ (oxytone), grave ` (replaces acute on ultima before another word), circumflex ῀ (perispomenon) only on long.
Enclitics: εἰμί, ἐστί(ν) throws accent back: ἄνθρωπός τις.
Movable ν: ἐστί(ν), λέγουσι(ν), ἔλυσε(ν) — add ν before vowel or pause.
Elision: ἀλλ' < ἀλλά, crasis: κἀγώ < καὶ ἐγώ, prodelision.
"""
    tk.Label(wrap, text=txt.strip(), font=F_BODY, fg=FG, bg=PANEL, justify="left", wraplength=850).pack(padx=12, pady=10)

def page_nouns(parent):
    tk.Label(parent, text="Nouns — 3 Declensions (Attic)", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    tk.Label(parent, text="Endings are gold. Stem is dim. Left bar = case color. 5 cases only (no Ablative).", font=F_SMALL, fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,10))
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
                tk.Label(r, text=cell, font=F_BODY, fg=FG, bg=ROW_A, width=18, padx=6, pady=4, bd=1, relief="flat").pack(side="left", padx=1)
        tk.Label(wrap, text=adj["note"], font=F_SMALL, fg=DIM, bg=PANEL, wraplength=900, justify="left").pack(anchor="w", padx=12, pady=6)

def page_pronouns(parent):
    tk.Label(parent, text="Pronouns & Article", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    tk.Label(parent, text="Article ὁ ἡ τό is MANDATORY in Greek (Latin has none).", font=F_SMALL, fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,10))
    for pr in PRONOUNS:
        wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        wrap.pack(fill="x", padx=20, pady=8)
        tk.Label(wrap, text=pr["title"], font=F_H2, fg=GOLD, bg=HEAD_BG).pack(fill="x", padx=12, pady=8)
        for row in pr["forms"]:
            r = tk.Frame(wrap, bg=PANEL)
            r.pack(fill="x", padx=8, pady=1)
            for cell in row:
                tk.Label(r, text=cell, font=F_BODY, fg=FG, bg=ROW_A, width=16, padx=6, pady=4, bd=1, relief="flat").pack(side="left", padx=1)

def page_verbs(parent):
    tk.Label(parent, text="Verbs — ω-verbs & Contract", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    tk.Label(parent, text="Augment ἐ- in past (imperfect/aorist). Reduplication λε- in perfect. Middle = for oneself. Passive shares Middle forms except Fut/Aor.", font=F_SMALL, fg=DIM, bg=BG).pack(anchor="w", padx=20, pady=(0,10))
    for v in VERBS:
        verb_table(parent, v)

def page_irregular(parent):
    tk.Label(parent, text="Irregular Verbs — εἰμί & μι-verbs", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    for irr in IRREGULAR:
        wrap = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
        wrap.pack(fill="x", padx=20, pady=8)
        tk.Label(wrap, text=irr["label"], font=F_H2, fg=GOLD, bg=HEAD_BG).pack(fill="x", padx=12, pady=8)
        for tense, forms in irr["tables"].items():
            tframe = tk.Frame(wrap, bg=PANEL)
            tframe.pack(fill="x", padx=12, pady=4)
            tcol = GOLD
            tl = tense.lower()
            if "pres" in tl: tcol = TCOL["pres"]
            elif "impf" in tl or "imperfect" in tl: tcol = TCOL["impf"]
            elif "fut" in tl: tcol = TCOL["fut"]
            elif "aor" in tl: tcol = TCOL["aor"]
            elif "perf" in tl: tcol = TCOL["perf"]
            tk.Label(tframe, text=tense, font=F_BOLD, fg=tcol, bg=PANEL).pack(anchor="w")
            grid = tk.Frame(wrap, bg=PANEL)
            grid.pack(fill="x", padx=12, pady=2)
            for idx, form in enumerate(forms):
                if idx >= len(PERS_LABELS) and tense not in ("Infinitive", "Imperative"): 
                    continue
                cell = tk.Frame(grid, bg=ROW_A, bd=1, relief="flat")
                cell.grid(row=idx//3, column=idx%3, sticky="ew", padx=2, pady=2)
                grid.columnconfigure(idx%3, weight=1)
                pers = PERS_LABELS[idx] if idx < len(PERS_LABELS) else ""
                if pers and tense not in ("Infinitive","Imperative"):
                    tk.Label(cell, text=pers, font=F_SMALL, fg=DIM, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(4,0))
                tk.Label(cell, text=form, font=F_BODY, fg=FG, bg=cell["bg"]).pack(anchor="w", padx=8, pady=(0,6))

def page_reference(parent):
    tk.Label(parent, text="Reference — Cheat Sheet", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    ref = tk.Frame(parent, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
    ref.pack(fill="x", padx=20, pady=8)
    txt = """
Attic Noun Endings (bare):
1st fem η: -η, -ης, -ῃ, -ην, -η | -αι, -ων, -αις, -ας, -αι
1st fem α short: -α, -ης, -ῃ, -αν, -α | -αι, -ων, -αις, -ας, -αι
1st masc ας: -ας, -ου, -ᾳ, -αν, -α | -αι, -ων, -αις, -ας, -αι
1st masc ης: -ης, -ου, -ῃ, -ην, -α | -αι, -ων, -αις, -ας, -αι
2nd masc ος: -ος, -ου, -ῳ, -ον, -ε | -οι, -ων, -οις, -ους, -οι
2nd neut ον: -ον, -ου, -ῳ, -ον, -ον | -α, -ων, -οις, -α, -α
3rd cons: -, -ος, -ι, -α, - | -ες, -ων, -σι(ν), -ας, -ες ; neut -, -ος, -ι, -, - | -α, -ων, -σι, -α, -α

Verb endings ω-verb (λύω):
Present Act: -ω, -εις, -ει, -ομεν, -ετε, -ουσι(ν)
Present Mid/Pass: -ομαι, -ῃ/-ει, -εται, -όμεθα, -εσθε, -ονται
Imperfect Act: -ον, -ες, -ε(ν), -ομεν, -ετε, -ον  (+ augment ἐ-)
Imperfect Mid: -όμην, -ου, -ετο, -όμεθα, -εσθε, -οντο
Aorist Act -σα: -σα, -σας, -σε(ν), -σαμεν, -σατε, -σαν
Aorist Pass -θη: -θην, -θης, -θη, -θημεν, -θητε, -θησαν
Perfect Act: -κα, -κας, -κε(ν), -καμεν, -κατε, -κασι(ν)  (reduplication λε-)
Infinitive: -ειν, -εσθαι, -σαι, -σθαι, -ναι ; Participle: -ων, -ουσα, -ον / -όμενος / -θείς

Contract verbs:
-άω: α+ε=ᾱ, α+ο=ω, α+ει=ᾷ, α+οι=ῷ, α+ου=ω  → τιμάω = τιμῶ
-έω: ε+ε=ει, ε+ο=ου, ε+ου=ου  → ποιέω = ποιῶ
-όω: ο+ε=ου, ο+ο=ου, ο+ει=οι  → δηλόω = δηλῶ

μι-verbs: -μι, -ς, -σι(ν), -μεν, -τε, -ασι(ν)  → δίδωμι, δίδως, δίδωσι, δίδομεν, δίδοτε, διδόασι
"""
    tk.Label(ref, text=txt.strip(), font=("Courier New", 12), fg=FG, bg=PANEL, justify="left", anchor="w").pack(fill="x", padx=12, pady=10)

def page_memory(parent):
    tk.Label(parent, text="Memory Aids", font=F_H1, fg=GOLD, bg=BG).pack(anchor="w", padx=20, pady=(16,6))
    aids = [
        ("1st fem η – τιμή", "ή, ῆς, ῇ, ήν, ή — αί, ῶν, αῖς, άς, αί\nSing to 'Twinkle Twinkle'"),
        ("2nd masc ος – λόγος", "ος, ου, ῳ, ον, ε — οι, ων, οις, ους, οι\nVoc -ε! ὦ λόγε!"),
        ("Neuter Rule (like Latin)", "Neuter Nom=Acc=Voc always. Pl -α. δῶρον, δῶρα; σῶμα, σώματα; πόλις is fem exception."),
        ("3rd Decl Trick", "Find gen: φύλαξ, φύλακος → stem φυλακ-. Dat pl -σι(ν) with ν before vowel. ἄρχων < ἄρχοντ+ς."),
        ("Present λύω chant", "λύω, λύεις, λύει, λύομεν, λύετε, λύουσι — Present Middle λύομαι, λύῃ, λύεται..."),
        ("Aorist ἐ- + -σα-", "ἔλυσα, ἔλυσας, ἔλυσε, ἐλύσαμεν, ἐλύσατε, ἔλυσαν. Imperfect same but without σα."),
        ("Perfect reduplication", "λέλυκα, λέλυκας, λέλυκε — reduplicate first consonant + ε: λ→λε, γρ→γεγραφα, λαβ→εἴληφα."),
        ("εἰμί essential", "εἰμί, εἶ, ἐστί(ν), ἐσμέν, ἐστέ, εἰσί(ν) — Impf ἦν, ἦσθα, ἦν — Fut ἔσομαι — Subj ὦ, ᾖς, ᾖ — Opt εἴην."),
        ("μι-verb pattern", "δίδωμι, δίδως, δίδωσι — Aorist ἔδωκα vs root ἔδομεν. Contract all -άω → -ῶ after learning."),
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
        tk.Checkbutton(top, text="Ignore accents + movable ν (ν)", variable=self.opt_var, bg=HEAD_BG, fg=DIM, selectcolor=PANEL2, activebackground=HEAD_BG, command=self.toggle_ignore).pack(side="right", padx=8)

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
        tk.Label(top, text="Worksheet — Fill the endings (Attic Greek)", font=F_H2, fg=GOLD, bg=HEAD_BG).pack(side="left", padx=16, pady=12)
        tk.Label(top, text="Type Greek. Gold = to memorize.", font=F_SMALL, fg=DIM, bg=HEAD_BG).pack(side="left", padx=12)

        self.scroll = Scroll(self)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=12)

        self.entries = []

        def section(title):
            tk.Label(self.scroll.inner, text=title, font=F_H2, fg=GOLD, bg=BG).pack(anchor="w", pady=(20,6))

        def make_decl_block(noun):
            section(f"{noun['title']} — {noun['word']} ({noun['meaning']})")
            forms = noun_forms(noun)
            grid = tk.Frame(self.scroll.inner, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
            grid.pack(fill="x", pady=4)
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
                    ov = noun["ov"].get((num,i))
                    full = ov[0] if ov else stem+end
                    cell = tk.Frame(row, bg=row["bg"])
                    cell.pack(side="left", fill="x", expand=True, padx=8, pady=4)
                    e = tk.Entry(cell, font=F_BODY, bg=PANEL2, fg=FG, relief="flat", bd=0, width=18)
                    e.pack(side="left", ipady=4, padx=4)
                    tk.Label(cell, text=f"→ {full}", font=F_SMALL, fg=DIM, bg=row["bg"]).pack(side="left", padx=6)
                    self.entries.append((e, full, full))

        for key in ["1f_eta","2m","3c_k"]:
            n = next(x for x in NOUNS if x["key"]==key)
            make_decl_block(n)

        section("Verbs — Conjugation Drill")
        for v in VERBS[:2]:
            wrap = tk.Frame(self.scroll.inner, bg=PANEL, bd=1, relief="solid", highlightbackground=BORDER)
            wrap.pack(fill="x", pady=6)
            tk.Label(wrap, text=v["label"], font=F_BOLD, fg=GOLD, bg=HEAD_BG).pack(fill="x", padx=12, pady=6)
            for tense in ["Present Active","Present Mid/Pass","Aorist Active"]:
                if tense not in v["tables"]: continue
                t = tk.Frame(wrap, bg=PANEL)
                t.pack(fill="x", padx=12, pady=4)
                tcol = TCOL["pres"]
                tl = tense.lower()
                if "impf" in tl: tcol = TCOL["impf"]
                elif "fut" in tl: tcol = TCOL["fut"]
                elif "aor" in tl: tcol = TCOL["aor"]
                tk.Label(t, text=tense, font=F_SMALL, fg=tcol, bg=PANEL).pack(anchor="w")
                grid = tk.Frame(wrap, bg=PANEL)
                grid.pack(fill="x", padx=12, pady=2)
                for idx, form in enumerate(v["tables"][tense]):
                    cell = tk.Frame(grid, bg=ROW_A, bd=1, relief="flat")
                    cell.grid(row=idx//3, column=idx%3, sticky="ew", padx=2, pady=2)
                    grid.columnconfigure(idx%3, weight=1)
                    tk.Label(cell, text=PERS_LABELS[idx], font=F_SMALL, fg=DIM, bg=cell["bg"]).pack(anchor="w", padx=6, pady=(4,0))
                    e = tk.Entry(cell, font=F_BODY, bg=PANEL2, fg=FG, relief="flat", bd=0)
                    e.pack(fill="x", padx=6, pady=(2,6), ipady=4)
                    clean = form.split("→")[-1].strip() if "→" in form else form.split("/")[0].strip()
                    self.entries.append((e, clean, form))

        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=20, pady=10)
        tk.Label(ctrl, text="Blank = show answer after grading. Accents ignored if toggle on.", font=F_SMALL, fg=DIM, bg=BG).pack(side="left")
        def grade():
            correct=0; total=0
            for entry, expected, full in self.entries:
                user = entry.get().strip()
                total+=1
                if not user:
                    entry.config(bg=PANEL2); continue
                exp_norm = normalize(expected, self.app.opts.get("ignore",True))
                user_norm = normalize(user, self.app.opts.get("ignore",True))
                if user_norm == exp_norm or user_norm in normalize(full, self.app.opts.get("ignore",True)):
                    correct+=1; entry.config(bg="#1a2e1f")
                else:
                    entry.config(bg="#2e1a1a")
            messagebox.showinfo("Result", f"Score: {correct}/{total}\nGreen=correct, Red=check.\nMovable ν ignored.")
        def clear_all():
            for e,_,_ in self.entries:
                e.delete(0, tk.END); e.config(bg=PANEL2)
        def export_html():
            path = os.path.join(os.path.expanduser("~"), "attic_greek_worksheet.html")
            html_rows = []
            for entry, expected, full in self.entries[:60]:
                html_rows.append(f"<tr><td><span class='b'></span></td><td>{html.escape(full)}</td></tr>")
            page = f"<!doctype html><meta charset='utf-8'><title>Greek Worksheet</title><style>body{{font:16px Georgia;margin:40px}} table{{border-collapse:collapse}} td{{border:1px solid #bbb;padding:8px 14px}} .b{{display:inline-block;min-width:90px;border-bottom:1px solid #000}}</style><h1>Attic Greek Worksheet</h1><table>{''.join(html_rows)}</table>"
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

ICONS = {"Overview":"✦","Alphabet":"Ω","Nouns":"Ⅰ","Adjectives":"Ⅱ","Pronouns":"Ⅲ","Verbs":"Ⅳ","Irregular Verbs":"Ⅴ","Reference":"§","Flashcards":"◈","Type-in Drill":"⌨","Worksheet":"✎","Memory Aids":"♪"}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hellenika · Grammar Studio — Attic Greek Enhanced (FIXED)")
        self.geometry("1280x860")
        self.minsize(1100, 720)
        self.configure(bg=BG)
        self.opts = {"ignore": True}
        self.prog = load_progress()
        self.cards = build_cards()
        self.pages, self.cur, self.navbtns = {}, None, {}

        head = tk.Frame(self, bg=HEAD_BG)
        head.pack(fill="x")
        label(head, "HELLENIKA", fg=GOLD, font=F_TITLE, bg=HEAD_BG).pack(side="left", padx=(24,12), pady=(12,8))
        label(head, "Attic Greek Studio — FIXED · declensions & conjugations", fg=DIM, font=(SERIF, 14, "italic"), bg=HEAD_BG).pack(side="left", pady=(20,0))

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

        self.foot = label(self, "Tip: Accents + movable ν ignored by default — toggle in study modes. Space=show, 1=again, 3=good.", fg=DIM, font=F_SMALL, bg=HEAD_BG, anchor="w", padx=18, pady=5)
        self.foot.pack(fill="x", side="bottom")

        self.bind_all("<MouseWheel>", self._wheel)
        self.bind_all("<Button-4>", self._wheel)
        self.bind_all("<Button-5>", self._wheel)
        self.bind("<Key>", self._key)
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.show("Overview")

    def _strip(self, e):
        self.strip.delete("all")
        w = e.width / 5
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
