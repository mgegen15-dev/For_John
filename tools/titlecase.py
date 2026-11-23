"""Title-case a heading without damaging gene names, acronyms or code.

Words that already contain a capital letter or a digit (IL-6, VEGFR2, ctDNA,
microRNA, NIH) and anything that looks like code or a path are left alone.
Short joining words stay lower-case unless they start or end the heading or
follow a colon, question mark or full stop.
"""
import re

SMALL = {"a", "an", "the", "and", "or", "nor", "but", "of", "in", "on", "to", "for",
         "by", "at", "from", "with", "as", "vs", "via", "per"}


def _cap_part(part):
    if not part or re.search(r"[A-Z0-9]", part):
        return part
    m = re.search(r"[a-z]", part)
    if not m:
        return part
    i = m.start()
    return part[:i] + part[i].upper() + part[i + 1:]


def _cap_word(word):
    if re.search(r"[`/\\_@]|\.\w", word):          # code, paths, file names, URLs
        return word
    return "-".join(_cap_part(p) for p in word.split("-"))


def titlecase(text):
    words = text.split(" ")
    out, force = [], True
    last = max((i for i, w in enumerate(words) if re.search(r"[A-Za-z]", w)), default=-1)
    in_code = False
    for i, w in enumerate(words):
        ticks = w.count("`")
        if in_code or ticks:
            out.append(w)
            if ticks % 2:
                in_code = not in_code
            continue
        core = re.sub(r"[^A-Za-z'’-]", "", w).lower()
        if core in SMALL and not force and i != last:
            out.append(w)
        else:
            out.append(_cap_word(w))
        if re.search(r"[A-Za-z0-9]", w):
            # the next word starts a new clause after a colon, question or exclamation mark
            force = bool(re.search(r"[:?!]$", w))
    return " ".join(out)
