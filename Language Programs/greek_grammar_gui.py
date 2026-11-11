#!/usr/bin/env python3
"""
Ἑλληνικὴ Γραμματική — Ancient Greek Grammar Studio
A single-file Tkinter GUI: colour-coded reference guide, an interactive
worksheet, and a memorization drill for noun/verb endings.

Run:  python3 greek_grammar_gui.py
Standard library only (tkinter + ttk). Works fully offline.
"""

import os
import random
import unicodedata
import tkinter as tk
from tkinter import ttk, font as tkfont

# ======================================================================
# Palette & fonts
# ======================================================================

PAL = {
    "bg":      "#17140f",
    "panel":   "#1f1b14",
    "panel2":  "#262017",
    "card":    "#2a2419",
    "line":    "#4a3f2e",
    "ink":     "#f1e6cf",
    "mut":     "#a89878",
    "accent":  "#d8bf85",
    "nom":     "#6ea6ff",
    "gen":     "#6fd48f",
    "dat":     "#f0a55c",
    "acc":     "#ff8a7a",
    "voc":     "#c99cf0",
    "aug":     "#49d8d8",
    "ten":     "#e8c454",
    "end":     "#f17ab0",
    "ok":      "#6fd48f",
    "no":      "#ff8a7a",
}
CASE_COLOR = {"Nom": "nom", "Gen": "gen", "Dat": "dat", "Acc": "acc", "Voc": "voc"}
CASES = ["Nom", "Gen", "Dat", "Acc", "Voc"]
PERSONS = ["1 sg", "2 sg", "3 sg", "1 pl", "2 pl", "3 pl"]


def pick_family(root, candidates, fallback):
    try:
        available = set(tkfont.families(root))
    except Exception:
        available = set()
    for c in candidates:
        if c in available:
            return c
    return fallback


# ======================================================================
# Reference data (tokenised with '|'; tokens prefixed a: = augment /
# reduplication, t: = tense sign; the final untagged token is the ending)
# ======================================================================

ALPHABET = [
    ("Α α", "alpha", "a"), ("Β β", "beta", "b"), ("Γ γ", "gamma", "g"),
    ("Δ δ", "delta", "d"), ("Ε ε", "epsilon", "e (short)"), ("Ζ ζ", "zeta", "zd"),
    ("Η η", "eta", "ē (long)"), ("Θ θ", "theta", "th"), ("Ι ι", "iota", "i"),
    ("Κ κ", "kappa", "k"), ("Λ λ", "lambda", "l"), ("Μ μ", "mu", "m"),
    ("Ν ν", "nu", "n"), ("Ξ ξ", "xi", "x"), ("Ο ο", "omicron", "o (short)"),
    ("Π π", "pi", "p"), ("Ρ ρ", "rho", "r"), ("Σ σ/ς", "sigma", "s (ς final)"),
    ("Τ τ", "tau", "t"), ("Υ υ", "upsilon", "u / ü"), ("Φ φ", "phi", "ph"),
    ("Χ χ", "chi", "kh"), ("Ψ ψ", "psi", "ps"), ("Ω ω", "omega", "ō (long)"),
]

ARTICLE = {
    "name": "ὁ, ἡ, τό  —  \u201cthe\u201d",
    "sg": {"m": ["ὁ|", "τοῦ|", "τῷ|", "τόν|", "—"],
           "f": ["ἡ|", "τῆς|", "τῇ|", "τήν|", "—"],
           "n": ["τό|", "τοῦ|", "τῷ|", "τό|", "—"]},
    "pl": {"m": ["οἱ|", "τῶν|", "τοῖς|", "τούς|", "—"],
           "f": ["αἱ|", "τῶν|", "ταῖς|", "τάς|", "—"],
           "n": ["τά|", "τῶν|", "τοῖς|", "τά|", "—"]},
}

NOUNS = [
    {"name": "τιμή", "gloss": "honor", "type": "1st decl. · fem. η-stem",
     "sg": ["τιμ|ή", "τιμ|ῆς", "τιμ|ῇ", "τιμ|ήν", "τιμ|ή"],
     "pl": ["τιμ|αί", "τιμ|ῶν", "τιμ|αῖς", "τιμ|άς", "τιμ|αί"]},
    {"name": "χώρα", "gloss": "land", "type": "1st decl. · fem. α-stem",
     "sg": ["χώρ|α", "χώρ|ας", "χώρ|ᾳ", "χώρ|αν", "χώρ|α"],
     "pl": ["χώρ|αι", "χωρ|ῶν", "χώρ|αις", "χώρ|ας", "χώρ|αι"]},
    {"name": "πολίτης", "gloss": "citizen", "type": "1st decl. · masc.",
     "sg": ["πολίτ|ης", "πολίτ|ου", "πολίτ|ῃ", "πολίτ|ην", "πολῖτ|α"],
     "pl": ["πολῖτ|αι", "πολιτ|ῶν", "πολίτ|αις", "πολίτ|ας", "πολῖτ|αι"]},
    {"name": "λόγος", "gloss": "word", "type": "2nd decl. · masc.",
     "sg": ["λόγ|ος", "λόγ|ου", "λόγ|ῳ", "λόγ|ον", "λόγ|ε"],
     "pl": ["λόγ|οι", "λόγ|ων", "λόγ|οις", "λόγ|ους", "λόγ|οι"]},
    {"name": "δῶρον", "gloss": "gift", "type": "2nd decl. · neut.",
     "sg": ["δῶρ|ον", "δώρ|ου", "δώρ|ῳ", "δῶρ|ον", "δῶρ|ον"],
     "pl": ["δῶρ|α", "δώρ|ων", "δώρ|οις", "δῶρ|α", "δῶρ|α"]},
    {"name": "φύλαξ", "gloss": "guard", "type": "3rd decl. · consonant stem",
     "sg": ["φύλαξ|", "φύλακ|ος", "φύλακ|ι", "φύλακ|α", "φύλαξ|"],
     "pl": ["φύλακ|ες", "φυλάκ|ων", "φύλα|ξι(ν)", "φύλακ|ας", "φύλακ|ες"]},
    {"name": "σῶμα", "gloss": "body", "type": "3rd decl. · neut. -ματ",
     "sg": ["σῶμα|", "σώματ|ος", "σώματ|ι", "σῶμα|", "σῶμα|"],
     "pl": ["σώματ|α", "σωμάτ|ων", "σώμα|σι(ν)", "σώματ|α", "σώματ|α"]},
    {"name": "πόλις", "gloss": "city", "type": "3rd decl. · ι-stem",
     "sg": ["πόλις|", "πόλ|εως", "πόλ|ει", "πόλ|ιν", "πόλ|ι"],
     "pl": ["πόλ|εις", "πόλ|εων", "πόλ|εσι(ν)", "πόλ|εις", "πόλ|εις"]},
]

