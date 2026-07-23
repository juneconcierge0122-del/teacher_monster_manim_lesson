"""
opus_lesson_writer.py  (v3 — integrated, with deduction-to-bonus flip)
=======================================================================

Drop-in lesson generator. Three layers of defense + scoring-flip prompting:

  1. Streaming generate (32k max_tokens requires streaming)
  2. Sanitize layer  — regex-patch known Opus footguns BEFORE rendering
  3. Validate layer  — AST parse + import dry-run BEFORE rendering
  4. Retry on probe-render failure (cheaper than debugging dead videos)

The PROMPT explicitly trains Opus to AVOID deduction triggers AND
ACTIVELY HIT bonus triggers (each level=1 flag = +0.2 to that axis).

CLI:
    export ANTHROPIC_API_KEY=...
    python opus_lesson_writer.py \\
        --course_req "Big Concept: ...\\nTopic: ..." \\
        --persona   "Grade: 8th\\nFocus: 10min..." \\
        --output_dir manim_lessons/lessons/

From pipeline (T2V_pipeline.py):
    from opus_lesson_writer import generate_lesson_with_retry
    py_path, md_path = generate_lesson_with_retry(
        course_req, persona,
        output_dir=os.path.join(job_tmp, "lessons"),
        probe_scene="S01_Hook",
        max_retries=2,
    )
"""

import os
import re
import ast
import argparse
import importlib.util
import pathlib
import subprocess
import tempfile
from anthropic import Anthropic


# ════════════════════════════════════════════════════════════════════
#  SYSTEM PROMPT
# ════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """You are a lesson generator for the manim_lessons competition pipeline.

[HARD SCOPE — violations require restart]
- Output exactly ONE lesson.py and ONE _script.md. Nothing else.
- Do NOT modify any file under lib/ or archetypes/.
- Do NOT create new archetypes. Choose one of:
  GeometryArchetype / StatsArchetype / BiologyArchetype /
  PhysicsArchetype / MethodCompareArchetype / MisconceptionArchetype
- Do NOT refactor, do NOT optimize, do NOT add features I did not request.
- You MUST set PERSONA = Persona(grade=..., focus_minutes=..., has=[...], lacks=[...])
  on the lesson class. Example:
      PERSONA = Persona(
          grade=7,
          focus_minutes=20,
          has=["..."],
          lacks=["..."],
      )
  Required: grade (int), focus_minutes (int). Optional: has, lacks (lists).
  Do NOT invent other kwargs.
- You MUST call self.teach_concept(term, definition, example=...) for every
  concept listed in PERSONA.lacks BEFORE using that term anywhere else.

If you have ideas beyond scope, put them in the lesson docstring as a comment.

[OUTPUT FORMAT — STRICTLY ENFORCED]
- First a ```python code block: the full lesson.py
- Then a ```markdown code block: the full _script.md
- script.md MUST use this exact format:
    ## Scene N
    > narration line 1
    > narration line 2

  Use "## Scene 1", "## Scene 2"... (NOT "## S01", NOT "Scene 1 — title").
  All narration MUST start with "> " on its own line.
- NO text outside these two blocks. No preamble. No "hope this helps".
"""


# ════════════════════════════════════════════════════════════════════
#  PLAYBOOK — the scoring contract, with FLIP strategy baked in
# ════════════════════════════════════════════════════════════════════

PLAYBOOK = """
[SCORING RULES — REVERSE-ENGINEERED FROM 30 EVALUATIONS]

The rubric is POSITIVE-CODED, not negative-coded.
  - Base score for every axis = 4.0
  - Each rubric "level=1" flag triggered = +0.2 on its axis
  - Deductions ("-0.3", "-0.5") only fire on visible failure modes
  - Therefore the FASTEST way to gain points is to TRIGGER MORE +1 FLAGS,
    not just to "avoid mistakes"

