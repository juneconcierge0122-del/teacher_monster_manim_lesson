"""
opus_lesson_writer.py
=====================
Give Opus a topic + reference, get back lesson.py + _script.md.

CLI:
    export ANTHROPIC_API_KEY=...
    python opus_lesson_writer.py \\
        --course_req "Big Concept: ...\\nTopic: ..." \\
        --persona   "Grade: 8th\\nFocus: 10min..." \\
        --output_dir manim_lessons/lessons/

From pipeline:
    from opus_lesson_writer import generate_lesson
    py_path, md_path = generate_lesson(course_req, persona, "manim_lessons/lessons/")
"""
import os, re, argparse, pathlib
from anthropic import Anthropic


# ── Scope lock: keep Opus from over-engineering ─────────────────────
SYSTEM_PROMPT = """You are a lesson generator for the manim_lessons competition pipeline.

[HARD SCOPE — violations require restart]
- Output exactly ONE lesson.py and ONE _script.md. Nothing else.
- Do NOT modify any file under lib/ or archetypes/.
- Do NOT create new archetypes. Choose one of:
  GeometryArchetype / StatsArchetype / BiologyArchetype /
  PhysicsArchetype / MethodCompareArchetype / MisconceptionArchetype
- Do NOT refactor, do NOT optimize, do NOT add features I did not request.
- Do NOT change colors or font sizes in design_tokens.
- You MUST set PERSONA = Persona(...) on the lesson class.
  EXACT signature — these are the ONLY kwargs allowed:
      Persona(grade: int,
              focus_minutes: float,
              has: list[str],
              lacks: list[str])
  Do NOT pass jargon_budget, dwell_seconds, speech_chars_per_min, or
  anything else — those are derived automatically.
- ALL output MUST be in English only — zero exceptions.
  Any non-English character (Chinese, Japanese, Arabic, accented letters, etc.)
  in lesson.py or _script.md causes an automatic score deduction on both
  visual and audio axes. This includes comments, docstrings, variable names,
  Text() content, narration lines, and visual cue lines.
- You MUST call self.teach_concept(term, definition, example=...) for every
  concept listed in PERSONA.lacks BEFORE using that term anywhere else.
- The narration script MUST mark a duration for every paragraph and align to
  exactly one scene.
- Every scene's teach() or construct() MUST end with FadeOut of ALL
  Mobjects it added. Use self.play(FadeOut(*self.mobjects), run_time=0.4)
  as the last call before returning. Otherwise content bleeds into the next scene.
- Within any teach() or construct(), before introducing a NEW conceptual
  block (new Text, new diagram), fade out the previous block:
  self.play(FadeOut(prev_block), run_time=0.3)
  Never let two unrelated Text Mobjects coexist on screen.

- NEVER use self.play(FadeOut(*self.mobjects)) directly.
  Instead, track added mobjects explicitly with a VGroup:
    added = VGroup()
    obj = Text(...)
    self.add(obj); added.add(obj)
    self.play(FadeOut(added), run_time=0.4)
  This prevents accidental double-FadeOut of persistent elements.
- To clear the stage at scene end, use `Group(*self.mobjects)` NOT
  `VGroup(*self.mobjects)`. VGroup rejects non-vector Mobjects like
  ValueTrackers or updater-tracked objects, causing render crash.
  Even better: `self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)`

[BANNED MANIM APIs]

- You MUST NOT use `always_redraw(...)` anywhere. It crashes Manim's
align_points routine mid-render whenever the rebuilt mobject's SVG
subpath structure changes between frames (which happens with any text
content tied to a ValueTracker — sign flips, decimal widths, glyph swaps).

- Replacement patterns:

### For geometric mobjects (Line, Dot, Arc, DashedLine, Circle, Polygon, Vector):
```python
# WRONG:
line = always_redraw(lambda: Line(ax.c2p(0,0), pt(theta.get_value()), color=RED))

# RIGHT:
line = Line(ax.c2p(0,0), pt(theta.get_value()), color=RED)  # build once
line.add_updater(lambda m: m.become(
    Line(ax.c2p(0,0), pt(theta.get_value()), color=RED)
))
self.add(line)
```

### For numeric readouts (any number tied to a ValueTracker):
```python
# WRONG:
readout = always_redraw(lambda: MathTex(f"x = {theta.get_value():.2f}"))

# RIGHT:
label = MathTex(r"x = ")                              # static, build once
num = DecimalNumber(0, num_decimal_places=2,
                   include_sign=True)                 # safe live number
num.add_updater(lambda m: m.set_value(theta.get_value()))
readout = VGroup(label, num).arrange(RIGHT, buff=0.1)
self.add(readout)
```

`DecimalNumber.set_value` mutates the digit submobjects in place — it does
not call `.become()`, so align_points is never invoked. `include_sign=True`
keeps the glyph width constant so the number never visually jumps.

### For positioning (move something to track a value, content stays the same):
```python
label = MathTex(r"\theta")                            # static content
label.add_updater(lambda m: m.move_to(
    ax.c2p(0.55*np.cos(theta.get_value()/2),
           0.55*np.sin(theta.get_value()/2))
))
self.add(label)
```

### Animation cleanup:
Before leaving the scene or playing a new big animation, call
`mob.clear_updaters()` on everything that had an updater. This prevents
stale updaters from firing during transitions.

- If a title/header persists across blocks, keep it in a SEPARATE variable
  and never include it in the per-block FadeOut VGroup.

- Before ANY self.play() that introduces new objects, write a comment:
    # CLEARED: [list what was just faded]
  Untracked objects are the #1 cause of ghost elements.

- In the _script.md, NARRATION lines START with "> " (markdown blockquote).
  Visual cue lines start with backtick-bracket like `[...]` and MUST be
  on their own line (no "> " prefix). The pipeline strips non-quote lines
  before TTS — NEVER write narration in a `[...]` line.

If you have ideas beyond the scope — do NOT act on them. Put them in the
lesson docstring as a comment instead.

[BANNED SELF METHODS — these do NOT exist, never call them]
The following method names have been hallucinated in past outputs.
Calling any of them causes an immediate AttributeError crash:

  self.show_comparison_rows(...)
  self.show_table(...)
  self.render_table(...)
  self.comparison_table(...)
  self.build_rows(...)
  self.show_rows(...)
  self.display_comparison(...)

[APPROVED self.* methods — ONLY these are available]
Check the archetype base class. The ONLY helper methods you may call are:
  self.teach_concept(term, definition, example=...)
  self.narrator.say(text)
  self.fade_heading()
  self.intro_bridge()
  self.intro_heading()
  self.outro()

For comparison tables: you MUST build them manually using VGroup + Text/MathTex.
There is no shortcut method. Build it yourself, line by line.

SELF-CHECK before output: grep every `self.xxx(` call in your code.
If `xxx` is not in the approved list above and not defined in the same file,
DELETE it and rewrite using approved primitives.

[FACTUAL SAFETY — contrast by addition, never by denial]
When emphasizing why X is special, NEVER claim "Y lacks the feature."
Y might have a weaker version of that feature, which makes the
denial factually wrong.

WRONG: "The stomach has smooth walls, but the intestine has folds."
       (false — the stomach has rugae)
RIGHT: "The intestine has special finger-like folds called villi that
       multiply its surface area by ~30x more than other organs."

Apply this everywhere — anatomy, physics regimes, ML model types,
historical claims. State the unique strength, do NOT erase the other side.

[SAFE MANIM API — manim 0.19.1]
The execution environment is Manim Community v0.19.1. Follow these
exactly; deviations CRASH the render.

[Forbidden — never emit these]
- arc.get_arc_center()           ← returns None in 0.19.1
- Arc(..., arc_center=X)         ← kwarg removed
- move_to(obj, aligned_edge=X)   ← X often None at runtime
- .scale_to_fit_width(...) on VGroups containing MathTex  (use scale())
- Custom shaders, .set_shader, OpenGL renderer kwargs

[Required patterns for common shapes]
- Arc at a custom center:
    arc = Arc(radius=r, start_angle=0, angle=theta, color=...)
    arc.move_to(center_point)        # NOT arc_center=

- Circle at a custom center:
    Circle(radius=r).move_to(center_point)

- Dot at custom position: Dot(point, color=...)

[Symbol-definition rule]
EVERY name used in code MUST be either:
  (a) imported at top of file, or
  (b) defined as a constant in the same file BEFORE first use.
If a docstring mentions RULE_CLR / EXPERT_CLR / similar, that name MUST
have a `RULE_CLR = "#xxxxxx"` line in code. No orphan symbols.

[**Self-check before output**]
Mentally grep your output for these names: every Mobject class
(Arc, Circle, ...), every color constant, every imported function.
If any is used but not defined or imported, fix the import.

[OPTIMIZATION TARGETS, in priority order]
1. Avoid the fatal -4.0 (Title/Depth Mismatch): teach what the title promises;
   leave no placeholders in output.
2. Push hard on visuals: in the dataset, no submission broke 4.0 on
   adaptability — that axis is your real battlefield.
3. Pair every narration paragraph with a visible visual event
   (visual signaling earns points).
4. Every PERSONA.lacks concept must be introduced via teach_concept() before
   it is used anywhere later.

[FIVE-POINT RECIPE — must trigger ≥4 of these to break 4.0]
1. Beyond-the-definition layer: identify ONE conceptual layer above the
   basic topic and weave it in (e.g., for Energy Conservation: "system
   boundaries"; for Quadratic Vertex: "marginal benefit / turning point").
   Pick something that bridges to an adjacent concept the persona has.

2. Multi-context comparison: present the same concept in 2 contexts
   side-by-side at least once (different domains, different scales, or
   "with assumption X" vs "without X").

3. Address one common misconception explicitly. Format:
   "Many think X. Let's check..." → walk through reasoning → "Actually Y."

4. Closing analytical framework: end NOT with a fact recap, but with a
   3-4 step METHOD the student can apply to future problems of this type.

5. Real-time visual highlighting: every time the narration says a term,
   the visual must highlight (color, box, scale) the matching element
   within 0.3 seconds.

6. Semantic colors: assign one color per concept and keep it for the
   entire lesson. Document the mapping in the lesson docstring.

7. Boxed conclusions: every key result gets a visible box (Rectangle
   stroke around the answer). At least 3 boxed conclusions per lesson.

[SPATIAL LAYOUT RULES — non-negotiable]
1. If your teach() adds anything at top-of-screen (to_edge(UP), shift(UP*n)),
   the FIRST line of teach() MUST be: self.fade_heading()
2. Multiple Texts or MathTexs sharing a region MUST be wrapped in VGroup
   and arranged: VGroup(...).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
3. NEVER use absolute coordinates move_to([x, y, 0]). Use to_edge / to_corner
   / next_to(other_obj, DIRECTION, buff=...) instead.
4. Long equations: append .scale_to_fit_width(config.frame_width - 2)
5. Max 4 distinct visual elements on screen at once. Before adding a 5th,
   FadeOut the oldest.


[FORMULA PACING — non-negotiable for Adaptability]
- NEVER introduce more than ONE new formula per scene.
- Before ANY formula, you MUST show a 2-step conceptual bridge:
  Step 1: "What does this quantity mean physically?" (analogy or diagram)
  Step 2: "Why does it depend on these variables?" (intuition, NOT algebra)
  Only THEN: write the formula.
- Example for a_c = v²/r:
  WRONG: "Centripetal acceleration is a_c = v²/r."
  RIGHT: Scene shows: "Tighter circle → sharper turn → bigger acceleration.
         Faster speed → direction changes quicker → also bigger acceleration.
         So a_c grows with v² and shrinks with r. Formula: a_c = v²/r."
- If persona Grade ≤ 10: each formula scene MUST last ≥ 15 seconds.
- If persona Grade ≤ 10: maximum 2 formulas per minute of runtime.

[TEXT MINIMALISM]
- Max ONE complete sentence of body text on screen at any moment.
- Bullet lists: max 3 items, each ≤ 6 words.
- Headings: ≤ 6 words.
- If you need to say more, narrate it via self.narrator (audio only),
  do NOT add more on-screen Text.
- Replace text with visuals wherever possible: a diagram, an icon,
  a single highlighted formula. Text is the last resort.

[OUTPUT FORMAT — STRICTLY ENFORCED]
- First a ```python code block: the full lesson.py
- Then a ```markdown code block: the full _script.md
- NO text outside these two blocks. No preamble. No closing remarks.
  No "hope this helps". No improvement suggestions.
"""