ADJ = {
    "name": "ἀγαθός, ἀγαθή, ἀγαθόν  —  \u201cgood\u201d",
    "sg": {"m": ["ἀγαθ|ός", "ἀγαθ|οῦ", "ἀγαθ|ῷ", "ἀγαθ|όν", "ἀγαθ|έ"],
           "f": ["ἀγαθ|ή", "ἀγαθ|ῆς", "ἀγαθ|ῇ", "ἀγαθ|ήν", "ἀγαθ|ή"],
           "n": ["ἀγαθ|όν", "ἀγαθ|οῦ", "ἀγαθ|ῷ", "ἀγαθ|όν", "ἀγαθ|όν"]},
    "pl": {"m": ["ἀγαθ|οί", "ἀγαθ|ῶν", "ἀγαθ|οῖς", "ἀγαθ|ούς", "ἀγαθ|οί"],
           "f": ["ἀγαθ|αί", "ἀγαθ|ῶν", "ἀγαθ|αῖς", "ἀγαθ|άς", "ἀγαθ|αί"],
           "n": ["ἀγαθ|ά", "ἀγαθ|ῶν", "ἀγαθ|οῖς", "ἀγαθ|ά", "ἀγαθ|ά"]},
}

PRONOUNS = [
    ("I / we", ["ἐγώ / ἡμεῖς", "ἐμοῦ (μου) / ἡμῶν", "ἐμοί (μοι) / ἡμῖν", "ἐμέ (με) / ἡμᾶς"]),
    ("you sg / pl", ["σύ / ὑμεῖς", "σοῦ (σου) / ὑμῶν", "σοί (σοι) / ὑμῖν", "σέ (σε) / ὑμᾶς"]),
]

VERB_TABLES = [
    ("Present active", ["λύ|ω", "λύ|εις", "λύ|ει", "λύ|ομεν", "λύ|ετε", "λύ|ουσι(ν)"]),
    ("Present mid./pass.", ["λύ|ομαι", "λύ|ῃ", "λύ|εται", "λυ|όμεθα", "λύ|εσθε", "λύ|ονται"]),
    ("Imperfect active", ["a:ἔ|λυ|ον", "a:ἔ|λυ|ες", "a:ἔ|λυ|ε(ν)", "a:ἐ|λύ|ομεν", "a:ἐ|λύ|ετε", "a:ἔ|λυ|ον"]),
    ("Imperfect mid./pass.", ["a:ἐ|λυ|όμην", "a:ἐ|λύ|ου", "a:ἐ|λύ|ετο", "a:ἐ|λυ|όμεθα", "a:ἐ|λύ|εσθε", "a:ἐ|λύ|οντο"]),
    ("Future active", ["λύ|t:σ|ω", "λύ|t:σ|εις", "λύ|t:σ|ει", "λύ|t:σ|ομεν", "λύ|t:σ|ετε", "λύ|t:σ|ουσι(ν)"]),
    ("Aorist active", ["a:ἔ|λυ|t:σ|α", "a:ἔ|λυ|t:σ|ας", "a:ἔ|λυ|t:σ|ε(ν)", "a:ἐ|λύ|t:σ|αμεν", "a:ἐ|λύ|t:σ|ατε", "a:ἔ|λυ|t:σ|αν"]),
    ("Aorist passive", ["a:ἐ|λύ|t:θ|ην", "a:ἐ|λύ|t:θ|ης", "a:ἐ|λύ|t:θ|η", "a:ἐ|λύ|t:θ|ημεν", "a:ἐ|λύ|t:θ|ητε", "a:ἐ|λύ|t:θ|ησαν"]),
    ("Perfect active", ["a:λέ|λυ|t:κ|α", "a:λέ|λυ|t:κ|ας", "a:λέ|λυ|t:κ|ε(ν)", "a:λε|λύ|t:κ|αμεν", "a:λε|λύ|t:κ|ατε", "a:λε|λύ|t:κ|ασι(ν)"]),
    ("Perfect mid./pass.", ["a:λέ|λυ|μαι", "a:λέ|λυ|σαι", "a:λέ|λυ|ται", "a:λε|λύ|μεθα", "a:λέ|λυ|σθε", "a:λέ|λυ|νται"]),
    ("Subjunctive active", ["λύ|ω", "λύ|ῃς", "λύ|ῃ", "λύ|ωμεν", "λύ|ητε", "λύ|ωσι(ν)"]),
    ("Optative active", ["λύ|οιμι", "λύ|οις", "λύ|οι", "λύ|οιμεν", "λύ|οιτε", "λύ|οιεν"]),
]

IMPERATIVE = [
    ("2 sg", "λῦ|ε", "λύ|ου"), ("3 sg", "λυ|έτω", "λυ|έσθω"),
    ("2 pl", "λύ|ετε", "λύ|εσθε"), ("3 pl", "λυ|έτωσαν", "λυ|έσθωσαν"),
]

INFINITIVES = [
    ("Present", "λύ|ειν", "λύ|εσθαι"), ("Future", "λύσ|ειν", "λύσ|εσθαι"),
    ("Aorist", "λῦσ|αι", "λύσ|ασθαι / λυθ|ῆναι"), ("Perfect", "λελυκ|έναι", "λελῦσθαι|"),
]

CONTRACT = {
    "τιμάω (α-contract)": ["τιμ|ῶ", "τιμ|ᾷς", "τιμ|ᾷ", "τιμ|ῶμεν", "τιμ|ᾶτε", "τιμ|ῶσι(ν)"],
    "ποιέω (ε-contract)": ["ποι|ῶ", "ποι|εῖς", "ποι|εῖ", "ποι|οῦμεν", "ποι|εῖτε", "ποι|οῦσι(ν)"],
    "δηλόω (ο-contract)": ["δηλ|ῶ", "δηλ|οῖς", "δηλ|οῖ", "δηλ|οῦμεν", "δηλ|οῦτε", "δηλ|οῦσι(ν)"],
}

IRREGULAR = {
    "εἰμί — present (\u201cbe\u201d)": ["εἰμί", "εἶ", "ἐστί(ν)", "ἐσμέν", "ἐστέ", "εἰσί(ν)"],
    "εἰμί — imperfect": ["ἦν", "ἦσθα", "ἦν", "ἦμεν", "ἦτε", "ἦσαν"],
    "εἰμί — future": ["ἔσομαι", "ἔσῃ", "ἔσται", "ἐσόμεθα", "ἔσεσθε", "ἔσονται"],
    "δίδωμι — present": ["δίδωμι", "δίδως", "δίδωσι(ν)", "δίδομεν", "δίδοτε", "διδόασι(ν)"],
    "οἶδα — perfect (\u201cknow\u201d)": ["οἶδα", "οἶσθα", "οἶδε(ν)", "ἴσμεν", "ἴστε", "ἴσασι(ν)"],
}

SYNTAX_NOTES = [
    ("Nom", "subject, predicate noun"),
    ("Gen", "possession, separation, partitive; after ἀπό, ἐκ, περί, ἀντί"),
    ("Dat", "indirect object, means, time when; after ἐν, σύν"),
    ("Acc", "direct object, extent, motion to; after εἰς, ἀνά"),
    ("Voc", "direct address — ὦ ἄνθρωπε"),
]
SYNTAX_EXTRA = [
    "Word order is free; case endings carry grammatical function.",
    "A neuter plural subject takes a singular verb.",
    "μέν … δέ (on the one hand … on the other) · γάρ (for) · ἀλλά (but) · οὖν (so)",
    "Article + participle = \u201cthe one who…\u201d (ὁ λέγων).",
    "Negatives: οὐ with the indicative, μή with everything else.",
]

