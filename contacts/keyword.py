"""Keyword operations."""


from itertools import chain, combinations

LETTER_TRANS = {
    "c": ("ç",),
    "C": ("Ç",),
    "g": ("ğ",),
    "G": ("Ğ",),
    "i": ("ı",),
    "I": ("İ",),
    "o": ("ö",),
    "O": ("Ö",),
    "s": ("ş",),
    "S": ("Ş",),
    "u": ("ü",),
    "U": ("Ü",),
}


def prepare(keywords: list[str], *, extend: bool = False) -> list[str]:
    """Capitalize keywords to match contacts.

    :param extend: extend the search space to find near matches
    """
    result = {" ".join(x.capitalize() for x in k.split()) for k in keywords}

    if extend:
        for keyword in list(result):
            trans_pairs = list(
                chain(
                    *(
                        [(i, y) for y in LETTER_TRANS.get(c, ())]
                        for (i, c) in enumerate(keyword)
                    )
                )
            )
            for trans_count in range(1, len(trans_pairs) + 1):
                for trans_combination in combinations(trans_pairs, trans_count):
                    translated = list(keyword)
                    for trans in trans_combination:
                        translated[trans[0]] = trans[1]
                        result.add("".join(translated))

    return sorted(result)
