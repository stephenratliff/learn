#!/usr/bin/env python3
"""
Ἑλληνικὴ Γραμματική — Ancient Greek Grammar Trainer
A single-file, dependency-free terminal program:
  1. Colour-coded reference guide (alphabet, declensions, conjugations, syntax)
  2. Worksheet — type the requested form, get checked immediately
  3. Ending Drill — flashcard-style memorization of case/tense endings,
     with wrong answers recycled until you get them right

Run:  python3 greek_grammar.py
Works fully offline. Uses only the standard library (ANSI colour codes,
which macOS Terminal / iTerm2 support natively).
"""
import os
import random
import sys
import unicodedata

# ----------------------------------------------------------------------
# Colour
# ----------------------------------------------------------------------
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITAL = "\033[3m"
    NOM = "\033[38;5;33m"    # blue
    GEN = "\033[38;5;35m"    # green
    DAT = "\033[38;5;214m"   # orange
    ACC = "\033[38;5;196m"   # red
    VOC = "\033[38;5;135m"   # purple
    AUG = "\033[38;5;37m"    # teal   (augment / reduplication)
    TEN = "\033[38;5;178m"   # gold   (tense sign)
    END = "\033[38;5;205m"   # pink   (personal / case ending)
    HEAD = "\033[38;5;250m\033[1m"
    OK = "\033[38;5;40m"
    NO = "\033[38;5;203m"
    TITLE = "\033[38;5;229m\033[1m"

CASE_COLOR = {"Nom": C.NOM, "Gen": C.GEN, "Dat": C.DAT, "Acc": C.ACC, "Voc": C.VOC}
NO_COLOR = "--no-color" in sys.argv or not sys.stdout.isatty()

def cz(text, color):
    if NO_COLOR:
        return text
    return f"{color}{text}{C.RESET}"

def clear():
    if not NO_COLOR:
        os.system("cls" if os.name == "nt" else "clear")

def pause():
    input(cz("\n  ↵ Press Enter to continue…", C.DIM))

def rule(ch="─", n=64):
    print(cz(ch * n, C.DIM))

def title(t):
    clear()
    print(cz(f"  {t}", C.TITLE))
    rule()

# ----------------------------------------------------------------------
# Reference data
# ----------------------------------------------------------------------
ALPHABET = [
    ("Α α", "alpha", "a"), ("Β β", "beta", "b"), ("Γ γ", "gamma", "g"),
    ("Δ δ", "delta", "d"), ("Ε ε", "epsilon", "e (short)"), ("Ζ ζ", "zeta", "zd"),
    ("Η η", "eta", "ē (long)"), ("Θ θ", "theta", "th"), ("Ι ι", "iota", "i"),
    ("Κ κ", "kappa", "k"), ("Λ λ", "lambda", "l"), ("Μ μ", "mu", "m"),
    ("Ν ν", "nu", "n"), ("Ξ ξ", "xi", "x"), ("Ο ο", "omicron", "o (short)"),
    ("Π π", "pi", "p"), ("Ρ ρ", "rho", "r"), ("Σ σ/ς", "sigma", "s (ς final)"),
    ("Τ τ", "tau", "t"), ("Υ υ", "upsilon", "u/ü"), ("Φ φ", "phi", "ph"),
    ("Χ χ", "chi", "kh"), ("Ψ ψ", "psi", "ps"), ("Ω ω", "omega", "ō (long)"),
]

CASES = ["Nom", "Gen", "Dat", "Acc", "Voc"]

# noun paradigms: name, gloss, sg forms, pl forms  (Nom Gen Dat Acc Voc)
ARTICLE = ("Article", "the",
           ["ὁ", "τοῦ", "τῷ", "τόν", "—"], ["οἱ", "τῶν", "τοῖς", "τούς", "—"],
           ["ἡ", "τῆς", "τῇ", "τήν", "—"], ["αἱ", "τῶν", "ταῖς", "τάς", "—"],
           ["τό", "τοῦ", "τῷ", "τό", "—"], ["τά", "τῶν", "τοῖς", "τά", "—"])