# ---- plain ending inventories, used by the memorization drill ----
NOUN_ENDINGS = {
    "1st decl. η-stem (τιμή) — sg": dict(zip(CASES, ["η", "ης", "ῃ", "ην", "η"])),
    "1st decl. η-stem (τιμή) — pl": dict(zip(CASES, ["αι", "ων", "αις", "ας", "αι"])),
    "1st decl. α-stem (χώρα) — sg": dict(zip(CASES, ["α", "ας", "ᾳ", "αν", "α"])),
    "2nd decl. masc. (λόγος) — sg": dict(zip(CASES, ["ος", "ου", "ῳ", "ον", "ε"])),
    "2nd decl. masc. (λόγος) — pl": dict(zip(CASES, ["οι", "ων", "οις", "ους", "οι"])),
    "2nd decl. neut. (δῶρον) — sg": dict(zip(CASES, ["ον", "ου", "ῳ", "ον", "ον"])),
    "3rd decl. cons. (φύλαξ) — pl": dict(zip(CASES, ["ες", "ων", "σι(ν)", "ας", "ες"])),
    "3rd decl. ι-stem (πόλις) — sg": {"Gen": "εως", "Dat": "ει", "Acc": "ιν"},
}
VERB_ENDINGS = {
    "Primary active (pres/fut)": dict(zip(PERSONS, ["ω", "εις", "ει", "ομεν", "ετε", "ουσι(ν)"])),
    "Secondary active (impf/aor)": dict(zip(PERSONS, ["ον", "ες", "ε(ν)", "ομεν", "ετε", "ον"])),
    "Primary mid/pass (pres/fut)": dict(zip(PERSONS, ["ομαι", "ῃ", "εται", "όμεθα", "εσθε", "ονται"])),
    "Aorist active (add -σα-)": dict(zip(PERSONS, ["α", "ας", "ε(ν)", "αμεν", "ατε", "αν"])),
    "Perfect active (add -κα-)": dict(zip(PERSONS, ["α", "ας", "ε(ν)", "αμεν", "ατε", "ασι(ν)"])),
}
MARKERS = [
    ("Augment", "ἐ-", "prefixed to a consonant-initial stem in past indicative tenses"),
    ("Reduplication", "cons.+ε-", "prefixed in the perfect stem — λύω → λέλυκα"),
    ("Future/aorist sign", "-σ-", "λύσω, ἔλυσα"),
    ("Aorist passive sign", "-θ-", "ἐλύθην"),
    ("Perfect active sign", "-κ-", "λέλυκα"),
]

# ======================================================================
# Worksheet question bank
# ======================================================================

WORKSHEET = [
    ("Nouns & article", [
        ("λόγος → genitive singular", "λόγου"),
        ("λόγος → accusative plural", "λόγους"),
        ("χώρα → dative singular", "χώρᾳ"),
        ("τιμή → genitive plural", "τιμῶν"),
        ("πολίτης → vocative singular", "πολῖτα"),
        ("δῶρον → nominative plural", "δῶρα"),
        ("φύλαξ → genitive singular", "φύλακος"),
        ("σῶμα → dative plural", "σώμασι(ν)"),
        ("πόλις → genitive singular", "πόλεως"),
        ("πόλις → accusative plural", "πόλεις"),
        ("Article, feminine genitive singular", "τῆς"),
        ("Article, neuter dative plural", "τοῖς"),
        ("Article, masculine accusative plural", "τούς"),
    ]),
    ("Verbs — λύω", [
        ("1 sg present active", "λύω"),
        ("3 pl present active", "λύουσι(ν)"),
        ("2 sg present middle/passive", "λύῃ"),
        ("1 pl imperfect active", "ἐλύομεν"),
        ("3 sg future active", "λύσει"),
        ("1 sg aorist active", "ἔλυσα"),
        ("3 pl aorist active", "ἔλυσαν"),
        ("1 sg aorist passive", "ἐλύθην"),
        ("1 sg perfect active", "λέλυκα"),
        ("Present active infinitive", "λύειν"),
    ]),
    ("Contract & irregular verbs", [
        ("τιμάω → 1 sg present", "τιμῶ"),
        ("ποιέω → 3 sg present", "ποιεῖ"),
        ("δηλόω → 3 sg present", "δηλοῖ"),
        ("εἰμί → 3 pl present", "εἰσί(ν)"),
        ("εἰμί → 1 sg imperfect", "ἦν"),
        ("εἰμί → 3 sg future", "ἔσται"),
        ("δίδωμι → 3 pl present", "διδόασι(ν)"),
    ]),
]

# ======================================================================
# Answer checking
# ======================================================================

