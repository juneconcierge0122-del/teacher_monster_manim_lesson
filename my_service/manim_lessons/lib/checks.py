"""
Checks
======
渲染前防呆. 偵測 ensemble_feedback 裡看到的所有死亡 pattern.

CLI usage:
    python -m lib.checks lessons/triangle_centers_script.md \
        --topic "Multi-scenario Applications of Triangle Centers" \
        --klps "Incenter,Circumcenter,Optimization,Modeling"

Programmatic usage:
    from lib.checks import preflight_check
    errors = preflight_check(script_text, topic, klps)
"""
import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


# ── 從 16 份 feedback 整理出的「會被扣分」的 pattern ──────────────────────
META_FORBIDDEN = [
    "define the central",
    "central term",
    "explain the conceptual",
    "here we will",
    "i will explain",
    "we will define",
    "we will discuss",
    "we will cover",
    "covers the topic",
    "is studied because",
    "list the key vocabulary",
]

PLACEHOLDER_PATTERNS = [
    r"\{\{[^}]*\}\}",           # {{ X }}
    r"\[INSERT[^\]]*\]",         # [INSERT X]
    r"\bTODO\b",
    r"\bXXX\b",
    r"\bFIXME\b",
    r"\bplaceholder\b",
]

TRUNCATION_PATTERNS = [
    "physical sist",
    "Bloo ",                    # "Bloo" 但避開 "Blood"
    " Defi ",
    " Defi.",
    "Comp ",                    # "Comp" 通常是 "Computer" 或 "Components" 截斷
    "De covers",
    "De is studied",
    "Spe is",
    "Plant Anatom ",            # "Anatomy" 截斷
]


def check_meta_content(script: str) -> List[str]:
    """偵測 meta 句 (致命傷, 直接 −4.0 Title/Depth Mismatch)."""
    errors = []
    low = script.lower()
    for pattern in META_FORBIDDEN:
        if pattern in low:
            errors.append(f"META 句殘留 (致命): {pattern!r}")
    return errors


def check_placeholders(script: str) -> List[str]:
    """偵測未填入的 template 變數 / TODO."""
    errors = []
    for pat in PLACEHOLDER_PATTERNS:
        matches = re.findall(pat, script, flags=re.IGNORECASE)
        for m in matches:
            errors.append(f"PLACEHOLDER 殘留: {m!r}")
    return errors


def check_truncations(script: str) -> List[str]:
    """偵測常見的截斷字 (e.g. 'physical sist' = 'Physical Systems' 被截)."""
    errors = []
    for trunc in TRUNCATION_PATTERNS:
        if trunc in script:
            errors.append(f"截斷字疑似存在: {trunc!r}")
    return errors


def check_klp_coverage(script: str, klps: List[str],
                       min_keywords_per_klp: int = 2) -> List[str]:
    """每個 KLP 至少要有 min_keywords 個關鍵字出現在 script 裡."""
    errors = []
    low = script.lower()
    for klp in klps:
        keywords = [w.strip(".,;:()[]") for w in klp.split()
                    if len(w) > 2 and w.lower() not in
                    {"the", "and", "for", "with", "that", "this", "vs"}]
        keywords = [k for k in keywords if k]
        threshold = min(min_keywords_per_klp, len(keywords))
        hits = sum(1 for kw in keywords if kw.lower() in low)
        if hits < threshold:
            errors.append(
                f"KLP 覆蓋不足 (找到 {hits}/{threshold}): {klp!r}"
            )
    return errors


def check_topic_appearance(script: str, topic: str,
                           min_occurrences: int = 2) -> List[str]:
    """Topic 名稱要在 script 裡出現至少 N 次 (防 Title/Depth Mismatch)."""
    errors = []
    # 抓 topic 中的關鍵詞 (跳過 "of", "the" 等)
    keywords = [w for w in topic.split()
                if len(w) > 3 and w.lower() not in
                {"with", "that", "this", "from", "into"}]
    if not keywords:
        return errors
    # 至少一個 keyword 要 >= min_occurrences
    max_hits = max(script.lower().count(kw.lower()) for kw in keywords)
    if max_hits < min_occurrences:
        errors.append(
            f"Topic 字眼出現次數不足 ({max_hits} < {min_occurrences}): {topic!r}"
        )
    return errors


def check_numeric_consistency(script: str) -> List[str]:
    """
    偵測是否有 同一概念用兩個不同數字 (37683b40 死法).
    這個 heuristic 不完美, 只能標出可疑句, 留人工複查.
    """
    errors = []
    # 找出同一行內出現多個數字的情境
    money_pattern = re.findall(r'\$\s?\d+', script)
    if len(set(money_pattern)) > 5:
        errors.append(
            f"可疑: 出現超過 5 個不同金額, 請人工複查: {set(money_pattern)}"
        )
    return errors


def check_length_signals(script: str, max_chars: int = 6000) -> List[str]:
    """超長 script 通常代表沒被剪輯, 容易踩 information overload."""
    errors = []
    if len(script) > max_chars:
        errors.append(f"Script 過長 ({len(script)} chars > {max_chars})")
    return errors


def preflight_check(script: str,
                    topic: str = "",
                    klps: List[str] = None,
                    verbose: bool = False) -> Tuple[List[str], List[str]]:
    """
    跑全部檢查. 回傳 (errors, warnings).

    errors  = 一定會被扣分, 必修.
    warnings = 可能會被扣分, 強烈建議檢查.
    """
    errors = []
    warnings = []

    errors += check_meta_content(script)
    errors += check_placeholders(script)
    warnings += check_truncations(script)

    if klps:
        errors += check_klp_coverage(script, klps)

    if topic:
        errors += check_topic_appearance(script, topic)

    warnings += check_numeric_consistency(script)
    warnings += check_length_signals(script)

    if verbose:
        print(f"Script length: {len(script)} chars")
        print(f"Errors: {len(errors)}, Warnings: {len(warnings)}")

    return errors, warnings


def format_report(errors: List[str], warnings: List[str]) -> str:
    """印出漂亮的報告."""
    lines = []
    if not errors and not warnings:
        lines.append("✓ 全部檢查通過.")
        return "\n".join(lines)

    if errors:
        lines.append(f"✗ 發現 {len(errors)} 個致命錯誤:")
        for e in errors:
            lines.append(f"  ❌ {e}")
    if warnings:
        lines.append(f"⚠ 發現 {len(warnings)} 個警告:")
        for w in warnings:
            lines.append(f"  ⚠️  {w}")
    return "\n".join(lines)


# ─── CLI ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Manim lesson preflight check")
    parser.add_argument("script", help="Script markdown / text file path")
    parser.add_argument("--topic", default="", help="課程 topic")
    parser.add_argument("--klps", default="",
                        help="逗號分隔的 Key Learning Points")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    script_path = Path(args.script)
    if not script_path.exists():
        print(f"❌ 找不到檔案: {script_path}", file=sys.stderr)
        sys.exit(2)

    script = script_path.read_text(encoding="utf-8")
    klps = [k.strip() for k in args.klps.split(",") if k.strip()]

    errors, warnings = preflight_check(script, topic=args.topic,
                                       klps=klps, verbose=args.verbose)
    print(format_report(errors, warnings))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
