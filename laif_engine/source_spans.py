"""LAIF engine: source spans. Moved without changing assessment rules."""

import re


_OUTLINE_PATTERNS = [
    re.compile(r"^#{1,6}\s+(.{3,80})$", re.MULTILINE),                       # markdown headings
    re.compile(r"^((?:Article|Section|SECTION|Part|PART|Chapter)\s+[\dIVXA-Z]+[^\n]{0,90})$", re.MULTILINE),
    re.compile(r"^((?:GOVERN|MAP|MEASURE|MANAGE)\s+\d+(?:\.\d+)?:?[^\n]{0,60})", re.MULTILINE),
    re.compile(r"^(\d+\.\d*\.?\s+[A-Z][^\n]{3,60})$", re.MULTILINE),       # 2.1 Numbered heads
    re.compile(r"^([A-Z][A-Za-z ]{3,50})\n(?=\n)", re.MULTILINE),             # bare titles (blank line follows)
]


def _document_outline(text):
    """Return a deduplicated, offset-ordered [(offset, label)] outline of the
    document's own structure, detected from common heading conventions."""
    seen_labels = set()
    entries = []
    for pat in _OUTLINE_PATTERNS:
        for m in pat.finditer(text):
            label = " ".join(m.group(1).split())[:70].rstrip(" |#-")
            if len(label) < 4 or label.lower() in seen_labels:
                continue
            seen_labels.add(label.lower())
            entries.append((m.start(), label))
    entries.sort(key=lambda x: x[0])
    return entries


def _locate_offset(pos, outline):
    """Nearest document-structure label at or before pos."""
    best = "start of document"
    for off, label in outline:
        if off <= pos:
            best = label
        else:
            break
    return best


# Orphaned openers left behind when a window starts mid-structure: a clause
# letter "(b)", a split list number "3" from "3.3", a stray bullet or dash.
_ORPHAN_OPENER = re.compile(
    r"^(?:[)\]\}»”\'\"]+|[-–—•|]+|\(?[a-z0-9]{1,3}[).:]|\d{1,3}(?=\s))\s*",
    re.IGNORECASE,
)


def _quote_at(text, start, end, max_len=140):
    """A readable, verbatim window around a match.

    Quotes are the evidentiary backbone of the report, so they must be
    quotable: no partial leading word, no orphaned list numbering, and an
    ending at a clause boundary wherever one is available rather than a hard
    character cut. Keep the actual trigger in view, even when that requires
    exceeding the preferred length. Collapse display whitespace only.
    """
    # Prefer the start of the sentence containing the match, so a quote reads
    # as a statement rather than a fragment missing its subject.
    back = text.rfind(". ", max(0, start - 220), start)
    nl = text.rfind("\n", max(0, start - 220), start)
    lo = max(back + 2 if back != -1 else 0, nl + 1 if nl != -1 else 0)
    if start - lo > 220 or lo > start:
        lo = max(0, start - 15)

    # Never run a quote across a section heading or list break.
    hi_limit = min(len(text), end + 140)
    for marker in ("\n#", "\n\n", "\n- ", "\n| "):
        cut = text.find(marker, end, hi_limit)
        if cut != -1:
            hi_limit = cut
    hi = max(end, hi_limit)
    original_window = " ".join(text[lo:hi].split())
    window = original_window

    # Drop a leading partial word when the window still began mid-token.
    if lo > 0 and window:
        first_char = text[lo - 1] if lo - 1 < len(text) else " "
        if not first_char.isspace():
            window = window.partition(" ")[2] or window

    # Drop orphaned openers repeatedly ("3 (b) ..." -> "...").
    for _ in range(3):
        stripped = _ORPHAN_OPENER.sub("", window, count=1)
        if stripped == window:
            break
        window = stripped

    if len(window) <= max_len:
        excerpt = window.strip()
    else:
        # Prefer a clause boundary inside the last third of the allowance.
        head = window[:max_len]
        boundary = max(head.rfind("; "), head.rfind(", "), head.rfind(". "))
        excerpt = (head[:boundary + 1].strip() if boundary >= int(max_len * 0.55)
                   else head.rsplit(" ", 1)[0].strip() + "…")

    raw_match = text[start:end]
    matched = " ".join(raw_match.split())
    if not matched:
        return excerpt
    # Locate this occurrence in the normalized window. Finding the same
    # words elsewhere in the preview is not enough.
    first_word = start + len(raw_match) - len(raw_match.lstrip())
    prefix = text[lo:first_word]
    normalized_prefix = " ".join(prefix.split())
    separator = bool(normalized_prefix) and prefix[-1:].isspace()
    removed = len(original_window) - len(window)
    match_offset = len(normalized_prefix) + separator - removed
    if match_offset >= 0 and excerpt[match_offset:match_offset + len(matched)] == matched:
        return excerpt

    return _match_centered_quote(text, lo, hi, first_word, end, max_len)


def _match_centered_quote(text, lo, hi, start, end, max_len):
    """Keep a complete matched span and fit adjacent whole tokens when there is room."""
    # Prefix matches such as 'beneficiar' may end inside an actual source word.
    while start > lo and not text[start - 1].isspace():
        start -= 1
    while end < hi and end > start and not text[end - 1].isspace() and not text[end].isspace():
        end += 1
    matched = " ".join(text[start:end].split())
    available = max_len - len(matched)
    if available <= 0:
        return matched

    before, after = [], []
    remaining_before = available // 2
    for word in reversed(text[lo:start].split()):
        size = len(word) + 1
        if size > remaining_before:
            break
        before.append(word)
        remaining_before -= size
        available -= size
    for word in text[end:hi].split():
        size = len(word) + 1
        if size > available:
            break
        after.append(word)
        available -= size
    return " ".join([*reversed(before), matched, *after])
