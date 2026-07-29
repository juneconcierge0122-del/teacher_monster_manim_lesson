#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────
# Manim Lessons — 批次渲染 + 防呆檢查
# ─────────────────────────────────────────────────────────────────────
# Usage:
#   ./render.sh                           # 渲染所有 lessons (低畫質預覽)
#   ./render.sh -q h                      # 高畫質
#   ./render.sh -l triangle_centers       # 只渲染指定 lesson
#   ./render.sh --skip-checks             # 跳過 preflight (不建議)
#
# Exit codes:
#   0 — all good
#   1 — preflight 發現致命錯誤
#   2 — manim 渲染失敗
# ─────────────────────────────────────────────────────────────────────

set -e   # 任何一步失敗就 abort

# 預設選項
QUALITY="l"            # l=480p (預覽), m=720p, h=1080p, k=4K
SKIP_CHECKS=0
ONLY_LESSON=""
SCENE="FullLesson"

# 解析 argv
while [[ $# -gt 0 ]]; do
    case $1 in
        -q|--quality)     QUALITY="$2"; shift 2;;
        -l|--lesson)      ONLY_LESSON="$2"; shift 2;;
        -s|--scene)       SCENE="$2"; shift 2;;
        --skip-checks)    SKIP_CHECKS=1; shift;;
        -h|--help)
            grep '^#' "$0" | sed 's/^# \?//'
            exit 0;;
        *)
            echo "未知參數: $1" >&2; exit 1;;
    esac
done

# 顏色輸出 (給人看的)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ─── 1. 確認環境 ────────────────────────────────────────────────────
if ! command -v manim &> /dev/null; then
    echo -e "${RED}❌ manim 沒裝. 跑: pip install manim${NC}" >&2
    exit 2
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ python3 沒裝${NC}" >&2
    exit 2
fi

cd "$(dirname "$0")"   # 切到 manim_lessons/ 根目錄

# ─── 2. 找出要渲染的 lessons ──────────────────────────────────────
if [[ -n "$ONLY_LESSON" ]]; then
    LESSONS=("lessons/${ONLY_LESSON}.py")
    if [[ ! -f "${LESSONS[0]}" ]]; then
        echo -e "${RED}❌ 找不到 ${LESSONS[0]}${NC}" >&2
        exit 1
    fi
else
    mapfile -t LESSONS < <(find lessons -name "*.py" -not -name "__*" | sort)
fi

if [[ ${#LESSONS[@]} -eq 0 ]]; then
    echo -e "${YELLOW}⚠ lessons/ 目錄沒有任何 .py 檔${NC}"
    exit 0
fi

# ─── 3. 對每個 lesson 跑 preflight + 渲染 ────────────────────────
FAILED=()
for lesson in "${LESSONS[@]}"; do
    name=$(basename "$lesson" .py)
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE} ▶ ${name}${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

    # 3a. Preflight (找對應的 script.md)
    if [[ "$SKIP_CHECKS" -eq 0 ]]; then
        script_md="lessons/${name}_script.md"
        if [[ -f "$script_md" ]]; then
            echo -e "${YELLOW}▸ 跑 preflight: ${script_md}${NC}"
            if ! python3 -m manim_lessons.lib.checks "$script_md" -v; then
                echo -e "${RED}✗ ${name} preflight 失敗 — 跳過渲染${NC}"
                FAILED+=("$name")
                continue
            fi
        else
            echo -e "${YELLOW}▸ 沒找到 ${script_md} — 跳過 preflight${NC}"
        fi
    fi

    # 3b. 渲染
    echo -e "${YELLOW}▸ 渲染中... (quality=${QUALITY})${NC}"
    if manim "-pq${QUALITY}" "$lesson" "$SCENE"; then
        echo -e "${GREEN}✓ ${name} 渲染完成${NC}"
    else
        echo -e "${RED}✗ ${name} 渲染失敗${NC}"
        FAILED+=("$name")
    fi
done

# ─── 4. 總結 ────────────────────────────────────────────────────────
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
if [[ ${#FAILED[@]} -eq 0 ]]; then
    echo -e "${GREEN} ✓ 全部完成 (${#LESSONS[@]} lessons)${NC}"
    exit 0
else
    echo -e "${RED} ✗ 失敗 (${#FAILED[@]}/${#LESSONS[@]}):${NC}"
    for f in "${FAILED[@]}"; do
        echo -e "${RED}     - ${f}${NC}"
    done
    exit 1
fi
