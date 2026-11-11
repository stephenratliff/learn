#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LATINA · Grammar Studio
=======================
A colour-coded Latin grammar guide with built-in memorisation tools.

  GUIDE   Overview · Nouns · Adjectives · Pronouns · Verbs · Irregular Verbs · Reference
  STUDY   Flashcards (spaced repetition) · Type-in Drill · Worksheet · Memory Aids

Run:   python3 latin_grammar_studio.py
Needs: Python 3.8+ with Tkinter (bundled with the python.org macOS installer,
       or `brew install python-tk` for Homebrew Python).  No other packages.

Tip: macrons (ā ē ī ō ū) are ignored by default when checking answers, so you
can type plain letters.  Turn the option off to drill vowel length too.
"""
import html
import json
import os
import random
import unicodedata
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ════════════════════════════════════════════════════════════════════════════
#  THEME
# ════════════════════════════════════════════════════════════════════════════
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
F_BIG = (SERIF, 44, "bold")
F_MID = (SERIF, 22)

# ════════════════════════════════════════════════════════════════════════════
#  LATIN DATA
# ════════════════════════════════════════════════════════════════════════════
CASES = ["Nominative", "Genitive", "Dative", "Accusative", "Ablative", "Vocative"]
CASE_ABBR = ["Nom.", "Gen.", "Dat.", "Acc.", "Abl.", "Voc."]
CASE_USE = [
    ("Nominative", "who / what (does it)", "Subject; predicate noun", "puella cantat — the girl sings"),
    ("Genitive", "whose / of what", "Possession, 'of'", "librī puellae — the girl's books"),
    ("Dative", "to / for whom", "Indirect object; interest", "puellae librum dat — gives a book to the girl"),
    ("Accusative", "whom / what", "Direct object; motion toward; many prepositions", "puellam videt — sees the girl"),
    ("Ablative", "by / with / from / in", "Means, agent (ab), manner, separation, place where", "cum puellā — with the girl"),
    ("Vocative", "O …!", "Direct address", "puella! — O girl!"),
]

PERS = ["1st sg. (I)", "2nd sg. (you)", "3rd sg. (he/she/it)",
        "1st pl. (we)", "2nd pl. (you all)", "3rd pl. (they)"]


def _n(key, group, title, gender, word, meaning, stem, sg, pl, ov=None, note=""):
    return dict(key=key, group=group, title=title, gender=gender, word=word,
                meaning=meaning, stem=stem, sg=sg, pl=pl, ov=ov or {}, note=note)


NOUNS = [
    _n("1", "1st Decl", "1st Declension", "mostly feminine", "puella", "girl", "puell",
       ["a", "ae", "ae", "am", "ā", "a"], ["ae", "ārum", "īs", "ās", "īs", "ae"],
       note="Genitive singular -ae.  A few masculines: nauta, agricola, poēta.  Dat./abl. pl. of dea, fīlia: deābus, fīliābus."),
    _n("2m", "2nd Decl", "2nd Declension · masculine (-us)", "masculine", "dominus", "master, lord", "domin",
       ["us", "ī", "ō", "um", "ō", "e"], ["ī", "ōrum", "īs", "ōs", "īs", "ī"],
       note="Genitive singular -ī.  Only declension with a distinct vocative singular (-e; -ius → -ī: fīlī).  -er nouns: puer, ager (ager, agrī)."),
    _n("2n", "2nd Decl", "2nd Declension · neuter (-um)", "neuter", "bellum", "war", "bell",
       ["um", "ī", "ō", "um", "ō", "um"], ["a", "ōrum", "īs", "a", "īs", "a"],
       note="Neuter rule: nominative = accusative = vocative, and the plural of those three ends in -a."),
    _n("3c", "3rd Decl", "3rd Declension · consonant stem (m./f.)", "masculine / feminine", "rēx", "king", "rēg",
       ["", "is", "ī", "em", "e", ""], ["ēs", "um", "ibus", "ēs", "ibus", "ēs"],
       ov={("sg", 0): ("rēx", ""), ("sg", 5): ("rēx", "")},
       note="Genitive singular -is; find the stem there (rēgis → rēg-).  Nominative is irregular (rēx = rēg + s)."),
    _n("3n", "3rd Decl", "3rd Declension · consonant stem (neuter)", "neuter", "corpus", "body", "corpor",
       ["", "is", "ī", "", "e", ""], ["a", "um", "ibus", "a", "ibus", "a"],
       ov={("sg", 0): ("corpus", ""), ("sg", 3): ("corpus", ""), ("sg", 5): ("corpus", "")},
       note="Neuter: nom. = acc. = voc. in both numbers."),
    _n("3i", "3rd Decl", "3rd Declension · i-stem (m./f.)", "masculine / feminine", "cīvis", "citizen", "cīv",
       ["is", "is", "ī", "em", "e", "is"], ["ēs", "ium", "ibus", "ēs", "ibus", "ēs"],
       note="i-stems: gen. pl. -ium (accusative plural may also be -īs).  Rule: parisyllabic nouns (cīvis, hostis) and stems ending in two consonants (urbs, nox, mons)."),
    _n("3in", "3rd Decl", "3rd Declension · i-stem (neuter)", "neuter", "mare", "sea", "mar",
       ["e", "is", "ī", "e", "ī", "e"], ["ia", "ium", "ibus", "ia", "ibus", "ia"],
       note="Neuters in -e, -al, -ar: abl. sg. -ī, nom./acc. pl. -ia, gen. pl. -ium (animal, animālia)."),
    _n("4m", "4th Decl", "4th Declension · masculine (-us)", "masculine (some feminine)", "manus", "hand", "man",
       ["us", "ūs", "uī", "um", "ū", "us"], ["ūs", "uum", "ibus", "ūs", "ibus", "ūs"],
       note="Genitive singular -ūs.  Feminine: manus, domus (irregular in places)."),
    _n("4n", "4th Decl", "4th Declension · neuter (-ū)", "neuter", "cornū", "horn", "corn",
       ["ū", "ūs", "ū", "ū", "ū", "ū"], ["ua", "uum", "ibus", "ua", "ibus", "ua"],
       note="Only a handful: cornū, genū, verū."),
    _n("5", "5th Decl", "5th Declension", "feminine (diēs: m./f.)", "rēs", "thing, matter", "r",
       ["ēs", "eī", "eī", "em", "ē", "ēs"], ["ēs", "ērum", "ēbus", "ēs", "ēbus", "ēs"],
       note="Genitive singular -eī (-ēī after a vowel: diēī).  Plural is complete only in rēs and diēs."),
]


def noun_forms(d):
    return {num: [d["ov"].get((num, i), (d["stem"], e)) for i, e in enumerate(d[num])]
            for num in ("sg", "pl")}


# ---- Adjectives ------------------------------------------------------------
ADJ12 = dict(stem="bon", cols=[
    ("M sg.", ["us", "ī", "ō", "um", "ō", "e"]), ("F sg.", ["a", "ae", "ae", "am", "ā", "a"]),
    ("N sg.", ["um", "ī", "ō", "um", "ō", "um"]), ("M pl.", ["ī", "ōrum", "īs", "ōs", "īs", "ī"]),
    ("F pl.", ["ae", "ārum", "īs", "ās", "īs", "ae"]), ("N pl.", ["a", "ōrum", "īs", "a", "īs", "a"])])
ADJ3 = dict(stem="fort", cols=[
    ("M/F sg.", ["is", "is", "ī", "em", "ī", "is"]), ("N sg.", ["e", "is", "ī", "e", "ī", "e"]),
    ("M/F pl.", ["ēs", "ium", "ibus", "ēs", "ibus", "ēs"]), ("N pl.", ["ia", "ium", "ibus", "ia", "ibus", "ia"])])
COMPARISON = [
    ("lātus, -a, -um", "lātior, lātius", "lātissimus, -a, -um", "lātē · lātius · lātissimē"),
    ("fortis, -e", "fortior, fortius", "fortissimus, -a, -um", "fortiter · fortius · fortissimē"),
    ("ācer, ācris, ācre", "ācrior, ācrius", "ācerrimus, -a, -um", "ācriter · ācrius · ācerrimē"),
    ("facilis, -e", "facilior, facilius", "facillimus, -a, -um", "facile · facilius · facillimē"),
    ("bonus, -a, -um", "melior, melius", "optimus, -a, -um", "bene · melius · optimē"),
    ("malus, -a, -um", "pēior, pēius", "pessimus, -a, -um", "male · pēius · pessimē"),
    ("magnus, -a, -um", "māior, māius", "maximus, -a, -um", "magnopere · magis · maximē"),
    ("parvus, -a, -um", "minor, minus", "minimus, -a, -um", "paulum · minus · minimē"),
    ("multus, -a, -um", "— , plūs", "plūrimus, -a, -um", "multum · plūs · plūrimum"),
]

# ---- Pronouns (5 cases) ----------------------------------------------------
PRON = {
    "ego / tū": (["ego sg.", "nōs pl.", "tū sg.", "vōs pl."], [
        ["ego", "nōs", "tū", "vōs"], ["meī", "nostrum / nostrī", "tuī", "vestrum / vestrī"],
        ["mihi", "nōbīs", "tibi", "vōbīs"], ["mē", "nōs", "tē", "vōs"], ["mē", "nōbīs", "tē", "vōbīs"]]),
    "is, ea, id": (["M sg.", "F sg.", "N sg.", "M pl.", "F pl.", "N pl."], [
        ["is", "ea", "id", "eī / iī", "eae", "ea"], ["eius"] * 3 + ["eōrum", "eārum", "eōrum"],
        ["eī"] * 3 + ["eīs / iīs"] * 3, ["eum", "eam", "id", "eōs", "eās", "ea"],
        ["eō", "eā", "eō", "eīs / iīs", "eīs / iīs", "eīs / iīs"]]),
    "hic, haec, hoc": (["M sg.", "F sg.", "N sg.", "M pl.", "F pl.", "N pl."], [
        ["hic", "haec", "hoc", "hī", "hae", "haec"], ["huius"] * 3 + ["hōrum", "hārum", "hōrum"],
        ["huic"] * 3 + ["hīs"] * 3, ["hunc", "hanc", "hoc", "hōs", "hās", "haec"],
        ["hōc", "hāc", "hōc", "hīs", "hīs", "hīs"]]),
    "ille, illa, illud": (["M sg.", "F sg.", "N sg.", "M pl.", "F pl.", "N pl."], [
        ["ille", "illa", "illud", "illī", "illae", "illa"], ["illīus"] * 3 + ["illōrum", "illārum", "illōrum"],
        ["illī"] * 3 + ["illīs"] * 3, ["illum", "illam", "illud", "illōs", "illās", "illa"],
        ["illō", "illā", "illō", "illīs", "illīs", "illīs"]]),
    "quī, quae, quod": (["M sg.", "F sg.", "N sg.", "M pl.", "F pl.", "N pl."], [
        ["quī", "quae", "quod", "quī", "quae", "quae"], ["cuius"] * 3 + ["quōrum", "quārum", "quōrum"],
        ["cui"] * 3 + ["quibus"] * 3, ["quem", "quam", "quod", "quōs", "quās", "quae"],
        ["quō", "quā", "quō", "quibus", "quibus", "quibus"]]),
}

# ---- Verbs -----------------------------------------------------------------
TENSE_NAME = {"pres": "Present", "impf": "Imperfect", "fut": "Future",
              "perf": "Perfect", "plup": "Pluperfect", "fpf": "Fut. Perfect"}


def _impf(b):
    return [b + "am", b + "ās", b + "at", b + "āmus", b + "ātis", b + "ant"]


def _impfp(b):
    return [b + "ar", b + "āris", b + "ātur", b + "āmur", b + "āminī", b + "antur"]


def _fut12(b):
    return [b + "ō", b + "is", b + "it", b + "imus", b + "itis", b + "unt"]


def _fut12p(b):
    return [b + "or", b + "eris", b + "itur", b + "imur", b + "iminī", b + "untur"]


def _perf(b):
    return [b + "ī", b + "istī", b + "it", b + "imus", b + "istis", b + "ērunt"]


def _fut3(b):
    return [b + "am", b + "ēs", b + "et", b + "ēmus", b + "ētis", b + "ent"]


PERF_E = ["ī", "istī", "it", "imus", "istis", "ērunt"]
PLUP_E = ["eram", "erās", "erat", "erāmus", "erātis", "erant"]
FPF_E = ["erō", "eris", "erit", "erimus", "eritis", "erint"]
SPERF_E = ["erim", "erīs", "erit", "erīmus", "erītis", "erint"]
SPLUP_E = ["issem", "issēs", "isset", "issēmus", "issētis", "issent"]
ISJ_A = ["em", "ēs", "et", "ēmus", "ētis", "ent"]
ISJ_P = ["er", "ēris", "ētur", "ēmur", "ēminī", "entur"]

NF_LABELS = ["Infinitive (act. / pass.)", "Perfect infinitive", "Imperative (sg. / pl.)",
             "Present participle", "Perfect passive participle", "Future active participle",
             "Gerund (gen.)", "Gerundive"]

_SJ_IO_A = ["iam", "iās", "iat", "iāmus", "iātis", "iant"]
_SJ_IO_P = ["iar", "iāris", "iātur", "iāmur", "iāminī", "iantur"]

CONJ = [
    dict(key="1", group="1st Conj", title="1st Conjugation (-āre)", short="1st", pp="amō, amāre, amāvī, amātum",
         mean="to love", stem="am", perf="amāv", istem="amār",
         a=dict(pres=["ō", "ās", "at", "āmus", "ātis", "ant"], impf=_impf("āb"), fut=_fut12("āb")),
         p=dict(pres=["or", "āris", "ātur", "āmur", "āminī", "antur"], impf=_impfp("āb"), fut=_fut12p("āb")),
         sj_a=["em", "ēs", "et", "ēmus", "ētis", "ent"], sj_p=["er", "ēris", "ētur", "ēmur", "ēminī", "entur"],
         nf=["amāre / amārī", "amāvisse", "amā / amāte", "amāns, amantis", "amātus, -a, -um",
             "amātūrus, -a, -um", "amandī", "amandus, -a, -um"]),
    dict(key="2", group="2nd Conj", title="2nd Conjugation (-ēre)", short="2nd", pp="moneō, monēre, monuī, monitum",
         mean="to warn, advise", stem="mon", perf="monu", istem="monēr",
         a=dict(pres=["eō", "ēs", "et", "ēmus", "ētis", "ent"], impf=_impf("ēb"), fut=_fut12("ēb")),
         p=dict(pres=["eor", "ēris", "ētur", "ēmur", "ēminī", "entur"], impf=_impfp("ēb"), fut=_fut12p("ēb")),
         sj_a=["eam", "eās", "eat", "eāmus", "eātis", "eant"], sj_p=["ear", "eāris", "eātur", "eāmur", "eāminī", "eantur"],
         nf=["monēre / monērī", "monuisse", "monē / monēte", "monēns, monentis", "monitus, -a, -um",
             "monitūrus, -a, -um", "monendī", "monendus, -a, -um"]),
    dict(key="3", group="3rd Conj", title="3rd Conjugation (-ere)", short="3rd", pp="regō, regere, rēxī, rēctum",
         mean="to rule", stem="reg", perf="rēx", istem="reger",
         a=dict(pres=["ō", "is", "it", "imus", "itis", "unt"], impf=_impf("ēb"), fut=_fut3("")),
         p=dict(pres=["or", "eris", "itur", "imur", "iminī", "untur"], impf=_impfp("ēb"),
                fut=["ar", "ēris", "ētur", "ēmur", "ēminī", "entur"]),
         sj_a=["am", "ās", "at", "āmus", "ātis", "ant"], sj_p=["ar", "āris", "ātur", "āmur", "āminī", "antur"],
         nf=["regere / regī", "rēxisse", "rege / regite", "regēns, regentis", "rēctus, -a, -um",
             "rēctūrus, -a, -um", "regendī", "regendus, -a, -um"]),
    dict(key="3io", group="3rd-iō Conj", title="3rd Conjugation -iō (-ere)", short="3rd -iō",
         pp="capiō, capere, cēpī, captum", mean="to take, seize", stem="cap", perf="cēp", istem="caper",
         a=dict(pres=["iō", "is", "it", "imus", "itis", "iunt"], impf=_impf("iēb"),
                fut=["iam", "iēs", "iet", "iēmus", "iētis", "ient"]),
         p=dict(pres=["ior", "eris", "itur", "imur", "iminī", "iuntur"], impf=_impfp("iēb"),
                fut=["iar", "iēris", "iētur", "iēmur", "iēminī", "ientur"]),
         sj_a=_SJ_IO_A, sj_p=_SJ_IO_P,
         nf=["capere / capī", "cēpisse", "cape / capite", "capiēns, capientis", "captus, -a, -um",
             "captūrus, -a, -um", "capiendī", "capiendus, -a, -um"]),
    dict(key="4", group="4th Conj", title="4th Conjugation (-īre)", short="4th", pp="audiō, audīre, audīvī, audītum",
         mean="to hear, listen", stem="aud", perf="audīv", istem="audīr",
         a=dict(pres=["iō", "īs", "it", "īmus", "ītis", "iunt"], impf=_impf("iēb"),
                fut=["iam", "iēs", "iet", "iēmus", "iētis", "ient"]),
         p=dict(pres=["ior", "īris", "ītur", "īmur", "īminī", "iuntur"], impf=_impfp("iēb"),
                fut=["iar", "iēris", "iētur", "iēmur", "iēminī", "ientur"]),
         sj_a=_SJ_IO_A, sj_p=_SJ_IO_P,
         nf=["audīre / audīrī", "audīvisse", "audī / audīte", "audiēns, audientis", "audītus, -a, -um",
             "audītūrus, -a, -um", "audiendī", "audiendus, -a, -um"]),
]
# fix 3rd-conj future active, which has no stem vowel
CONJ[2]["a"]["fut"] = _fut3("")


def verb_cols(cj, kind):
    def col(name, key, stem, ends):
        return dict(name=name, key=key, color=TCOL[key], stem=stem, ends=ends)
    s, pf, ist = cj["stem"], cj["perf"], cj["istem"]
    if kind == "ind_a":
        return [col("Present", "pres", s, cj["a"]["pres"]), col("Imperfect", "impf", s, cj["a"]["impf"]),
                col("Future", "fut", s, cj["a"]["fut"]), col("Perfect", "perf", pf, PERF_E),
                col("Pluperfect", "plup", pf, PLUP_E), col("Fut. Perfect", "fpf", pf, FPF_E)]
    if kind == "ind_p":
        return [col("Present", "pres", s, cj["p"]["pres"]), col("Imperfect", "impf", s, cj["p"]["impf"]),
                col("Future", "fut", s, cj["p"]["fut"])]
    if kind == "sj_a":
        return [col("Present", "pres", s, cj["sj_a"]), col("Imperfect", "impf", ist, ISJ_A),
                col("Perfect", "perf", pf, SPERF_E), col("Pluperfect", "plup", pf, SPLUP_E)]
    if kind == "sj_p":
        return [col("Present", "pres", s, cj["sj_p"]), col("Imperfect", "impf", ist, ISJ_P)]
    raise ValueError(kind)


KIND_NAME = {"ind_a": "Indicative Active", "ind_p": "Indicative Passive",
             "sj_a": "Subjunctive Active", "sj_p": "Subjunctive Passive"}

# ---- Irregular verbs (full forms) -----------------------------------------
IRREGULAR = [
    dict(name="sum, esse, fuī, futūrus", mean="to be", cols=[
        ("Present", "pres", ["sum", "es", "est", "sumus", "estis", "sunt"]),
        ("Imperfect", "impf", ["eram", "erās", "erat", "erāmus", "erātis", "erant"]),
        ("Future", "fut", ["erō", "eris", "erit", "erimus", "eritis", "erunt"]),
        ("Perfect", "perf", ["fuī", "fuistī", "fuit", "fuimus", "fuistis", "fuērunt"]),
        ("Pluperfect", "plup", ["fueram", "fuerās", "fuerat", "fuerāmus", "fuerātis", "fuerant"]),
        ("Fut. Perfect", "fpf", ["fuerō", "fueris", "fuerit", "fuerimus", "fueritis", "fuerint"]),
        ("Pres. Subj.", "pres", ["sim", "sīs", "sit", "sīmus", "sītis", "sint"]),
        ("Impf. Subj.", "impf", ["essem", "essēs", "esset", "essēmus", "essētis", "essent"])],
         note="Imperative es / este · infinitives esse, fuisse, futūrum esse · future participle futūrus."),
    dict(name="possum, posse, potuī", mean="to be able, can", cols=[
        ("Present", "pres", ["possum", "potes", "potest", "possumus", "potestis", "possunt"]),
        ("Imperfect", "impf", ["poteram", "poterās", "poterat", "poterāmus", "poterātis", "poterant"]),
        ("Future", "fut", ["poterō", "poteris", "poterit", "poterimus", "poteritis", "poterunt"]),
        ("Perfect", "perf", ["potuī", "potuistī", "potuit", "potuimus", "potuistis", "potuērunt"])],
         note="possum = pot- + sum (pot- becomes poss- before s).  Infinitive posse; no imperative."),
    dict(name="eō, īre, iī (īvī), itum", mean="to go", cols=[
        ("Present", "pres", ["eō", "īs", "it", "īmus", "ītis", "eunt"]),
        ("Imperfect", "impf", ["ībam", "ībās", "ībat", "ībāmus", "ībātis", "ībant"]),
        ("Future", "fut", ["ībō", "ībis", "ībit", "ībimus", "ībitis", "ībunt"]),
        ("Perfect", "perf", ["iī", "īstī", "iit", "iimus", "īstis", "iērunt"])],
         note="Imperative ī / īte · present participle iēns, euntis · compounds: exeō, redeō, adeō, trānseō."),
    dict(name="ferō, ferre, tulī, lātum", mean="to bear, carry", cols=[
        ("Present", "pres", ["ferō", "fers", "fert", "ferimus", "fertis", "ferunt"]),
        ("Imperfect", "impf", _impf("ferēb")),
        ("Future", "fut", _fut3("fer")),
        ("Perfect", "perf", _perf("tul"))],
         note="Imperative fer / ferte · passive infinitive ferrī · present passive feror, ferris, fertur…"),
    dict(name="volō, velle, voluī", mean="to want, wish", cols=[
        ("Present", "pres", ["volō", "vīs", "vult", "volumus", "vultis", "volunt"]),
        ("Imperfect", "impf", _impf("volēb")), ("Future", "fut", _fut3("vol")), ("Perfect", "perf", _perf("volu"))],
         note="No imperative.  Present subjunctive velim, velīs, velit…"),
    dict(name="nōlō, nōlle, nōluī", mean="to be unwilling", cols=[
        ("Present", "pres", ["nōlō", "nōn vīs", "nōn vult", "nōlumus", "nōn vultis", "nōlunt"]),
        ("Imperfect", "impf", _impf("nōlēb")), ("Future", "fut", _fut3("nōl")), ("Perfect", "perf", _perf("nōlu"))],
         note="Imperative nōlī / nōlīte + infinitive = polite prohibition: nōlī currere! (Don't run!)"),
    dict(name="mālō, malle, māluī", mean="to prefer", cols=[
        ("Present", "pres", ["mālō", "māvīs", "māvult", "mālumus", "māvultis", "mālunt"]),
        ("Imperfect", "impf", _impf("mālēb")), ("Future", "fut", _fut3("māl")), ("Perfect", "perf", _perf("mālu"))],
         note="mālō = magis + volō.  No imperative."),
]

PRINCIPAL_PARTS = [
    ("1", "amō", "amāre", "amāvī", "amātum", "love"), ("1", "dō", "dare", "dedī", "datum", "give"),
    ("1", "stō", "stāre", "stetī", "statum", "stand"), ("2", "moneō", "monēre", "monuī", "monitum", "warn"),
    ("2", "habeō", "habēre", "habuī", "habitum", "have"), ("2", "videō", "vidēre", "vīdī", "vīsum", "see"),
    ("3", "regō", "regere", "rēxī", "rēctum", "rule"), ("3", "dūcō", "dūcere", "dūxī", "ductum", "lead"),
    ("3", "mittō", "mittere", "mīsī", "missum", "send"), ("3io", "capiō", "capere", "cēpī", "captum", "take"),
    ("3io", "faciō", "facere", "fēcī", "factum", "do, make"), ("4", "audiō", "audīre", "audīvī", "audītum", "hear"),
    ("4", "veniō", "venīre", "vēnī", "ventum", "come"),
]
CONJ_COL = {"1": "#f2c94c", "2": "#4fd1b5", "3": "#5fa8ff", "3io": "#c58af9", "4": "#ff7a7a"}

# ════════════════════════════════════════════════════════════════════════════
#  HELPERS – text normalisation & flashcard deck
# ════════════════════════════════════════════════════════════════════════════
def norm(s, ignore=True):
    s = unicodedata.normalize("NFC", s.strip().lower())
    if ignore:
        s = unicodedata.normalize("NFD", s)
        s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
        s = unicodedata.normalize("NFC", s)
    for dash in "-–—":
        s = s.replace(dash, "")
    return " ".join(s.split())


def accepted(stem, end, mode, ignore):
    out = set()
    for v in (x.strip() for x in end.split("/")):
        out.add(norm(stem + v, ignore))
        if mode != "full":
            out.add(norm(v, ignore))
    return out


def build_cards():
    cards = []
    for d in NOUNS:
        f = noun_forms(d)
        for num, nm in (("sg", "singular"), ("pl", "plural")):
            for i in range(6):
                stem, end = f[num][i]
                if end == "" or (i == 5 and f[num][5] == f[num][0]):
                    continue
                cards.append(dict(key=f"N|{d['key']}|{num}|{i}", group=d["group"], stem=stem, ans=end,
                                  title=f"{CASES[i]} {nm}", color=CASE_COL[i],
                                  sub=f"{d['title']} — {d['word']}, {d['meaning']}"))
    for cj in CONJ:
        spec = [("ind_a", 0, 3), ("ind_p", 0, 3), ("sj_a", 0, 1), ("sj_p", 0, 1)]
        for kind, lo, hi in spec:
            for c in verb_cols(cj, kind)[lo:hi]:
                for i in range(6):
                    cards.append(dict(key=f"V|{cj['key']}|{kind}|{c['key']}|{i}", group=cj["group"],
                                      stem=c["stem"], ans=c["ends"][i], title=PERS[i], color=c["color"],
                                      sub=f"{c['name']} {KIND_NAME[kind]} · {cj['title']} ({cj['pp'].split(',')[0]})"))
    cj = CONJ[0]
    for kind in ("ind_a", "sj_a"):
        for c in verb_cols(cj, kind):
            if c["key"] in ("perf", "plup", "fpf"):
                for i in range(6):
                    cards.append(dict(key=f"P|{kind}|{c['key']}|{i}", group="Perfect System", stem=c["stem"],
                                      ans=c["ends"][i], title=PERS[i], color=c["color"],
                                      sub=f"{c['name']} {KIND_NAME[kind]} · ALL conjugations (perfect stem + ending)"))
    for c in cards:
        c["full"] = c["stem"] + c["ans"].split("/")[0].strip()
    return cards


GROUPS = ["1st Decl", "2nd Decl", "3rd Decl", "4th Decl", "5th Decl",
          "1st Conj", "2nd Conj", "3rd Conj", "3rd-iō Conj", "4th Conj", "Perfect System"]

PROG_PATH = os.path.join(os.path.expanduser("~"), ".latin_grammar_studio.json")


def load_progress():
    try:
        with open(PROG_PATH, encoding="utf-8") as fh:
            data = json.load(fh)
            data.setdefault("box", {})
            return data
    except Exception:
        return {"box": {}}


def save_progress(prog):
    try:
        with open(PROG_PATH, "w", encoding="utf-8") as fh:
            json.dump(prog, fh)
    except Exception:
        pass


# ════════════════════════════════════════════════════════════════════════════
#  UI PRIMITIVES
# ════════════════════════════════════════════════════════════════════════════
def _lighten(h, a=0.18):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    r, g, b = [int(v + (255 - v) * a) for v in (r, g, b)]
    return f"#{r:02x}{g:02x}{b:02x}"


def S(text, color=None, bold=False):
    return (text, color or FG, bold)


def label(parent, text, fg=FG, font=F_BODY, bg=None, **kw):
    return tk.Label(parent, text=text, fg=fg, bg=bg or parent["bg"], font=font, **kw)


class Btn(tk.Label):
    def __init__(self, master, text, command=None, color=GOLD, fg=BG, font=F_BTN, padx=16, pady=7):
        super().__init__(master, text=text, bg=color, fg=fg, font=font, padx=padx, pady=pady, cursor="hand2")
        self.base, self.command = color, command
        self.bind("<Enter>", lambda e: self.config(bg=_lighten(self.base)))
        self.bind("<Leave>", lambda e: self.config(bg=self.base))
        self.bind("<Button-1>", lambda e: self.command() if self.command else None)


class Chip(tk.Label):
    def __init__(self, master, text, on=False, color=GOLD, command=None):
        super().__init__(master, text=text, font=F_SMALL, padx=10, pady=4, cursor="hand2")
        self.on, self.color, self.command = on, color, command
        self.bind("<Button-1>", self._click)
        self._paint()

    def _paint(self):
        self.config(bg=self.color, fg=BG) if self.on else self.config(bg=PANEL2, fg=DIM)

    def _click(self, _e=None):
        self.on = not self.on
        self._paint()
        if self.command:
            self.command(self)

    def set(self, value):
        self.on = value
        self._paint()


class Scroll(tk.Frame):
    """Vertically scrolling container; put widgets in `.inner`."""

    def __init__(self, master, bg=BG):
        super().__init__(master, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.win, width=e.width))


def grid_table(parent, headers, rows, corner=""):
    """headers: [(text,color)]; rows: [(rowhead, [cell,…])]; cell = list of segs or callable(frame,bg)."""
    t = tk.Frame(parent, bg=BORDER)

    def put(r, c, content, bg):
        cell = tk.Frame(t, bg=bg)
        cell.grid(row=r, column=c, sticky="nsew", padx=(0, 1), pady=(0, 1))
        inner = tk.Frame(cell, bg=bg)
        inner.pack(padx=9, pady=5)
        if callable(content):
            content(inner, bg)
        else:
            for txt, col, bold in content:
                tk.Label(inner, text=txt, fg=col, bg=bg, font=F_BOLD if bold else F_BODY,
                         bd=0, padx=0, pady=0).pack(side="left")

    put(0, 0, [S(corner, DIM)], HEAD_BG)
    for c, (h, col) in enumerate(headers):
        put(0, c + 1, [S(h, col, True)], HEAD_BG)
    for r, (rh, cells) in enumerate(rows):
        bg = ROW_A if r % 2 == 0 else ROW_B
        put(r + 1, 0, [S(rh, DIM)] if isinstance(rh, str) else rh, bg)
        for c, cell in enumerate(cells):
            put(r + 1, c + 1, cell if cell is not None else [S("")], bg)
    for c in range(len(headers) + 1):
        t.grid_columnconfigure(c, weight=1)
    return t


def card(parent, title=None, sub=None, color=GOLD, pady=(0, 14)):
    outer = tk.Frame(parent, bg=BORDER)
    outer.pack(fill="x", pady=pady, padx=2)
    inner = tk.Frame(outer, bg=PANEL)
    inner.pack(fill="both", expand=True, padx=1, pady=1)
    tk.Frame(inner, bg=color, width=4).pack(side="left", fill="y")
    body = tk.Frame(inner, bg=PANEL)
    body.pack(side="left", fill="both", expand=True, padx=14, pady=12)
    if title:
        label(body, title, fg=color, font=F_H2, bg=PANEL).pack(anchor="w")
    if sub:
        label(body, sub, fg=DIM, font=F_SMALL, bg=PANEL, justify="left", wraplength=820).pack(anchor="w", pady=(2, 8))
    return body


def para(parent, text, fg=FG, font=F_BODY, pady=2, bg=None):
    return label(parent, text, fg=fg, font=font, bg=bg or parent["bg"], justify="left",
                 wraplength=840, anchor="w").pack(anchor="w", pady=pady)


def legend(parent, items):
    f = tk.Frame(parent, bg=parent["bg"])
    f.pack(anchor="w", pady=(0, 10))
    for text, col in items:
        label(f, "■", fg=col, font=F_BODY, bg=f["bg"]).pack(side="left")
        label(f, text + "   ", fg=DIM, font=F_SMALL, bg=f["bg"]).pack(side="left")


def case_legend(p):
    legend(p, [(c, CASE_COL[i]) for i, c in enumerate(CASES)])


def tense_legend(p):
    legend(p, [(TENSE_NAME[k], TCOL[k]) for k in TCOL])


class SubTabs(tk.Frame):
    def __init__(self, master, tabs, color=GOLD):
        super().__init__(master, bg=BG)
        self.tabs, self.chips = tabs, []
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", pady=(0, 10))
        for i, (name, _) in enumerate(tabs):
            c = Chip(bar, name, color=color, command=lambda ch, i=i: self.select(i))
            c.pack(side="left", padx=(0, 6))
            self.chips.append(c)
        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True)
        self.select(0)

    def select(self, i):
        for j, c in enumerate(self.chips):
            c.set(j == i)
        for w in self.body.winfo_children():
            w.destroy()
        sc = Scroll(self.body)
        sc.pack(fill="both", expand=True)
        self.tabs[i][1](sc.inner)


def scrolled(builder):
    def make(parent):
        sc = Scroll(parent)
        builder(sc.inner)
        return sc
    return make


def macron_bar(parent, app):
    bar = tk.Frame(parent, bg=BG)
    label(bar, "Insert vowel:", fg=DIM, font=F_SMALL).pack(side="left", padx=(0, 6))

    def ins(ch):
        try:
            w = app.focus_get()
            if isinstance(w, tk.Entry):
                w.insert("insert", ch)
        except Exception:
            pass
    for ch in "āēīōū":
        Btn(bar, ch, command=lambda ch=ch: ins(ch), color=PANEL2, fg=FG, font=(SERIF, 14), padx=10, pady=2).pack(side="left", padx=2)
    return bar


# ════════════════════════════════════════════════════════════════════════════
#  GUIDE PAGES
# ════════════════════════════════════════════════════════════════════════════
def verb_table(p, cols):
    headers = [(c["name"], c["color"]) for c in cols]
    rows = [(PERS[i], [[S(c["stem"]), S(c["ends"][i], c["color"], True)] for c in cols]) for i in range(6)]
    return grid_table(p, headers, rows)


def page_overview(p):
    b = card(p, "Welcome to Latina", None, GOLD)
    para(b, "A compact, colour-coded gym for Latin morphology.  Every case, tense and person keeps the same colour "
            "from the guide through the flashcards, drills and worksheets, so colour becomes a memory hook.", pady=(0, 8))
    label(b, "Cases", fg=DIM, font=F_SMALL, bg=PANEL).pack(anchor="w")
    case_legend(b)
    label(b, "Tenses", fg=DIM, font=F_SMALL, bg=PANEL).pack(anchor="w")
    tense_legend(b)

    b = card(p, "Latin on one screen", None, CASE_COL[1])
    for line in [
        "• No articles (a / the).  Endings carry the grammar, so word order is flexible.",
        "• Nouns have gender (m., f., n.), number (sg., pl.) and case (6).  Five declensions – identified by the genitive singular.",
        "• Adjectives agree with their noun in gender, number and case.",
        "• Verbs have person, number, tense, voice (active/passive) and mood (indicative, subjunctive, imperative).  "
        "Four conjugations – identified by the present infinitive.",
        "• Dictionary entries: nouns give nominative, genitive, gender (puella, -ae, f.); verbs give four principal parts.",
    ]:
        para(b, line)

    b = card(p, "Which declension?  Look at the genitive singular", None, CASE_COL[2])
    rows = [("1st", "-ae", "puella, puellae", "mostly f."), ("2nd", "-ī", "dominus, dominī · bellum, bellī", "m. / n."),
            ("3rd", "-is", "rēx, rēgis · corpus, corporis", "m. / f. / n."), ("4th", "-ūs", "manus, manūs · cornū, cornūs", "m. (f.) / n."),
            ("5th", "-eī", "rēs, reī", "f.")]
    grid_table(b, [("Genitive sg.", CASE_COL[1]), ("Example", DIM), ("Gender", DIM)],
               [(f"{a} decl.", [[S(g, CASE_COL[1], True)], [S(e)], [S(gen, DIM)]]) for a, g, e, gen in rows]).pack(fill="x")

    b = card(p, "Which conjugation?  Look at the present infinitive", None, CASE_COL[3])
    grid_table(b, [("Infinitive", CASE_COL[3]), ("Stem vowel", DIM), ("Example", DIM)],
               [(cj["short"], [[S(cj["pp"].split(", ")[1], CONJ_COL[cj["key"]], True)],
                               [S({"1": "ā", "2": "ē", "3": "short e / i / u", "3io": "short e (i in pres.)", "4": "ī"}[cj["key"]])],
                               [S(cj["pp"])]]) for cj in CONJ]).pack(fill="x")

    b = card(p, "How to study with this program", None, CASE_COL[5])
    for line in ["1.  Read a paradigm in Nouns or Verbs, then say it aloud (see Chants in Memory Aids).",
                 "2.  Fill in a Worksheet at 25 % blanks; raise the slider to 100 % as you improve.",
                 "3.  Run Flashcards – cards you miss come back more often (a Leitner box system saved in your home folder).",
                 "4.  Finish with the Type-in Drill for active recall.",
                 "Keys: Flashcards – Space flips, ← missed, → got it.  Drill – Return checks / advances."]:
        para(b, line)


def page_nouns(parent):
    def glance(p):
        case_legend(p)
        for num, nm in (("sg", "Singular"), ("pl", "Plural")):
            b = card(p, f"{nm} endings at a glance", None, GOLD)
            heads = [(f"{d['group'][:3]}·{d['word']}", GOLD) for d in NOUNS]
            rows = []
            for i in range(6):
                cells = []
                for d in NOUNS:
                    stem, end = noun_forms(d)[num][i]
                    if d["ov"].get((num, i)) and end == "":
                        cells.append([S("—", DIM)])
                    else:
                        cells.append([S("-", DIM), S(end, CASE_COL[i], True)] if end else [S("—", DIM)])
                rows.append(([S(CASE_ABBR[i], CASE_COL[i], True)], cells))
            grid_table(b, heads, rows).pack(fill="x")
        para(p, "— means zero ending (the nominative is built from the stem plus special changes, e.g. rēx, corpus).",
             fg=DIM, font=F_SMALL)

    def decl(group):
        def build(p):
            case_legend(p)
            for d in [x for x in NOUNS if x["group"] == group]:
                b = card(p, d["title"], f"{d['word']}, {d['meaning']} · {d['gender']}.   {d['note']}", GOLD)
                f = noun_forms(d)
                rows = [([S(CASES[i], CASE_COL[i], True)],
                         [[S(f[n][i][0]), S(f[n][i][1], CASE_COL[i], True)] for n in ("sg", "pl")]) for i in range(6)]
                grid_table(b, [("Singular", GOLD), ("Plural", GOLD)], rows).pack(fill="x")
        return build

    tabs = [("At a glance", glance)] + [(g, decl(g)) for g in ("1st Decl", "2nd Decl", "3rd Decl", "4th Decl", "5th Decl")]
    return SubTabs(parent, tabs)


def page_adjectives(parent):
    def first_second(p):
        case_legend(p)
        b = card(p, "1st / 2nd declension adjectives  ·  bonus, bona, bonum (good)",
                 "Masculine follows dominus, feminine follows puella, neuter follows bellum.  "
                 "Like these: magnus, parvus, multus, novus, pulcher (pulchra, pulchrum).", GOLD)
        a = ADJ12
        rows = [([S(CASES[i], CASE_COL[i], True)],
                 [[S(a["stem"]), S(e[i], CASE_COL[i], True)] for _, e in a["cols"]]) for i in range(6)]
        grid_table(b, [(n, GOLD) for n, _ in a["cols"]], rows).pack(fill="x")

    def third(p):
        case_legend(p)
        b = card(p, "3rd declension adjectives  ·  fortis, forte (brave)",
                 "i-stem pattern: abl. sg. -ī, gen. pl. -ium, neuter pl. -ia.  One-ending adjectives (ingēns, audāx) "
                 "use the same endings; nominative is irregular, e.g. ingēns, ingentis.", GOLD)
        a = ADJ3
        rows = [([S(CASES[i], CASE_COL[i], True)],
                 [[S(a["stem"]), S(e[i], CASE_COL[i], True)] for _, e in a["cols"]]) for i in range(6)]
        grid_table(b, [(n, GOLD) for n, _ in a["cols"]], rows).pack(fill="x")

    def compare(p):
        b = card(p, "Degrees of comparison",
                 "Comparative: stem + -ior (m./f.), -ius (n.), declined like 3rd-declension consonant stems.  "
                 "Superlative: stem + -issimus, -a, -um.  Adverbs: -ē (1st/2nd adj.) or -iter (3rd).  "
                 "Comparative 'than' = quam + same case, or ablative of comparison.", CASE_COL[3])
        rows = [(pos, [[S(c, CASE_COL[i + 1], True)] for i, c in enumerate((cmp_, sup, adv))]) for pos, cmp_, sup, adv in COMPARISON]
        grid_table(b, [("Comparative", CASE_COL[1]), ("Superlative", CASE_COL[2]), ("Adverb (pos · comp · sup)", CASE_COL[3])],
                   rows, corner="Positive").pack(fill="x")

    return SubTabs(parent, [("1st / 2nd decl.", first_second), ("3rd decl.", third), ("Comparison", compare)])


def page_pronouns(parent):
    def make(name):
        heads, rows5 = PRON[name]

        def build(p):
            case_legend(p)
            b = card(p, name, "Personal pronouns (ego, tū) have no gender; reflexive sē: gen. suī, dat. sibi, acc./abl. sē (same in singular and plural)."
                     if name.startswith("ego") else None, GOLD)
            rows = [([S(CASES[i], CASE_COL[i], True)], [[S(w, CASE_COL[i], True)] for w in rows5[i]]) for i in range(5)]
            grid_table(b, [(h, GOLD) for h in heads], rows).pack(fill="x")
            if name.startswith("is"):
                para(b, "is, ea, id = he, she, it / that.  Also the pronoun 'him, her, it'.  Genitive eius is used for 'his/her/its' (not reflexive).",
                     fg=DIM, font=F_SMALL, pady=(8, 0))
            if name.startswith("hic"):
                para(b, "hic = this (near me).  ille = that (over there).  Both decline with -īus in the genitive and -ī in the dative singular.",
                     fg=DIM, font=F_SMALL, pady=(8, 0))
            if name.startswith("quī"):
                para(b, "Relative pronoun: who, which, that.  Agrees in gender and number with its antecedent; case is set by its own clause.  "
                        "Interrogative: quis? quid? = who? what?  (nom. sg. m./f. quis, n. quid; other forms like quī).",
                     fg=DIM, font=F_SMALL, pady=(8, 0))
        return build
    return SubTabs(parent, [(n, make(n)) for n in PRON])


def page_verbs(parent):
    def summary(p):
        tense_legend(p)
        b = card(p, "Personal endings", "Learn these six positions once – they reappear in every tense.", GOLD)
        act, pas, prf = ("#f2c94c", "#5fa8ff", "#ff7a7a")
        A, P = ["ō / m", "s", "t", "mus", "tis", "nt"], ["r", "ris", "tur", "mur", "minī", "ntur"]
        rows = [(PERS[i], [[S("-", DIM), S(A[i], act, True)], [S("-", DIM), S(P[i], pas, True)],
                           [S("-", DIM), S(PERF_E[i], prf, True)]]) for i in range(6)]
        grid_table(b, [("Active (-ō or -m)", act), ("Passive", pas), ("Perfect active", prf)], rows).pack(fill="x")

        b = card(p, "Tense & mood signs", None, CASE_COL[1])
        ex = [("pres", "stem + personal ending", "amō · regō"), ("impf", "-bā- (-ēbā- in 3rd/4th)", "amābam · regēbam"),
              ("fut", "1st/2nd: -bi- / -bo- / -bu-;  3rd/4th: -a- / -ē-", "amābō · regam, regēs"),
              ("perf", "perfect stem + -ī, -istī, -it…", "amāvī"), ("plup", "perfect stem + -erā-", "amāveram"),
              ("fpf", "perfect stem + -eri-", "amāverō")]
        rows = [([S(TENSE_NAME[k], TCOL[k], True)], [[S(sig)], [S(e, TCOL[k], True)]]) for k, sig, e in ex]
        grid_table(b, [("Sign", DIM), ("Example", DIM)], rows).pack(fill="x", pady=(0, 10))
        sj = [("Present subjunctive", "vowel flip: amō → amem · moneō → moneam · regō → regam · audiō → audiam", TCOL["pres"]),
              ("Imperfect subjunctive", "present infinitive + endings: amārem · monērem · regerem · audīrem", TCOL["impf"]),
              ("Perfect subjunctive", "perfect stem + -erim, -erīs…: amāverim", TCOL["perf"]),
              ("Pluperfect subjunctive", "perfect stem + -issem, -issēs…: amāvissem", TCOL["plup"])]
        for n, t, c in sj:
            r = tk.Frame(b, bg=PANEL)
            r.pack(anchor="w", pady=1)
            label(r, n + ":  ", fg=c, font=F_BOLD, bg=PANEL).pack(side="left")
            label(r, t, fg=FG, font=F_BODY, bg=PANEL).pack(side="left")
        para(b, "Perfect passive system = perfect passive participle + sum:  amātus sum (perf.), amātus eram (plup.), "
                "amātus erō (fut. perf.).  Participle agrees with the subject.", fg=DIM, font=F_SMALL, pady=(8, 0))

        for title, voice, key in (("Present active", "a", "pres"), ("Imperfect active", "a", "impf"),
                                  ("Future active", "a", "fut"), ("Present passive", "p", "pres")):
            b = card(p, f"{title} endings by conjugation", None, TCOL[key])
            rows = [(PERS[i], [[S("-", DIM), S(cj[voice][key][i], TCOL[key], True)] for cj in CONJ]) for i in range(6)]
            grid_table(b, [(cj["short"], CONJ_COL[cj["key"]]) for cj in CONJ], rows).pack(fill="x")

    def conj_page(cj):
        def build(p):
            tense_legend(p)
            b = card(p, cj["title"], f"{cj['pp']}  —  {cj['mean']}.   Present stem {cj['stem']}-, perfect stem {cj['perf']}-.",
                     CONJ_COL[cj["key"]])
            for kind in ("ind_a", "ind_p", "sj_a", "sj_p"):
                label(b, KIND_NAME[kind], fg=GOLD, font=F_H2, bg=PANEL).pack(anchor="w", pady=(10, 4))
                verb_table(b, verb_cols(cj, kind)).pack(fill="x")
            label(b, "Non-finite forms", fg=GOLD, font=F_H2, bg=PANEL).pack(anchor="w", pady=(14, 4))
            cols = [CASE_COL[i % 6] for i in range(len(NF_LABELS))]
            grid_table(b, [("Form", DIM)], [([S(NF_LABELS[i], DIM)], [[S(cj["nf"][i], cols[i], True)]]) for i in range(8)]).pack(fill="x")
            para(b, "Passive perfect system is periphrastic: " + cj["pp"].split(", ")[3].replace("um", "us") + " sum / eram / erō …",
                 fg=DIM, font=F_SMALL, pady=(8, 0))
        return build

    tabs = [("Endings at a glance", summary)] + [(cj["short"] + " conj.", conj_page(cj)) for cj in CONJ]
    return SubTabs(parent, tabs)


def page_irregular(parent):
    def make(v):
        def build(p):
            tense_legend(p)
            b = card(p, v["name"], f"{v['mean']}.   {v['note']}", GOLD)
            cols = [dict(name=n, color=TCOL[k], stem="", ends=f) for n, k, f in v["cols"]]
            verb_table(b, cols).pack(fill="x")
        return build
    names = ["sum", "possum", "eō", "ferō", "volō", "nōlō", "mālō"]
    return SubTabs(parent, [(n, make(v)) for n, v in zip(names, IRREGULAR)])


def page_reference(parent):
    def cases(p):
        case_legend(p)
        b = card(p, "The six cases and what they do", None, GOLD)
        rows = [([S(n, CASE_COL[i], True)], [[S(q, DIM)], [S(u)], [S(e, CASE_COL[i])]]) for i, (n, q, u, e) in enumerate(CASE_USE)]
        grid_table(b, [("Question", DIM), ("Main uses", DIM), ("Example", DIM)], rows).pack(fill="x")

    def preps(p):
        data = [("Accusative", CASE_COL[3], "ad to · ante before · apud at, among · circum around · contrā against · inter between · "
                 "intrā within · ob, propter because of · per through · post after · prope near · trans across · ultrā beyond"),
                ("Ablative", CASE_COL[4], "ā / ab from, by (agent) · cum with · dē down from, about · ē / ex out of · prō for, before · "
                 "sine without · coram in the presence of"),
                ("Accusative OR Ablative", GOLD, "in + acc. = into, onto  |  in + abl. = in, on  ·  sub + acc. = to under  |  sub + abl. = under  ·  "
                 "super, subter  (acc. = motion, abl. = position)")]
        for t, c, txt in data:
            b = card(p, f"Prepositions + {t}", None, c)
            para(b, txt)

    def numerals(p):
        nums = [("1", "I", "ūnus, -a, -um", "prīmus"), ("2", "II", "duo, duae, duo", "secundus"), ("3", "III", "trēs, tria", "tertius"),
                ("4", "IV", "quattuor", "quārtus"), ("5", "V", "quīnque", "quīntus"), ("6", "VI", "sex", "sextus"),
                ("7", "VII", "septem", "septimus"), ("8", "VIII", "octō", "octāvus"), ("9", "IX", "novem", "nōnus"),
                ("10", "X", "decem", "decimus")]
        b = card(p, "Numerals 1–10", "ūnus, duo and trēs decline (ūnus like a pronoun: gen. ūnīus, dat. ūnī); the rest up to 100 do not.", GOLD)
        grid_table(b, [("Roman", DIM), ("Cardinal", GOLD), ("Ordinal", CASE_COL[1])],
                   [(n, [[S(r, DIM)], [S(c, GOLD, True)], [S(o, CASE_COL[1], True)]]) for n, r, c, o in nums]).pack(fill="x")

    def parts(p):
        b = card(p, "Principal parts of common verbs", "1st sg. pres. · pres. infinitive · 1st sg. perfect · supine / perfect participle stem.", GOLD)
        rows = [(k, [[S(a, CONJ_COL[k], True)], [S(b_)], [S(c)], [S(d)], [S(m, DIM)]]) for k, a, b_, c, d, m in PRINCIPAL_PARTS]
        grid_table(b, [("Present", GOLD), ("Infinitive", DIM), ("Perfect", DIM), ("Supine", DIM), ("Meaning", DIM)], rows, corner="Conj.").pack(fill="x")

    return SubTabs(parent, [("Case uses", cases), ("Prepositions", preps), ("Numerals", numerals), ("Principal parts", parts)])


# ════════════════════════════════════════════════════════════════════════════
#  MEMORY AIDS
# ════════════════════════════════════════════════════════════════════════════
MNEMONICS = [
    ("Case order", "New Grammar Delights All Bookish Vagabonds  →  Nominative · Genitive · Dative · Accusative · Ablative · Vocative"),
    ("Name the declension from the genitive singular", "-ae · -ī · -is · -ūs · -eī   (say: 'ay, ee, iss, oos, ay-ee')  =  1st, 2nd, 3rd, 4th, 5th."),
    ("Neuter rule", "Nominative = accusative = vocative, always.  In the plural they all end in -a."),
    ("Dative = ablative in the plural", "puellīs · dominīs · rēgibus · manibus · rēbus – learn one, get the other free."),
    ("Accusative: M and S", "Singular -m, plural -s (non-neuter): puellam / puellās · dominum / dominōs · rēgem / rēgēs · rem / rēs."),
    ("Genitive plural has R or M", "-ārum · -ōrum · -um (-ium) · -uum · -ērum.  The 'r' endings belong to the 1st, 2nd and 5th."),
    ("i-stem rule (3rd declension)", "Gen. pl. -ium if the nominative has equal syllables (cīvis, hostis) or the stem ends in two consonants (urbs, mons, nox); "
                                     "neuters in -e, -al, -ar take -ī, -ia, -ium."),
    ("Personal endings", "-ō/-m, -s, -t, -mus, -tis, -nt  –  chant 'm-s-t, mus-tis-nt'.   Passive: -r, -ris, -tur, -mur, -minī, -ntur."),
    ("Perfect endings are unique", "-ī, -istī, -it, -imus, -istis, -ērunt – they never change with the conjugation."),
    ("Tense signs", "Imperfect = BA (amābam).  Future 1st/2nd = BO-BI-BU (amābō, amābit, amābunt).  Future 3rd/4th = A-Ē (regam, regēs).  "
                    "Pluperfect = ERA.  Future perfect = ERI."),
    ("Conjugation from the infinitive", "-āre (1st) · -ēre with LONG ē (2nd) · -ere with SHORT e (3rd) · -īre (4th)."),
    ("Present subjunctive: flip the vowel", "amō → amem · moneō → moneam · regō → regam · audiō → audiam."),
    ("Imperfect subjunctive is a free gift", "Present infinitive + m, s, t, mus, tis, nt: amārem, monērem, regerem, audīrem."),
    ("Vocative", "Same as nominative except 2nd-declension -us → -e (dominus → domine; fīlius → fīlī)."),
]


def page_memory(parent):
    def chants(p):
        case_legend(p)
        para(p, "Say each row aloud in order: Nom – Gen – Dat – Acc – Abl (– Voc).  Then cover the row and repeat from memory.", fg=DIM, font=F_SMALL, pady=(0, 8))
        for d in NOUNS:
            b = card(p, f"{d['title']}  ·  {d['word']}", None, GOLD, pady=(0, 10))
            for num, nm in (("sg", "Singular"), ("pl", "Plural")):
                r = tk.Frame(b, bg=PANEL)
                r.pack(anchor="w", pady=2)
                label(r, f"{nm:<9}", fg=DIM, font=F_SMALL, bg=PANEL, width=9, anchor="w").pack(side="left")
                for i, e in enumerate(d[num]):
                    label(r, ("–" + e) if e else "—", fg=CASE_COL[i], font=F_MID, bg=PANEL).pack(side="left", padx=9)
        b = card(p, "Verb personal endings", None, GOLD, pady=(0, 10))
        for name, ends, col in (("Active", ["-ō/-m", "-s", "-t", "-mus", "-tis", "-nt"], "#f2c94c"),
                                ("Passive", ["-r", "-ris", "-tur", "-mur", "-minī", "-ntur"], "#5fa8ff"),
                                ("Perfect", ["-ī", "-istī", "-it", "-imus", "-istis", "-ērunt"], "#ff7a7a")):
            r = tk.Frame(b, bg=PANEL)
            r.pack(anchor="w", pady=2)
            label(r, name, fg=DIM, font=F_SMALL, bg=PANEL, width=9, anchor="w").pack(side="left")
            for e in ends:
                label(r, e, fg=col, font=F_MID, bg=PANEL).pack(side="left", padx=9)

    def mnem(p):
        for i, (t, txt) in enumerate(MNEMONICS):
            b = card(p, t, None, CASE_COL[i % 6], pady=(0, 8))
            para(b, txt, bg=PANEL)

    return SubTabs(parent, [("Chants", chants), ("Mnemonics & rules", mnem)])


# ════════════════════════════════════════════════════════════════════════════
#  STUDY: FLASHCARDS  &  TYPE-IN DRILL
# ════════════════════════════════════════════════════════════════════════════
class StudyPage(tk.Frame):
    def __init__(self, master, app, mode):
        super().__init__(master, bg=BG)
        self.app, self.mode = app, mode
        self.sel = {g: True for g in GROUPS}
        self.cur, self.last, self.flipped, self.answered = None, None, False, False
        self.ok = self.bad = self.streak = 0

        label(self, "Flashcards" if mode == "flash" else "Type-in Drill", fg=GOLD, font=F_H1).pack(anchor="w")
        label(self, ("Flip the card, then grade yourself.  Missed cards return more often (Leitner boxes 1–5)."
                     if mode == "flash" else
                     "Type the ending (or the whole form).  Return checks, Return again moves on."),
              fg=DIM, font=F_SMALL).pack(anchor="w", pady=(2, 8))

        row = tk.Frame(self, bg=BG)
        row.pack(fill="x")
        self.chips = {}
        for g in GROUPS:
            c = Chip(row, g, on=True, color=CASE_COL[GROUPS.index(g) % 6], command=lambda ch, g=g: self.toggle(g, ch))
            c.pack(side="left", padx=(0, 5), pady=2)
            self.chips[g] = c
        Btn(row, "All", lambda: self.setall(True), PANEL2, FG, F_SMALL, 10, 3).pack(side="left", padx=(8, 3))
        Btn(row, "None", lambda: self.setall(False), PANEL2, FG, F_SMALL, 10, 3).pack(side="left")

        stat = tk.Frame(self, bg=BG)
        stat.pack(fill="x", pady=(10, 0))
        self.l_stats = label(stat, "", fg=DIM, font=F_SMALL)
        self.l_stats.pack(side="left")
        self.bar = tk.Canvas(stat, width=260, height=10, bg=PANEL2, highlightthickness=0)
        self.bar.pack(side="right")
        self.l_mast = label(stat, "mastery ", fg=DIM, font=F_SMALL)
        self.l_mast.pack(side="right", padx=(0, 6))

        outer = tk.Frame(self, bg=BORDER)
        outer.pack(fill="x", pady=10)
        self.stage = tk.Frame(outer, bg=PANEL, height=330)
        self.stage.pack(fill="both", padx=1, pady=1)
        self.stage.pack_propagate(False)
        self.stripe = tk.Frame(self.stage, bg=GOLD, height=5)
        self.stripe.pack(fill="x")
        self.l_kind = label(self.stage, "", fg=DIM, font=F_SMALL, bg=PANEL)
        self.l_kind.pack(pady=(16, 0))
        self.l_title = label(self.stage, "", fg=GOLD, font=F_H1, bg=PANEL)
        self.l_title.pack(pady=(6, 0))
        self.l_sub = label(self.stage, "", fg=FG, font=F_BODY, bg=PANEL, wraplength=780, justify="center")
        self.l_sub.pack(pady=(2, 6))
        self.l_ans = label(self.stage, "", fg=GOLD, font=F_BIG, bg=PANEL)
        self.l_ans.pack(pady=(4, 0))
        self.entry = None
        if mode == "type":
            self.entry = tk.Entry(self.stage, width=16, font=(SERIF, 26), justify="center", bg="#0e1018", fg=FG,
                                  insertbackground=GOLD, relief="flat", highlightthickness=1,
                                  highlightbackground=BORDER, highlightcolor=GOLD)
            self.entry.pack(pady=(4, 0))
            self.entry.bind("<Return>", lambda e: self.enter())
        self.l_full = label(self.stage, "", fg=DIM, font=F_BODY, bg=PANEL)
        self.l_full.pack(pady=(6, 0))

        ctl = tk.Frame(self, bg=BG)
        ctl.pack(fill="x")
        if mode == "flash":
            Btn(ctl, "Flip  (space)", self.flip, PANEL2, FG).pack(side="left", padx=(0, 8))
            Btn(ctl, "✘  Missed  (←)", lambda: self.grade(False), RED).pack(side="left", padx=(0, 8))
            Btn(ctl, "✔  Got it  (→)", lambda: self.grade(True), GREEN).pack(side="left")
        else:
            Btn(ctl, "Check / Next  (⏎)", self.enter, GOLD).pack(side="left", padx=(0, 8))
            Btn(ctl, "Show answer", self.reveal, PANEL2, FG).pack(side="left", padx=(0, 18))
            macron_bar(ctl, app).pack(side="left")
            self.mchip = Chip(ctl, "Ignore macrons", on=app.opts["ignore"], command=self.set_ignore)
            self.mchip.pack(side="right")
        Btn(ctl, "Reset progress", self.reset, BG, DIM, F_SMALL, 6, 3).pack(side="right", padx=8)
        self.next_card()

    # -- selection -----------------------------------------------------------
    def toggle(self, g, chip):
        self.sel[g] = chip.on
        self.update_bar()

    def setall(self, v):
        for g, c in self.chips.items():
            c.set(v)
            self.sel[g] = v
        self.update_bar()

    def set_ignore(self, chip):
        self.app.opts["ignore"] = chip.on

    def pool(self):
        return [c for c in self.app.cards if self.sel[c["group"]]]

    def pick(self):
        pool = self.pool()
        if not pool:
            return None
        box = self.app.prog["box"]
        for _ in range(6):
            c = random.choices(pool, [(6 - box.get(c["key"], 1)) ** 2 for c in pool])[0]
            if c is not self.last or len(pool) == 1:
                break
        return c

    def update_bar(self):
        pool = self.pool()
        box = self.app.prog["box"]
        mastered = sum(1 for c in pool if box.get(c["key"], 1) >= 4)
        frac = mastered / len(pool) if pool else 0
        self.bar.delete("all")
        self.bar.create_rectangle(0, 0, 260 * frac, 10, fill=GREEN, width=0)
        self.l_mast.config(text=f"mastery {mastered}/{len(pool)}")
        self.l_stats.config(text=f"✔ {self.ok}   ✘ {self.bad}   streak {self.streak}   ·   {len(pool)} cards selected")

    # -- flow ----------------------------------------------------------------
    def next_card(self):
        self.cur = self.pick()
        self.flipped = self.answered = False
        self.update_bar()
        if self.entry:
            self.entry.config(state="normal", bg="#0e1018")
            self.entry.delete(0, "end")
        if not self.cur:
            self.l_kind.config(text="")
            self.l_title.config(text="Select at least one topic above", fg=DIM)
            self.l_sub.config(text="")
            self.l_ans.config(text="")
            self.l_full.config(text="")
            return
        c = self.cur
        self.stripe.config(bg=c["color"])
        self.l_kind.config(text=c["group"].upper())
        self.l_title.config(text=c["title"], fg=c["color"])
        self.l_sub.config(text=c["sub"])
        self.l_ans.config(text="?" if self.mode == "flash" else "", fg=DIM)
        self.l_full.config(text="")
        if self.entry:
            self.entry.focus_set()

    def show_answer(self):
        c = self.cur
        self.l_ans.config(text="-" + c["ans"], fg=c["color"])
        self.l_full.config(text=f"e.g.  {c['full']}")

    def flip(self):
        if self.cur and not self.flipped:
            self.flipped = True
            self.show_answer()

    def reveal(self):
        if self.cur:
            self.show_answer()
            self.answered = True

    def grade(self, ok):
        if not self.cur:
            return
        box = self.app.prog["box"]
        k = self.cur["key"]
        box[k] = min(5, box.get(k, 1) + 1) if ok else 1
        self.ok += ok
        self.bad += (not ok)
        self.streak = self.streak + 1 if ok else 0
        save_progress(self.app.prog)
        self.last = self.cur
        self.next_card()

    def enter(self):
        if not self.cur:
            return
        if self.answered:
            self.last = self.cur
            self.next_card()
            return
        guess = norm(self.entry.get(), self.app.opts["ignore"])
        good = guess in accepted(self.cur["stem"], self.cur["ans"], "ends", self.app.opts["ignore"])
        self.entry.config(bg="#173a2a" if good else "#4a1f2a")
        self.show_answer()
        self.answered = True
        box = self.app.prog["box"]
        k = self.cur["key"]
        box[k] = min(5, box.get(k, 1) + 1) if good else 1
        self.ok += good
        self.bad += (not good)
        self.streak = self.streak + 1 if good else 0
        save_progress(self.app.prog)
        self.update_bar()

    def reset(self):
        if messagebox.askyesno("Reset progress", "Forget all flashcard progress?"):
            self.app.prog["box"] = {}
            save_progress(self.app.prog)
            self.ok = self.bad = self.streak = 0
            self.next_card()

    def on_key(self, e):
        if self.mode != "flash":
            return
        if e.keysym == "space":
            self.flip()
        elif e.keysym in ("Right", "k", "K"):
            self.grade(True)
        elif e.keysym in ("Left", "j", "J"):
            self.grade(False)


# ════════════════════════════════════════════════════════════════════════════
#  STUDY: WORKSHEET
# ════════════════════════════════════════════════════════════════════════════
def build_topics():
    T = []
    for d in NOUNS:
        f = noun_forms(d)
        T.append(dict(label=f"Noun · {d['title']}  ({d['word']})", cols=[("Singular", GOLD), ("Plural", GOLD)],
                      rows=[(CASES[i], CASE_COL[i]) for i in range(6)],
                      cells=[[f["sg"][i], f["pl"][i]] for i in range(6)],
                      colors=[[CASE_COL[i]] * 2 for i in range(6)]))
    for nm, a in (("bonus, bona, bonum", ADJ12), ("fortis, forte", ADJ3)):
        T.append(dict(label=f"Adjective · {nm}", cols=[(n, GOLD) for n, _ in a["cols"]],
                      rows=[(CASES[i], CASE_COL[i]) for i in range(6)],
                      cells=[[(a["stem"], e[i]) for _, e in a["cols"]] for i in range(6)],
                      colors=[[CASE_COL[i]] * len(a["cols"]) for i in range(6)]))
    for name, (heads, rows5) in PRON.items():
        T.append(dict(label=f"Pronoun · {name}", cols=[(h, GOLD) for h in heads],
                      rows=[(CASES[i], CASE_COL[i]) for i in range(5)],
                      cells=[[("", w) for w in rows5[i]] for i in range(5)],
                      colors=[[CASE_COL[i]] * len(heads) for i in range(5)]))
    for cj in CONJ:
        for kind in ("ind_a", "ind_p", "sj_a", "sj_p"):
            cols = verb_cols(cj, kind)
            T.append(dict(label=f"Verb · {cj['title']} — {KIND_NAME[kind]}",
                          cols=[(c["name"], c["color"]) for c in cols], rows=[(PERS[i], DIM) for i in range(6)],
                          cells=[[(c["stem"], c["ends"][i]) for c in cols] for i in range(6)],
                          colors=[[c["color"] for c in cols] for i in range(6)]))
    for v in IRREGULAR:
        T.append(dict(label=f"Irregular · {v['name']}", cols=[(n, TCOL[k]) for n, k, _ in v["cols"]],
                      rows=[(PERS[i], DIM) for i in range(6)],
                      cells=[[("", f[i]) for _, _, f in v["cols"]] for i in range(6)],
                      colors=[[TCOL[k] for _, k, _ in v["cols"]] for i in range(6)]))
    return T


class WorksheetPage(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg=BG)
        self.app = app
        self.topics = build_topics()
        self.idx, self.mode, self.diff = 0, "ends", 60
        self.entries, self.blank = [], set()

        label(self, "Worksheet", fg=GOLD, font=F_H1).pack(anchor="w")
        label(self, "Fill the blanks, press Return to jump to the next box, then Check.  Lower the blanks slider for scaffolding, "
                    "raise it to 100 % for full recall.", fg=DIM, font=F_SMALL, wraplength=900, justify="left").pack(anchor="w", pady=(2, 8))

        top = tk.Frame(self, bg=BG)
        top.pack(fill="x")
        self.combo = ttk.Combobox(top, values=[t["label"] for t in self.topics], state="readonly", width=58)
        self.combo.current(0)
        self.combo.pack(side="left")
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.select(self.combo.current()))
        self.mchip = Chip(top, "Endings only", on=True, command=self.set_mode)
        self.mchip.pack(side="left", padx=(12, 4))
        self.ichip = Chip(top, "Ignore macrons", on=app.opts["ignore"], command=self.set_ignore)
        self.ichip.pack(side="left", padx=4)

        row2 = tk.Frame(self, bg=BG)
        row2.pack(fill="x", pady=(8, 4))
        self.l_diff = label(row2, "Blanks: 60 %", fg=DIM, font=F_SMALL, width=12, anchor="w")
        self.l_diff.pack(side="left")
        self.scale = tk.Scale(row2, from_=10, to=100, resolution=10, orient="horizontal", showvalue=False, length=220,
                              bg=BG, troughcolor=PANEL2, highlightthickness=0, fg=FG, activebackground=GOLD,
                              command=self.set_diff)
        self.scale.set(self.diff)
        self.scale.pack(side="left")
        Btn(row2, "New worksheet", self.build, PANEL2, FG, F_SMALL, 12, 4).pack(side="left", padx=12)
        macron_bar(row2, app).pack(side="left", padx=12)

        self.sc = Scroll(self)
        self.sc.pack(fill="both", expand=True, pady=(4, 6))

        bot = tk.Frame(self, bg=BG)
        bot.pack(fill="x")
        Btn(bot, "✔ Check", self.check, GREEN).pack(side="left", padx=(0, 8))
        Btn(bot, "Reveal answers", self.reveal, PANEL2, FG).pack(side="left", padx=(0, 8))
        Btn(bot, "Clear", self.clear, PANEL2, FG).pack(side="left", padx=(0, 8))
        Btn(bot, "Export printable ↗", self.export, GOLD).pack(side="left")
        self.l_score = label(bot, "", fg=GOLD, font=F_H2)
        self.l_score.pack(side="right")
        self.build()

    # -- controls ------------------------------------------------------------
    def select(self, i):
        self.idx = i
        self.build()

    def set_mode(self, chip):
        self.mode = "ends" if chip.on else "full"
        chip.config(text="Endings only" if chip.on else "Full forms")
        self.build()

    def set_ignore(self, chip):
        self.app.opts["ignore"] = chip.on

    def set_diff(self, v):
        self.diff = int(float(v))
        self.l_diff.config(text=f"Blanks: {self.diff} %")

    # -- construction --------------------------------------------------------
    def build(self):
        for w in self.sc.inner.winfo_children():
            w.destroy()
        self.entries = []
        self.l_score.config(text="")
        t = self.topics[self.idx]
        nr, nc = len(t["rows"]), len(t["cols"])
        pool = [(r, c) for r in range(nr) for c in range(nc)
                if self.mode == "full" or t["cells"][r][c][1] != ""]
        n = max(1, round(len(pool) * self.diff / 100))
        self.blank = set(random.sample(pool, n))

        b = card(self.sc.inner, t["label"], "Type the missing " + ("endings (stems are shown)." if self.mode == "ends"
                 else "complete forms.") + "  Zero-ending forms and irregular tables are always complete words.", GOLD)
        rows = []
        for r in range(nr):
            cells = []
            for c in range(nc):
                stem, end = t["cells"][r][c]
                color = t["colors"][r][c]
                if (r, c) in self.blank:
                    cells.append(self._entry_cell(stem, end, color))
                elif end == "":
                    cells.append([S(stem, color, True)])
                else:
                    cells.append([S(stem), S(end, color, True)])
            rn, rc = t["rows"][r]
            rows.append(([S(rn, rc, True)], cells))
        grid_table(b, [(h, col) for h, col in t["cols"]], rows).pack(fill="x")
        self.sc.canvas.yview_moveto(0)

    def _entry_cell(self, stem, end, color):
        def make(frame, bg):
            if self.mode == "ends" and stem:
                tk.Label(frame, text=stem, fg=FG, bg=bg, font=F_BODY, bd=0, padx=0, pady=0).pack(side="left")
            e = tk.Entry(frame, width=9 if self.mode == "ends" else 12, font=F_BODY, justify="center", bg="#0e1018",
                         fg=color, insertbackground=color, relief="flat", highlightthickness=1,
                         highlightbackground=BORDER, highlightcolor=color)
            e.pack(side="left")
            e.bind("<Return>", lambda ev: (ev.widget.tk_focusNext().focus_set(), "break")[1])
            self.entries.append((e, stem, end, color))
        return make

    # -- actions -------------------------------------------------------------
    def expected(self, stem, end):
        end = end.split("/")[0].strip()
        return end if self.mode == "ends" else stem + end

    def check(self):
        ign, good = self.app.opts["ignore"], 0
        for e, stem, end, color in self.entries:
            ok = norm(e.get(), ign) in accepted(stem, end, self.mode, ign) and e.get().strip() != ""
            e.config(bg="#173a2a" if ok else "#4a1f2a", fg=GREEN if ok else RED)
            good += ok
        n = len(self.entries)
        self.l_score.config(text=f"Score  {good} / {n}   ({round(100 * good / n) if n else 0} %)")

    def reveal(self):
        for e, stem, end, color in self.entries:
            e.delete(0, "end")
            e.insert(0, self.expected(stem, end))
            e.config(bg="#2a2412", fg=GOLD)

    def clear(self):
        for e, stem, end, color in self.entries:
            e.delete(0, "end")
            e.config(bg="#0e1018", fg=color)
        self.l_score.config(text="")

    def export(self):
        t = self.topics[self.idx]
        path = filedialog.asksaveasfilename(defaultextension=".html", initialfile="latin_worksheet.html",
                                            filetypes=[("HTML page", "*.html")])
        if not path:
            return

        def table(key):
            h = ["<table><tr><th></th>" + "".join(f"<th style='color:{c}'>{html.escape(n)}</th>" for n, c in t["cols"]) + "</tr>"]
            for r, (rn, rc) in enumerate(t["rows"]):
                h.append(f"<tr><th style='color:{rc if rc != DIM else '#555'}'>{html.escape(rn)}</th>")
                for c in range(len(t["cols"])):
                    stem, end = t["cells"][r][c]
                    if (r, c) in self.blank:
                        if key:
                            h.append(f"<td><b>{html.escape(stem + end)}</b></td>")
                        else:
                            h.append(f"<td>{html.escape(stem if self.mode == 'ends' else '')}<span class='b'></span></td>")
                    else:
                        h.append(f"<td>{html.escape(stem + end)}</td>")
                h.append("</tr>")
            h.append("</table>")
            return "".join(h)
        page = f"""<!doctype html><meta charset='utf-8'><title>Latin worksheet</title>
