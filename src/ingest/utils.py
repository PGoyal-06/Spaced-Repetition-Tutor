import re

def jaccard(a: str, b: str) -> float:
    """
    Compute Jaccard similarity between two strings on whitespace tokens.
    """
    # simple tokenizer: lowercase, split on non-word
    toks_a = set(re.findall(r"\w+", a.lower()))
    toks_b = set(re.findall(r"\w+", b.lower()))
    if not toks_a or not toks_b:
        return 0.0
    inter = toks_a & toks_b
    union = toks_a | toks_b
    return len(inter) / len(union)