# ── Scoring playbook (compressed from 16 ensemble + 32 gpt feedback files) ──

PLAYBOOK = """
[SCORING — exact mechanism]
Each dimension: score = clamp(4.0 + bonus - penalties, 0, 5).
Bonus = (# metrics rated +1) / N, capped at +1.0 per dimension.
Shared flags S1-S4 apply to BOTH Accuracy and Logic — fix once, gain twice.

[BONUS DENOMINATORS — these are the ONLY metrics that earn +1]
Accuracy N=5:     S1 Scaffolding, S2 PureCalc, S3 Completeness, S4 Depth, A6 VisualAlign
Logic N=4:        S1, S2, S3, S4
Adaptability N=4: D2 PrereqGap, D3 Pacing, D5 Scaffolding, D6 VisualRep
Engagement N=3:   E7 Audio, E10 V/A Sync, E12 Visual Signaling

D2 PrereqGap: PROACTIVELY bridges gaps — for every formula, ask "can this
  persona derive this intuitively?" If no, add a visual intuition scene
  BEFORE the formula appears. Assume Grade ≤ 10 cannot intuitively accept
  v²/r, F=ma applications, or any chain-rule derivatives without a bridge.
  -0.3 per unbridged formula jump detected.

[+1 EARNING CONDITIONS — "clearly beyond typical for topic and runtime"]
S1: every formula motivated (intuition + analogy + sketch); zero unjustified jumps
S3: content NOTABLY RICHER than the title implies (go beyond stated scope)
S4: depth clearly above typical, SUSTAINED across all covered topics
A6: visuals track spoken argument in real time, anticipate/repair confusion
D2: PROACTIVELY bridges gaps BEYOND what persona's "Has" field requires
D5: scaffolding goes BEYOND minimum, anticipates confusion before it happens
D6: visuals EXCEPTIONALLY illuminate concepts (not merely "no issue")
E10: visuals and narration TIGHTLY synchronized throughout
E12: consistently timed + precise cueing; viewer ALWAYS knows where to look

[HARD CEILING — never trigger]
S2 Pure Calc Bias at -2 or worse → Accuracy AND Logic CAPPED at 2.5.
Keep calculations subordinate to a visible conceptual spine.

[DEVASTATING PENALTIES — avoid above all]
A5 Title-Content Mismatch: 0.5 / 2.0 / 4.0. Level -3 = -4.0 = floor at 1.0.
A7 Critical Fact Error: count × 0.3 each (cap 2.0). Each invented fact = -0.3.
S4 Depth at -3: -2.0. S3 Completeness at -3: -1.5.

[FACTUAL SAFETY — contrast by addition, never by denial]
NEVER claim "Y lacks the feature" to emphasize X. Y likely has a weaker
version, making the denial factually wrong.
  WRONG: "The stomach has smooth walls, but the intestine has folds."
         (false — the stomach has rugae)
  RIGHT: "The intestine has special folds called villi that multiply
         surface area ~30x more than other organs."

[NO-+1 METRICS — don't waste effort trying to "excel" here]
A5, A7, A8, L9, L10, D1 Jargon, D4 Illegible Text,
E8 AI Fatigue, E9 Clutter, E11 Decorative Eye-Candy
These can only hurt. Just avoid penalties — no excellence achievable.

[REALISTIC CEILING]
Theoretical max: 5/5/5/5 (every +1-eligible metric earns +1).
Observed exemplar (Energy Conservation): 5/5/4.5/4.67 — Adaptability and
Engagement are harder to push to 5 because they require subjective "beyond
typical" calls from Agent 3 watching the raw video.
"""