<style>body{{font:18px Georgia,serif;margin:40px;color:#222}}h1{{font-size:24px}}
table{{border-collapse:collapse;margin:14px 0}}td,th{{border:1px solid #bbb;padding:8px 14px;text-align:center}}
.b{{display:inline-block;min-width:70px;border-bottom:1.5px solid #000}}.key{{page-break-before:always}}</style>
<h1>Latin worksheet — {html.escape(t['label'])}</h1><p>Name: ____________________ &nbsp; Date: ____________</p>
{table(False)}<div class='key'><h1>Answer key</h1>{table(True)}</div>"""
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(page)
            webbrowser.open("file://" + path)
        except OSError as err:
            messagebox.showerror("Export failed", str(err))


# ════════════════════════════════════════════════════════════════════════════
#  APPLICATION SHELL
# ════════════════════════════════════════════════════════════════════════════
NAV = [("GUIDE", None),
       ("Overview", lambda p, a: scrolled(page_overview)(p)),
       ("Nouns", lambda p, a: page_nouns(p)),
       ("Adjectives", lambda p, a: page_adjectives(p)),
       ("Pronouns", lambda p, a: page_pronouns(p)),
       ("Verbs", lambda p, a: page_verbs(p)),
       ("Irregular Verbs", lambda p, a: page_irregular(p)),
       ("Reference", lambda p, a: page_reference(p)),
       ("STUDY", None),
       ("Flashcards", lambda p, a: StudyPage(p, a, "flash")),
       ("Type-in Drill", lambda p, a: StudyPage(p, a, "type")),
       ("Worksheet", lambda p, a: WorksheetPage(p, a)),
       ("Memory Aids", lambda p, a: page_memory(p))]
ICONS = {"Overview": "✦", "Nouns": "Ⅰ", "Adjectives": "Ⅱ", "Pronouns": "Ⅲ", "Verbs": "Ⅳ", "Irregular Verbs": "Ⅴ",
         "Reference": "§", "Flashcards": "◈", "Type-in Drill": "⌨", "Worksheet": "✎", "Memory Aids": "♪"}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Latina · Grammar Studio")
        self.geometry("1260x840")
        self.minsize(1060, 700)
        self.configure(bg=BG)
        self.opts = {"ignore": True}
        self.prog = load_progress()
        self.cards = build_cards()
        self.pages, self.cur, self.navbtns = {}, None, {}

        head = tk.Frame(self, bg=HEAD_BG)
        head.pack(fill="x")
        label(head, "LATINA", fg=GOLD, font=F_TITLE, bg=HEAD_BG).pack(side="left", padx=(24, 12), pady=(12, 8))
        label(head, "Grammar Studio  ·  declensions & conjugations", fg=DIM, font=(SERIF, 14, "italic"),
              bg=HEAD_BG).pack(side="left", pady=(20, 0))
        self.strip = tk.Canvas(self, height=4, bg=BG, highlightthickness=0)
        self.strip.pack(fill="x")
        self.strip.bind("<Configure>", self._strip)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)
        side = tk.Frame(body, bg=HEAD_BG, width=210)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        self.content = tk.Frame(body, bg=BG)
        self.content.pack(side="left", fill="both", expand=True, padx=(22, 14), pady=(16, 10))

        for name, builder in NAV:
            if builder is None:
                label(side, name, fg=DIM, font=(SANS, 10, "bold"), bg=HEAD_BG).pack(anchor="w", padx=20, pady=(18, 4))
                continue
            b = tk.Label(side, text=f"  {ICONS[name]}   {name}", anchor="w", fg=FG, bg=HEAD_BG, font=F_NAV,
                         padx=14, pady=9, cursor="hand2")
            b.pack(fill="x")
            b.bind("<Button-1>", lambda e, n=name: self.show(n))
            b.bind("<Enter>", lambda e, n=name: self.navbtns[n].config(bg=PANEL2) if n != self.cur else None)
            b.bind("<Leave>", lambda e, n=name: self.navbtns[n].config(bg=HEAD_BG) if n != self.cur else None)
            self.navbtns[name] = b

        self.foot = label(self, "Tip: macrons are ignored in answers by default — toggle “Ignore macrons” to drill vowel length.",
                          fg=DIM, font=F_SMALL, bg=HEAD_BG, anchor="w", padx=18, pady=5)
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
        for i, c in enumerate(CASE_COL):
            self.strip.create_rectangle(i * w, 0, (i + 1) * w + 1, 4, fill=c, width=0)

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
                    if getattr(e, "num", 0) == 4:
                        d = -1
                    elif getattr(e, "num", 0) == 5:
                        d = 1
                    else:
                        d = -e.delta if abs(e.delta) < 30 else -int(e.delta / 120)
                    w.canvas.yview_scroll(d, "units")
                return
            w = w.master

    def _key(self, e):
        try:
            if isinstance(self.focus_get(), (tk.Entry, ttk.Combobox)):
                return
        except Exception:
            return
        page = self.pages.get(self.cur)
        if hasattr(page, "on_key"):
            page.on_key(e)

    def _close(self):
        save_progress(self.prog)
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
