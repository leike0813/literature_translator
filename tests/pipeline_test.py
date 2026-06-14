#!/usr/bin/env python3
"""
pipeline_test.py — Structural pipeline test harness for literature-translator.

Runs blockify → sentencify → mock translations → concatenate on given inputs,
then verifies structural integrity at each stage. No actual translation involved.

Usage:
    python3 tests/pipeline_test.py <input.md>... [--keep]

Output: prints a per-file report; exit code 0 only if all pass.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "literature-translator" / "scripts"
BLOCKIFY = SCRIPTS_DIR / "blockify.py"
SENTENCIFY = SCRIPTS_DIR / "sentencify.py"
CONCATENATE = SCRIPTS_DIR / "concatenate.py"

# Block marker regex (must match what sentencify.py uses)
BLOCK_START_RE = re.compile(
    r'<!--\s*BLOCK:\s*(\S+)\s*\|\s*type:\s*(\S+)(?:\s*\|\s*heading:\s*(.*?))?\s*-->'
)
BLOCK_END_RE = re.compile(r'<!--\s*BLOCK_END:\s*(\S+)\s*-->')


def run_script(script: Path, args: list[str], label: str) -> dict:
    """Run a script, return {"ok": bool, "stdout": str, "stderr": str}."""
    cmd = [sys.executable, str(script)] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        ok = r.returncode == 0
        return {"ok": ok, "stdout": r.stdout.strip(), "stderr": r.stderr.strip()}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": f"TIMEOUT ({label})"}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e)}


def count_blocks(text: str) -> dict:
    """Count block markers in text, return summary."""
    starts = BLOCK_START_RE.findall(text)
    ends = BLOCK_END_RE.findall(text)
    ids_ = [s[0] for s in starts]
    return {
        "count": len(starts),
        "ends": len(ends),
        "balanced": len(starts) == len(ends),
        "unique_ids": len(set(ids_)),
        "id_count": len(ids_),
        "no_duplicate_ids": len(set(ids_)) == len(ids_),
    }


def create_mock_translations(batches_dir: Path, translations_dir: Path) -> list[str]:
    """Create mock translation JSON files from batch payloads."""
    manifest_path = batches_dir / "manifest.json"
    if not manifest_path.exists():
        return [f"manifest not found: {manifest_path}"]

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    output_dir = translations_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    errors = []

    for entry in manifest.get("batches", []):
        batch_id = entry["batch_id"]
        payload_path = Path(entry["payload_path"])
        if not payload_path.exists():
            errors.append(f"batch payload missing: {payload_path}")
            continue

        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        blocks = payload.get("blocks", {})

        trans_blocks = {}
        for block_id, block_data in blocks.items():
            sentences = block_data.get("sentences", [])
            trans_blocks[block_id] = {
                "type": block_data.get("type", "paragraph"),
                "sentences": list(sentences),
            }

        trans_result = {
            "batch_id": batch_id,
            "original_batch": batch_id,
            "blocks": trans_blocks,
        }

        out_path = output_dir / f"{batch_id}_translated.json"
        out_path.write_text(json.dumps(trans_result, ensure_ascii=False, indent=2), encoding="utf-8")

    return errors


def test_one_file(input_path: Path, keep: bool) -> dict:
    """Run full pipeline on one input file and return results."""
    name = input_path.name
    result = {"file": name, "passed": True, "stages": {}, "checks": {}}

    tmpdir = tempfile.mkdtemp(prefix=f"pipe_test_{name}_")
    ws = Path(tmpdir)

    try:
        # === Stage 1: blockify ===
        blocked = ws / "blocked.md"
        r = run_script(BLOCKIFY, ["--input", str(input_path), "--output", str(blocked)], "blockify")
        result["stages"]["blockify"] = {"ok": r["ok"], "stdout": r["stdout"], "stderr": r["stderr"]}
        if not r["ok"]:
            result["passed"] = False
            return result

        try:
            blockify_out = json.loads(r["stdout"])
            result["stages"]["blockify"]["blocks"] = blockify_out.get("blocks", 0)
            result["stages"]["blockify"]["strategy"] = blockify_out.get("heading_strategy", "")
        except (json.JSONDecodeError, KeyError):
            pass

        blocked_text = blocked.read_text(encoding="utf-8")
        blocked_info = count_blocks(blocked_text)
        result["checks"]["blocked_balanced"] = blocked_info["balanced"]
        result["checks"]["blocked_count"] = blocked_info["count"]
        result["checks"]["blocked_no_dup_ids"] = blocked_info["no_duplicate_ids"]
        if not blocked_info["balanced"] or not blocked_info["no_duplicate_ids"]:
            result["passed"] = False

        # === Stage 2: sentencify ===
        sentences = ws / "sentences.json"
        r = run_script(SENTENCIFY, ["--input", str(blocked), "--output", str(sentences)], "sentencify")
        result["stages"]["sentencify"] = {"ok": r["ok"], "stdout": r["stdout"], "stderr": r["stderr"]}
        if not r["ok"]:
            result["passed"] = False
            return result

        try:
            sent_data = json.loads(sentences.read_text(encoding="utf-8"))
            sent_blocks = sent_data.get("blocks", {})
            stats = sent_data.get("stats", {})
            result["checks"]["sentencify_blocks"] = len(sent_blocks)
            result["checks"]["sentencify_sentences"] = stats.get("total_sentences", 0)
            bf_ids = set(s[0] for s in BLOCK_START_RE.findall(blocked_text))
            sf_ids = set(sent_blocks.keys())
            missing_in_sent = bf_ids - sf_ids
            if missing_in_sent:
                result["checks"]["sentencify_missing_blocks"] = sorted(missing_in_sent)
                result["passed"] = False
        except (json.JSONDecodeError, KeyError) as e:
            result["checks"]["sentencify_parse_error"] = str(e)
            result["passed"] = False
            return result

        # === Stage 3: batch partitioning + mock translations ===
        batches_dir = ws / "batches"
        r = run_script(
            SCRIPTS_DIR / "partition_batches.py",
            ["--sentences", str(sentences), "--workspace", str(batches_dir), "--target-size", "1500"],
            "partition",
        )
        result["stages"]["partition"] = {"ok": r["ok"], "stdout": r["stdout"], "stderr": r["stderr"]}
        if not r["ok"]:
            result["passed"] = False
            return result

        translations_dir = ws / "translations"
        mock_errors = create_mock_translations(batches_dir, translations_dir)
        result["checks"]["mock_translation_errors"] = mock_errors
        if mock_errors:
            result["passed"] = False

        # === Stage 4: concatenate ===
        assembled = ws / "assembled.md"
        r = run_script(
            CONCATENATE,
            ["--blocked", str(blocked), "--translations-dir", str(translations_dir), "--output", str(assembled)],
            "concatenate",
        )
        result["stages"]["concatenate"] = {"ok": r["ok"], "stdout": r["stdout"], "stderr": r["stderr"]}
        if not r["ok"]:
            result["passed"] = False
            return result

        assembled_text = assembled.read_text(encoding="utf-8")
        assembled_info = count_blocks(assembled_text)
        result["checks"]["assembled_balanced"] = assembled_info["balanced"]
        result["checks"]["assembled_count"] = assembled_info["count"]
        if not assembled_info["balanced"]:
            result["passed"] = False

        # === Content integrity checks ===
        blocked_ids = set(s[0] for s in BLOCK_START_RE.findall(blocked_text))
        assembled_ids = set(s[0] for s in BLOCK_START_RE.findall(assembled_text))
        missing_assembled = blocked_ids - assembled_ids
        if missing_assembled:
            result["checks"]["missing_in_assembled"] = sorted(missing_assembled)
            result["passed"] = False

        # Check 2: sentence-per-line
        lines = assembled_text.split("\n")
        line_violations = []
        in_block = False
        current_id = ""
        current_type = ""
        line_count = 0
        skip_types = {"equation", "code", "table"}

        for line in lines:
            sm = BLOCK_START_RE.search(line)
            em = BLOCK_END_RE.search(line)
            if sm:
                current_id = sm.group(1)
                current_type = sm.group(2)
                in_block = True
                line_count = 0
                continue
            if em:
                if in_block and current_id and current_type not in skip_types:
                    sent_count = len(sent_blocks.get(current_id, {}).get("sentences", []))
                    if sent_count > 0 and line_count != sent_count:
                        line_violations.append(
                            {"block_id": current_id, "type": current_type,
                             "lines": line_count, "expected_sentences": sent_count}
                        )
                in_block = False
                current_id = ""
                current_type = ""
                continue
            if in_block:
                line_count += 1

        result["checks"]["line_violations"] = line_violations
        if line_violations:
            result["passed"] = False

        # Check 3: no empty blocks
        empty_blocks = []
        for bid in sorted(blocked_ids):
            in_b = False
            content_found = False
            for line in lines:
                sm2 = BLOCK_START_RE.search(line)
                em2 = BLOCK_END_RE.search(line)
                if sm2 and sm2.group(1) == bid:
                    in_b = True
                    continue
                if em2 and em2.group(1) == bid:
                    break
                if in_b and line.strip():
                    content_found = True
                    break
            if not content_found:
                empty_blocks.append(bid)
        result["checks"]["empty_blocks"] = empty_blocks
        if empty_blocks:
            result["passed"] = False

    finally:
        if not keep:
            shutil.rmtree(tmpdir, ignore_errors=True)

    return result


def print_report(results: list[dict]):
    """Print a human-readable report."""
    print("=" * 72)
    print("PIPELINE STRUCTURAL TEST REPORT")
    print("=" * 72)

    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"\n[{status}] {r['file']}")
        print(f"  Stages:")
        for sname, sinfo in sorted(r.get("stages", {}).items()):
            s_ok = "✓" if sinfo.get("ok") else "✗"
            extra = ""
            if sname == "blockify":
                extra = f"  [{sinfo.get('blocks', '?')} blocks, strategy={sinfo.get('strategy', '?')}]"
            print(f"    {s_ok} {sname}{extra}")

        print(f"  Checks:")
        checks = r.get("checks", {})
        for ck, cv in sorted(checks.items()):
            if isinstance(cv, list):
                if cv:
                    print(f"    ✗ {ck}: {len(cv)} items")
                    for v in cv[:5]:
                        print(f"      - {v}")
                else:
                    print(f"    ✓ {ck}: 0")
            elif isinstance(cv, bool):
                print(f"    {'✓' if cv else '✗'} {ck}: {cv}")
            elif isinstance(cv, int):
                print(f"    · {ck}: {cv}")
            elif isinstance(cv, str):
                if cv:
                    print(f"    ✗ {ck}: {cv[:100]}")
            else:
                print(f"    · {ck}: {cv}")

        if not r["passed"]:
            for sname, sinfo in r.get("stages", {}).items():
                if not sinfo.get("ok"):
                    stderr = sinfo.get("stderr", "")
                    if stderr:
                        print(f"  [stderr {sname}]: {stderr[:200]}")

    print("\n" + "=" * 72)
    total = len(results)
    ok = sum(1 for r in results if r["passed"])
    print(f"Result: {ok}/{total} passed")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(description="Structural pipeline test harness")
    parser.add_argument("inputs", nargs="+", help="Input markdown files to test")
    parser.add_argument("--keep", action="store_true", help="Keep temp workspaces for debugging")
    args = parser.parse_args()

    if not BLOCKIFY.exists():
        print(f"Error: BLOCKIFY not found at {BLOCKIFY}", file=sys.stderr)
        print("Run this script from the project root (literature_translator/).", file=sys.stderr)
        sys.exit(1)

    results = []
    for path_str in args.inputs:
        p = Path(path_str)
        if not p.exists():
            print(f"SKIP (not found): {p}", file=sys.stderr)
            continue
        r = test_one_file(p, keep=args.keep)
        results.append(r)

    print_report(results)
    sys.exit(0 if all(r["passed"] for r in results) else 1)


if __name__ == "__main__":
    main()