PLAYBOOK_old = """
[FOUR-AXIS SCORING FORMULA — reverse-engineered from score_breakdown fields]
acc = 4.0 - Title/Depth_Mismatch[-4.0 FATAL] - Scaffolding[-1.5]
       - Completeness[-1.5] - Depth[-2.0] - VisualAlignment[-1.0]
       - Critical[-0.3 each] + consistency_bonus 0.2
       - Any non-English character anywhere in output → -1.0 per axis (visual + audio)
log = 4.0 - Scaffolding - Completeness - Depth
       - Causal_Inconsistency[-0.4 each]
adp = 4.0 - Jargon_Overload - Prerequisite_Gap - Pacing_Mismatch
       - Missing_Scaffolding - Ineffective_Visual[-0.3 to -1.0]
       (any plain-text-only slide hits Ineffective_Visual)
eng = 4.0 - Monotone_Audio[-0.8] - AI_Generated_Fatigue[-1.0]
       - Visual_Audio_Disconnect - Visual_Signaling[-0.6]

[FATAL PATTERNS — never produce]
- Meta-only slides: "Define X", "Explain Y", "Here we will" → acc collapses to 1.0
- Leftover placeholders: {{, [INSERT, TODO, Defi, Bloo, "physical sist"
  → -0.3 per occurrence (counts every one)
- Numbers on slide differ from numbers in narration → -1.0
- Plain-text slides for >50% of runtime → adp -1.0

[PERSONA THRESHOLDS — derived from 32 gpt_feedback files where "rushed" was flagged]
- Grade 8 : >=22s per Lacks concept, jargon budget 3
- Grade 9 : >=20s per Lacks concept, jargon budget 4
- Grade 10: >=16s per Lacks concept, jargon budget 5
- Grade 11: >=13s per Lacks concept, jargon budget 6
- Grade 12: >=11s per Lacks concept, jargon budget 7
- College : >=10s per Lacks concept, jargon budget 8

[WHEN TO USE MisconceptionArchetype]
- Topic mentions overfitting / underfitting
- Any "approaching != reaching" style concept (limits, asymptotes, convergence)
- course_requirement explicitly asks to "address misconception" or
  "correct intuition" before introducing the formal concept
"""