NOUNS = [
    ("τιμή", "1st · fem. η-stem — 'honor'",
     ["τιμή", "τιμῆς", "τιμῇ", "τιμήν", "τιμή"],
     ["τιμαί", "τιμῶν", "τιμαῖς", "τιμάς", "τιμαί"]),
    ("χώρα", "1st · fem. α-stem — 'land'",
     ["χώρα", "χώρας", "χώρᾳ", "χώραν", "χώρα"],
     ["χῶραι", "χωρῶν", "χώραις", "χώρας", "χῶραι"]),
    ("πολίτης", "1st · masc. — 'citizen'",
     ["πολίτης", "πολίτου", "πολίτῃ", "πολίτην", "πολῖτα"],
     ["πολῖται", "πολιτῶν", "πολίταις", "πολίτας", "πολῖται"]),
    ("λόγος", "2nd · masc. — 'word'",
     ["λόγος", "λόγου", "λόγῳ", "λόγον", "λόγε"],
     ["λόγοι", "λόγων", "λόγοις", "λόγους", "λόγοι"]),
    ("δῶρον", "2nd · neut. — 'gift'",
     ["δῶρον", "δώρου", "δώρῳ", "δῶρον", "δῶρον"],
     ["δῶρα", "δώρων", "δώροις", "δῶρα", "δῶρα"]),
    ("φύλαξ", "3rd · consonant stem — 'guard'",
     ["φύλαξ", "φύλακος", "φύλακι", "φύλακα", "φύλαξ"],
     ["φύλακες", "φυλάκων", "φύλαξι(ν)", "φύλακας", "φύλακες"]),
    ("σῶμα", "3rd · neut. -ματ — 'body'",
     ["σῶμα", "σώματος", "σώματι", "σῶμα", "σῶμα"],
     ["σώματα", "σωμάτων", "σώμασι(ν)", "σώματα", "σώματα"]),
    ("πόλις", "3rd · ι-stem — 'city'",
     ["πόλις", "πόλεως", "πόλει", "πόλιν", "πόλι"],
     ["πόλεις", "πόλεων", "πόλεσι(ν)", "πόλεις", "πόλεις"]),
]

ADJ_AGATHOS = ("ἀγαθός, -ή, -όν", "good",
               ["ἀγαθός", "ἀγαθοῦ", "ἀγαθῷ", "ἀγαθόν", "ἀγαθέ"],
               ["ἀγαθοί", "ἀγαθῶν", "ἀγαθοῖς", "ἀγαθούς", "ἀγαθοί"],
               ["ἀγαθή", "ἀγαθῆς", "ἀγαθῇ", "ἀγαθήν", "ἀγαθή"],
               ["ἀγαθαί", "ἀγαθῶν", "ἀγαθαῖς", "ἀγαθάς", "ἀγαθαί"],
               ["ἀγαθόν", "ἀγαθοῦ", "ἀγαθῷ", "ἀγαθόν", "ἀγαθόν"],
               ["ἀγαθά", "ἀγαθῶν", "ἀγαθοῖς", "ἀγαθά", "ἀγαθά"])

PERSONS = ["1 sg", "2 sg", "3 sg", "1 pl", "2 pl", "3 pl"]
PRONOUN_I_WE = ["ἐγώ / ἡμεῖς", "ἐμοῦ (μου) / ἡμῶν", "ἐμοί (μοι) / ἡμῖν",
                "ἐμέ (με) / ἡμᾶς", "σύ / ὑμεῖς", "σοῦ (σου) / ὑμῶν",
                "σοί (σοι) / ὑμῖν", "σέ (σε) / ὑμᾶς"]

