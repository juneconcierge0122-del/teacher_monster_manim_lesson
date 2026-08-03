"""Bilingual source copy for the advcalc series.

Loomis & Sternberg, *Advanced Calculus*, revised edition (Jones and Bartlett,
1990; originally Addison-Wesley, 1968). `books/Advanced_Calculus.pdf`.

TOPICS_ADVCALC[n] -> {"zh": (title, [narration lines]), "en": (title, [...])}
FORMULAS_ADVCALC[n] -> {beat index: on-screen formula string}

Two rules carried over from the earlier series (see docs/PLAYBOOK.md):

* The narration is the subtitle and the voice-over at once, so it stays plain
  spoken language — no integral signs, roots or angle brackets in here, the TTS
  mispronounces them. Symbols belong on screen, i.e. in FORMULAS.
* FORMULAS must be language independent. This book is heavy on named objects
  ("the space of alternating tensors", "the pullback"), and it is very easy to
  slip a Chinese or an English gloss into a formula string; anything that reads
  as a word goes into the scene's own MODE_LABEL dict instead.
"""

TOPICS_ADVCALC: dict[int, dict[str, tuple[str, list[str]]]] = {

# E00 — what this book is. Sourced from the title page and the preface
# (book pp. i-ii = PDF pp. 3-4) and the table of contents (PDF pp. 7-13).
0: {"zh": ("《高等微積分》導論：這本書是什麼", [
 "這本書封面寫著高等微積分，但它不是一般大學裡那門算偏導數與重積分的課。作者是 Loomis 與 Sternberg，兩位哈佛大學數學系的教授；書的內容來自他們在一九六零年代開的榮譽班，一九六八年出版，一九九零年出了修訂版。",
 "序言把門檻寫得很清楚。你需要嚴格觀點下的單變數微積分，還要一些線性代數，要熟悉極限與連續這類論證，並且對偏導數有一點經驗。作者建議的入門書是 Courant、Apostol、Spivak 與 Hardy。",
 "全書大致分成兩半。前半把微分學整個建立在賦範向量空間上，後半處理可微流形上的微積分。這個安排決定了整本書的風格：先把空間本身的結構講清楚，再談在上面怎麼做微分與積分。",
 "核心的觀念轉換在這裡。在初等微積分裡，導數是一個數，是切線的斜率。在這本書裡，微分是一個線性映射，是最接近真實變化量的那一個線性逼近；它與真實變化的差，比位移本身還要小一個等級。",
 "第零章到第二章是代數的準備。第零章講邏輯、量詞與集合，作者說這章主要是給人回頭查閱用的；第一章與第二章建立向量空間、對偶空間、矩陣、跡與行列式。",
 "第三章是全書前半的重心，微分學本身。從範數與連續性開始，經過無窮小的三個類、微分、方向導數與均值定理，一路走到隱函數定理、子流形與拉格朗日乘子。",
 "第四章補上分析需要的地基：度量空間、緊緻性、完備性，還有壓縮映射不動點定理。第五章處理純量積空間，第六章把前面的工具用在微分方程與傅立葉級數上。",
 "第七章是多重線性代數，交錯張量、行列式與外代數；作者自己說這章主要當作後面各章的參考。第八章建立黎曼積分的公理化理論，其中包含變數變換公式。",
 "第九章到第十一章是後半的主線。可微流形、切空間、向量場與李導數，接著是流形上的積分、單位分割與散度定理，最後匯集到外微積分與斯托克斯定理。序言提醒，第九章是學生最難吸收的一章。",
 "第十二章與第十三章彼此獨立，是示範性質的應用。前者是位勢論，包含格林公式、卜瓦松積分與狄利克雷問題；後者用辛幾何重講一次古典力學，從餘切叢一路做到正則變換。",
 "這個系列會照著書的順序走，大約兩到四個書頁做成一集，加星號的進階節也不跳過，全書預計一百五十五集。下一集從第零章開始，講邏輯與量詞。",
]), "en": ("Advanced Calculus: What This Book Is", [
 "The cover says Advanced Calculus, but this is not the usual course in partial derivatives and multiple integrals. It is by Loomis and Sternberg, both of the Harvard mathematics department, and it grew out of an honors course they gave in the nineteen sixties.",
 "The preface states the prerequisites plainly. You need one variable calculus from a rigorous point of view, some linear algebra, comfort with limit and continuity arguments, and a little experience with partial derivatives. It suggests Courant, Apostol, Spivak and Hardy.",
 "The book divides roughly in half. The first half develops the calculus entirely in the setting of normed vector spaces. The second half deals with the calculus of differentiable manifolds. The structure of the space comes first, and doing calculus on it comes second.",
 "Here is the central shift. In elementary calculus the derivative is a number, the slope of the tangent line. Here the differential is a linear map, the one linear approximation closest to the actual change, and the gap between them is of smaller order than the displacement.",
 "Chapters zero through two are algebraic preparation. Chapter zero covers logic, quantifiers and sets, and the authors say it is mainly there to be referred back to. Chapters one and two build vector spaces, the dual space, matrices, trace and determinant.",
 "Chapter three is the heart of the first half, the differential calculus itself. It starts from norms and continuity, passes through infinitesimals, the differential, directional derivatives and the mean value theorem, and reaches the implicit function theorem.",
 "Chapter four lays the analytic groundwork: metric spaces, compactness, completeness, and the contraction mapping fixed point theorem. Chapter five treats scalar product spaces, and chapter six turns those tools on differential equations and Fourier series.",
 "Chapter seven is multilinear algebra, with alternating tensors, the determinant and the exterior algebra; the authors call it a reference chapter. Chapter eight builds the axiomatic theory of Riemann integration, including the change of variables formula.",
 "Chapters nine through eleven carry the second half: manifolds, the tangent space, vector fields and Lie derivatives, then integration on manifolds and the divergence theorem, and finally exterior calculus and Stokes theorem. The preface warns that chapter nine is the hardest.",
 "Chapters twelve and thirteen are independent of each other and serve as illustrative applications. The first is potential theory, with Green's formulas, the Poisson integral and Dirichlet's problem. The second redoes classical mechanics using symplectic geometry.",
 "This series follows the book in order, at roughly two to four printed pages per episode, and it does not skip the starred advanced sections. That comes to about one hundred and fifty five episodes. The next one starts at chapter zero, with logic and quantifiers.",
])},

# E01 — Chapter 0, sections 1-3 (book pp. 1-6 = PDF pp. 13-18).
1: {"zh": ("第 0 章：邏輯、量詞與連接詞", [
 "這一集開始讀第 0 章。作者說這章主要是給人回頭查閱用的，但其中有一件事非讀不可，就是量詞的順序。先從最基本的說起：一個句子如果當下就能判斷真假，叫做敘述；含有變數、要給了值才能判斷的，叫做敘述框架。",
 "從框架變出敘述有兩條路。第一條是給變數一個值。第二條是宣告它永遠為真，也就是在前面加上「對每一個 x」，這叫全稱量詞；同義的說法有「對所有的 x」與「對每個 x」。",
 "另一條路是宣告它有時為真，寫成「存在一個 x 使得」，這叫存在量詞。被量詞綁住的變數叫束縛變數，沒被綁住的叫自由變數。加上量詞以後 x 還留在句子裡，但它已經不能再被賦值了。",
 "現在來到這一節最重要的地方。如果句子裡有兩個自由變數，就需要兩個量詞；而當兩種量詞混用時，寫的順序會改變整句話的意思。",
 "書上的例子是這樣。對每一個 x 都存在一個 y 使得 x 小於 y，這是真的，y 取 x 加一就行。但存在一個 y 使得對每一個 x 都有 x 小於 y，這是假的，因為那個 y 加一就不小於它自己。",
 "差別在於，第一句裡的 y 可以跟著 x 改變，第二句卻要求同一個 y 對所有 x 都成立，所以第二句強得多。作者在這裡寫了一句很重的話：讀者必須把這一點弄得絕對清楚，他往後的整個數學生涯都繫於此。",
 "反過來，同一種量詞連在一起時，順序不影響意思，可以縮寫成一個量詞符號。而收斂與連續的定義都用到三個量詞：數列收斂是對每個誤差都存在一個項數，使得之後每一項都夠接近；函數連續的定義形式完全一樣。",
 "接著是連接詞。「而且」只有兩邊都真的時候才真。「或」在日常語言裡有排他與相容兩種用法，數學不能容忍這種歧義，所以數學裡的「或」永遠是相容的：至少一個為真，兩個都真也算。",
 "最麻煩的是「如果就」。因為「若 x 小於三則 x 小於五」對每一個 x 都成立，我們被迫承認前提為假時整句話仍然是真的。所以只有在前提真、而結論假的時候，這個句子才是假的。",
 "真值表永遠為真的形式叫恆真式；任何不涉及量詞的有效推理原則，都必須用恆真式表達。常用的等價有三條：非「P 或 Q」等於非 P 且非 Q；「P 蘊涵 Q」等於「Q 或非 P」；非「P 蘊涵 Q」等於「P 且非 Q」。",
 "最後是量詞的否定。「並非總是真」與「有時為假」意思相同，這條規則可以把否定號一路推過整串量詞。實用的規則是：取否定時，把每個量詞換成相反的那一種，再把否定號移到整串的最後面。",
]), "en": ("Chapter 0: Logic, Quantifiers and the Connectives", [
 "This episode starts chapter zero. The authors say it is mainly there to be referred back to, but one thing in it must be read: the order of quantifiers. First the basics. A sentence that is true or false as it stands is a statement; one containing a variable is a statement frame.",
 "There are two ways to turn a frame into a statement. One is to give the variable a value. The other is to assert that it is always true, by prefixing 'for every x'. That prefix is the universal quantifier; 'for each x' and 'for all x' say the same thing.",
 "The other way is to assert that it is sometimes true, written 'there exists an x such that'. That is the existential quantifier. A quantified variable is called bound, an unquantified one free. The x is still in the sentence, but it can no longer be given values.",
 "Now the most important point in this section. A sentence with two free variables needs two quantifiers, and when quantifiers of both kinds are used, the order in which they are written changes what the sentence says.",
 "Here is the book's example. For every x there exists a y with x less than y is true: take y to be x plus one. But there exists a y such that for every x, x is less than y is false, because that y plus one is not less than itself.",
 "The difference is that in the first the y may change with x, while the second demands a single y that works for every x, which is far stronger. The authors put it bluntly: the reader must be absolutely clear on this point, his whole mathematical future is at stake.",
 "Among quantifiers of the same kind the order does not matter, and they can be abbreviated into one symbol. Convergence and continuity both need three quantifiers: for every error there is an index beyond which every term is close enough, and continuity has exactly the same shape.",
 "Next, the connectives. And is true only when both sides are true. Or is used in ordinary speech both exclusively and inclusively; mathematics cannot tolerate that ambiguity, so in mathematics or is always inclusive: at least one is true, and possibly both.",
 "The troublesome one is if-then. Since if x is less than three then x is less than five holds for every x, we are forced to accept that the whole sentence is true whenever the premise is false. So it is false only when the premise is true and the conclusion false.",
 "A form whose truth table is always true is called a tautology, and any valid principle of reasoning not involving quantifiers must be expressed by one. Three useful equivalences: not P or Q is not P and not Q; P implies Q is Q or not P; not of P implies Q is P and not Q.",
 "Finally, negating quantifiers. Not always true means the same as sometimes false, and that lets a negation sign move past a whole string of quantifiers. The practical rule: change each quantifier to the opposite kind, and move the negation sign to the end of the string.",
])},

# E02 — Chapter 0, sections 4-6 (book pp. 6-10 = PDF pp. 18-22).
2: {"zh": ("第 0 章：集合、受限變數與關係", [
 "現在的數學把每一個對象都定義成某種集合，所以要先把這個最基本的概念看清楚。集合是一堆對象的聚集，而這個聚集本身也被當成一個實體。裡面的對象叫做元素或成員，表示屬於的符號是一個像大寫希臘字母的記號。",
 "等號在數學裡表示邏輯上的同一。兩個集合被視為同一個對象，若且唯若它們的成員完全相同。所以集合相等這件事，整個化約成一句話：對每一個 x，x 屬於 A 若且唯若 x 屬於 B。",
 "如果 A 的每個元素都是 B 的元素，就說 A 是 B 的子集，或說 A 包含於 B。於是 A 等於 B 等價於 A 包含於 B 而且 B 包含於 A。這是證明兩個集合相等最常用的辦法：分別證明兩個方向的包含。",
 "有限集可以直接把成員列出來，用大括號框起來；只有一個成員的叫單元集，兩個的叫對集。無限集通常用敘述框架來定義，寫成滿足 P 的所有 x 所成的集合。例如平方小於九的所有實數，就是開區間負三到三。",
 "我們需要空集，就像算術裡需要零一樣。如果 P 從來不成立，那麼滿足 P 的集合就是空集；例如不等於自己的那些 x，構成的就是空集。作者順帶提到，四這個數本身通常定義成零一二三所成的集合。",
 "為了不讓集合這個詞過勞，書上還用類、聚集、族、總體這些同義詞。接下來是受限變數。數學裡的變數不能拿任意對象當值，它只能取某個集合裡的成員，這個集合就叫做該變數的定義域。",
 "定義域有時明講，更多時候是隱含的。例如字母 n 通常就代表整數。有疑慮的時候就明白寫出來，讀成對每一個屬於整數集的 n。注意這裡的屬於符號要讀成介系詞「在」。這種量詞叫做受限量詞。",
 "受限變數其實只是無限制變數的縮寫。全稱的情形展開成：對每一個 x，如果 x 屬於 A 就有 P。存在的情形展開成：存在一個 x，x 屬於 A 而且 P。一個用蘊涵、一個用而且，這兩者不能弄混。",
 "接著是有序對。它同樣被定義成某種集合，但我們不在乎是哪一種，只要它保證那個關鍵性質就好：兩個有序對相等，若且唯若第一個元素相等而且第二個元素相等。所以一三這個有序對不等於三一。",
 "對應或說關係，以及它的特例映射，是數學裡最基本的概念。既然關係的圖形是一組有序對，而現在的做法是把每個數學對象都看成集合，那就乾脆讓關係就是它的圖形：一個關係就是一組有序對。",
 "由此就能定義：定義域是所有第一元素所成的集合，值域是所有第二元素所成的集合，反關係是把每一對顛倒過來。而第一元素在 A、第二元素在 B 的所有有序對所成的集合，叫做 A 與 B 的笛卡兒積；實數平面就是實數線乘上實數線。",
]), "en": ("Chapter 0: Sets, Restricted Variables and Relations", [
 "Modern practice defines every mathematical object as a set of some kind, so this notion must be examined first. A set is a collection of objects that is itself considered an entity. Its objects are its elements, and the membership symbol is a sort of capital epsilon.",
 "The equals sign means logical identity. Two sets are considered the same object if and only if they have exactly the same members. So set equality reduces entirely to one line: for every x, x belongs to A if and only if x belongs to B.",
 "If every element of A is an element of B, then A is a subset of B, or A is included in B. So A equals B is equivalent to A included in B together with B included in A. That is the usual way of establishing set identity: prove both inclusions.",
 "A finite set can have its members listed inside braces: one member gives a unit set, two a pair set. Infinite sets are generally defined by statement frames, the set of all x such that P of x. The reals whose square is under nine form the open interval minus three to three.",
 "We need the empty set much as arithmetic needs zero. If P is never true, the set of x satisfying it is empty; the x that differ from themselves form the empty set. In passing, the authors note that the number four is usually defined as the set of zero, one, two and three.",
 "To avoid overworking the word set, the book also uses class, collection, family and aggregate. Next, restricted variables. A variable is not allowed to take all objects as values; it can only take members of a certain set, called the domain of the variable.",
 "The domain is sometimes stated and more often implied: the letter n customarily means an integer. In case of doubt we write it out, read as for every n in the integers. Note that the membership symbol is read here as the preposition in. Such quantifiers are called restricted.",
 "Restricted variables are just abbreviations of unrestricted ones. The universal case unfolds as: for every x, if x is in A then P. The existential case unfolds as: there exists an x with x in A and P. One uses implication, the other uses and; they must not be mixed up.",
 "Then ordered pairs. A pair is again taken to be some set, but we do not care which, so long as it guarantees the crucial property: two ordered pairs are equal exactly when their first elements agree and their second elements agree. So one three is not three one.",
 "Correspondence, or relation, and its special case, mapping, are fundamental. Since the graph of a relation is a set of ordered pairs, and every object is now regarded as a set, it is efficient to take the graph to be the relation: a relation is simply a set of ordered pairs.",
 "From this: the domain is the set of all first elements, the range the set of all second elements, and the inverse reverses every pair. All pairs with first element in A and second in B form the Cartesian product; the analytic plane is the reals times the reals.",
])},

# E03 — Chapter 0, sections 7-9 (book pp. 10-15 = PDF pp. 22-27).
3: {"zh": ("第 0 章：函數、映射與合成", [
 "函數是一種特別的關係：定義域裡的每一個 x，恰好只配上一個值域元素 y。寫成條件就是，如果 x 配 y 而且 x 也配 z，那麼 y 就等於 z。由 f 與 x 唯一決定的那個 y，就寫成 f 括號 x。",
 "人們傾向把函數看成主動的，把不是函數的關係看成被動的。函數作用在定義域裡的一個元素上，給出一個值；我們拿 x 來套用 f，所以也常把函數叫做算子。而一般的關係並沒有特定的 y，配對就比較被動。",
 "我們常常是靠指定每一點的值來定義函數，這時會用一種帶尾巴的箭頭表示配對。x 對應到 x 的平方，就是把每個數配上它的平方的那個函數。要讓這個記法有意義，定義域必須是清楚的。",
 "如果 f 是函數，它的反關係一定是關係，但通常不是函數。平方就是例子：它的反關係同時含有四配二與四配負二這兩對，所以不是函數。反關係也是函數的那種 f，就叫做一對一。",
 "從 A 到 B 的函數這個記法，隱含了三件事：f 是函數、f 的定義域正好是 A、而且 f 的值域包含於 B。很多人覺得函數本來就該包含這三樣，也就是應該看成 f、A、B 這個有序三元組，其中 B 叫做上域。",
 "書上把映射、變換這些詞留給這個三元組。一個映射如果是一對一的就叫嵌射，如果值域正好等於上域就叫滿射，兩者都成立就叫雙射。函數對它自己的值域永遠是滿的，說它是滿射，指的是值域等於那個講好的上域。",
 "現代數學有個習慣：一種新的對象一出現，馬上就去看所有這種對象所成的集合。有了從 A 到 S 的函數，自然就去看所有這種函數所成的集合。子集則對應到特徵函數，取值只有零與一，所以所有子集所成的集合寫成二的 S 次方。",
 "有序三元組通常定義成前兩個先配成對、再與第三個配對。理由是兩個變數的函數，通常被看成單一個有序對變數的函數。於是三維空間就定義成平面再乘上實數線；不過三元組也可以讀成長度三的序列，那是另一個對象。",
 "這種把其實不同的兩個對象視為同一的含糊，是為了精確而付出的必要代價；在數學還比較模糊的年代，本來就只有一個籠統的概念。指標集合也一樣：一個加了指標的集合，其實就是那個指標函數。",
 "一般的笛卡兒積就由此定義。一族用 I 編號的集合，它們的乘積是所有這樣的函數所成的集合：定義域是 I，而且在每一個 i 上取的值都落在對應的那個集合裡。",
 "最後是合成。g 與 f 的合成，把 x 送到 g 括號 f 括號 x。這大概是數學裡最基本的二元運算，而且滿足結合律。恆等映射把每個元素送回它自己。而一個映射有反映射，若且唯若它是雙射。",
]), "en": ("Chapter 0: Functions, Mappings and Composition", [
 "A function is a special kind of relation: each element x of the domain is paired with exactly one range element y. As a condition: if x is paired with y and x is also paired with z, then y equals z. The y thus uniquely determined by f and x is written f of x.",
 "One tends to think of a function as active and a relation that is not a function as passive. A function acts on an element of its domain to give a value; we take x and apply f to it, so a function is often called an operator. A plain relation pairs more passively.",
 "Often we define a function by specifying its value at each point, and then a stopped arrow notation indicates the pairing. x stopped-arrow x squared is the function assigning to each number its square. For this notation to mean anything, the domain must be understood.",
 "If f is a function its relational inverse is certainly a relation, but in general not a function. Squaring is the example: its inverse contains both four paired with two and four paired with minus two, so it is not a function. An f whose inverse is a function is called one-to-one.",
 "The notation f from A to B implies three things: that f is a function, that its domain is exactly A, and that its range is included in B. Many feel a function should include all of this, that is, be considered the ordered triple f, A, B, where B is called the codomain.",
 "The book keeps the words map, mapping and transformation for that triple. A mapping is injective if it is one-to-one, surjective if its range equals the codomain, and bijective if both. A function is always onto its own range, so surjective refers to the stated codomain.",
 "A habit of the modern mathematician: once a new object appears, look at the set of all such objects. Having functions from A to S, consider the set of them all. Subsets correspond to characteristic functions taking only zero and one, so the set of all subsets is written two to the S.",
 "An ordered triple is usually defined as the first two paired, then paired with the third, because a function of two variables is read as a function of one ordered pair variable. So three-space is the plane crossed with the line, though a triple can also be read as a sequence.",
 "This blurring, identifying two objects that are really distinct, is a necessary price for deciding exactly what things are; when mathematics was vaguer there was one fuzzy notion instead. Indexed sets are the same: an indexed set is really just the indexing function.",
 "The general Cartesian product is defined from this. For a collection of sets indexed by I, their product is the set of all functions with domain I whose value at each i lies in the corresponding set.",
 "Finally composition. The composition of g with f sends x to g of f of x. It is perhaps the basic binary operation of mathematics, and it is associative. The identity map sends each element to itself, and a mapping has an inverse exactly when it is bijective.",
])},

}