def strip_accents(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", s)


def normalize(s, lax=True):
    s = s.strip().lower().replace("ς", "σ")
    if lax:
        s = strip_accents(s)
    return " ".join(s.split())


def answer_variants(ans):
    out = []
    for part in ans.split("/"):
        part = part.strip()
        if "(ν)" in part:
            out.append(part.replace("(ν)", ""))
            out.append(part.replace("(ν)", "ν"))
        else:
            out.append(part)
    return out


def check_answer(user, ans, lax=True):
    u = normalize(user, lax)
    if not u:
        return False
    return any(normalize(v, lax) == u for v in answer_variants(ans))


# ======================================================================
# Scrollable frame helper
# ======================================================================

class ScrollFrame(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.canvas = tk.Canvas(self, bg=PAL["bg"], highlightthickness=0)
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas, style="Panel.TFrame")
        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self._win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(self._win, width=e.width),
        )
        self.canvas.configure(yscrollcommand=vsb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        for widget in (self.canvas, self.inner):
            widget.bind("<MouseWheel>", self._on_wheel)
            widget.bind("<Button-4>", lambda e: self.canvas.yview_scroll(-3, "units"))
            widget.bind("<Button-5>", lambda e: self.canvas.yview_scroll(3, "units"))

    def _on_wheel(self, event):
        self.canvas.yview_scroll(int(-event.delta / 40) or -1, "units")


# ======================================================================
# Main application
# ======================================================================

class GreekApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ἑλληνικὴ Γραμματική — Ancient Greek Grammar Studio")
        self.geometry("1180x760")
        self.minsize(880, 560)
        self.configure(bg=PAL["bg"])

        self.serif = pick_family(
            self, ["Gentium Plus", "GFS Didot", "New Athena Unicode",
                   "Palatino Linotype", "Palatino", "Georgia"], "Georgia")
        self.ui = pick_family(
            self, ["Avenir Next", "Helvetica Neue", "Segoe UI"], "TkDefaultFont")

        self.F = {
            "h1": tkfont.Font(family=self.serif, size=22, weight="bold"),
            "h2": tkfont.Font(family=self.serif, size=15, weight="bold"),
            "h3": tkfont.Font(family=self.serif, size=13, weight="bold"),
            "gr": tkfont.Font(family=self.serif, size=15),
            "gr_sm": tkfont.Font(family=self.serif, size=12),
            "gr_lg": tkfont.Font(family=self.serif, size=26, weight="bold"),
            "ui": tkfont.Font(family=self.ui, size=11),
            "ui_b": tkfont.Font(family=self.ui, size=11, weight="bold"),
            "mono": tkfont.Font(family="Menlo" if "Menlo" in tkfont.families() else "Courier", size=11),
        }

        self._style()
        self._build_shell()

    # -- style ----------------------------------------------------------
    def _style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(".", background=PAL["bg"], foreground=PAL["ink"],
                         fieldbackground=PAL["panel2"], font=self.F["ui"])
        style.configure("TFrame", background=PAL["bg"])
        style.configure("Panel.TFrame", background=PAL["bg"])
        style.configure("Card.TFrame", background=PAL["card"])
        style.configure("TLabel", background=PAL["bg"], foreground=PAL["ink"])
        style.configure("Card.TLabel", background=PAL["card"], foreground=PAL["ink"])
        style.configure("Mut.TLabel", background=PAL["bg"], foreground=PAL["mut"])
        style.configure("CardMut.TLabel", background=PAL["card"], foreground=PAL["mut"])

        style.configure("TNotebook", background=PAL["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=PAL["panel"], foreground=PAL["mut"],
                         padding=(18, 10), font=self.F["ui_b"])
        style.map("TNotebook.Tab",
                  background=[("selected", PAL["card"])],
                  foreground=[("selected", PAL["accent"])])

        style.configure("Side.TButton", background=PAL["panel"], foreground=PAL["ink"],
                         borderwidth=0, padding=(14, 9), font=self.F["ui"])
        style.map("Side.TButton",
                  background=[("active", PAL["panel2"])])
        style.configure("SideSel.TButton", background=PAL["accent"], foreground="#211a0c",
                         borderwidth=0, padding=(14, 9), font=self.F["ui_b"])

        style.configure("Accent.TButton", background=PAL["accent"], foreground="#211a0c",
                         borderwidth=0, padding=(14, 8), font=self.F["ui_b"])
        style.map("Accent.TButton", background=[("active", "#e8d49e")])
        style.configure("Ghost.TButton", background=PAL["panel"], foreground=PAL["ink"],
                         borderwidth=0, padding=(14, 8), font=self.F["ui"])
        style.map("Ghost.TButton", background=[("active", PAL["panel2"])])

        style.configure("TCheckbutton", background=PAL["bg"], foreground=PAL["ink"],
                         font=self.F["ui"])
        style.map("TCheckbutton", background=[("active", PAL["bg"])])

        style.configure("TEntry", fieldbackground=PAL["panel2"], foreground=PAL["ink"],
                         insertcolor=PAL["ink"], borderwidth=1, relief="flat")
        style.configure("TScrollbar", background=PAL["panel"], troughcolor=PAL["bg"],
                         borderwidth=0, arrowsize=12)

    # -- shell / header ---------------------------------------------------
    def _build_shell(self):
        header = tk.Frame(self, bg=PAL["bg"])
        header.pack(fill="x", padx=22, pady=(18, 6))
        tk.Label(header, text="Ἑλληνικὴ Γραμματική", font=self.F["h1"],
                  bg=PAL["bg"], fg=PAL["accent"]).pack(side="left")
        tk.Label(header, text="  Ancient Greek Grammar Studio", font=self.F["ui"],
                  bg=PAL["bg"], fg=PAL["mut"]).pack(side="left", padx=(4, 0))

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        ref_tab = ttk.Frame(nb, style="TFrame")
        work_tab = ttk.Frame(nb, style="TFrame")
        drill_tab = ttk.Frame(nb, style="TFrame")
        nb.add(ref_tab, text="  Reference Guide  ")
        nb.add(work_tab, text="  Worksheet  ")
        nb.add(drill_tab, text="  Memorization Drill  ")

        ReferencePane(ref_tab, self).pack(fill="both", expand=True)
        WorksheetPane(work_tab, self).pack(fill="both", expand=True)
        DrillPane(drill_tab, self).pack(fill="both", expand=True)

    # -- shared render helpers -------------------------------------------
    def render_word(self, parent, token_str, size="gr", default_key=None, bg=None):
        """Render a token string like 'a:ἔ|λυ|t:σ|α' as a row of coloured
        Labels packed left-to-right, forming a single visual word."""
        bg = bg or PAL["bg"]
        box = tk.Frame(parent, bg=bg)
        tokens = token_str.split("|")
        f = self.F[size]
        n = len(tokens)
        for i, tok in enumerate(tokens):
            last = (i == n - 1)
            if tok.startswith("a:"):
                text, color = tok[2:], PAL["aug"]
            elif tok.startswith("t:"):
                text, color = tok[2:], PAL["ten"]
            elif last and n > 1:
                text, color = tok, PAL["end"]
            else:
                text, color = tok, (PAL[default_key] if default_key else PAL["ink"])
            if text == "":
                continue
            tk.Label(box, text=text, font=f, bg=box.cget("bg"), fg=color).pack(side="left")
        if not tokens or all(t == "" for t in tokens):
            tk.Label(box, text="—", font=f, bg=box.cget("bg"), fg=PAL["mut"]).pack(side="left")
        return box

    def card(self, parent, **kw):
        f = tk.Frame(parent, bg=PAL["card"], highlightbackground=PAL["line"],
                      highlightthickness=1, **kw)
        return f

    def h2(self, parent, text, bg=None):
        return tk.Label(parent, text=text, font=self.F["h2"], bg=bg or PAL["bg"],
                         fg=PAL["accent"])

    def h3(self, parent, text, bg=None):
        return tk.Label(parent, text=text, font=self.F["h3"], bg=bg or PAL["bg"],
                         fg=PAL["ink"])

    def mut(self, parent, text, bg=None, **kw):
        return tk.Label(parent, text=text, font=self.F["ui"], bg=bg or PAL["bg"],
                         fg=PAL["mut"], **kw)


# ======================================================================
# Reference pane
# ======================================================================

class ReferencePane(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.sections = [
            ("Alphabet", self.sec_alphabet),
            ("Nouns & Article", self.sec_nouns),
            ("Adjectives & Pronouns", self.sec_adjectives),
            ("Verbs", self.sec_verbs),
            ("Endings — Colour Key", self.sec_legend),
            ("Syntax Notes", self.sec_syntax),
        ]
        self.current = tk.StringVar(value=self.sections[0][0])
        self._build()
        self.show(self.sections[0][0])

    def _build(self):
        wrap = tk.Frame(self, bg=PAL["bg"])
        wrap.pack(fill="both", expand=True)

        side = tk.Frame(wrap, bg=PAL["panel"], width=230)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        tk.Label(side, text="SECTIONS", font=("", 10, "bold"), bg=PAL["panel"],
                  fg=PAL["mut"]).pack(anchor="w", padx=16, pady=(18, 6))
        self.buttons = {}
        for name, _ in self.sections:
            b = ttk.Button(side, text=name, style="Side.TButton",
                            command=lambda n=name: self.show(n))
            b.pack(fill="x", padx=10, pady=2)
            self.buttons[name] = b

        self.body_host = tk.Frame(wrap, bg=PAL["bg"])
        self.body_host.pack(side="left", fill="both", expand=True)
        self.scroll = ScrollFrame(self.body_host)
        self.scroll.pack(fill="both", expand=True, padx=18, pady=18)

    def show(self, name):
        self.current.set(name)
        for n, b in self.buttons.items():
            b.configure(style="SideSel.TButton" if n == name else "Side.TButton")
        for w in self.scroll.inner.winfo_children():
            w.destroy()
        fn = dict(self.sections)[name]
        fn(self.scroll.inner)
        self.scroll.canvas.yview_moveto(0)

    # ---- individual sections ----
    def sec_alphabet(self, root):
        app = self.app
        app.h2(root, "Alphabet & Pronunciation").pack(anchor="w", pady=(0, 10))
        grid = tk.Frame(root, bg=PAL["bg"])
        grid.pack(anchor="w", fill="x")
        for i, (g, name, pron) in enumerate(ALPHABET):
            r, c = divmod(i, 4)
            cell = tk.Frame(grid, bg=PAL["bg"])
            cell.grid(row=r, column=c, sticky="w", padx=(0, 22), pady=6)
            tk.Label(cell, text=g, font=app.F["gr"], bg=PAL["bg"], fg=PAL["nom"]).pack(anchor="w")
            tk.Label(cell, text=name, font=app.F["ui"], bg=PAL["bg"], fg=PAL["ink"]).pack(anchor="w")
            tk.Label(cell, text=pron, font=app.F["ui"], bg=PAL["bg"], fg=PAL["mut"]).pack(anchor="w")
        app.mut(root, "Breathings: smooth ἀ (no h) vs. rough ἁ (adds h) on every initial vowel/ρ.").pack(
            anchor="w", pady=(16, 2))
        app.mut(root, "Accents: acute ά · grave ὰ · circumflex ᾶ (long syllables only).").pack(anchor="w")
        app.mut(root, "Diphthongs: αι ει οι υι αυ ευ ου ηυ   ·   iota subscript: ᾳ ῃ ῳ").pack(
            anchor="w", pady=(2, 0))

    def _case_table(self, root, title, cols, rows_by_case, pl_cols=None, pl_rows=None):
        """cols: list of column headings. rows_by_case: dict case -> list of token strings."""
        app = self.app
        card = app.card(root)
        card.pack(fill="x", pady=(0, 16))
        inner = tk.Frame(card, bg=PAL["card"])
        inner.pack(fill="x", padx=16, pady=14)
        app.h3(inner, title, bg=PAL["card"]).grid(row=0, column=0, columnspan=len(cols) + 1, sticky="w", pady=(0, 10))
        for j, c in enumerate(cols):
            tk.Label(inner, text=c, font=app.F["ui_b"], bg=PAL["card"], fg=PAL["mut"]).grid(
                row=1, column=j + 1, sticky="w", padx=(18, 0))
        r = 2
        for case in CASES:
            if case not in rows_by_case:
                continue
            color = PAL[CASE_COLOR[case]]
            tk.Label(inner, text=case, font=app.F["ui_b"], bg=PAL["card"], fg=color).grid(
                row=r, column=0, sticky="w", pady=3)
            for j, tokstr in enumerate(rows_by_case[case]):
                box = app.render_word(inner, tokstr, size="gr_sm")
                box.configure(bg=PAL["card"])
                for lbl in box.winfo_children():
                    lbl.configure(bg=PAL["card"])
                box.grid(row=r, column=j + 1, sticky="w", padx=(18, 0), pady=3)
            r += 1
        return card

    def sec_nouns(self, root):
        app = self.app
        app.h2(root, "Nouns & the Definite Article").pack(anchor="w", pady=(0, 4))
        app.mut(root, "Coloured text = the case ending. Neuter nom./acc./voc. are identical; "
                       "neuter plural ends in -α.").pack(anchor="w", pady=(0, 14))

        rows = {case: [ARTICLE["sg"]["m"][i], ARTICLE["sg"]["f"][i], ARTICLE["sg"]["n"][i],
                        ARTICLE["pl"]["m"][i], ARTICLE["pl"]["f"][i], ARTICLE["pl"]["n"][i]]
                for i, case in enumerate(CASES)}
        self._case_table(root, ARTICLE["name"],
                          ["m sg", "f sg", "n sg", "m pl", "f pl", "n pl"], rows)

        for n in NOUNS:
            rows = {case: [n["sg"][i], n["pl"][i]] for i, case in enumerate(CASES)}
            title = f'{n["name"]}  —  "{n["gloss"]}"   ·   {n["type"]}'
            self._case_table(root, title, ["Singular", "Plural"], rows)

        app.mut(root, "3rd-declension stem = genitive singular minus -ος: "
                       "φύλακος → φύλακ-, σώματος → σωματ-.").pack(anchor="w", pady=(4, 0))
        app.mut(root, "Dative plural -σι(ν): κ/γ/χ + σ = ξ (φύλαξι); τ/δ/θ drop before σ "
                       "(σώμασι).").pack(anchor="w", pady=(2, 0))

    def sec_adjectives(self, root):
        app = self.app
        app.h2(root, "Adjectives & Pronouns").pack(anchor="w", pady=(0, 14))
        rows = {case: [ADJ["sg"]["m"][i], ADJ["sg"]["f"][i], ADJ["sg"]["n"][i],
                        ADJ["pl"]["m"][i], ADJ["pl"]["f"][i], ADJ["pl"]["n"][i]]
                for i, case in enumerate(CASES)}
        self._case_table(root, ADJ["name"],
                          ["m sg", "f sg", "n sg", "m pl", "f pl", "n pl"], rows)

        card = app.card(root)
        card.pack(fill="x", pady=(0, 16))
        inner = tk.Frame(card, bg=PAL["card"])
        inner.pack(fill="x", padx=16, pady=14)
        app.h3(inner, "Personal Pronouns", bg=PAL["card"]).grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 10))
        labels = ["Nom", "Gen", "Dat", "Acc"]
        for j, lab in enumerate(labels):
            tk.Label(inner, text=lab, font=app.F["ui_b"], bg=PAL["card"],
                      fg=PAL[CASE_COLOR[lab]]).grid(row=1, column=j + 1, sticky="w", padx=(18, 0))
        for i, (who, forms) in enumerate(PRONOUNS):
            tk.Label(inner, text=who, font=app.F["ui_b"], bg=PAL["card"], fg=PAL["ink"]).grid(
                row=2 + i, column=0, sticky="w", pady=3)
            for j, f in enumerate(forms):
                tk.Label(inner, text=f, font=app.F["gr_sm"], bg=PAL["card"], fg=PAL["ink"]).grid(
                    row=2 + i, column=j + 1, sticky="w", padx=(18, 0), pady=3)

        app.mut(root, "Comparison: -τερος / -τατος  (σοφός → σοφώτερος → σοφώτατος). "
                       "Adverb: -ως (καλῶς).").pack(anchor="w", pady=(4, 2))
        app.mut(root, "αὐτός, -ή, -ό declines like ἀγαθός: predicate position = \u201cself\u201d; "
                       "attributive (between article and noun) = \u201csame\u201d.").pack(anchor="w")
        app.mut(root, "Demonstratives: οὗτος (this) · ἐκεῖνος (that).").pack(anchor="w", pady=(2, 0))

    def _person_table(self, root, title, rows):
        app = self.app
        card = app.card(root)
        card.pack(fill="x", pady=(0, 14))
        inner = tk.Frame(card, bg=PAL["card"])
        inner.pack(fill="x", padx=16, pady=12)
        app.h3(inner, title, bg=PAL["card"]).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
        for i, p in enumerate(PERSONS):
            r, c = divmod(i, 3)
            tk.Label(inner, text=p, font=app.F["ui_b"], bg=PAL["card"], fg=PAL["end"],
                      width=6, anchor="w").grid(row=1 + r, column=c * 2, sticky="w", pady=3)
            box = app.render_word(inner, rows[i], size="gr_sm")
            box.configure(bg=PAL["card"])
            for lbl in box.winfo_children():
                lbl.configure(bg=PAL["card"])
            box.grid(row=1 + r, column=c * 2 + 1, sticky="w", padx=(4, 26), pady=3)

    def sec_verbs(self, root):
        app = self.app
        app.h2(root, "Verbs — λύω  \u201cI loosen\u201d").pack(anchor="w", pady=(0, 2))
        app.mut(root, "Six principal parts: λύω · λύσω · ἔλυσα · λέλυκα · λέλυμαι · ἐλύθην").pack(
            anchor="w", pady=(0, 8))
        legend = tk.Frame(root, bg=PAL["bg"])
        legend.pack(anchor="w", pady=(0, 14))
        for text, key in [("augment / reduplication", "aug"), ("tense sign", "ten"), ("personal ending", "end")]:
            tk.Label(legend, text="●", font=app.F["ui_b"], bg=PAL["bg"], fg=PAL[key]).pack(side="left")
            tk.Label(legend, text=f" {text}   ", font=app.F["ui"], bg=PAL["bg"], fg=PAL["mut"]).pack(side="left")

        for name, forms in VERB_TABLES:
            self._person_table(root, name, forms)

        card = app.card(root)
        card.pack(fill="x", pady=(0, 14))
        inner = tk.Frame(card, bg=PAL["card"])
        inner.pack(fill="x", padx=16, pady=12)
        app.h3(inner, "Imperative (present)", bg=PAL["card"]).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
        tk.Label(inner, text="Active", font=app.F["ui_b"], bg=PAL["card"], fg=PAL["mut"]).grid(
            row=1, column=1, sticky="w", padx=(20, 0))
        tk.Label(inner, text="Mid./Pass.", font=app.F["ui_b"], bg=PAL["card"], fg=PAL["mut"]).grid(
            row=1, column=2, sticky="w", padx=(20, 0))
        for i, (p, act, mp) in enumerate(IMPERATIVE):
            tk.Label(inner, text=p, font=app.F["ui_b"], bg=PAL["card"], fg=PAL["end"]).grid(
                row=2 + i, column=0, sticky="w", pady=3)
            for j, tokstr in enumerate([act, mp]):
                box = app.render_word(inner, tokstr, size="gr_sm")
                box.configure(bg=PAL["card"])
                for lbl in box.winfo_children():
                    lbl.configure(bg=PAL["card"])
                box.grid(row=2 + i, column=1 + j, sticky="w", padx=(20, 0), pady=3)

        card2 = app.card(root)
        card2.pack(fill="x", pady=(0, 14))
        inner2 = tk.Frame(card2, bg=PAL["card"])
        inner2.pack(fill="x", padx=16, pady=12)
        app.h3(inner2, "Infinitives & Participles", bg=PAL["card"]).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))
        for j, h in enumerate(["", "Inf. active", "Inf. mid./pass.", "Participle (m/f/n)"]):
            if h:
                tk.Label(inner2, text=h, font=app.F["ui_b"], bg=PAL["card"], fg=PAL["mut"]).grid(
                    row=1, column=j, sticky="w", padx=(0 if j == 0 else 20, 0))
        PTC = {
            "Present": "λύων, λύουσα, λῦον", "Future": "λύσων, λύσουσα, λῦσον",
            "Aorist": "λύσας, λύσασα, λῦσαν", "Perfect": "λελυκώς, λελυκυῖα, λελυκός",
        }
        for i, (tense, act_inf, mp_inf) in enumerate(INFINITIVES):
            tk.Label(inner2, text=tense, font=app.F["ui_b"], bg=PAL["card"], fg=PAL["ink"]).grid(
                row=2 + i, column=0, sticky="w", pady=3)
            b1 = app.render_word(inner2, act_inf, size="gr_sm"); b1.configure(bg=PAL["card"])
            for lbl in b1.winfo_children(): lbl.configure(bg=PAL["card"])
            b1.grid(row=2 + i, column=1, sticky="w", padx=(20, 0), pady=3)
            tk.Label(inner2, text=mp_inf, font=app.F["gr_sm"], bg=PAL["card"], fg=PAL["ink"]).grid(
                row=2 + i, column=2, sticky="w", padx=(20, 0), pady=3)
            tk.Label(inner2, text=PTC[tense], font=app.F["gr_sm"], bg=PAL["card"], fg=PAL["ink"]).grid(
                row=2 + i, column=3, sticky="w", padx=(20, 0), pady=3)

        card3 = app.card(root)
        card3.pack(fill="x", pady=(0, 14))
        inner3 = tk.Frame(card3, bg=PAL["card"])
        inner3.pack(fill="x", padx=16, pady=12)
        app.h3(inner3, "Contract Verbs (present active)", bg=PAL["card"]).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))
        for ci, (name, forms) in enumerate(CONTRACT.items()):
            tk.Label(inner3, text=name, font=app.F["ui_b"], bg=PAL["card"], fg=PAL["ink"]).grid(
                row=1 + ci * 3, column=0, columnspan=3, sticky="w", pady=(8 if ci else 0, 2))
            for i, p in enumerate(PERSONS):
                r, c = divmod(i, 3)
                box = app.render_word(inner3, forms[i], size="gr_sm")
                box.configure(bg=PAL["card"])
                for lbl in box.winfo_children(): lbl.configure(bg=PAL["card"])
                box.grid(row=2 + ci * 3 + r, column=c, sticky="w", padx=(0, 26), pady=2)
        app.mut(root, "Contraction: α+ε→ᾱ, α+ο→ω, ε+ε→ει, ε+ο→ου, ο+ε/ει→ου/οι.").pack(
            anchor="w", pady=(0, 14))

        card4 = app.card(root)
        card4.pack(fill="x", pady=(0, 14))
        inner4 = tk.Frame(card4, bg=PAL["card"])
        inner4.pack(fill="x", padx=16, pady=12)
        app.h3(inner4, "Irregular & -μι Verbs", bg=PAL["card"]).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
        row = 1
        for name, forms in IRREGULAR.items():
            tk.Label(inner4, text=name, font=app.F["ui_b"], bg=PAL["card"], fg=PAL["ink"]).grid(
                row=row, column=0, columnspan=3, sticky="w", pady=(8, 2))
            row += 1
            for i, p in enumerate(PERSONS):
                r, c = divmod(i, 3)
                tk.Label(inner4, text=f"{p}: {forms[i]}", font=app.F["gr_sm"], bg=PAL["card"],
                          fg=PAL["ink"]).grid(row=row + r, column=c, sticky="w", padx=(0, 20), pady=2)
            row += 2

        app.mut(root, "Negatives: οὐ with the indicative; μή with everything else.").pack(
            anchor="w", pady=(0, 4))

    def sec_legend(self, root):
        app = self.app
        app.h2(root, "Endings & Markers — Colour Key").pack(anchor="w", pady=(0, 14))

        card = app.card(root)
        card.pack(fill="x", pady=(0, 14))
        inner = tk.Frame(card, bg=PAL["card"])
        inner.pack(fill="x", padx=16, pady=12)
        app.h3(inner, "Noun case endings", bg=PAL["card"]).grid(row=0, column=0, sticky="w", pady=(0, 8))
        row = 1
        for group, d in NOUN_ENDINGS.items():
            tk.Label(inner, text=group, font=app.F["ui"], bg=PAL["card"], fg=PAL["mut"]).grid(
                row=row, column=0, sticky="w", pady=(6, 0))
            row += 1
            line = tk.Frame(inner, bg=PAL["card"])
            line.grid(row=row, column=0, sticky="w", pady=(0, 2))
            for case, end in d.items():
                tk.Label(line, text=f"{case} ", font=app.F["ui_b"], bg=PAL["card"],
                          fg=PAL[CASE_COLOR[case]]).pack(side="left")
                tk.Label(line, text=f"-{end}   ", font=app.F["gr_sm"], bg=PAL["card"],
                          fg=PAL["end"]).pack(side="left")
            row += 1

        card2 = app.card(root)
        card2.pack(fill="x", pady=(0, 14))
        inner2 = tk.Frame(card2, bg=PAL["card"])
        inner2.pack(fill="x", padx=16, pady=12)
        app.h3(inner2, "Verb personal endings", bg=PAL["card"]).grid(row=0, column=0, sticky="w", pady=(0, 8))
        row = 1
        for group, d in VERB_ENDINGS.items():
            tk.Label(inner2, text=group, font=app.F["ui"], bg=PAL["card"], fg=PAL["mut"]).grid(
                row=row, column=0, sticky="w", pady=(6, 0))
            row += 1
            line = tk.Frame(inner2, bg=PAL["card"])
            line.grid(row=row, column=0, sticky="w", pady=(0, 2))
            for p, end in d.items():
                tk.Label(line, text=f"{p} ", font=app.F["ui_b"], bg=PAL["card"],
                          fg=PAL["ink"]).pack(side="left")
                tk.Label(line, text=f"-{end}   ", font=app.F["gr_sm"], bg=PAL["card"],
                          fg=PAL["end"]).pack(side="left")
            row += 1

        card3 = app.card(root)
        card3.pack(fill="x", pady=(0, 14))
        inner3 = tk.Frame(card3, bg=PAL["card"])
        inner3.pack(fill="x", padx=16, pady=12)
        app.h3(inner3, "Augment / tense markers", bg=PAL["card"]).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
        for i, (name, sign, note) in enumerate(MARKERS):
            color = PAL["aug"] if "ugment" in name or "edup" in name else PAL["ten"]
            tk.Label(inner3, text=name, font=app.F["ui_b"], bg=PAL["card"], fg=color).grid(
                row=1 + i, column=0, sticky="w", pady=3)
            tk.Label(inner3, text=sign, font=app.F["gr_sm"], bg=PAL["card"], fg=PAL["end"]).grid(
                row=1 + i, column=1, sticky="w", padx=(16, 0), pady=3)
            tk.Label(inner3, text=note, font=app.F["ui"], bg=PAL["card"], fg=PAL["mut"]).grid(
                row=1 + i, column=2, sticky="w", padx=(16, 0), pady=3)

    def sec_syntax(self, root):
        app = self.app
        app.h2(root, "Quick Syntax Notes").pack(anchor="w", pady=(0, 14))
        card = app.card(root)
        card.pack(fill="x", pady=(0, 14))
        inner = tk.Frame(card, bg=PAL["card"])
        inner.pack(fill="x", padx=16, pady=12)
        app.h3(inner, "Case uses", bg=PAL["card"]).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        for i, (case, note) in enumerate(SYNTAX_NOTES):
            tk.Label(inner, text=case, font=app.F["ui_b"], bg=PAL["card"],
                      fg=PAL[CASE_COLOR[case]]).grid(row=1 + i, column=0, sticky="nw", pady=3)
            tk.Label(inner, text=note, font=app.F["ui"], bg=PAL["card"], fg=PAL["ink"],
                      wraplength=620, justify="left").grid(row=1 + i, column=1, sticky="w",
                                                            padx=(16, 0), pady=3)
        card2 = app.card(root)
        card2.pack(fill="x")
        inner2 = tk.Frame(card2, bg=PAL["card"])
        inner2.pack(fill="x", padx=16, pady=12)
        app.h3(inner2, "Patterns", bg=PAL["card"]).pack(anchor="w", pady=(0, 8))
        for line in SYNTAX_EXTRA:
            tk.Label(inner2, text="•  " + line, font=app.F["ui"], bg=PAL["card"], fg=PAL["ink"],
                      wraplength=760, justify="left").pack(anchor="w", pady=2)