# λύω principal parts and full indicative system
LUO_PARTS = "λύω · λύσω · ἔλυσα · λέλυκα · λέλυμαι · ἐλύθην"
LUO = {
    "Present active":   ["λύω", "λύεις", "λύει", "λύομεν", "λύετε", "λύουσι(ν)"],
    "Present mid/pass": ["λύομαι", "λύῃ", "λύεται", "λυόμεθα", "λύεσθε", "λύονται"],
    "Imperfect active":   ["ἔλυον", "ἔλυες", "ἔλυε(ν)", "ἐλύομεν", "ἐλύετε", "ἔλυον"],
    "Imperfect mid/pass": ["ἐλυόμην", "ἐλύου", "ἐλύετο", "ἐλυόμεθα", "ἐλύεσθε", "ἐλύοντο"],
    "Future active": ["λύσω", "λύσεις", "λύσει", "λύσομεν", "λύσετε", "λύσουσι(ν)"],
    "Future middle": ["λύσομαι", "λύσῃ", "λύσεται", "λυσόμεθα", "λύσεσθε", "λύσονται"],
    "Aorist active": ["ἔλυσα", "ἔλυσας", "ἔλυσε(ν)", "ἐλύσαμεν", "ἐλύσατε", "ἔλυσαν"],
    "Aorist middle": ["ἐλυσάμην", "ἐλύσω", "ἐλύσατο", "ἐλυσάμεθα", "ἐλύσασθε", "ἐλύσαντο"],
    "Aorist passive": ["ἐλύθην", "ἐλύθης", "ἐλύθη", "ἐλύθημεν", "ἐλύθητε", "ἐλύθησαν"],
    "Perfect active": ["λέλυκα", "λέλυκας", "λέλυκε(ν)", "λελύκαμεν", "λελύκατε", "λελύκασι(ν)"],
    "Perfect mid/pass": ["λέλυμαι", "λέλυσαι", "λέλυται", "λελύμεθα", "λέλυσθε", "λέλυνται"],
}
LUO_SUBJ = ["λύω", "λύῃς", "λύῃ", "λύωμεν", "λύητε", "λύωσι(ν)"]
LUO_OPT = ["λύοιμι", "λύοις", "λύοι", "λύοιμεν", "λύοιτε", "λύοιεν"]
LUO_IMPV_ACT = {"2 sg": "λῦε", "3 sg": "λυέτω", "2 pl": "λύετε", "3 pl": "λυέτωσαν"}
LUO_IMPV_MP = {"2 sg": "λύου", "3 sg": "λυέσθω", "2 pl": "λύεσθε", "3 pl": "λυέσθωσαν"}
LUO_INF = {"Present act": "λύειν", "Present mid/pass": "λύεσθαι", "Future act": "λύσειν",
           "Aorist act": "λῦσαι", "Aorist mid": "λύσασθαι", "Aorist pass": "λυθῆναι",
           "Perfect act": "λελυκέναι", "Perfect mid/pass": "λελῦσθαι"}

CONTRACT = {
    "τιμάω (α + )": ["τιμῶ", "τιμᾷς", "τιμᾷ", "τιμῶμεν", "τιμᾶτε", "τιμῶσι(ν)"],
    "ποιέω (ε + )": ["ποιῶ", "ποιεῖς", "ποιεῖ", "ποιοῦμεν", "ποιεῖτε", "ποιοῦσι(ν)"],
    "δηλόω (ο + )": ["δηλῶ", "δηλοῖς", "δηλοῖ", "δηλοῦμεν", "δηλοῦτε", "δηλοῦσι(ν)"],
}
EIMI = {
    "Present": ["εἰμί", "εἶ", "ἐστί(ν)", "ἐσμέν", "ἐστέ", "εἰσί(ν)"],
    "Imperfect": ["ἦν", "ἦσθα", "ἦν", "ἦμεν", "ἦτε", "ἦσαν"],
    "Future": ["ἔσομαι", "ἔσῃ", "ἔσται", "ἐσόμεθα", "ἔσεσθε", "ἔσονται"],
}
DIDOMI_PRES = ["δίδωμι", "δίδως", "δίδωσι(ν)", "δίδομεν", "δίδοτε", "διδόασι(ν)"]
OIDA_PERF = ["οἶδα", "οἶσθα", "οἶδε(ν)", "ἴσμεν", "ἴστε", "ἴσασι(ν)"]