Empirical correlations (high-score >= 4.5 vs low-score < 4.2):
  +100% delta  eng.disconnect_level=1
    → trigger by making narration and visual EVENTS aligned to the same beat
  +88%  delta  ped.scaffolding_failure_level=1
    → trigger by stating the motivation BEFORE introducing each new concept
  +75%  delta  adp.ineffective_visual_representation_level=1
    → trigger by using shape/diagram/animation rather than text-on-screen
  +62%  delta  acc.visual_alignment_issue_level=1
    → trigger by making EVERY on-screen element update WITH the narration
  +38%  delta  comp.explanatory_depth_level=1
    → trigger by addressing one common misconception explicitly
  +25%  delta  eng.visual_signaling_level=1
    → trigger by using color-boxing, progressive reveal, attention arrows

[FLIP STRATEGY — convert every potential deduction into a bonus]

For each axis: avoid the deduction trigger AND actively hit the bonus trigger.

ACCURACY
  AVOID:
    - On-screen text not matching narration (Visual Alignment Issue -0.5~1.0)
    - Wrong numbers on slides vs script (Critical Error -0.3 each)
    - Placeholder strings ("Define the central", "{{ }}", truncated words)
  HIT THE BONUS (+0.2 each):
    - Each on-screen label appears EXACTLY when narration mentions it
    - Numbers shown match script verbatim (run grep to verify)
    - For every key term, on-screen label + spoken word + diagram element
      all appear within 0.5s of each other

LOGIC
  AVOID:
    - Concept B used before A is introduced (Causal Inconsistency -0.4 each)
    - Missing prerequisite step (Scaffolding Failure -1.0~1.5)
  HIT THE BONUS (+0.2 each):
    - Open each scene with "We know X, so now Y" bridging language
    - End each scene with a one-sentence recap connecting back to motivation
    - Treat each new term as: motivation → definition → example → use case

ADAPTABILITY  (the historical ceiling — your real battlefield)
  AVOID:
    - Pure-text slides (Ineffective Visual Representation -0.3~1.0)
    - Jargon used before defined (Jargon Overload -0.3~0.6)
    - Stacking multiple example texts on the same screen position!
      (the "villi bug" — failing to FadeOut before adding next example)
  HIT THE BONUS (+0.2 each):
    - Each abstract concept gets a concrete visual anchor
      (e.g., 1000 dots for confusion matrix, profit curve for vertex)
    - Persona.has → persona.lacks bridging line in opening 15s
    - When swapping example text on a slide, use ReplacementTransform NEVER
      Write-on-top-of-old (this is the most common Opus mistake)

ENGAGEMENT
  AVOID:
    - Robotic TTS / monotone narration (Monotone Audio -0.4~0.8)
    - Visual happening without matching narration (Disconnect -0.3~1.0)
  HIT THE BONUS (+0.2 each):
    - Pre-announce each visual event: "Now we'll see X..." THEN play animation
    - Use color-boxing/progressive reveal to direct attention
    - End each scene with a 0.5s beat of stillness for concepts to land

[GOLD-STANDARD PATTERNS — DIRECTLY OBSERVED IN 4.68-AVG LESSONS]

The highest-scoring lessons all share three patterns. Use them, period.

PATTERN A — Density gate (max 1 new variable/formula per 15s of runtime)
  Every new symbol (ω, T, f, v=rω, a=v²/r, etc.) costs the student attention.
  RULE: after introducing a formula, insert >=3 seconds of "why this form?"
  before introducing the next. Code:

      self.narrator.say("We just saw angular velocity, omega.", 2.5)
      self.play(Indicate(omega_formula))
      self.narrator.silent(BEAT_L)  # let it land
      self.narrator.say("So how fast is the tip moving? It depends on the radius...", 3.0)
      self.play(Write(v_formula))   # NOW introduce v=r*omega

  If you find yourself writing >=3 formulas inside a 20s window — STOP and
  rewrite the scene with intermediate "why" beats. This is the #1 cause of
  Pacing Mismatch and Prerequisite Gap deductions in physics/math topics.

PATTERN B — Bridge mode (use persona.has as a stepping stone)
  Do NOT teach persona.lacks concepts from scratch. Find the closest
  persona.has concept and explain the new one as a CONTRAST or EXTENSION.
  This is how the 4.68-avg "Neural Networks" lesson scored — it taught NN
  by first explaining KNN (which the student already understood), then
  contrasting: "KNN remembers examples; NN invents features."

  In your lesson, BEFORE any new concept, ask yourself: "What in persona.has
  is closest to this?" Then write:

      "You already know A [from persona.has]. B is like A, except ____."

  This single pattern alone reliably triggers BOTH ped.scaffolding_failure=1
  (+0.2 acc) AND adp.missing_scaffolding=1 (+0.2 adp). Worth ~+0.4 to total.

