#!/bin/bash
# Render lessons at 1080p60, one at a time.
#
#   bash tools/queue.sh 49:landau_l49_adiabatic.py 50:landau_l50_canonical_vars.py
#
# Strictly sequential on purpose: media/texts/*.svg is a shared cache, and two
# manim processes racing for the same uncached string raise FileNotFoundError.
# Each scene is retried once, and the log is grepped for `Rendered <name>` --
# manim silently renders the base class instead when a scene name does not
# resolve, so a finished mp4 is not on its own proof the right thing ran.
#
# The file name is looked up under lessons/ rather than joined onto it, so the
# same call works whichever series subdirectory the lesson lives in. Set
# SCENE_PREFIX for a series that does not name its scenes LandauL<n>ZH/EN.
cd "$(dirname "$0")/.." || exit 1
LOG="${RENDER_LOG:-/tmp/render.log}"
PREFIX="${SCENE_PREFIX:-LandauL}"
: > "$LOG"
echo "logging to $LOG"

find_lesson () {
  local hits
  hits=$(find lessons -name "$1" -type f)
  if [ "$(printf '%s\n' "$hits" | grep -c .)" -ne 1 ]; then
    echo "AMBIGUOUS-OR-MISSING $1: [$hits]" | tee -a "$LOG"; return 1
  fi
  printf '%s' "$hits"
}

run () {
  local path
  path=$(find_lesson "$1") || return 1
  for attempt in 1 2; do
    echo "=== $2 attempt $attempt $(date +%H:%M:%S)" >> "$LOG"
    if manim -qh --fps 60 "$path" "$2" >> "$LOG" 2>&1; then
      if grep -q "Rendered $2\b" "$LOG"; then
        echo "OK $2 $(date +%H:%M:%S)" >> "$LOG"; return 0
      fi
      echo "MISMATCH $2: manim did not report rendering this scene" >> "$LOG"
    fi
    sleep 5
  done
  echo "FAIL $2" >> "$LOG"; return 1
}

for spec in "$@"; do
  n="${spec%%:*}"; f="${spec#*:}"
  run "$f" "${PREFIX}${n}ZH"
  run "$f" "${PREFIX}${n}EN"
done
echo "QUEUE DONE $(date +%H:%M:%S)" >> "$LOG"
grep -E "^(OK|FAIL|MISMATCH|QUEUE)" "$LOG"
