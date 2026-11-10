#!/usr/bin/env python3
"""Check zh-TW technical Markdown against the thc-zhtw-style punctuation rules.

Only mechanical rules are checked. Semantic rules (term translation, first-use
glosses, tone) still need a human or model review.

Usage:
    check_zhtw.py FILE [FILE ...]      # use "-" for stdin
    check_zhtw.py --no-warn FILE       # show errors only

Exit code: 0 = no errors, 1 = errors found, 2 = usage / IO problem.
Output:    path:line:col: E|W [rule] message
"""

from __future__ import annotations

import argparse
import re
import sys

CJK = r"㐀-䶿一-鿿豈-﫿"
CJK_RE = re.compile(f"[{CJK}]")
FULL_PUNCT = "，。、；：「」『』《》【】"

BANNED = {
    "≥": "改用 `>=` 或「以上」", "≧": "改用 `>=` 或「以上」",
    "≤": "改用 `<=` 或「以下」", "≦": "改用 `<=` 或「以下」",
    "≠": "改用 `!=` 或「不等於」",
    "→": "改用 `->` 或「改為」「至」「對應」", "←": "改用 `->` 或中文改寫",
    "⇒": "改用 `->` 或中文改寫",
    "×": "改用 `x` 或 `*`", "÷": "改用 `/`",
    "±": "改用 `+/-` 或「正負」",
    "≈": "改用「約」", "≒": "改用「約」",
    "—": "破折號改寫為冒號或逗號分句", "–": "改寫為冒號或逗號分句，或用半形 `-`",
    "…": "改用半形 `...`",
    "～": "範圍改用「至」",
    "✓": "改用「是」「否」或 O、X", "✗": "改用「是」「否」或 O、X",
    "✔": "改用「是」「否」或 O、X", "✘": "改用「是」「否」或 O、X",
    "↑": "改用「上升」或「增」", "↓": "改用「下降」或「減」",
    "•": "改用 Markdown 清單 `-` 或頓號", "‧": "改用 Markdown 清單 `-` 或頓號",
    "・": "改用 Markdown 清單 `-` 或頓號",
    "※": "改用【注意】標籤或 blockquote",
    "＞": "改用半形 `>`", "＜": "改用半形 `<`", "＝": "改用半形 `=`",
    "＋": "改用半形 `+`", "－": "改用半形 `-`",
    "？": "問號一律半形 `?`", "！": "驚嘆號一律半形 `!`",
    "（": "夾注括號一律半形 `(`", "）": "夾注括號一律半形 `)`",
    "／": "改用半形 `/`", "　": "全形空格改用半形空格",
}
DECOR_RE = re.compile(r"[★☆■□▲△▼▽●○◆◇]")
BOX_RE = re.compile(r"[─-╿]")
CIRCLED_RE = re.compile(r"[①-⓿❶-➓]")

TAG_WHITELIST = {"注意", "重要", "必要", "實測", "暫譯", "待辦", "正式環境"}
SECTION_NUMS = set("一二三四五六七八九十")

MAINLAND = {
    "軟件": "軟體", "網絡": "網路", "數據": "資料", "內存": "記憶體",
    "默認": "預設", "服務器": "伺服器", "字符": "字元", "接口": "介面",
    "算法": "演算法", "優化": "最佳化", "散列": "雜湊", "補丁": "修補程式",
    "零日": "零時差", "運維": "維運", "視頻": "影片",
}
MAINLAND_CONTEXT = {
    "程序": "指 program 時用「程式」", "信息": "指 information 時用「資訊」",
    "質量": "指 quality 時用「品質」", "支持": "指 support 時用「支援」",
}

INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
LINK_TARGET_RE = re.compile(r"\]\(([^)]*)\)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->")
TAG_RE = re.compile(r"【([^】]*)】")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
# Markdown line prefixes (heading, list, quote, table cell) that legitimately precede a space.
MD_PREFIX_RE = re.compile(r"^\s*(#{1,6}|[-*+]|\d+\.|>+|.*\|)\s*$")


