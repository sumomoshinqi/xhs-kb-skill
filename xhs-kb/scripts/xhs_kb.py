#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_KB_ROOT = Path.home() / "Documents/Codex/2026-06-18/sous/outputs/xhs_codex_kb"


def tokenize(text):
    text = (text or "").lower()
    zh = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    alnum = re.findall(r"[a-z0-9_\-]{2,}", text)
    grams = []
    for seq in zh:
        grams.extend(seq[i : i + 2] for i in range(max(1, len(seq) - 1)))
    return set(zh + alnum + grams)


def resolve_kb_root(args):
    root = Path(args.kb or os.environ.get("XHS_KB_ROOT") or DEFAULT_KB_ROOT).expanduser().resolve()
    required = [root / "index" / "catalog.json", root / "index" / "chunks.jsonl"]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit("Missing XHS KB files:\n" + "\n".join(missing))
    return root


def load_catalog(root):
    with (root / "index" / "catalog.json").open(encoding="utf-8") as f:
        return json.load(f)


def iter_chunks(root):
    with (root / "index" / "chunks.jsonl").open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def normalize(text):
    return re.sub(r"\s+", " ", text or "").strip()


def rank_chunks(root, query, limit, category=None):
    q_tokens = tokenize(query)
    results = []
    for item in iter_chunks(root):
        if category and category not in item.get("category", "") and category not in item.get("path", ""):
            continue
        haystack = f"{item.get('title', '')} {item.get('path', '')} {item.get('text', '')}"
        tokens = tokenize(haystack)
        score = len(q_tokens & tokens)
        if query and query in haystack:
            score += 10
        if score:
            results.append((score, item))
    results.sort(key=lambda pair: (-pair[0], pair[1].get("path", ""), pair[1].get("chunk_index", 0)))
    return results[:limit]


def cmd_stats(args):
    root = resolve_kb_root(args)
    catalog = load_catalog(root)
    payload = {"kb_root": str(root), **catalog.get("stats", {})}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(f"KB root: {payload['kb_root']}")
    print(f"Sources: {payload.get('total_sources')}")
    print(f"Searchable text sources: {payload.get('text_sources')}")
    print(f"Chunks: {payload.get('chunk_count')}")
    print("Categories:")
    for name, count in sorted(payload.get("category_counts", {}).items()):
        print(f"- {name}: {count}")
    return 0


def format_search_result(score, item, chars):
    snippet = normalize(item.get("text", ""))[:chars]
    source = item.get("source_url") or ""
    header = f"[score={score}] {item.get('path')} :: {item.get('kb_path')}#chunk-{item.get('chunk_index')}"
    if source:
        header += f" :: {source}"
    return f"{header}\n{snippet}\n"


def cmd_search(args):
    root = resolve_kb_root(args)
    results = rank_chunks(root, args.query, args.limit, args.category)
    if args.json:
        payload = [
            {
                "score": score,
                "chunk_id": item.get("chunk_id"),
                "source_id": item.get("source_id"),
                "title": item.get("title"),
                "path": item.get("path"),
                "category": item.get("category"),
                "kb_path": item.get("kb_path"),
                "source_url": item.get("source_url"),
                "chunk_index": item.get("chunk_index"),
                "snippet": normalize(item.get("text", ""))[: args.chars],
            }
            for score, item in results
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    for score, item in results:
        print(format_search_result(score, item, args.chars))
    return 0


def cmd_context(args):
    root = resolve_kb_root(args)
    results = rank_chunks(root, args.query, args.limit, args.category)
    print(f"# XHS KB Evidence Pack\n\nQuery: {args.query}\n")
    for idx, (score, item) in enumerate(results, 1):
        snippet = normalize(item.get("text", ""))[: args.chars]
        print(f"## {idx}. {item.get('title')}")
        print(f"- score: {score}")
        print(f"- path: {item.get('path')}")
        print(f"- kb_path: {item.get('kb_path')}#chunk-{item.get('chunk_index')}")
        if item.get("source_url"):
            print(f"- source_url: {item.get('source_url')}")
        print(f"\n{snippet}\n")
    return 0


def find_source(catalog, selector):
    sources = catalog.get("sources", [])
    exact = [
        item
        for item in sources
        if selector in {item.get("id"), item.get("kb_path"), item.get("path"), item.get("title")}
    ]
    if exact:
        return exact[0]
    lowered = selector.lower()
    fuzzy = [
        item
        for item in sources
        if lowered in (item.get("kb_path") or "").lower()
        or lowered in (item.get("path") or "").lower()
        or lowered in (item.get("title") or "").lower()
    ]
    if not fuzzy:
        return None
    fuzzy.sort(key=lambda item: (not item.get("extracted_text"), len(item.get("kb_path") or "")))
    return fuzzy[0]


def cmd_source(args):
    root = resolve_kb_root(args)
    catalog = load_catalog(root)
    source = find_source(catalog, args.selector)
    if not source:
        raise SystemExit(f"No source matched: {args.selector}")
    rel = source.get("kb_path")
    path = root / rel
    if not path.exists():
        raise SystemExit(f"Source file does not exist: {path}")
    text = path.read_text(encoding="utf-8", errors="replace")
    if args.json:
        print(
            json.dumps(
                {
                    "source": source,
                    "absolute_path": str(path),
                    "text": text[: args.head] if args.head else text,
                    "truncated": bool(args.head and len(text) > args.head),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    print(f"# {source.get('title')}")
    print(f"kb_path: {rel}")
    print(f"path: {source.get('path')}")
    if source.get("source_url"):
        print(f"source_url: {source.get('source_url')}")
    print()
    print(text[: args.head] if args.head else text)
    if args.head and len(text) > args.head:
        print(f"\n[truncated at {args.head} chars; full file: {path}]")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Search and inspect the local Xiaohongshu knowledge base.")
    parser.add_argument("--kb", help="Path to xhs_codex_kb root. Defaults to XHS_KB_ROOT or this machine's local bundle.")
    sub = parser.add_subparsers(dest="command", required=True)

    stats = sub.add_parser("stats", help="Show KB coverage statistics.")
    stats.add_argument("--json", action="store_true")
    stats.set_defaults(func=cmd_stats)

    search = sub.add_parser("search", help="Search ranked KB chunks.")
    search.add_argument("query")
    search.add_argument("-n", "--limit", type=int, default=10)
    search.add_argument("--category")
    search.add_argument("--chars", type=int, default=260)
    search.add_argument("--json", action="store_true")
    search.set_defaults(func=cmd_search)

    context = sub.add_parser("context", help="Print a markdown evidence pack for a query.")
    context.add_argument("query")
    context.add_argument("-n", "--limit", type=int, default=6)
    context.add_argument("--category")
    context.add_argument("--chars", type=int, default=420)
    context.set_defaults(func=cmd_context)

    source = sub.add_parser("source", help="Read a source by kb_path, source id, title, or fuzzy path.")
    source.add_argument("selector")
    source.add_argument("--head", type=int, default=4000)
    source.add_argument("--json", action="store_true")
    source.set_defaults(func=cmd_source)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