LAYER_PATTERN = """
[MANDATORY LAYER PATTERN — copy this pattern exactly in every scene block]
```python
# ── Correct pattern ──────────────────────────────────────
block1 = VGroup(Text("A"), Text("B").shift(DOWN))
self.play(FadeIn(block1))
self.wait(1.5)

self.play(FadeOut(block1), run_time=0.3)  # CLEARED: block1

block2 = VGroup(...)
self.play(FadeIn(block2))
self.wait(1.5)

self.play(FadeOut(block2), run_time=0.4)  # scene end
```
"""

USER_TEMPLATE = """Before anything else: read the student_persona's Grade carefully.
Word choice MUST match — Grade 8 uses everyday words; Grade 12 may use technical terms.
If you would not say a word in front of that grade level, do not write it.

Below is the topic and a reference lesson. Produce one lesson.py
and one _script.md, fully imitating the reference's structure and style.

[TOPIC]
course_requirement:
{course_req}

student_persona:
{persona}

[SCORING RULES]
{playbook}

[MANDATORY LAYER PATTERN — copy this in every scene block]
```python
block1 = VGroup(Text("A"), Text("B").shift(DOWN))
self.play(FadeIn(block1))
self.wait(1.5)
self.play(FadeOut(block1), run_time=0.3)  # CLEARED: block1

block2 = VGroup(...)
self.play(FadeIn(block2))
self.wait(1.5)
self.play(FadeOut(block2), run_time=0.4)  # scene end
```

[MANDATORY PACING STRUCTURE for Grade ≤ 10]
If student_persona Grade ≤ 10, the formula section MUST follow this structure:
  Scene N:   Intuition + analogy (no formula yet)        ≥ 12s
  Scene N+1: One formula introduced with visual proof    ≥ 15s  
  Scene N+2: Next formula (never two in the same scene)  ≥ 15s

Forbidden: introducing ω, T, f, v=rω, a_c=v²/r all in the same scene.
Each gets its OWN scene with its OWN intuition build-up.

[CORRECT PATTERN for comparison tables — copy verbatim]
```python
# MethodCompareArchetype: build comparison manually, NO helper methods
headers = VGroup(
    Text("Memory-Based", color=BLUE, font_size=28),
    Text("Feature-Based", color=GREEN, font_size=28),
).arrange(RIGHT, buff=2.0)

row1 = VGroup(
    Text("stores raw data", font_size=24),
    Text("learns patterns", font_size=24),
).arrange(RIGHT, buff=2.5)

table = VGroup(headers, row1).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
self.play(FadeIn(table))
self.wait(2.0)
self.play(FadeOut(table), run_time=0.4)
```

[REFERENCE — imitate this structure exactly]
```python
{reference}
```

Begin now. Two code blocks only. No prose before or after."""