# ======================================================================
# Worksheet pane
# ======================================================================

class WorksheetPane(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.lax = tk.BooleanVar(value=True)
        self.entries = []   # list of (entry_widget, result_label, answer, status_label)
        self._build()

    def _build(self):
        app = self.app
        top = tk.Frame(self, bg=PAL["bg"])
        top.pack(fill="x", padx=18, pady=(16, 6))
        app.h2(top, "Worksheet").pack(side="left")
        ttk.Checkbutton(top, text="Ignore accents & breathings", variable=self.lax).pack(
            side="left", padx=(24, 0))
        ttk.Button(top, text="Check All", style="Accent.TButton", command=self.check_all).pack(
            side="right", padx=4)
        ttk.Button(top, text="Reveal Answers", style="Ghost.TButton", command=self.reveal).pack(
            side="right", padx=4)
        ttk.Button(top, text="Clear", style="Ghost.TButton", command=self.clear).pack(
            side="right", padx=4)

        self.score_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.score_var, font=app.F["ui_b"], bg=PAL["bg"],
                  fg=PAL["accent"]).pack(anchor="e", padx=22)

        self.scroll = ScrollFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=18, pady=10)
        root = self.scroll.inner

        n = 0
        for sect_name, items in WORKSHEET:
            card = app.card(root)
            card.pack(fill="x", pady=(0, 14))
            inner = tk.Frame(card, bg=PAL["card"])
            inner.pack(fill="x", padx=16, pady=12)
            app.h3(inner, sect_name, bg=PAL["card"]).pack(anchor="w", pady=(0, 8))
            for prompt, ans in items:
                n += 1
                row = tk.Frame(inner, bg=PAL["card"])
                row.pack(fill="x", pady=4)
                tk.Label(row, text=f"{n}.", font=app.F["ui_b"], bg=PAL["card"],
                          fg=PAL["mut"], width=3, anchor="e").pack(side="left")
                tk.Label(row, text=prompt, font=app.F["ui"], bg=PAL["card"], fg=PAL["ink"],
                          width=34, anchor="w").pack(side="left", padx=(6, 10))
                e = tk.Entry(row, font=app.F["gr_sm"], bg=PAL["panel2"], fg=PAL["ink"],
                              insertbackground=PAL["ink"], relief="flat", width=18)
                e.pack(side="left", ipady=4)
                status = tk.Label(row, text="", font=app.F["ui_b"], bg=PAL["card"], width=24,
                                    anchor="w")
                status.pack(side="left", padx=(12, 0))
                idx = len(self.entries)
                e.bind("<Return>", lambda ev, i=idx: self._check_one(i, advance=True))
                self.entries.append({"entry": e, "status": status, "answer": ans, "prompt": prompt})

    def _check_one(self, i, advance=False):
        item = self.entries[i]
        user = item["entry"].get()
        if not user.strip():
            item["status"].configure(text="")
            return None
        ok = check_answer(user, item["answer"], self.lax.get())
        item["status"].configure(
            text=("✓ correct" if ok else f"✗ → {item['answer'].split('/')[0]}"),
            fg=(PAL["ok"] if ok else PAL["no"]))
        if advance and i + 1 < len(self.entries):
            self.entries[i + 1]["entry"].focus_set()
        return ok

    def check_all(self):
        score = 0
        total = len(self.entries)
        for i in range(total):
            ok = self._check_one(i)
            if ok:
                score += 1
        self.score_var.set(f"Score: {score} / {total}")

    def reveal(self):
        for item in self.entries:
            user = item["entry"].get()
            if user.strip():
                self._check_one(self.entries.index(item))
            else:
                item["status"].configure(text=f"→ {item['answer'].split('/')[0]}", fg=PAL["mut"])

    def clear(self):
        for item in self.entries:
            item["entry"].delete(0, "end")
            item["status"].configure(text="")
        self.score_var.set("")