PATTERN C — Pre-announce, play, settle (the "tight sync" pattern)
  This is the ONLY reliable way to trigger eng.disconnect_level=1 (+0.2).
  For every visual event, narration leads by 0.5-1.0s:

      # ❌ WRONG — narration and animation start together → no bonus
      self.play(Write(formula), self.narrator.say("Here is the formula", 1.5))

      # ✅ RIGHT — narration leads, animation reveals, beat settles
      self.narrator.say("Now look at the formula.", 1.0)
      self.play(Write(formula), run_time=1.5)
      self.narrator.silent(0.5)  # settle beat

  The agent literally checks for this temporal offset. No offset = no bonus,
  even if your visuals are otherwise gorgeous.

[ZERO-FAULT REQUIREMENTS — fatal if violated]

1. NEVER use `Write()` or `FadeIn()` on an example/text mobject without
   FIRST FadeOut-ing the previous one in the same screen position.
   When showing a sequence of examples, use this pattern:

       example_holder = Text("", font_size=28).to_edge(DOWN)
       self.add(example_holder)
       for term, defn, eg in vocab_list:
           new_eg = Text(f"e.g. {eg}", font_size=28).to_edge(DOWN)
           self.play(ReplacementTransform(example_holder, new_eg))
           example_holder = new_eg

2. NEVER use `always_redraw(lambda: MathTex(...))` or
   `always_redraw(lambda: Text(...))` — this crashes Manim on ValueTracker
   changes because subpath counts differ between frames.
   Use DecimalNumber with add_updater instead:

       x_val = DecimalNumber(0, num_decimal_places=2)
       x_val.add_updater(lambda m: m.set_value(np.cos(theta.get_value())))

3. NEVER use `VGroup(*self.mobjects)` to clear stage — VGroup rejects
   non-VMobject items. Use `Group(*self.mobjects)` or explicit FadeOut.

4. NEVER leave placeholders: forbidden strings are
   "Define the central", "central term", "{{", "}}", "[INSERT", "TODO",
   "Here we will", "I will explain", "physical sist", "Bloo", "Defi ", "Comp "

