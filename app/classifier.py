import re
from collections import Counter

# Transparent baseline classifier; swap for a persisted sklearn pipeline when trained data is available.
KEYWORDS = {
    "sales": {"price", "pricing", "buy", "purchase", "quote", "demo", "plan"},
    "support": {"broken", "error", "help", "issue", "problem", "not working", "bug"},
    "partnership": {"partner", "partnership", "integrate", "integration", "affiliate"},
}

def classify_lead(message: str) -> tuple[str, float]:
    tokens = set(re.findall(r"[a-z]+", message.lower()))
    scores = {label: sum(1 for word in words if word in message.lower() or word in tokens)
              for label, words in KEYWORDS.items()}
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    if ranked[0][1] == 0:
        return "general", 0.45
    total = sum(scores.values())
    return ranked[0][0], round(ranked[0][1] / max(total, 1), 2)

# Keep baseline triage deterministic and easy to audit.