# ---- ending inventories used for drilling & reference legends ----
NOUN_ENDINGS = {
    "1st decl. fem. (η-stem, sg)": dict(zip(CASES, ["-η", "-ης", "-ῃ", "-ην", "-η"])),
    "1st decl. fem. (η-stem, pl)": dict(zip(CASES, ["-αι", "-ων", "-αις", "-ας", "-αι"])),
    "2nd decl. masc. (sg)": dict(zip(CASES, ["-ος", "-ου", "-ῳ", "-ον", "-ε"])),
    "2nd decl. masc. (pl)": dict(zip(CASES, ["-οι", "-ων", "-οις", "-ους", "-οι"])),
    "2nd decl. neut. (sg)": dict(zip(CASES, ["-ον", "-ου", "-ῳ", "-ον", "-ον"])),
    "2nd decl. neut. (pl)": dict(zip(CASES, ["-α", "-ων", "-οις", "-α", "-α"])),
    "3rd decl. cons. stem (sg)": dict(zip(CASES, ["(varies)", "-ος", "-ι", "-α", "(varies)"])),
    "3rd decl. cons. stem (pl)": dict(zip(CASES, ["-ες", "-ων", "-σι(ν)", "-ας", "-ες"])),
}
VERB_ENDINGS = {
    "Primary active (pres/fut)": dict(zip(PERSONS, ["-ω", "-εις", "-ει", "-ομεν", "-ετε", "-ουσι(ν)"])),
    "Secondary active (impf/aor)": dict(zip(PERSONS, ["-ον", "-ες", "-ε(ν)", "-ομεν", "-ετε", "-ον"])),
    "Primary mid/pass (pres/fut)": dict(zip(PERSONS, ["-ομαι", "-ῃ", "-εται", "-ομεθα", "-εσθε", "-ονται"])),
    "Secondary mid/pass (impf/aor mid)": dict(zip(PERSONS, ["-όμην", "-ου", "-ετο", "-όμεθα", "-εσθε", "-οντο"])),
}
MARKERS = [
    ("Augment", "ἐ-", "prefixed to a consonant-initial stem in past indicative tenses (impf, aor)"),
    ("Reduplication", "consonant + ε-", "prefixed in the perfect stem, e.g. λύω → λέλυκα"),
    ("Future/aorist active-mid sign", "-σ-", "λύσω, ἔλυσα"),
    ("Aorist passive sign", "-θ-", "ἐλύθην"),
    ("Perfect active sign", "-κ-", "λέλυκα"),
]

SYNTAX_NOTES = [
    ("Nom", "subject, predicate noun"),
    ("Gen", "possession, separation, partitive; after ἀπό, ἐκ, περί, ἀντί"),
    ("Dat", "indirect object, means, time when; after ἐν, σύν"),
    ("Acc", "direct object, extent, motion to; after εἰς, ἀνά"),
    ("Voc", "direct address (ὦ ἄνθρωπε)"),
]

# ----------------------------------------------------------------------
# Reference-guide printing
# ----------------------------------------------------------------------
def print_row(label, forms, w=16):
    col = CASE_COLOR.get(label, C.END)
    lab = f"{label + ':':<7}"
    print(f"    {cz(lab, col)}" + "  ".join(f"{f:<{w}}" for f in forms))

def show_alphabet():
    title("Alphabet & Pronunciation")
    for i in range(0, len(ALPHABET), 3):
        row = ALPHABET[i:i + 3]
        print("   " + "    ".join(f"{cz(g,C.NOM):<7}{n:<10}{cz(r,C.DIM)}" for g, n, r in row))
    print()
    print("  Breathings: smooth ἀ (no h) vs rough ἁ (adds h) on every initial vowel/ρ.")
    print("  Accents: acute ά · grave ὰ · circumflex ᾶ (long syllables only).")
    pause()

def show_noun_table(name, gloss, sg, pl):
    print(f"\n  {cz(name, C.HEAD)}  {cz('— ' + gloss, C.DIM)}")
    print(f"    {'':7}{'Singular':<16}{'Plural'}")
    for i, c in enumerate(CASES):
        print_row(c, [sg[i], pl[i]])

def show_article():
    title("Definite Article — ὁ ἡ τό")
    _, _, ms, mp, fs, fp, ns, np_ = ARTICLE
    print(f"    {'':7}{'M sg':<9}{'M pl':<9}{'F sg':<9}{'F pl':<9}{'N sg':<9}{'N pl'}")
    for i, c in enumerate(CASES):
        col = CASE_COLOR[c]
        print(f"    {cz(c+':',col):<16}" +
              "".join(f"{f:<9}" for f in [ms[i], mp[i], fs[i], fp[i], ns[i], np_[i]]))
    pause()

