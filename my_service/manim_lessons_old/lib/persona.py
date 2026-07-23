"""
Persona
=======
把 student_persona 從「裝飾性字串」變成「runtime 強制機制」.

從 32 份 gpt_feedback 提煉出 3 條規則:
  1. 每個 Lacks 概念有最低 dwell time (依 grade 反比於資訊密度承受度)
  2. Lacks 概念必須先 define 才能用 (透過 teach_concept 自動登記)
  3. Jargon 數量上限 (依 grade 線性), 用超就 abort

Usage:
    from manim_lessons.lib.persona import Persona

    PERSONA = Persona(
        grade=9, focus_minutes=15,
        has=["basic geometry", "triangle", "distance"],
        lacks=["incenter", "circumcenter", "optimization"],
    )
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Persona:
    grade: int                           # 9 ~ 12
    focus_minutes: float                 # 從 student_persona["Focus Time"] 抓
    has: List[str] = field(default_factory=list)
    lacks: List[str] = field(default_factory=list)

    # ── 衍生預算 ───────────────────────────────────────────────────────
    #@property
    #def seconds_per_lacks_concept(self) -> float:
    #    """
    #    每個 Lacks 概念的最低 dwell time. 依 grade 給固定值,
    #    而非用 focus_minutes 除 — 因為 focus_minutes 是學生注意力上限,
    #    不是影片長度. 從 gpt_feedback 觀察: 9 年級 < 15s 就會被判 rushed.
    #    """
    #    return {9: 20.0, 10: 16.0, 11: 13.0, 12: 11.0}.get(self.grade, 15.0)
    @property
    def seconds_per_lacks_concept(self) -> float:
        return {6:25, 7:22, 8:22, 9:20, 10:16, 11:13, 12:11, 13:10, 14:9}.get(self.grade, 15.0)

    @property
    def lesson_target_minutes(self) -> float:
        """建議的影片長度. 約 focus 上限的 1/3, 留時間給應用練習."""
        return self.focus_minutes / 3

    #@property
    #def jargon_budget(self) -> int:
    #    """整支影片可引入的「persona 不熟」術語數上限. 超過 = jargon overload."""
    #    return max(3, self.grade - 5)         # 9→4, 10→5, 11→6, 12→7
    @property
    def jargon_budget(self) -> int:
        return max(3, self.grade-5)


    #@property
    #def speech_chars_per_min(self) -> int:
    #    """旁白語速建議. 中文字符/分."""
    #    return {9: 110, 10: 125, 11: 140, 12: 155}.get(self.grade, 125)

    @property
    def speech_chars_per_min(self) -> int:
        return {6:95, 7:100, 8:105, 9:110, 10:125, 11:140, 12: 155, 13:165, 14:175}.get(self.grade, 125)


    # ── 判斷 ────────────────────────────────────────────────────────
    def is_known(self, term: str) -> bool:
        """這個術語對 persona 來說已知嗎?"""
        t = term.lower()
        return any(h.lower() in t or t in h.lower() for h in self.has)

    def summary(self) -> str:
        return (f"Grade {self.grade}, {self.focus_minutes}min focus "
                f"(target lesson ≈{self.lesson_target_minutes:.1f}min) | "
                f"{len(self.has)} known, {len(self.lacks)} gaps | "
                f"≥{self.seconds_per_lacks_concept:.0f}s/concept | "
                f"jargon budget={self.jargon_budget}")


class PersonaTracker:
    """
    Runtime 防呆. 在 Scene 裡追蹤:
      - 哪些 Lacks 概念已透過 teach_concept() 引入
      - 引入了多少 jargon
      - 每個概念的累積 dwell 是否達標
    """

    def __init__(self, persona: Persona):
        self.persona = persona
        self._defined = set(h.lower() for h in persona.has)
        self._concept_dwell = {}            # {term_lower: seconds}
        self._jargon_used = set()
        self._violations = []

    def register_definition(self, term: str):
        """teach_concept() 呼叫. 標記這個 term 被正式引入."""
        t = term.lower()
        self._defined.add(t)
        if not self.persona.is_known(term):
            self._jargon_used.add(t)

    def add_dwell(self, term: str, seconds: float):
        t = term.lower()
        self._concept_dwell[t] = self._concept_dwell.get(t, 0) + seconds

    def report(self) -> List[str]:
        """收尾呼叫. 回傳問題清單."""
        problems = []

        # 1. 有 Lacks 沒被 teach_concept 引入過
        for lk in self.persona.lacks:
            if lk.lower() not in self._defined:
                problems.append(f"❌ Lacks 概念從未被 teach_concept 引入: {lk!r}")

        # 2. 引入的 jargon 超過 grade 預算
        if len(self._jargon_used) > self.persona.jargon_budget:
            problems.append(
                f"❌ Jargon overload: 用了 {len(self._jargon_used)} 個未知術語 "
                f"(預算 {self.persona.jargon_budget})"
            )

        # 3. 個別 concept dwell 不足
        target = self.persona.seconds_per_lacks_concept
        for lk in self.persona.lacks:
            t = lk.lower()
            if t in self._defined:
                actual = self._concept_dwell.get(t, 0)
                if actual < target * 0.7:    # 容許 30% 寬容
                    problems.append(
                        f"⚠ {lk!r} 只 dwell {actual:.1f}s (建議 ≥{target:.0f}s)"
                    )

        return problems