def mask(line: str) -> str:
    """Blank out spans the rules exempt, keeping column positions stable."""
    line = INLINE_CODE_RE.sub(lambda m: m.group(1) + "C" * len(m.group(2)) + m.group(1), line)
    line = HTML_COMMENT_RE.sub(lambda m: " " * len(m.group(0)), line)
    line = LINK_TARGET_RE.sub(lambda m: "](" + "U" * len(m.group(1)) + ")", line)
    line = URL_RE.sub(lambda m: "U" * len(m.group(0)), line)
    return line


def is_cjk(ch: str) -> bool:
    return bool(ch) and bool(CJK_RE.match(ch))


def neighbor(s: str, i: int, step: int) -> str:
    j = i + step
    while 0 <= j < len(s) and s[j] == " ":
        j += step
    return s[j] if 0 <= j < len(s) else ""


def check_line(s: str, raw: str):
    """Yield (col, level, rule, message) for one masked line."""
    has_cjk = bool(CJK_RE.search(s))

    for i, ch in enumerate(s):
        if ch in BANNED:
            yield i, "E", "e-banned", f"禁用符號 `{ch}`: {BANNED[ch]}"
    for m in DECOR_RE.finditer(s):
        yield m.start(), "E", "e-banned", f"裝飾符號 `{m.group()}` 禁用，改用【】標籤或粗體"
    for m in BOX_RE.finditer(s):
        yield m.start(), "E", "f-box", f"框線字元 `{m.group()}` 僅可用於程式碼區塊內的架構圖"
    for m in CIRCLED_RE.finditer(s):
        yield m.start(), "E", "e-banned", f"圈號 `{m.group()}` 改用 `1.` `2.` 編號"
    for m in re.finditer(r"\d\s*~\s*\d", s):
        yield m.start(), "E", "e-banned", "範圍 `~` 改用「至」"

    for i, ch in enumerate(s):
        prev_c = s[i - 1] if i > 0 else ""
        next_c = s[i + 1] if i + 1 < len(s) else ""
        if ch in ",;":
            # In a CJK line, a half-width comma/semicolon is wrong when it touches CJK
            # text or is glued to the next word (English style would add a space).
            if is_cjk(neighbor(s, i, -1)) or is_cjk(neighbor(s, i, 1)) or (
                    has_cjk and next_c not in ("", " ") and not (prev_c.isdigit() and next_c.isdigit())):
                yield i, "E", "b-halfwidth", f"中文行文使用半形 `{ch}`，應為 `{'，' if ch == ',' else '；'}`"
        elif ch == ".":
            if is_cjk(prev_c) and s[i:i + 3] != "...":
                yield i, "E", "b-halfwidth", "中文句尾使用半形 `.`，應為 `。`"
        elif ch == ":":
            if is_cjk(prev_c):
                yield i, "E", "d-colon", "冒號前為中文字，應用全形 `：`"
            elif (has_cjk and next_c not in ("", " ")
                  and not (prev_c.isdigit() and next_c.isdigit())
                  and next_c not in "/:"):
                yield i, "W", "d-colon", "半形冒號後應加一個半形空格"
        elif ch == "：":
            # Look through Markdown emphasis markers: "**標題**：" counts as preceded by CJK.
            j = i - 1
            while j >= 0 and s[j] in "*_":
                j -= 1
            prev_c = s[j] if j >= 0 else ""
            if prev_c and not is_cjk(prev_c) and prev_c not in FULL_PUNCT and prev_c != " ":
                yield i, "E", "d-colon", "冒號前非中文字，應用半形 `: `"
        elif ch in "?!":
            if is_cjk(next_c):
                yield i, "E", "c-qmark", f"`{ch}` 後接中文應加一個半形空格"
            elif next_c == " " and i + 2 < len(s) and s[i + 2] in ")\"」":
                yield i, "E", "c-qmark", f"`{ch}` 後接右括號或引號不應加空格"

        if ch in FULL_PUNCT:
            if prev_c == " " and s[:i].strip() and not MD_PREFIX_RE.match(s[:i]):
                yield i, "E", "k-spacing", f"全形標點 `{ch}` 前不應有空格"
            if next_c == " " and neighbor(s, i, 1) not in ("", "|"):
                yield i, "E", "k-spacing", f"全形標點 `{ch}` 後不應有空格"

    for m in re.finditer(f"[{CJK}][A-Za-z0-9`]|[A-Za-z0-9`][{CJK}]", s):
        yield m.start() + 1, "E", "k-spacing", "中文與英文、數字之間應加一個半形空格"

    for m in re.finditer(r"\(", s):
        i = m.start()
        if i > 0 and (is_cjk(s[i - 1]) or s[i - 1].isalpha()) and has_cjk:
            yield i, "W", "k-spacing", "夾注括號外側應與文字間留一個半形空格"
        depth_open = s.count("(", 0, i) - s.count(")", 0, i)
        if depth_open > 0:
            yield i, "E", "i-nested", "禁止巢狀括號"
    for m in re.finditer(r"\)", s):
        i = m.end()
        if i < len(s) and is_cjk(s[i]):
            yield m.start(), "W", "k-spacing", "夾注括號外側應與文字間留一個半形空格"

    # Left and right parentheses of one pair must be the same width.
    stack = []
    for i, ch in enumerate(s):
        if ch in "(（":
            stack.append((i, ch))
        elif ch in ")）" and stack:
            j, opener = stack.pop()
            if (opener == "(") != (ch == ")"):
                yield j, "E", "k-paren", f"左右括號形制不一致 (`{opener}` 與 `{ch}`)，必須同為半形或同為全形"

    for m in TAG_RE.finditer(s):
        word = m.group(1)
        if word in TAG_WHITELIST or not word:  # empty 【】 is a mention of the bracket itself
            continue
        if word[0] in SECTION_NUMS and (len(word) == 1 or word[1] == "、"):
            yield m.start(), "W", "j-tag", f"【{word}】: 一般文件章節引用請寫「第 N 章」"
        else:
            yield m.start(), "E", "j-tag", f"【{word}】不在標籤白名單內"

    for word, fix in MAINLAND.items():
        for m in re.finditer(word, s):
            yield m.start(), "W", "g-mainland", f"疑似中國大陸用語「{word}」，台灣慣用「{fix}」"
    for word, hint in MAINLAND_CONTEXT.items():
        for m in re.finditer(word, s):
            yield m.start(), "W", "g-mainland", f"「{word}」請確認語境: {hint}"