def show_nouns():
    title("Noun Declensions")
    for name, gloss, sg, pl in NOUNS:
        show_noun_table(name, gloss, sg, pl)
    print()
    print("  " + cz("Tip:", C.TEN) + " find the 3rd-decl. stem by dropping -ος from the genitive")
    print("  singular: φύλακος → φύλακ-, σώματος → σωματ-.")
    pause()

def show_adjectives():
    title("Adjectives & Pronouns")
    name, gloss, ms, mp, fs, fp, ns, np_ = ADJ_AGATHOS
    print(f"  {cz(name, C.HEAD)}  {cz('— ' + gloss, C.DIM)}")
    print(f"    {'':7}{'M sg':<9}{'M pl':<9}{'F sg':<9}{'F pl':<9}{'N sg':<9}{'N pl'}")
    for i, c in enumerate(CASES):
        col = CASE_COLOR[c]
        print(f"    {cz(c+':',col):<16}" +
              "".join(f"{f:<9}" for f in [ms[i], mp[i], fs[i], fp[i], ns[i], np_[i]]))
    print(f"\n  {cz('Personal pronouns', C.HEAD)} (I / we, then you-sg / you-pl):")
    labels = ["Nom", "Gen", "Dat", "Acc"]
    for i, lab in enumerate(labels):
        col = CASE_COLOR[lab]
        print(f"    {cz(lab+':',col):<16}{PRONOUN_I_WE[i]:<28}{PRONOUN_I_WE[i+4]}")
    print("\n  Comparison: -τερος / -τατος (σοφός → σοφώτερος → σοφώτατος).")
    print("  αὐτός/-ή/-ό: predicate position = 'self'; attributive = 'same'.")
    pause()

def show_verbs():
    title("Verbs — λύω  (principal parts: " + LUO_PARTS + ")")
    for name, forms in LUO.items():
        print(f"\n  {cz(name, C.HEAD)}")
        for i, p in enumerate(PERSONS):
            print(f"    {cz(p+':',C.END):<12}{forms[i]}")
    pause()

    title("Subjunctive, Optative & Imperative (present)")
    print(f"  {cz('Subjunctive active', C.HEAD)}")
    for i, p in enumerate(PERSONS):
        print(f"    {cz(p+':',C.END):<12}{LUO_SUBJ[i]}")
    print(f"\n  {cz('Optative active', C.HEAD)}")
    for i, p in enumerate(PERSONS):
        print(f"    {cz(p+':',C.END):<12}{LUO_OPT[i]}")
    print(f"\n  {cz('Imperative', C.HEAD)}   (active / mid-pass)")
    for p in ["2 sg", "3 sg", "2 pl", "3 pl"]:
        print(f"    {cz(p+':',C.END):<12}{LUO_IMPV_ACT[p]:<14}{LUO_IMPV_MP[p]}")
    print(f"\n  {cz('Infinitives', C.HEAD)}")
    for k, v in LUO_INF.items():
        print(f"    {cz(k+':',C.END):<16}{v}")
    print("\n  Negatives: οὐ with the indicative, μή with everything else.")
    pause()

    title("Contract Verbs & Irregular Verbs (present)")
    print(f"  {cz('Contract verbs', C.HEAD)}")
    for i, p in enumerate(PERSONS):
        row = "  ".join(f"{name.split()[0]}: {forms[i]:<12}" for name, forms in CONTRACT.items())
        print(f"    {cz(p+':',C.END):<8}{row}")
    print(f"\n  {cz('εἰμί (to be)', C.HEAD)}")
    for name, forms in EIMI.items():
        print(f"    {cz(name+':',C.END):<12}" + "  ".join(forms))
    print(f"\n  {cz('δίδωμι (pres):', C.END)} " + "  ".join(DIDOMI_PRES))
    print(f"  {cz('οἶδα (perf, = know):', C.END)} " + "  ".join(OIDA_PERF))
    pause()

