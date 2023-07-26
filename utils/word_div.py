import jieba
from typing import Set, List
import re
import functools


def get_tokens(code: str) -> Set[str]:
    """Tokenize a code snippet."""
    return {t for t in jieba.cut(code) if len(t.strip()) > 0}


def jaccard_similar(code1: str, code2: str) -> float:
    """Compute the Jaccard similarity of two code snippets."""
    if len(code1) == 0 or len(code2) == 0:
        return 0
    tokens1 = get_tokens(code1)
    tokens2 = get_tokens(code2)
    return len(tokens1 & tokens2) / len(tokens1 | tokens2)


@functools.singledispatch
def hard_similar(flags, code: str) -> bool:
    raise TypeError(f"Not a supported type for {type(flags)}")


@hard_similar.register(list)
def _(flags: List[str], code: str) -> bool:
    """check whether the flags words exists in code"""

    re_flag = "|".join(
        map(lambda x: f"({x})" if not re.match("\(.+\)", x) else x, flags)
    )
    return re.compile(re_flag).match(code) != None


@hard_similar.register(str)
def _(flags: str, code: str) -> bool:
    """check whether the flags words exists in code"""
    return re.match(flags, code) != None
