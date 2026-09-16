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
#
# --disable_caching is not optional. Scene.add_sound begins with
#   if self.renderer.skip_animations: return
# and skip_animations is exactly what manim sets when it reuses a cached
# partial movie file. So re-rendering a lesson that has been rendered before
# silently drops the narration for every beat that hits the cache: the video
# comes out full length and correct, with an audio track that stops a few
# seconds in. Caching only ever helps on a re-render, which is precisely the
# case it breaks, so it is switched off outright.
#
# PARALLEL=1 renders every scene at once instead of one at a time:
#
#   PARALLEL=1 SCENE_PREFIX=AdvCalcE bash tools/queue.sh 75:a.py 76:b.py
#
# which is four manim processes on a 32-core box that was using one. The reason
# it was serial is the shared media/texts/*.svg font cache, so in this mode each
# scene gets its own --media_dir and the finished mp4 is moved back to the
# canonical media/videos/<lesson>/1080p60/ path afterwards -- checkvideo,
# grabbeats and the copy into samples/output all stay exactly as they were.
# The cost is that each process rebuilds its own font cache, which is nothing
# next to 1300 frames a beat.
#
# Each scene now gets its own log in both modes, because `grep "Rendered <name>"`
# is the only thing between a silently mis-resolved scene name and an uploaded
# video of the base class -- and on a shared log that grep can match a line some
# other scene wrote. $LOG keeps the one-line-per-event trace; watch a particular
# scene in its own log.
cd "$(dirname "$0")/.." || exit 1
LOG="${RENDER_LOG:-/tmp/render.log}"
PREFIX="${SCENE_PREFIX:-LandauL}"
PARALLEL="${PARALLEL:-0}"
: > "$LOG"
echo "logging to $LOG  (per-scene logs alongside it)"

find_lesson () {
  local hits
  hits=$(find lessons -name "$1" -type f)
  if [ "$(printf '%s\n' "$hits" | grep -c .)" -ne 1 ]; then
    echo "AMBIGUOUS-OR-MISSING $1: [$hits]" | tee -a "$LOG"; return 1
  fi
  printf '%s' "$hits"
}

run () {
  local path slog mdir out want
  path=$(find_lesson "$1") || return 1
  slog="${LOG%.log}.$2.log"
  : > "$slog"
  if [ "$PARALLEL" = "1" ]; then mdir="media/par/$2"; else mdir="media"; fi
  for attempt in 1 2; do
    echo "=== $2 attempt $attempt $(date +%H:%M:%S)  log $slog" >> "$LOG"
    if manim -qh --fps 60 --disable_caching --media_dir "$mdir" "$path" "$2" >> "$slog" 2>&1; then
      if grep -q "Rendered $2\b" "$slog"; then
        if [ "$mdir" != "media" ]; then
          out=$(find "$mdir/videos" -name "$2.mp4" -type f | head -1)
          want="media/videos/$(basename "${path%.py}")/1080p60/$2.mp4"
          if [ -z "$out" ] || ! { mkdir -p "$(dirname "$want")" && mv "$out" "$want"; }; then
            echo "FAIL $2: rendered but could not be moved out of $mdir" >> "$LOG"; return 1
          fi
          rm -rf "$mdir"
        fi
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
  if [ "$PARALLEL" = "1" ]; then
    run "$f" "${PREFIX}${n}ZH" &
    run "$f" "${PREFIX}${n}EN" &
  else
    run "$f" "${PREFIX}${n}ZH"
    run "$f" "${PREFIX}${n}EN"
  fi
done
wait
echo "QUEUE DONE $(date +%H:%M:%S)" >> "$LOG"
grep -E "^(OK|FAIL|MISMATCH|QUEUE)" "$LOG"
