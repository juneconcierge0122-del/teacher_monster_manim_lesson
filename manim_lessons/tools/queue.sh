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
cd "$(dirname "$0")/.." || exit 1
LOG="${RENDER_LOG:-/tmp/render.log}"
: > "$LOG"
echo "logging to $LOG"

run () {
  for attempt in 1 2; do
    echo "=== $2 attempt $attempt $(date +%H:%M:%S)" >> "$LOG"
    if manim -qh --fps 60 "lessons/$1" "$2" >> "$LOG" 2>&1; then
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
  run "$f" "LandauL${n}ZH"
  run "$f" "LandauL${n}EN"
done
echo "QUEUE DONE $(date +%H:%M:%S)" >> "$LOG"
grep -E "^(OK|FAIL|MISMATCH|QUEUE)" "$LOG"
