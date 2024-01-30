"""Keyword operations."""

from functools import cache
from itertools import chain, combinations

from unidecode import unidecode

from contacts.config import get_config


@cache
def romanization() -> dict[str, list[str]]:
    """Generate romanizations from app config."""
    config = get_config()
    trans: dict[str, list[str]] = {}
    for c in config.romanize:
        trans.setdefault(unidecode(c.lower()), []).append(c.lower())
    return trans


def prepare_keywords(keywords: list[str]) -> list[str]:
    """Capitalize keywords to match contacts.

    :param extend: extend the search space to find near matches
    """
    result = {" ".join(x.capitalize() for x in k.split()) for k in keywords}

    for keyword in list(result):
        trans_pairs = list(
            chain(
                *(
                    [(i, y) for y in romanization().get(c.lower(), [])]
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