5. On-screen numbers MUST equal script numbers. Run mental grep before output.
6. THE STACKING-TEXT BUG (villi pattern) — FATAL if violated.
   When you have a sequence of definitions/examples that occupy the SAME
   screen region across iterations (e.g. a vocabulary walkthrough where
   each term's example appears at the same bottom-edge position),
   you MUST FadeOut or ReplacementTransform the previous one before
   showing the next. Otherwise they stack into unreadable garbage.

   ❌ FATAL — produces stacked overlapping text:
       for term, defn, eg in vocab_list:
           title = Text(term).to_edge(UP)
           defn_t = Text(defn)
           eg_t = Text(f"e.g. {eg}").to_edge(DOWN)
           self.play(Write(title), Write(defn_t), Write(eg_t))
           self.wait(3)

   ✅ CORRECT — explicit cleanup each iteration:
       for term, defn, eg in vocab_list:
           title = Text(term).to_edge(UP)
           defn_t = Text(defn)
           eg_t = Text(f"e.g. {eg}").to_edge(DOWN)
           self.play(Write(title), Write(defn_t), Write(eg_t))
           self.wait(3)
           self.play(FadeOut(title), FadeOut(defn_t), FadeOut(eg_t))

   ✅ ALSO CORRECT — multi-row layout where items coexist permanently:
       (decision tables, comparison charts — items go to DIFFERENT positions
       via arrange(DOWN) or absolute coords, so no cleanup needed)

   RULE: if iteration N's mobject lands on the same screen region as
   iteration N-1's, you MUST clear N-1 first.
"""


# ════════════════════════════════════════════════════════════════════
#  USER TEMPLATE
# ════════════════════════════════════════════════════════════════════

USER_TEMPLATE = """Produce one lesson.py and one _script.md, fully imitating the reference's
structure and style.

[TOPIC]
course_requirement:
{course_req}

student_persona:
{persona}

[SCORING RULES]
{playbook}

[REFERENCE — imitate this structure exactly]
```python
{reference}
```

Begin now. Two code blocks only. No prose before or after."""


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
    #for match in re.finditer(
    #    r"for\s+\w+[^\n]*in[^\n]*:\s*\n((?:\s{4,}.*\n)+)", text
    #):
    #    block = match.group(1)
    #    creates_text = bool(re.search(
    #        r"=\s*(Text|MathTex|Tex|MarkupText|Paragraph)\s*\(", block
    #    ))
    #    writes = len(re.findall(r"\b(Write|FadeIn)\s*\(", block))
    #    clears = len(re.findall(
    #        r"\b(FadeOut|Transform|ReplacementTransform|self\.clear)\s*\(",
    #        block,
    #    ))
    #    # 同時滿足三條件才算: (a) 迴圈內新建 Text (b) 有 Write (c) 0 clears
    #    if creates_text and writes >= 1 and clears == 0:
    #        fixes.append(
    #            f"⚠ stack-bug: loop creates Text + writes ({writes}) without any clear"
    #        )


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
        r"\[INSERT", r"\bTODO\b",
        r"Here we will", r"I will explain",
        r"physical sist", r"\bBloo\b", r"\bDefi\b(?!ne)", r"\bComp\b(?!are|ute|lete|onent|onsole)",
    ]
    for pat in BANNED:
        if re.search(pat, text):
            fixes.append(f"⚠ placeholder: {pat}")

    open(py_path, "w", encoding="utf-8").write(text)
    return fixes


# ════════════════════════════════════════════════════════════════════
#  VALIDATE LAYER — AST parse + import dry-run
# ════════════════════════════════════════════════════════════════════

def validate_lesson(py_path: str) -> None:
    """Cheap pre-render checks. Raises RuntimeError on failure."""
    text = open(py_path, encoding="utf-8").read()

    try:
        ast.parse(text)
    except SyntaxError as e:
        raise RuntimeError(f"Lesson syntax error: {e.lineno}:{e.offset}: {e.msg}")

    spec = importlib.util.spec_from_file_location("lesson_check", py_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot create import spec for {py_path}")
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        raise RuntimeError(f"Lesson import failed: {type(e).__name__}: {e}")


# ════════════════════════════════════════════════════════════════════
#  GENERATE — streaming Opus call
# ════════════════════════════════════════════════════════════════════

def load_reference(reference_path: str = None) -> str:
    """Default reference: triangle_centers.py."""
    if reference_path is None:
        here = pathlib.Path(__file__).resolve().parent
        for cand in [
            here / "manim_lessons/lessons/triangle_centers.py",
            here / "lessons/triangle_centers.py",
            here / "02_triangle_centers.py",
        ]:
            if cand.exists():
                return cand.read_text(encoding="utf-8")
        raise FileNotFoundError(
            "Could not find triangle_centers.py. Pass --reference PATH."
        )
    return pathlib.Path(reference_path).read_text(encoding="utf-8")


def generate_lesson(
    course_req: str,
    persona: str,
    output_dir: str = "manim_lessons/lessons",
    reference_path: str = None,
    model: str = "claude-opus-4-7",
    #model: str = "claude-sonnet-4-6",
    max_tokens: int = 32000,
) -> tuple[str, str]:
    """Produce lesson.py + _script.md. Does NOT sanitize/validate."""
    client = Anthropic()
    reference = load_reference(reference_path)

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

    py_match = re.search(r"```python\s*\n(.*?)\n```", text, re.DOTALL)
    md_match = re.search(r"```markdown\s*\n(.*?)\n```", text, re.DOTALL)
    if not (py_match and md_match):
        debug_path = pathlib.Path(output_dir) / "_opus_raw_dump.txt"
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        debug_path.write_text(text, encoding="utf-8")
        raise ValueError(
            f"Opus did not return two valid code blocks. "
            f"Dumped to {debug_path}. First 1500 chars:\n{text[:1500]}"
        )

    py_code = py_match.group(1)
    md_text = md_match.group(1)

    topic_match = re.search(r"Topic:\s*(.+)", py_code)
    slug = (
        re.sub(r"\W+", "_", topic_match.group(1).lower())[:50]
        if topic_match
        else "lesson"
    )

    out = pathlib.Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    py_path = out / f"{slug}.py"
    md_path = out / f"{slug}_script.md"
    py_path.write_text(py_code, encoding="utf-8")
    md_path.write_text(md_text, encoding="utf-8")

    print(f"✓ wrote {py_path}")
    print(f"✓ wrote {md_path}")
    print(f"  ↳ tokens: in={final.usage.input_tokens}, out={final.usage.output_tokens}")
    return str(py_path), str(md_path)


# ════════════════════════════════════════════════════════════════════
#  RETRY WRAPPER — generate → sanitize → validate → probe-render
# ════════════════════════════════════════════════════════════════════

def generate_lesson_with_retry(
    course_req: str,
    persona: str,
    output_dir: str = "manim_lessons/lessons",
    reference_path: str = None,
    model: str = "claude-opus-4-7",
    max_tokens: int = 32000,
    max_retries: int = 2,
    probe_scene: str = None,    # None = auto-detect first S\d{2}_ class
    probe_timeout: int = 120,
) -> tuple[str, str]:
    """Full pipeline. Returns (py_path, md_path). Raises if exhausted."""
    last_err = None
    for attempt in range(max_retries + 1):
        try:
            print(f"\n── Attempt {attempt + 1}/{max_retries + 1} ──")
            py_path, md_path = generate_lesson(
                course_req, persona, output_dir, reference_path, model, max_tokens,
            )

            fixes = sanitize_lesson_code(py_path)
            for f in fixes:
                print(f"  sanitize: {f}")
            if any(f.startswith("⚠") for f in fixes):
                raise RuntimeError(
                    f"Sanitize raised unfixable issues: "
                    f"{[f for f in fixes if f.startswith('⚠')]}"
                )

            validate_lesson(py_path)
            print("  validate: ✓ AST + import OK")

            # Auto-detect probe scene if not specified
            if probe_scene is None:
                py_text = open(py_path, encoding="utf-8").read()
                matches = re.findall(r"^class\s+(S\d{2}_\w+)\s*\(", py_text, re.MULTILINE)
                if not matches:
                    raise RuntimeError("No S\\d{2}_ scene class found in lesson.py")
                actual_probe = matches[0]
            else:
                actual_probe = probe_scene

            with tempfile.TemporaryDirectory() as probe_dir:
                result = subprocess.run(
                    ["manim", "-ql", py_path, actual_probe, "--media_dir", probe_dir],
                    capture_output=True,
                    timeout=probe_timeout,
                )
                if result.returncode != 0:
                    err = result.stderr.decode("utf-8", errors="replace")[-2000:]
                    raise RuntimeError(f"Probe render failed:\n{err}")
            print(f"  probe-render: ✓ {actual_probe}")

            return py_path, md_path

        except Exception as e:
            last_err = e
            print(f"  ✗ attempt {attempt + 1}: {type(e).__name__}: {str(e)[:300]}")
            if attempt < max_retries:
                print("  → regenerating...")

    raise RuntimeError(
        f"All {max_retries + 1} attempts exhausted. Last error: {last_err}"
    )


# ════════════════════════════════════════════════════════════════════
#  CLI
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--course_req", required=True)
    ap.add_argument("--persona", required=True)
    ap.add_argument("--output_dir", default="manim_lessons/lessons")
    ap.add_argument("--reference", default=None)
    ap.add_argument("--model", default="claude-opus-4-7")
    ap.add_argument("--max_tokens", type=int, default=32000)
    ap.add_argument("--max_retries", type=int, default=2)
    ap.add_argument("--no_probe", action="store_true")
    ap.add_argument("--probe_scene", default="S01_Hook")
    args = ap.parse_args()

    if args.no_probe:
        py, md = generate_lesson(
            args.course_req, args.persona, args.output_dir,
            args.reference, args.model, args.max_tokens,
        )
        sanitize_lesson_code(py)
        validate_lesson(py)
    else:
        generate_lesson_with_retry(
            args.course_req, args.persona, args.output_dir,
            args.reference, args.model, args.max_tokens,
            max_retries=args.max_retries,
            probe_scene=args.probe_scene,
        )