def show_endings_legend():
    title("Endings & Markers — Colour Key")
    print(f"  {cz('Case endings:', C.HEAD)}")
    for group, d in NOUN_ENDINGS.items():
        print(f"\n    {cz(group, C.DIM)}")
        print("      " + "   ".join(f"{cz(c,CASE_COLOR[c])}={cz(e,C.END)}" for c, e in d.items()))
    print(f"\n  {cz('Verb personal endings:', C.HEAD)}")
    for group, d in VERB_ENDINGS.items():
        print(f"\n    {cz(group, C.DIM)}")
        print("      " + "   ".join(f"{p}={cz(e,C.END)}" for p, e in d.items()))
    print(f"\n  {cz('Augment / tense markers:', C.HEAD)}")
    for name, sign, note in MARKERS:
        print(f"    {cz(name+':',C.AUG):<32}{cz(sign,C.TEN):<10}{cz(note,C.DIM)}")
    pause()

def show_syntax():
    title("Quick Syntax Notes")
    for c, note in SYNTAX_NOTES:
        print(f"    {cz(c+':',CASE_COLOR[c]):<8}{note}")
    print()
    print("  Word order is free — case shows function.")
    print("  A neuter plural subject takes a SINGULAR verb.")
    print("  μέν … δέ (on the one hand … on the other) · γάρ (for) · ἀλλά (but) · οὖν (so)")
    print("  Article + participle = 'the one who…' (ὁ λέγων).")
    pause()

def reference_menu():
    items = [
        ("1", "Alphabet & pronunciation", show_alphabet),
        ("2", "Article", show_article),
        ("3", "Noun declensions", show_nouns),
        ("4", "Adjectives & pronouns", show_adjectives),
        ("5", "Verbs (λύω + irregulars)", show_verbs),
        ("6", "Endings & markers — colour key", show_endings_legend),
        ("7", "Syntax notes", show_syntax),
        ("0", "Back to main menu", None),
    ]
    while True:
        title("Reference Guide")
        for k, label, _ in items:
            print(f"    {cz(k, C.END)}) {label}")
        choice = input(cz("\n  Choose: ", C.DIM)).strip()
        match = next((it for it in items if it[0] == choice), None)
        if not match:
            continue
        if match[2] is None:
            return
        match[2]()

# ----------------------------------------------------------------------
# Answer normalisation
# ----------------------------------------------------------------------
def normalize(s, strip_accents):
    s = unicodedata.normalize("NFD", s)
    if strip_accents:
        s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = unicodedata.normalize("NFC", s).lower().replace("ς", "σ")
    return " ".join(s.split())

def answer_variants(ans):
    """Expand '/' alternatives and optional (ν)."""
    out = []
    for part in ans.split("/"):
        part = part.strip()
        if "(ν)" in part:
            out.append(part.replace("(ν)", ""))
            out.append(part.replace("(ν)", "ν"))
        else:
            out.append(part)
    return out

def check(user_input, answer, strip_accents):
    u = normalize(user_input, strip_accents)
    return any(normalize(v, strip_accents) == u for v in answer_variants(answer))

def ask_strip_accents():
    r = input(cz("  Ignore accents/breathings while checking? [Y/n]: ", C.DIM)).strip().lower()
    return r != "n"

