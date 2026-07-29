"""
Lib 入口. 各模組 *不在這裡* eager-import,
讓 checks.py 在沒有 manim 環境也能單獨用 (給 CI / preflight 用).
需要哪個模組就直接 from manim_lessons.lib.xxx import yyy.
"""
