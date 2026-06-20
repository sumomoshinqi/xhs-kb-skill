#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / "index" / "chunks.jsonl"

def tokenize(text):
    text = text.lower()
    zh = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    alnum = re.findall(r"[a-z0-9_\-]{2,}", text)
    grams = []
    for seq in zh:
        grams.extend(seq[i:i+2] for i in range(max(1, len(seq)-1)))
    return set(zh + alnum + grams)

def main():
    if len(sys.argv) < 2:
        print("usage: search_kb.py <query> [limit]", file=sys.stderr)
        return 2
    query = " ".join(sys.argv[1:-1]) if len(sys.argv) > 2 and sys.argv[-1].isdigit() else " ".join(sys.argv[1:])
    limit = int(sys.argv[-1]) if len(sys.argv) > 2 and sys.argv[-1].isdigit() else 10
    q_tokens = tokenize(query)
    results = []
    with CHUNKS.open(encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            haystack = f"{item['title']} {item['path']} {item['text']}"
            tokens = tokenize(haystack)
            score = len(q_tokens & tokens)
            if query in haystack:
                score += 10
            if score:
                results.append((score, item))
    results.sort(key=lambda x: (-x[0], x[1]["path"], x[1]["chunk_index"]))
    for score, item in results[:limit]:
        snippet = re.sub(r"\s+", " ", item["text"])[:260]
        print(f"[score={score}] {item['path']} :: {item['kb_path']}#chunk-{item['chunk_index']}")
        print(snippet)
        print()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