# Language independent. Every word-like gloss lives in the scene's MODE_LABEL.
FORMULAS_ADVCALC: dict[int, dict[int, str]] = {

0: {
 0: "Loomis  ·  Sternberg      Harvard      1968  /  1990",
 1: "f : ℝ → ℝ  ,  lim  ,  ϵ – δ        +        V  ,  dim V  ,  A x = b",
 2: "Ch 1 – 8 :  ‖ · ‖          Ch 9 – 13 :  M",
 3: "ΔF ( ξ )  =  dF ( ξ )  +  𝒪 ( ξ )        dF  ∈  Hom ( V , W )",
 4: "Ch 0 :  ∀  ∃  ∈          Ch 1 – 2 :  V , V* , A",
 5: "Ch 3 :  ‖ · ‖  →  dF  →  F ( x , y ) = 0",
 6: "Ch 4 :  T ( x ) = x        Ch 5 :  ( α , β )        Ch 6 :  dx / dt = F",
 7: "Ch 7 :  Λ V*  ,  det          Ch 8 :  ∫",
 8: "Ch 9 – 11 :  Tₚ M  ,  d          ∫ dω  =  ∫ ω",
 9: "Ch 12 :  Δu = 0          Ch 13 :  T* ( M )  ,  ω = dθ",
 10: "155  ·  2 – 4 pp / ep  ·  Ch 0 § 1 – 3",
},

1: {
 0: "P ( x ) :  x < 4          P ( 5 ) :  5 < 4",
 1: "( ∀x ) P ( x )          ( ∀x ) ( x < 4 )",
 2: "( ∃x ) P ( x )          ( ∃x ) ( x < 4 )",
 3: "( ∃y ) ( ∀x ) P ( x , y )        ≠        ( ∀x ) ( ∃y ) P ( x , y )",
 4: "( ∀x ) ( ∃y ) ( x < y )  =  T          ( ∃y ) ( ∀x ) ( x < y )  =  F",
 5: "y  =  x + 1          y₀ + 1  ≮  y₀",
 6: "( ∀x ) ( ∀y )  =  ( ∀x , y )        ( ∀ε ) ( ∃N ) ( ∀n > N ) | xₙ − x | < ε",
 7: "P & Q :  T F F F          P or Q :  T T T F",
 8: "P ⇒ Q :  T F T T          F  ⟺  P = T  &  Q = F",
 9: "∼( P or Q ) ⇔ (∼P) & (∼Q)        ∼( P ⇒ Q ) ⇔ P & (∼Q)",
 10: "∼(∀x)(∃y)(∀z) P ( x , y , z )   ⇔   (∃x)(∀y)(∃z) ∼P ( x , y , z )",
},

2: {
 0: "x  ∈  A",
 1: "A = B    ⇔    ( ∀x ) ( x ∈ A  ⇔  x ∈ B )",
 2: "A ⊂ B  :  ( ∀x ) ( x ∈ A ⇒ x ∈ B )      ( A = B ) ⇔ ( A ⊂ B ) & ( B ⊂ A )",
 3: "{ 1 , 4 , 7 }    { x }    { x , y }        { x : x² < 9 }  =  ( −3 , 3 )",
 4: "{ x : x ≠ x }  =  ∅        4 = { 0 , 1 , 2 , 3 }    1 = { 0 }    0 = ∅",
 5: "x  ∈  A  =  dom",
 6: "( ∀n ∈ ℤ ) P ( n )        { n ∈ ℤ : P ( n ) }",
 7: "( ∀x ∈ A ) P ⇔ ( ∀x ) ( x ∈ A ⇒ P )      ( ∃x ∈ A ) P ⇔ ( ∃x ) ( x ∈ A & P )",
 8: "⟨ x , y ⟩ = ⟨ a , b ⟩  ⇔  x = a  &  y = b        ⟨ 1 , 3 ⟩  ≠  ⟨ 3 , 1 ⟩",
 9: "x R y    ⇔    ⟨ x , y ⟩  ∈  R",
 10: "dom R = { x : (∃y) ⟨x,y⟩ ∈ R }        A × B = { ⟨x,y⟩ : x ∈ A & y ∈ B }",
},

3: {
 0: "⟨x,y⟩ ∈ f  &  ⟨x,z⟩ ∈ f  ⇒  y = z        y = f ( x )  ⇔  ⟨x,y⟩ ∈ f",
 1: "f  :  x  ↦  f ( x )",
 2: "x  ↦  x²",
 3: "f : x ↦ x²        f ⁻¹  ⊃  ⟨ 4 , 2 ⟩ , ⟨ 4 , −2 ⟩",
 4: "f : A → B        ⟨ f , A , B ⟩        dom f = A  ,  range f ⊂ B",
 5: "1–1 : inj        range f = B : surj        inj & surj : bij",
 6: "{ f : A → S }        χ : S → { 0 , 1 }",
 7: "⟨ x , y , z ⟩  =  ⟨ ⟨ x , y ⟩ , z ⟩        ℝ³  =  ( ℝ × ℝ ) × ℝ",
 8: "{ xᵢ : i ∈ I }        i  ↦  xᵢ",
 9: "∏ Sᵢ  =  { f  :  dom f = I  ,  f ( i ) ∈ Sᵢ }",
 10: "( g ∘ f ) ( x ) = g ( f ( x ) )        f ∘ ( g ∘ h ) = ( f ∘ g ) ∘ h",
},

}