# ----------------------------------------------------------------------
# Worksheet
# ----------------------------------------------------------------------
def build_worksheet():
    return [
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
            ("1 sg aorist middle", "ἐλυσάμην"),
            ("3 sg aorist passive", "ἐλύθη"),
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

def run_worksheet():
    title("Worksheet")
    strip_accents = ask_strip_accents()
    sections = build_worksheet()
    total = sum(len(qs) for _, qs in sections)
    score = 0
    n = 0
    missed = []
    for sect_name, qs in sections:
        print(f"\n{cz(sect_name, C.HEAD)}")
        rule("·", 40)
        for q, a in qs:
            n += 1
            resp = input(f"  {n}/{total}. {q}\n    > ").strip()
            if resp == "":
                print(cz("    (skipped)", C.DIM))
                missed.append((q, a))
                continue
            if check(resp, a, strip_accents):
                print(cz(f"    ✓ correct", C.OK))
                score += 1
            else:
                print(cz(f"    ✗ answer: {a.split('/')[0]}", C.NO))
                missed.append((q, a))
    print()
    rule()
    print(cz(f"  Score: {score} / {total}", C.HEAD))
    if missed:
        print(cz("\n  Review these:", C.DIM))
        for q, a in missed:
            print(f"    - {q}  →  {cz(a.split('/')[0], C.END)}")
    pause()

# ----------------------------------------------------------------------
# Ending memorization drill
# ----------------------------------------------------------------------
def flatten_endings():
    """Return list of (deck, prompt, answer) for every ending in NOUN_ENDINGS
    and VERB_ENDINGS, skipping placeholders like '(varies)'."""
    cards = []
    for group, d in NOUN_ENDINGS.items():
        for case, ending in d.items():
            if "varies" in ending:
                continue
            cards.append(("Noun endings", f"{group} — {case}", ending))
    for group, d in VERB_ENDINGS.items():
        for person, ending in d.items():
            cards.append(("Verb endings", f"{group} — {person}", ending))
    for name, sign, note in MARKERS:
        cards.append(("Markers", f"{name} ({note})", sign))
    return cards

def choose_deck():
    decks = ["Noun endings", "Verb endings", "Markers", "All"]
    title("Ending Drill — choose a deck")
    for i, d in enumerate(decks, 1):
        print(f"    {i}) {d}")
    c = input(cz("\n  Choose [4]: ", C.DIM)).strip()
    idx = {"1": 0, "2": 1, "3": 2}.get(c, 3)
    return decks[idx]

def run_drill():
    deck_name = choose_deck()
    cards = flatten_endings()
    if deck_name != "All":
        cards = [c for c in cards if c[0] == deck_name]
    random.shuffle(cards)
    strip_accents = ask_strip_accents()

    title(f"Ending Drill — {deck_name}")
    print("  Type the ending (e.g. -ου, -εις). Wrong or skipped cards come back")
    print("  around again until you get each one right. Type 'q' to stop.\n")

    queue = list(cards)
    seen_once = {id(c): 0 for c in cards}   # wrong-count per card, for a light weighting
    correct_first_try = 0
    total_cards = len(cards)
    rounds = 0

    while queue:
        rounds += 1
        next_queue = []
        random.shuffle(queue)
        for card in queue:
            deck, prompt, answer = card
            resp = input(f"  [{cz(deck, C.DIM)}] {prompt}\n    ending? > ").strip()
            if resp.lower() in ("q", "quit", "exit"):
                print(cz("\n  Stopped early.", C.DIM))
                queue = []
                next_queue = []
                break
            ok = check(resp, answer, strip_accents) or check(resp.lstrip("-"), answer.lstrip("-"), strip_accents)
            if ok:
                print(cz(f"    ✓ {answer}", C.OK))
                if seen_once[id(card)] == 0:
                    correct_first_try += 1
            else:
                print(cz(f"    ✗ correct: {answer}", C.NO))
                seen_once[id(card)] += 1
                next_queue.append(card)
        queue = next_queue
        if queue:
            print(cz(f"\n  Round {rounds} done — {len(queue)} to review again.\n", C.TEN))
            rule("·", 40)

    print()
    rule()
    if total_cards:
        pct = round(100 * correct_first_try / total_cards)
        print(cz(f"  First-try accuracy: {correct_first_try}/{total_cards} ({pct}%)", C.HEAD))
        print(cz(f"  Rounds to full mastery: {rounds}", C.DIM))
    pause()

# ----------------------------------------------------------------------
# Main menu
# ----------------------------------------------------------------------
def main():
    while True:
        title("Ἑλληνικὴ Γραμματική — Ancient Greek Grammar Trainer")
        print(f"    {cz('1', C.END)}) Reference guide  (alphabet · declensions · conjugations · syntax)")
        print(f"    {cz('2', C.END)}) Worksheet  (type the requested form, get checked)")
        print(f"    {cz('3', C.END)}) Ending memorization drill  (flashcards, wrong ones repeat)")
        print(f"    {cz('0', C.END)}) Quit")
        choice = input(cz("\n  Choose: ", C.DIM)).strip()
        if choice == "1":
            reference_menu()
        elif choice == "2":
            run_worksheet()
        elif choice == "3":
            run_drill()
        elif choice == "0":
            clear()
            print(cz("  χαῖρε — farewell!\n", C.TITLE))
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(cz("\n\n  χαῖρε — farewell!\n", C.TITLE))
