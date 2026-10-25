"""Command-line interface for SlowCommit."""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from slowcommit.core import build_prompt, clean_message, MAX_DIFF_CHARS

DEFAULT_MODEL = "llama3.2:1b"
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"

class SlowCommitError(RuntimeError):
    """An actionable error for the CLI user."""

def get_staged_diff() -> str:
    """Return only staged changes; do not inspect unstaged or untracked files."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--no-ext-diff", "--unified=2"],
            check=False, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=15,
        )
    except FileNotFoundError as exc:
        raise SlowCommitError("Git was not found. Install Git and reopen PowerShell.") from exc
    except subprocess.TimeoutExpired as exc:
        raise SlowCommitError("Git took too long to read the staged diff.") from exc
    if result.returncode != 0:
        raise SlowCommitError(f"Could not read staged changes: {result.stderr.strip() or 'unknown Git error'}")
    diff = result.stdout.strip()
    if not diff:
        raise SlowCommitError("No staged changes found. Stage files first with `git add <file>`. ")
    return diff

def generate_message(diff: str, model: str, base_url: str, timeout: int = 180) -> str:
    """Call the local Ollama generate endpoint and return one suggestion."""
    url = base_url.rstrip("/") + "/api/generate"
    body = json.dumps({"model": model, "prompt": build_prompt(diff), "stream": False}).encode("utf-8")
    request = Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code == 404:
            raise SlowCommitError(f"Ollama could not find model '{model}'. Pull it with `ollama pull {model}`.") from exc
        raise SlowCommitError(f"Ollama returned HTTP {exc.code}.") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise SlowCommitError(f"Cannot reach Ollama at {base_url}. Start Ollama and check that it is listening locally.") from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise SlowCommitError("Ollama returned an invalid response.") from exc
    message = clean_message(str(payload.get("response", "")))
    if not message:
        raise SlowCommitError("The model returned an empty suggestion. Try again.")
    return message

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="slowcommit", description="Suggest a Git commit message using local Ollama AI.")
    parser.add_argument("--model", default=os.getenv("SLOWCOMMIT_MODEL", DEFAULT_MODEL), help=f"Ollama model (default: {DEFAULT_MODEL})")
    parser.add_argument("--ollama-url", default=os.getenv("OLLAMA_HOST", DEFAULT_OLLAMA_URL), help=f"Ollama base URL (default: {DEFAULT_OLLAMA_URL})")
    parser.add_argument("--version", action="version", version="slowcommit 0.1.0")
    return parser

def main() -> int:
    args = build_parser().parse_args()
    try:
        diff = get_staged_diff()
        if len(diff) > MAX_DIFF_CHARS:
            print(f"Note: staged diff is {len(diff):,} characters; input will be limited to {MAX_DIFF_CHARS:,} characters.", file=sys.stderr)
        suggestion = generate_message(diff, args.model, args.ollama_url)
    except SlowCommitError as exc:
        print(f"slowcommit: {exc}", file=sys.stderr)
        return 1
    print("\nSuggested commit message:\n")
    print(f"  {suggestion}\n")
    print("Review it before using it. SlowCommit never creates a commit automatically.")
    print('Copy the message above, then run: git commit -m "your message"')
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