# ======================================================================
# Drill pane (flashcard-style, missed cards requeue)
# ======================================================================

class DrillPane(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.lax = tk.BooleanVar(value=True)
        self.deck_name = tk.StringVar(value="All")
        self.queue = []
        self.current = None
        self.total_cards = 0
        self.correct_first = 0
        self.seen_wrong = {}
        self.streak = 0
        self.best_streak = 0
        self._build()

    def _build(self):
        app = self.app
        top = tk.Frame(self, bg=PAL["bg"])
        top.pack(fill="x", padx=18, pady=(16, 6))
        app.h2(top, "Memorization Drill").pack(side="left")

        ctrl = tk.Frame(self, bg=PAL["bg"])
        ctrl.pack(fill="x", padx=18, pady=(0, 10))
        tk.Label(ctrl, text="Deck:", font=app.F["ui"], bg=PAL["bg"], fg=PAL["mut"]).pack(side="left")
        decks = ["All", "Noun endings", "Verb endings", "Markers"]
        dd = ttk.OptionMenu(ctrl, self.deck_name, decks[0], *decks)
        dd.pack(side="left", padx=(8, 20))
        ttk.Checkbutton(ctrl, text="Ignore accents & breathings", variable=self.lax).pack(side="left")
        ttk.Button(ctrl, text="Start / Restart", style="Accent.TButton",
                   command=self.start).pack(side="right")

        stats = tk.Frame(self, bg=PAL["bg"])
        stats.pack(fill="x", padx=18)
        self.stat_var = tk.StringVar(value="Pick a deck and press Start.")
        tk.Label(stats, textvariable=self.stat_var, font=app.F["ui"], bg=PAL["bg"],
                  fg=PAL["mut"]).pack(anchor="w")

        self.card = app.card(self)
        self.card.pack(fill="both", expand=True, padx=18, pady=16)
        inner = tk.Frame(self.card, bg=PAL["card"])
        inner.pack(expand=True)

        self.deck_lbl = tk.Label(inner, text="", font=app.F["ui_b"], bg=PAL["card"], fg=PAL["accent"])
        self.deck_lbl.pack(pady=(30, 4))
        self.prompt_lbl = tk.Label(inner, text="Press Start to begin.", font=app.F["gr_lg"],
                                     bg=PAL["card"], fg=PAL["ink"], wraplength=700, justify="center")
        self.prompt_lbl.pack(pady=(6, 24))

        entry_row = tk.Frame(inner, bg=PAL["card"])
        entry_row.pack(pady=4)
        self.answer_entry = tk.Entry(entry_row, font=app.F["gr"], bg=PAL["panel2"], fg=PAL["ink"],
                                       insertbackground=PAL["ink"], relief="flat", width=22,
                                       justify="center")
        self.answer_entry.pack(side="left", ipady=8)
        self.answer_entry.bind("<Return>", lambda e: self.submit())

        btn_row = tk.Frame(inner, bg=PAL["card"])
        btn_row.pack(pady=18)
        ttk.Button(btn_row, text="Submit", style="Accent.TButton", command=self.submit).pack(
            side="left", padx=6)
        ttk.Button(btn_row, text="Skip", style="Ghost.TButton", command=self.skip).pack(
            side="left", padx=6)

        self.feedback_lbl = tk.Label(inner, text="", font=app.F["ui_b"], bg=PAL["card"], fg=PAL["ink"])
        self.feedback_lbl.pack(pady=(4, 10))

    # ---- deck building ----
    def _build_bank(self):
        bank = []
        for group, d in NOUN_ENDINGS.items():
            for case, end in d.items():
                bank.append(("Noun endings", f"{group} — {case}", end))
        for group, d in VERB_ENDINGS.items():
            for person, end in d.items():
                bank.append(("Verb endings", f"{group} — {person}", end))
        for name, sign, note in MARKERS:
            bank.append(("Markers", f"{name}\n({note})", sign))
        return bank

    def start(self):
        bank = self._build_bank()
        name = self.deck_name.get()
        if name != "All":
            bank = [c for c in bank if c[0] == name]
        random.shuffle(bank)
        self.queue = bank
        self.total_cards = len(bank)
        self.correct_first = 0
        self.seen_wrong = {}
        self.streak = 0
        self.best_streak = 0
        self.card.configure(highlightbackground=PAL["line"])
        self._update_stats()
        self._next_card()

    def _update_stats(self):
        pct = round(100 * self.correct_first / self.total_cards) if self.total_cards else 0
        self.stat_var.set(
            f"Cards remaining: {len(self.queue) + (1 if self.current else 0)}   ·   "
            f"First-try correct: {self.correct_first}/{self.total_cards} ({pct}%)   ·   "
            f"Best streak: {self.best_streak}"
        )

    def _next_card(self):
        self.feedback_lbl.configure(text="")
        self.answer_entry.delete(0, "end")
        if not self.queue:
            self.current = None
            self.deck_lbl.configure(text="")
            self.prompt_lbl.configure(text="Deck complete! 🎉  Press Start to drill again.")
            self._update_stats()
            return
        self.current = self.queue.pop(0)
        deck, prompt, ans = self.current
        self.deck_lbl.configure(text=deck.upper())
        self.prompt_lbl.configure(text=prompt)
        self.answer_entry.focus_set()
        self._update_stats()

    def submit(self):
        if not self.current:
            return
        deck, prompt, ans = self.current
        user = self.answer_entry.get()
        ok = check_answer(user, ans, self.lax.get()) or check_answer(
            user.lstrip("-"), ans.lstrip("-"), self.lax.get())
        if ok:
            self.feedback_lbl.configure(text=f"✓ correct — {ans}", fg=PAL["ok"])
            if self.seen_wrong.get(prompt, 0) == 0:
                self.correct_first += 1
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
            self.after(500, self._next_card)
        else:
            self.feedback_lbl.configure(text=f"✗ correct answer: {ans}", fg=PAL["no"])
            self.streak = 0
            self.seen_wrong[prompt] = self.seen_wrong.get(prompt, 0) + 1
            if self.seen_wrong[prompt] <= 2:
                insert_at = min(len(self.queue), random.randint(2, 5))
                self.queue.insert(insert_at, self.current)
            self.after(1200, self._next_card)
        self._update_stats()

    def skip(self):
        if not self.current:
            return
        self.queue.append(self.current)
        self._next_card()


# ======================================================================
# Entry point
# ======================================================================

def main():
    app = GreekApp()
    if os.environ.get("GUI_SELFTEST"):
        # Headless smoke test: touch every pane/section, then exit cleanly.
        app.update_idletasks()
        for frame in app.winfo_children():
            pass
        app.after(50, app.destroy)
    app.mainloop()


if __name__ == "__main__":
    main()