# ── Main ────────────────────────────────────────────────────────
def load_reference(reference_path: str = None) -> str:
    """Default reference: triangle_centers.py. It is the most complete example,
    covering all six scene patterns (Hook / TeachConcept / Compare / Apply /
    Decision / Recap)."""
    if reference_path is None:
        here = pathlib.Path(__file__).resolve().parent.parent
        for cand in [here / "manim_lessons/lessons/triangle_centers.py",
                      here / "lessons/triangle_centers.py"]:
            if cand.exists():
                return cand.read_text(encoding="utf-8")
        raise FileNotFoundError(
            "Could not find triangle_centers.py. Pass --reference PATH explicitly."
        )
    return pathlib.Path(reference_path).read_text(encoding="utf-8")


def generate_lesson(course_req: str, persona: str,
                    output_dir: str = "manim_lessons/lessons",
                    reference_path: str = None,
                    model: str = "claude-opus-4-7",
                    max_tokens: int = 32000) -> tuple[str, str]:
    """Produce lesson.py + _script.md inside output_dir.
    Returns (py_path, md_path)."""
    client = Anthropic()
    reference = load_reference(reference_path)

    #resp_12000 = client.messages.create(
    #    model=model,
    #    max_tokens=max_tokens,
    #    system=SYSTEM_PROMPT,
    #    messages=[{
    #        "role": "user",
    #        "content": USER_TEMPLATE.format(
    #            course_req=course_req,
    #            persona=persona,
    #            playbook=PLAYBOOK,
    #            reference=reference,
    #        ),
    #    }],
    #)
    #text_12000 = "".join(b.text for b in resp.content if hasattr(b, "text"))

    text_parts = []
    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": USER_TEMPLATE.format(
                course_req=course_req,
                persona=persona,
                playbook=PLAYBOOK,
                reference=reference,
            ),
        }],
    ) as stream:
        for chunk in stream.text_stream:
            text_parts.append(chunk)
        final = stream.get_final_message()

    text = "".join(text_parts)
   

    # ── Parse the two code blocks ──────────────────────────────
    py_match = re.search(r"```python\s*\n(.*?)\n```", text, re.DOTALL)
    md_match = re.search(r"```markdown\s*\n(.*?)\n```", text, re.DOTALL)
    if not (py_match and md_match):
        debug_path = pathlib.Path(output_dir) / "_last_opus_failure.txt"
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        debug_path.write_text(text, encoding="utf-8")
        raise ValueError(
            f"Opus did not return two valid code blocks. First 1500 chars:\n{text[:1500]}"
        )

    py_code = py_match.group(1)
    md_text = md_match.group(1)

    # ── Derive filename from the docstring's Topic line ────────
    topic_match = re.search(r"Topic:\s*(.+)", py_code)
    slug = (re.sub(r"\W+", "_", topic_match.group(1).lower())[:50]
            if topic_match else "lesson")

    # ── Write files ────────────────────────────────────────────
    out = pathlib.Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    py_path = out / f"{slug}.py"
    md_path = out / f"{slug}_script.md"
    py_path.write_text(py_code, encoding="utf-8")
    md_path.write_text(md_text, encoding="utf-8")

    print(f"✓ wrote {py_path}")
    print(f"✓ wrote {md_path}")
    print(f"  ↳ tokens: in={final.usage.input_tokens}, out={final.usage.output_tokens}")
    #print(f"  ↳ tokens: in={resp.usage.input_tokens}, out={resp.usage.output_tokens}")
    return str(py_path), str(md_path)


