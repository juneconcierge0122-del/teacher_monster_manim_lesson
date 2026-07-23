"""Localized copy for the Landau lesson 1 audiovisual sample."""

STRINGS = {
    "zh-TW": {
        "title": "Landau 力學 01｜用最少的數字描述運動",
        "objective": "目標：理解自由度、廣義座標與廣義速度",
        "prereq": "先備：三角函數、位置與速度",
        "hook": "要描述單擺，真的需要同時追蹤 x 和 y 嗎？",
        "redundant": "兩個座標，但受到一個約束",
        "constraint": "x² + y² = ℓ²",
        "one_number": "一個角度就能決定整個位置",
        "generalized": "廣義座標：能唯一描述系統形狀的獨立變數",
        "derive_1": "q ≡ θ",
        "derive_2": "x = ℓ sin q,     y = −ℓ cos q",
        "derive_3": "ẋ = ℓ cos q · q̇,     ẏ = ℓ sin q · q̇",
        "state": "機械狀態 = (q, q̇)",
        "question": "思考：若只知道擺角 q，能預測它下一秒往哪裡走嗎？",
        "answer": "不能；同一位置可能向左或向右，還需要廣義速度。",
        "summary_1": "自由度 = 描述構形所需的獨立數目",
        "summary_2": "廣義座標不必是直角座標",
        "summary_3": "位置與速度一起決定機械狀態",
    },
    "en": {
        "title": "Landau Mechanics 01 | Describe motion with fewer numbers",
        "objective": "Goal: understand degrees of freedom and generalized coordinates",
        "prereq": "Prerequisites: trigonometry, position, and velocity",
        "hook": "Do we really need both x and y to describe a pendulum?",
        "redundant": "Two coordinates, connected by one constraint",
        "constraint": "x² + y² = ℓ²",
        "one_number": "One angle determines the entire position",
        "generalized": "Generalized coordinate: an independent variable that fixes the configuration",
        "derive_1": "q ≡ θ",
        "derive_2": "x = ℓ sin q,     y = −ℓ cos q",
        "derive_3": "ẋ = ℓ cos q · q̇,     ẏ = ℓ sin q · q̇",
        "state": "mechanical state = (q, q̇)",
        "question": "Think: if you know only q, can you predict which way the bob moves next?",
        "answer": "No. At the same position it may move left or right; velocity is also needed.",
        "summary_1": "Degree of freedom = number of independent configuration variables",
        "summary_2": "A generalized coordinate need not be Cartesian",
        "summary_3": "Position and velocity together specify the mechanical state",
    },
}


def strings(language: str) -> dict[str, str]:
    """Return one complete locale, failing loudly on unsupported languages."""
    return STRINGS[language]
