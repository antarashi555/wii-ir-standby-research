"""Security/release gate for this intentionally minimal public repository.
Run: python tools/verify_public_release.py
Does NOT inspect or touch private NAND archives.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = {
    ".gitignore", "LICENSE", "README.md", "README.ja.md", "SECURITY.md",
    "docs/01-history.md", "docs/02-blockers-and-decisions.md",
    "docs/03-ios58-ios80-stm-negative-result.md",
    "docs/04-wc24-and-wakeup.md", "docs/05-green-power-and-libogc-idle.md",
    "docs/06-sensorbar-rail-and-carrier.md",
    "docs/07-methodology-and-reproduction.md", "docs/08-sources.md",
    "evidence/audit-metrics.json", "tests/test_public_arithmetic.py",
    "tools/verify_public_release.py",
}
# Match secret VALUES, not ordinary prose discussing privacy.
VALUE_PATTERNS = {
    "console serial identifier": re.compile(r"\bLJF\d{9,}\b", re.I),
    "local private IP": re.compile(r"\b(?:192\.168|10\.\d+|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b"),
    "absolute Windows path": re.compile(r"\b[A-Z]:\\", re.I),
    "GitHub token": re.compile(r"\b(?:ghp_|gho_|ghu_|ghs_|github_pat_)[A-Za-z0-9_]+", re.I),
    "key PEM header": re.compile(r"-----BEGIN (?:RSA|OPENSSH|EC|PRIVATE) KEY-----"),
    "email address": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    "legacy serialized NAND dump filename": re.compile(r"\b\d{6}_LJF\d+_nand_\d+\.bin", re.I),
}
def main():
    failures = []
    present=set()
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel=path.relative_to(ROOT).as_posix()
        if rel.startswith(".git/") or "__pycache__" in path.parts or rel.endswith(".pyc"):
            continue
        present.add(rel)
        if rel not in ALLOWLIST:
            failures.append(f"unexpected file, not in explicit allowlist: {rel}")
            continue
        if path.stat().st_size >= 100000:
            failures.append(f"file too large to assume document-only: {rel}")
            continue
        raw=path.read_bytes()
        if bytes([0]) in raw:
            failures.append(f"binary NUL byte: {rel}")
            continue
        text=raw.decode("utf-8")
        for label,pattern in VALUE_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"potential {label}: {rel}")
        if rel.endswith(".md"):
            for url in re.findall(r"\]\(([^)]+)\)",text):
                if url.startswith(("http://","https://","#","mailto:")):
                    continue
                link=url.split("#")[0].split("?")[0]
                if link and not (path.parent/link).exists():
                    failures.append(f"broken relative link in {rel}: {link}")
    missing=ALLOWLIST-present
    if missing:
        failures.append(f"missing release files: {sorted(missing)}")
    metrics=json.loads((ROOT/"evidence/audit-metrics.json").read_text(encoding="utf-8"))
    if metrics["stm_ioctl_u16"]["recognized_count"] !=13:
        failures.append("unexpected STM count")
    if failures:
        print("PUBLIC_RELEASE_GATE_FAIL")
        for problem in failures: print("FAIL",problem)
        return 1
    print(f"PUBLIC_RELEASE_GATE_PASS {len(present)} explicitly allowed UTF-8 text files")
    print("TESTS_EXPECTED: python -m unittest discover -s tests -v")
    print("NO PRIVATE FIRMWARE/BINARIES/KEYS IN ALLOWLIST")
    return 0
if __name__=="__main__":
    sys.exit(main())