# ════════════════════════════════════════════════════════════════════
#  SANITIZE LAYER — regex-patch known Opus footguns
# ════════════════════════════════════════════════════════════════════
 
def sanitize_lesson_code(py_path: str) -> list[str]:
    """
    Patch known Opus mistakes BEFORE render. Returns list of applied fixes.
    Items starting with '⚠' are unfixable and should trigger regeneration.
    """
    text = open(py_path, encoding="utf-8").read()
    fixes = []
 
    # 1. VGroup → Group for stage clear
    if "VGroup(*self.mobjects)" in text:
        text = text.replace("VGroup(*self.mobjects)", "Group(*self.mobjects)")
        fixes.append("VGroup→Group for stage clear")
 
    # 2. Invented Persona kwargs
    n = len(text)
    text = re.sub(r",\s*jargon_budget\s*=\s*\d+", "", text)
    text = re.sub(r",\s*speech_chars_per_min\s*=\s*\d+", "", text)
    text = re.sub(r",\s*focus_time_min\s*=\s*\d+", "", text)
    if len(text) != n:
        fixes.append("removed invented Persona kwargs")
 
    # 3. always_redraw with text class → Manim crash
    REDRAW_TEXT_PAT = re.compile(
        r"always_redraw\s*\(\s*lambda[^:]*:\s*[^)]*?"
        r"\b(MathTex|Tex|Text|MarkupText|Title|Integer|Variable)\b",
        re.DOTALL,
    )
    if REDRAW_TEXT_PAT.search(text):
        fixes.append("⚠ always_redraw with text class found")
 
    # 4. .become(MathTex/Text(...)) inside updater
    if re.search(r"\.become\s*\(\s*(MathTex|Tex|Text|MarkupText)\s*\(", text):
        fixes.append("⚠ .become(Text/MathTex) found in updater")
 
    # 5. Stacked Write/FadeIn without FadeOut (the villi bug)
    for match in re.finditer(r"for\s+\w+[^\n]*in[^\n]*:\s*\n((?:\s{4,}.*\n)+)", text):
        block = match.group(1)
        writes = len(re.findall(r"\b(Write|FadeIn)\s*\(", block))
        clears = len(re.findall(
            r"\b(FadeOut|Transform|ReplacementTransform|remove)\s*\(", block))
        if writes >= 2 and clears == 0:
            fixes.append(
                f"⚠ stack-bug: for-loop has {writes} Writes, 0 clears (villi pattern)"
            )
 
    # 6. Ensure Group import if used
    if re.search(r"\bGroup\s*\(", text) and not re.search(r"from manim import[^\n]*\bGroup\b", text):
        text = re.sub(
            r"(from manim import\s*\(?)",
            r"\1Group, ",
            text,
            count=1,
        )
        fixes.append("added Group import")
 
    # 7. Placeholder detector
    BANNED = [
        r"Define the central", r"central term",
        r"\{\{", r"\}\}", r"\[INSERT", r"\bTODO\b",
        r"Here we will", r"I will explain",
        r"physical sist", r"\bBloo\b", r"\bDefi\b(?!ne)", r"\bComp\b(?!are|ute|lete|onent|onsole)",
    ]
    for pat in BANNED:
        if re.search(pat, text):
            fixes.append(f"⚠ placeholder: {pat}")
 
    open(py_path, "w", encoding="utf-8").write(text)
    return fixes
 

# ════════════════════════════════════════════════════════════════════
#  RETRY WRAPPER — generate → sanitize → validate → probe-render
# ════════════════════════════════════════════════════════════════════
 

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--course_req", required=True)
    ap.add_argument("--persona", required=True)
    ap.add_argument("--output_dir", default="manim_lessons/lessons")
    ap.add_argument("--reference", default=None,
                    help="Custom reference path. Defaults to triangle_centers.py")
    ap.add_argument("--model", default="claude-opus-4-7")
    ap.add_argument("--max_tokens", type=int, default=12000)
    args = ap.parse_args()

    generate_lesson(
        course_req=args.course_req,
        persona=args.persona,
        output_dir=args.output_dir,
        reference_path=args.reference,
        model=args.model,
        max_tokens=args.max_tokens,
    )
