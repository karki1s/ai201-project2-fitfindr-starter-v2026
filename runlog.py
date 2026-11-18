"""
Structured run log — capstone instrumentation.

Every agent run appends ONE JSON object (one line) to logs/runs.jsonl, whether
it completed, stopped early, or blew up. Rejected HTTP requests get a line too.
A failure that only shows up as a missing line is one you'll never find.

    python runlog.py              summary of everything in the log
    python runlog.py --last 10    print the last 10 records

Fields (missing ones are null):
    ts              UTC time the run started, ISO 8601
    run_id          short random id
    source          cli | http | eval
    query           what the user typed
    ranker          weighted | keyword
    parsed          {description, size, max_price}
    outcome         completed | no_results | model_unavailable | rejected | exception
    n_results       how many listings search_listings returned
    top_item_id     the selected listing's id (search result #1)
    top_item_title
    top_item_price
    outfit_chars    length of the outfit suggestion
    fit_card        the fit card text (the run's final output)
    error           session["error"] or the exception text
    duration_ms     wall-clock time for the whole run
    model_calls     model calls made during this run (cache hits excluded)
    cache_hits      answers served from the local cache during this run
    prompt_tokens   tokens sent, as reported by the API, this run only
    output_tokens   tokens received, this run only
    cache_enabled   whether the response cache was on
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import config

LOG_DIR = Path(os.getenv("AI201_LOG_DIR", config.ROOT / "logs"))
LOG_PATH = LOG_DIR / "runs.jsonl"


def new_run_id() -> str:
    return uuid.uuid4().hex[:8]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def write(record: dict) -> None:
    """Append one record. Never raises — logging must not take down a run."""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    except OSError as exc:
        print(f"  [runlog] couldn't write {LOG_PATH}: {exc}", file=sys.stderr)


def outcome_of(session: dict | None, exc_text: str | None) -> str:
    if exc_text is not None or session is None:
        return "exception"
    if not session.get("error"):
        return "completed"
    if session.get("selected_item") is None:
        return "no_results"
    return "model_unavailable"


def read_all(path: Path = LOG_PATH) -> list[dict]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return records


def _summary(records: list[dict]) -> None:
    from collections import Counter

    print(f"{len(records)} records in {LOG_PATH}")
    print("outcomes:", dict(Counter(r.get("outcome") for r in records)))
    done = [r for r in records if r.get("outcome") == "completed" and r.get("model_calls")]
    if not done:
        print("no completed runs with real (uncached) model calls yet")
        return
    n = len(done)
    avg = lambda key: sum(r.get(key) or 0 for r in done) / n  # noqa: E731
    print(f"completed, uncached runs: {n}")
    print(f"  avg duration     {avg('duration_ms') / 1000:.2f} s")
    print(f"  avg model calls  {avg('model_calls'):.2f}")
    print(f"  avg tokens       {avg('prompt_tokens'):.0f} prompt + "
          f"{avg('output_tokens'):.0f} output = "
          f"{avg('prompt_tokens') + avg('output_tokens'):.0f} total")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="read the structured run log")
    parser.add_argument("--last", type=int, help="print the last N records")
    args = parser.parse_args()
    records = read_all()
    if args.last:
        for r in records[-args.last:]:
            print(json.dumps(r, ensure_ascii=False))
    else:
        _summary(records)