def check_text(path: str, text: str, show_warn: bool) -> int:
    errors = 0
    lines = text.splitlines()
    in_fence = False
    # YAML front matter is checked like body text, except that a folded or literal
    # block scalar is rejected: each line break becomes a space next to CJK text.
    fm_end = 0
    if lines and lines[0].strip() == "---":
        for k in range(1, len(lines)):
            if lines[k].strip() == "---":
                fm_end = k + 1
                break
    for n, raw in enumerate(lines, start=1):
        if n <= fm_end:
            if raw.strip() == "---":
                continue
            if re.match(r"^\w[\w-]*:\s*[>|][+-]?\s*$", raw):
                errors += 1
                print(f"{path}:{n}:1: E [fm-block] front matter 請寫成單行，多行區塊會在換行處產生空格")
                continue
        if FENCE_RE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        masked = mask(raw)
        for col, level, rule, msg in sorted(set(check_line(masked, raw))):
            if level == "E":
                errors += 1
            elif not show_warn:
                continue
            print(f"{path}:{n}:{col + 1}: {level} [{rule}] {msg}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description="zh-TW 技術文件標點與用字檢查")
    ap.add_argument("files", nargs="+", help="Markdown 檔案，`-` 代表 stdin")
    ap.add_argument("--no-warn", action="store_true", help="只顯示錯誤 (E)")
    args = ap.parse_args()

    total = 0
    for f in args.files:
        try:
            text = sys.stdin.read() if f == "-" else open(f, encoding="utf-8").read()
        except OSError as exc:
            print(f"{f}: 無法讀取: {exc}", file=sys.stderr)
            return 2
        total += check_text(f, text, not args.no_warn)
    print(f"共 {total} 個錯誤 (E)", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
