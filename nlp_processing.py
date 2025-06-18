import json
import re
from pathlib import Path

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from fuzzywuzzy import process     # switch to rapidfuzz for speed if you like

# ── One‑time NLTK downloads ──────────────────────────────────────────────
# Run these **once** at install/setup time, not every import.  Otherwise your
# server pings the NLTK mirror on every cold start.
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

# ── Load and index the knowledge base ────────────────────────────────────
with Path("data.json").open(encoding="utf‑8") as f:
    chatbot_data = json.load(f)

# Build an index: question (lower‑cased) → full QA dict
question_index = {
    qa["question"].lower(): qa
    for qa_list in chatbot_data.values()
    for qa in qa_list
}
possible_questions = list(question_index.keys())

# Cache stopwords so we don’t hit the NLTK corpus every call
STOP_WORDS = set(stopwords.words("english"))

# ── Helpers ──────────────────────────────────────────────────────────────
def preprocess_text(text: str) -> str:
    """Lower‑case, strip specials, drop stopwords."""
    text = re.sub(r"[^a-zA-Z\s]", "", text.lower().strip())
    tokens = [w for w in word_tokenize(text) if w not in STOP_WORDS]
    return " ".join(tokens)        # e.g. "install flask"

def find_best_match(user_input: str) -> str:
    """Return the chatbot’s answer or a fallback message."""
    cleaned_input = preprocess_text(user_input)

    # fuzzywuzzy returns (match, score); handle the None case
    match = process.extractOne(cleaned_input, possible_questions)
    if match is None:
        return "Sorry, I didn't quite understand. Can you rephrase?"

    best_match, score = match
    if score < 60:                 # tweak threshold to taste
        return "Sorry, I didn't quite understand. Can you rephrase?"

    qa = question_index[best_match]                # guaranteed present
    return qa.get("answer") or qa.get(
        "response",
        "Sorry, I don't have an answer for that.",
    )
