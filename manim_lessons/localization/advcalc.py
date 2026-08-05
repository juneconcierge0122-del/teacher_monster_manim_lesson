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
 "這個系列會照著書的順序走，大約兩到四個書頁做成一集，加星號的進階節也不跳過，全書預計一百六十九集。下一集從第零章開始，講邏輯與量詞。",
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
 "This series follows the book in order, at roughly two to four printed pages per episode, and it does not skip the starred advanced sections. That comes to about one hundred and sixty nine episodes. The next one starts at chapter zero, with logic and quantifiers.",
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

# E04 — chapter 0, sections 10-12 (book pp. 15-21 = PDF pp. 27-33). This is the
# episode chapter 0 was missing: E03's description claimed to finish the
# chapter, but §10-12 were never covered.
4: {"zh": ("第 0 章：對偶、布林運算與等價關係", [
 "先講對偶。設 F 是兩個變數的函數。把 x 固定住，剩下的就是一個只依賴 y 的函數。於是每一個 x 都給出一個函數，而這個對應本身又是一個映射，把 A 送到「所有從 B 到 C 的函數」所成的集合。",
 "反過來也成立：給定一個從 A 到那個函數集合的映射，就能把值回填成兩個變數的函數。所以兩變數的函數、從 A 出發的映射、從 B 出發的映射，是同一件事的三種看法，而最外側那兩個互稱對偶。",
 "第一個應用是矩陣。一個 m 乘 n 的矩陣，就是定義在「列指標與行指標的配對」上的函數。固定列指標就得到一整列，於是矩陣可以讀成若干個列所成的元組；對偶地，也可以讀成若干個行所成的元組。",
 "同樣的道理，n 個從 A 到 B 的函數所成的元組，可以看成單一個函數，它的值是 B 裡的 n 元組。稍後還有一個更重要的例子：對偶讓有限維向量空間可以被看成它自己的第二共軛空間。",
 "幾何裡也有。把點與線看成兩種原始對象，關聯函數在點落在線上時取一、否則取零。固定一條線，就得到線上所有點所成的集合；固定一個點，就得到通過它的所有線。線是點的集合，點也是線的集合，這是投影幾何的基本觀點。",
 "固定變數時常用一個點記號：在變動的那個位置擺一個點。這個記法很方便，但有個缺陷——沒辦法一邊代入一邊保留意思，因為看到代入後的值，讀不回原來是哪個函數。書上後面的方向導數就會用到它。",
 "接著是布林運算。固定一個定義域，取它的一族子集。這一族的聯集，是至少屬於其中一個集合的所有元素；交集則是落在每一個集合裡的元素。加上指標之後寫起來更方便，書上說這在技術上與心理上都有好處。",
 "補集是定義域裡不屬於它的那部分。De Morgan 律說，交集的補集等於補集的聯集——這只是量詞否定規則的直接結果：不是每個都在，就等於有時候不在。各種分配律同樣來自量詞的性質。",
 "還有一組重要的等式：函數的原像保持聯集、保持交集，也保持補集。注意只有第一條對一般的關係仍然成立，另外兩條會壞掉，因為兩個量詞交換次序之後意思就變了。",
 "最後是分割。把一個集合切成互不相交的一族子集，聯集正好是原集合，這就是纖維化，每一塊叫一根纖維。把一個點送到它所在的那根纖維，這個映射叫投影。任何函數都自動把定義域纖維化成它取值不變的那些集合。",
 "等價關係是自反、對稱又遞移的關係。每個纖維化都給出一個等價關係，而這一節的定理是反過來的那半：每一個等價關係，都恰好是某個纖維化的等價關係。有理數與模 p 的整數，都是這樣造出來的。",
]), "en": ("Chapter 0: Duality, the Boolean Operations and Equivalence Relations", [
 "First, duality. Let F be a function of two variables. Hold x fixed and what remains is a function of y alone. So each x yields a function, and that correspondence is itself a mapping, from A into the set of all functions from B to C.",
 "The converse holds too. Given a mapping from A into that set of functions, we can fill the values back in to get a function of two variables. So the two-variable function and the two mappings are three ways of viewing one phenomenon; the outer two are said to be dual.",
 "The first application is the matrix. An m by n matrix is a function defined on pairs of a row index and a column index. Fix the row index and you get a whole row, so the matrix can be read as a tuple of rows; dually, it can be read as a tuple of columns.",
 "In the same vein, an n-tuple of functions from A to B can be regarded as a single function whose values are n-tuples in B. A more important case comes later: duality is what lets a finite-dimensional vector space be regarded as its own second conjugate space.",
 "Geometry has it too. Take points and lines as two kinds of primitive object, with an incidence function that is one when the point lies on the line. Fix a line and you get the set of points on it; fix a point, the lines through it. This duality is basic to projective geometry.",
 "When a variable is held fixed there is a convenient device: put a dot in the position of the varying one. The notation is useful but flawed, since we cannot indicate substitution without losing meaning; from the value we cannot read back which function was evaluated.",
 "Now the Boolean operations. Fix a domain and take a family of its subsets. The union of the family is the set of elements belonging to at least one of them, and the intersection is the set of those lying in every one. Indexing the family makes all of this easier to write.",
 "The complement of a subset is what is left of the domain. De Morgan's law says the complement of an intersection is the union of the complements, and this is an immediate consequence of the rule for negating quantifiers: not always in means the same as sometimes not in.",
 "There are also identities for preimages: a preimage preserves unions, intersections and complements. Only the first survives when the function is replaced by a general relation; the other two fail, because swapping the order of two quantifiers changes the meaning.",
 "Finally partitions. Cut a set into a disjoint family of subsets whose union is the whole set: that is a fibering, and each piece is a fiber. Sending a point to its own fiber is the projection. Any function automatically fibers its domain into the sets where it is constant.",
 "An equivalence relation is reflexive, symmetric and transitive. Every fibering gives one, and the theorem of this section is the converse: every equivalence relation is the equivalence relation of a fibering. The rationals and the integers modulo p are both built this way.",
])},

# E05 — chapter 1, section 1, first half (book pp. 21-25 = PDF pp. 33-37):
# the axioms, the standard function-space example, and subspaces.
5: {"zh": ("第 1 章：向量空間與子空間", [
 "第一章開始講向量空間。多變數的微積分把單變數的微積分與向量空間理論接在一起，而處理得好不好，直接取決於這套理論用得夠不夠徹底。所以書上花前兩章專講向量空間本身：這一章講一般的，下一章講有限維的。",
 "先從讀者大概已經見過的幾何向量開始。它們是從一個選定的原點畫出的箭頭，相加用平行四邊形法則：以兩個箭頭為鄰邊作平行四邊形，從原點出發的那條對角線就是它們的和。",
 "向量也可以乘上一個數。把一個箭頭乘上 x，得到的是同一條直線上的另一個箭頭，長度是原來的 x 倍的絕對值；x 是正的就在原點的同一側，是負的就在另一側。",
 "這兩個運算滿足一些代數律。不過書上提醒，幾何的證明通常比較粗略，說服力有餘而嚴密不足。像加法結合律的標準證明，就是畫一個平行六面體，去看那條從原點出發的對角線。",
 "另一個大家可能見過的系統是座標三元組。這裡的三維向量是三個數排成的有序組，加法與數乘都是逐項代數地定義的。向量律對這種對象好證得多，因為幾乎只是形式上的推演。",
 "如果把三元組看成一個函數，定義域是一到三這三個整數，第 i 項就是函數在 i 的值，那麼這個例子就提示了一個更一般的型別，叫做函數空間。",
 "現在給定義。設 V 是一個集合，上面給了一個加法與一個數乘。前四條公理只管加法：結合律、交換律、有一個零元素加上去不改變任何向量、而且每個向量都有一個加起來等於零的伙伴。",
 "後四條把數乘接上來：兩個數連續乘等於乘上它們的積、和可以往兩邊分配、乘以一就是原來的向量。從這些公理立刻可以推出零元素唯一、每個向量的反元素唯一，而且零乘任何向量都是零向量。",
 "書上的標準例子是這樣：取任何一個集合 A，看所有定義在 A 上的實值函數。兩個函數相加就是逐點相加，乘上一個數就是每一點的值都乘上去。A 取一到三就回到三元組，A 取整條實線就是一元實函數的空間。",
 "接著是子空間。取 V 的一個非空子集，如果它對 V 的兩個運算封閉，那麼它自己就是一個向量空間。理由很短：那些對所有元素都成立的律在小集合裡自動成立，而封閉性保證零元素與反元素也都留在裡面。",
 "所以閉區間上的連續函數，是該區間上所有實值函數的子空間，而這樣的子空間就叫函數空間。書上預設向量空間是實的，但把純量換成複數、甚至換成任何一個體，大部分內容都照樣成立。",
]), "en": ("Chapter 1: Vector Spaces and Subspaces", [
 "Chapter one begins vector spaces. The calculus of several variables unites the calculus of one variable with the theory of vector spaces, and how well it goes depends on how thoroughly that theory is used. So the first two chapters study vector spaces themselves.",
 "We start from the geometric vectors the reader has probably met: arrows drawn from a chosen origin. Two of them are added by the parallelogram rule. Build the parallelogram having the two arrows as sides, and the diagonal from the origin is their sum.",
 "Vectors can also be multiplied by numbers. Multiplying an arrow by x gives another arrow along the same line, whose length is the absolute value of x times the original. It lies on the same side of the origin when x is positive, the opposite side when x is negative.",
 "These two operations satisfy certain laws of algebra. The book warns that geometric proofs of them are sketchy, more plausibility argument than airtight logic. The usual proof of the associative law is a picture of a parallelepiped and its diagonal from the origin.",
 "Another system the reader may have seen is coordinate triples. Here a three-dimensional vector is an ordered triple of numbers, and both operations are defined algebraically, entry by entry. The vector laws are much easier to prove here, since they are almost formalities.",
 "If we think of a triple as a function whose domain is the integers from one to three, with the ith entry the value at i, then this example suggests a much more general type, called a function space.",
 "Now the definition. Let V be a set carrying an addition and a multiplication by numbers. The first four axioms concern addition alone: it is associative, it is commutative, there is a zero that changes nothing, and every vector has a partner summing to zero.",
 "The last four tie in the scalars: multiplying by two numbers in turn is multiplying by their product, sums distribute both ways, and multiplying by one changes nothing. From these, the zero is unique, each negative is unique, and zero times any vector is zero.",
 "The book's standard example: take any set A and look at all real-valued functions on it. Two are added pointwise, and one is scaled by scaling its value at every point. Taking A to be one to three returns the triples; taking A to be the line gives functions of one real variable.",
 "Now subspaces. Take a nonempty subset of V closed under the two operations; then it is a vector space in its own right. The laws holding for all elements hold automatically in the smaller set, and closure keeps the zero and the negatives inside it.",
 "So the continuous functions on a closed interval form a subspace of all real-valued functions there, and such a subspace is called a function space. The book takes vector spaces to be real, but replacing the scalars by complex numbers, or by any field, leaves most of it standing.",
])},

# E06 — chapter 1, section 1, second half (book pp. 26-29 = PDF pp. 38-41):
# unordered sums, linear combinations, Theorem 1.1 and the linear span.
6: {"zh": ("第 1 章：線性組合與線性擴張", [
 "因為加法有交換律與結合律，一個有限集合的向量和，跟你用什麼順序、怎麼分組去加完全無關。書上舉的例子是三個向量，一共有十二種算法，結果都一樣。",
 "既然如此，只要把指標集合寫出來，和就沒有歧義了。所以可以寫成對 I 裡的每個 i 把對應的向量加起來，完全不必說明是怎麼加的。一般來說，任何一個有限的、加了指標的向量集合，都唯一決定一個和向量。",
 "指標集常常就是一到 n 這一段整數，這時向量排成一個 n 元組，沒特別交代就照自然順序相加。不過經常會用到沒有次序的指標集：兩個變數、次數不超過五的一般多項式，它的單項式所成的集合就沒有自然次序。",
 "書上把那個形式證明標了星號，只給有興趣的讀者。做法是對元素個數做歸納：兩種算法各自的最後一次加法，把指標集分成兩塊；取兩組分法的交集得到四小塊，再用歸納假設把四塊的和重新結合，兩邊就相等了。",
 "有了和，就可以定義線性組合。一個向量叫做集合 A 的線性組合，如果它是有限個「純量乘上 A 裡的向量」加起來的結果，而那些純量是任意的。",
 "舉例來說，如果 A 是所有次方所成的集合，那麼線性組合就正好是多項式函數。如果 A 是正弦、餘弦與指數這三個函數，照這個順序排，那麼三倍正弦減掉指數，對應的係數三元組就是三、零、負一。",
 "再看一個具體的。取三維空間裡的兩個向量，它們所有的線性組合所成的集合，一眼就看得出對加法與數乘封閉，所以是一個子空間；而任何含有那兩個向量的子空間，一定也含有它們所有的線性組合。",
 "把這件事寫成定理：如果 A 是向量空間的一個非空子集，那麼 A 的所有線性組合所成的集合是一個子空間，而且是包含 A 的最小的那個子空間。",
 "證明分兩半。封閉性：兩個線性組合相加，按指標合併同類項就還是線性組合；乘上一個純量，用分配律與歸納法也還是。至於最小：這個集合含有 A 的每一個元素，而任何含有 A 的子空間都得含有每一個線性組合。",
 "如果 A 是無限集合，就沒辦法一次列完，但論證照樣走得通：兩個線性組合各自都是有限和，加起來仍然是有限個純量乘上 A 裡的向量，所以還是線性組合。",
 "這個子空間叫做 A 的線性擴張。如果它就是整個空間，就說 A 生成這個空間，而有有限生成集的空間叫有限維。n 維座標空間，由那些只有一個位置是一、其他都是零的向量生成。閉區間上的連續函數則沒有有限生成集。",
]), "en": ("Chapter 1: Linear Combinations and Linear Span", [
 "Because addition is commutative and associative, the sum of a finite set of vectors is the same for all ways of adding them. The book's example is three vectors, which can be summed in twelve ways, all giving the same result.",
 "So writing down the index set makes the sum unambiguous: we can write the sum over i in I without saying how we got it. In general any finite indexed set of vectors determines a unique sum vector.",
 "The index set is often a block of integers from one to n, and then the vectors form an n-tuple, added in their natural order unless directed otherwise. But unordered index sets come up often: the monomials of a general polynomial in two variables have no natural order.",
 "The book stars the formal proof and gives it only for the interested reader. It is an induction on the number of elements: the last addition in each computation splits the index set in two, intersecting the two splittings gives four pieces, and induction regroups them.",
 "With sums in hand we can define a linear combination. A vector is a linear combination of a set A if it is a finite sum of scalars times vectors of A, where the scalars are arbitrary.",
 "For example, if A is the set of all powers, the linear combinations are exactly the polynomial functions. If A is sine, cosine and the exponential in that listed order, then three sine minus the exponential has coefficient triple three, zero, minus one.",
 "Here is a concrete one. Take two vectors in three-space. The set of all their linear combinations is plainly closed under addition and scaling, so it is a subspace; and any subspace containing the two vectors must contain all of their linear combinations.",
 "As a theorem: if A is a nonempty subset of a vector space, then the set of all linear combinations of vectors of A is a subspace, and it is the smallest subspace which includes A.",
 "The proof has two halves. Closure: adding two linear combinations and collecting terms gives another, and scaling gives another by distributivity and induction. Smallest: the set contains each element of A, and any subspace including A must contain every linear combination.",
 "If A is infinite we cannot list it in one go, but the argument still runs: two linear combinations are each finite sums, so their sum is again a finite sum of scalars times vectors of A, hence again a linear combination.",
 "This subspace is the linear span of A. If it is the whole space, A spans the space, and a space with a finite spanning set is finite-dimensional. Coordinate n-space is spanned by the vectors with a single one and zeros elsewhere. Continuous functions on an interval are not.",
])},

# E07 — chapter 1, section 1, third part (book pp. 29-32 = PDF pp. 41-44):
# linear transformations, Theorem 1.2 and the skeleton.
7: {"zh": ("第 1 章：線性變換與 skeleton", [
 "先問一個問題。A 上的實值函數，除了相加與數乘之外，其實還可以逐點相乘；連續函數也一樣。既然有三個運算，為什麼還要特地談只有兩個運算的向量空間？",
 "答案是：最重要的那些映射，保持的正好是這兩個向量運算。書上的例子是積分：閉區間上連續函數的積分，把和送到和、把倍數送到倍數，但它完全不保持乘積，兩個函數乘起來的積分不等於各自積分的乘積。",
 "另一個例子是把三元組送到二元組的那種對應，每個分量都是原來三個座標的一次組合。線性方程組能不能解，本質上就是這種映射的理論。所以我們研究向量空間，有一部分正是為了研究保持向量運算的映射。",
 "定義因此是這樣：從 V 到 W 的一個映射叫線性變換，如果它把和送到和、把純量倍數送到純量倍數。這兩個條件可以併成一條：把「x 倍的 α 加上 y 倍的 β」送到「x 倍的 T α 加上 y 倍的 T β」。",
 "用歸納法，這件事馬上推廣到任意有限和：任何線性組合經過 T 之後，還是原來那些像的線性組合，係數一模一樣。積分的性質正是這個式子的特例。",
 "現在來找出所有以 n 維座標空間為定義域的線性映射。先看一個具體的：固定三個函數，把一個三元組送到「以它的三個分量為係數」的那個線性組合。這顯然是線性的。",
 "有趣的是，從這個映射可以把那三個函數讀回來。把只有第 j 個位置是一的那個向量餵進去，出來的正好是第 j 個函數。這一組像所成的 n 元組，書上叫做 T 的 skeleton。",
 "定理是這樣說的。給定 W 裡任何一個 n 元組，對應的線性組合映射是線性的，而且它的 skeleton 正好就是那個 n 元組。反過來，任何一個從 n 維座標空間出發的線性映射，都等於它自己 skeleton 的線性組合映射。",
 "證明兩半都很短。線性用的是跟前一集那個定理一樣的論證。至於 skeleton，把第 j 個單位向量餵進線性組合映射，只有第 j 項活下來。反過來，任何向量都是單位向量的線性組合，套上 T 再用線性，就回到線性組合映射。",
 "換個說法：從「W 裡的 n 元組」到「所有從 n 維座標空間到 W 的線性映射」，這個對應是一個雙射，而它的反函數就是取 skeleton。兩邊的資訊量完全一樣。",
 "書上說這是一個極其重要的定理，雖然看起來簡單，並且要讀者把它牢牢記住。skeleton 這個詞會一直用到第三章。下一集就從它最簡單的特例開始：上域是實數線的時候。",
]), "en": ("Chapter 1: Linear Transformations and the Skeleton", [
 "Start with a question. Real-valued functions on a set can be multiplied pointwise as well as added and scaled, and so can the continuous ones. With three operations available, why bother with vector spaces, which have only two?",
 "Because the most important mappings are exactly the ones that preserve those two. The book's example is the integral: it sends sums to sums and multiples to multiples, but it does not preserve products at all, since the integral of a product is not the product of the integrals.",
 "Another is the map sending a triple to a pair, each entry a combination of the three coordinates. Whether a linear system can be solved is essentially the theory of such maps. So we study vector spaces partly to study the maps that preserve their operations.",
 "The definition follows: a mapping from V to W is a linear transformation if it sends sums to sums and scalar multiples to scalar multiples. The two conditions combine into one: x times alpha plus y times beta goes to x times T alpha plus y times T beta.",
 "By induction this extends at once to any finite sum: a linear combination goes to the linear combination of the images, with exactly the same coefficients. The property of the integral is a special case of this equation.",
 "Now to find every linear map whose domain is coordinate n-space. Take a concrete one first: fix three functions and send a triple to the combination having its three entries as coefficients. This is plainly linear.",
 "What is interesting is that the three functions can be read back off the map. Feed in the vector with a one in the jth place and zeros elsewhere, and out comes the jth function. That n-tuple of images is what the book calls the skeleton of T.",
 "The theorem runs as follows. Given any n-tuple in W, the corresponding linear combination mapping is linear, and its skeleton is exactly that n-tuple. Conversely, every linear map out of coordinate n-space equals the linear combination mapping of its own skeleton.",
 "Both halves are short. Linearity repeats the previous episode's argument. For the skeleton, feeding in the jth unit vector leaves only the jth term. Conversely any vector is a combination of unit vectors, so applying T and using linearity gets us back.",
 "Put another way: the correspondence from n-tuples in W to linear maps from coordinate n-space into W is a bijection, and its inverse is taking the skeleton. The two sides carry exactly the same information.",
 "The book calls this a tremendously important theorem, simple though it may seem, and urges the reader to fix it in mind. The word skeleton stays with us for the first three chapters. The next episode starts from its simplest case, when the codomain is the real line.",
])},

# E08 — chapter 1, section 1, last part (book pp. 32-36 = PDF pp. 44-48):
# matrices, Theorem 1.3 and 1.4, the kernel, isomorphism, eigenvectors.
8: {"zh": ("第 1 章：矩陣、核與同構", [
 "先看最簡單的情形：上域是實數線。這時 skeleton 的每一個元素都只是一個數，所以整個 skeleton 就是一個數字 n 元組。把它寫成係數放在變數前面，這個線性泛函就是「係數乘座標再加起來」。",
 "所以 n 維座標空間上所有線性泛函，與這個空間自己有一個自然的一一對應：由泛函去取它在各個單位向量的值就得到那組係數，由係數去做加權和就得到泛函。",
 "接著看上域是 m 維座標空間的情形。這時 skeleton 的每一個元素都是一個 m 元組。把每個 m 元組畫成一直行，n 個 m 元組並排，就得到一個長方形的數字陣列。",
 "這個帶兩個指標的數組就叫 T 的矩陣，是 m 乘 n 的——m 列 n 行。矩陣唯一決定了 T，因為它的各行正好就是 T 的 skeleton。",
 "把線性組合映射攤開來算，就得到 m 個純量方程：第 i 個輸出等於「第 i 列的係數，分別乘上對應的輸入座標，再加起來」。這就是書上的定理，也是一般線性方程組的來歷。",
 "反過來，每一個 m 乘 n 的矩陣都決定一個線性映射，所以矩陣與線性映射之間也是雙射。線性泛函對應到只有一列的矩陣，也就是一列 n 行。",
 "還有一類特別的線性泛函叫座標泛函：在指標集上的函數空間裡，取第 i 個位置的值。它顯然是線性的——事實上，函數上的向量運算當初就是為了讓這些取值映射變成線性的，才那樣定義的。",
 "接下來是幾個結構上的結果。線性把線性擴張送到像的線性擴張，所以子空間的像還是子空間；而且子空間的原像也還是子空間。這兩件事之後會一直用到。",
 "被 T 送到零向量的那些向量，自己構成一個子空間，叫做零空間或核；T 的值域則是整個定義域的像。有了核就有一個很方便的判準：T 是嵌射，若且唯若它的核只有零向量。這比逐一去比對兩個向量省事得多。",
 "既線性又雙射的映射叫同構。兩個空間同構，意思是它們「有相同的形式」，作為抽象的向量空間根本就是同一個，只能靠它們有沒有的向量性質來區分。書上的例子是：n 維座標空間，與次數小於 n 的多項式所成的空間，是同構的。",
 "最後，當線性映射是從 V 到它自己的時候，會發生一些特別的事。可能有某個向量被送到自己的倍數，這時這個向量叫做特徵向量，那個倍數叫做特徵值。這條線索到第二章與第五章會再展開。",
]), "en": ("Chapter 1: Matrices, the Kernel and Isomorphism", [
 "Take the simplest case first: the codomain is the real line. Then every element of the skeleton is just a number, so the skeleton is an n-tuple of numbers. Written as coefficients in front of the variables, the functional is coefficients times coordinates, summed.",
 "So the linear functionals on coordinate n-space are in natural one-to-one correspondence with that space itself: evaluating a functional at the unit vectors gives the coefficients, and forming the weighted sum from the coefficients gives back the functional.",
 "Now let the codomain be coordinate m-space. Each element of the skeleton is then an m-tuple. Picture each m-tuple as a column, set the n of them side by side, and what appears is a rectangular array of numbers.",
 "That doubly indexed array is called the matrix of T, an m by n matrix, with m rows and n columns. The matrix determines T uniquely, because its columns are exactly the skeleton of T.",
 "Writing the combination mapping out gives m scalar equations: the ith output is the coefficients in the ith row, each multiplied by the matching input coordinate, and summed. That is the book's theorem, and it is where a general system of linear equations comes from.",
 "Conversely every m by n matrix determines a linear map, so matrices and linear maps correspond bijectively too. A linear functional matches a matrix with a single row, that is one row and n columns.",
 "Another special family is the coordinate functionals: on a function space over an index set, take the value at the ith place. These are plainly linear. In fact the vector operations on functions were defined precisely to make these evaluations linear.",
 "Now some structural results. A linear map carries a linear span onto the span of the images, so the image of a subspace is a subspace; and the preimage of a subspace is a subspace as well. Both facts get used constantly later.",
 "The vectors sent to zero form a subspace, the null space or kernel, and the range of T is the image of the whole domain. The kernel gives a test: T is injective exactly when its kernel is only the zero vector, far less work than comparing vectors in pairs.",
 "A map both linear and bijective is an isomorphism. Isomorphic spaces have the same form: as abstract spaces they are the same, told apart only by vector properties they do or do not have. The book pairs coordinate n-space with the polynomials of degree less than n.",
 "Finally, when a linear map goes from V to itself, special things can happen. Some vector may be carried to a multiple of itself, and then that vector is called an eigenvector and the multiple an eigenvalue. This thread is picked up again in chapters two and five.",
])},

# E09 — chapter 1, section 2, first half (book pp. 36-39 = PDF pp. 48-51):
# the coordinate correspondence, the four assumed geometric theorems, the
# scalar product, and the equation of a line.
9: {"zh": ("第 1 章：座標對應與純量積", [
 "這一節要把解析幾何的座標系接回向量空間。座標系讓我們能用向量的語言談直線與平面這些幾何對象，而這些幾何直觀反過來也會幫我們理解向量空間。所以先複習一下座標對應是怎麼建立的。",
 "先看直線。在一條直線上任選一個零點與一個相異的單位點，那麼線上每個點都對應到一個數：它的絕對值是該點到零點的距離，以零點到單位點那一段為單位；正負則看它與單位點在不在零點的同一側。",
 "三維的作法一樣。任選一個原點與三個單位點，四個點不共平面。每個單位點決定一條過原點的直線，這三條就是座標軸，而且每條軸上都已經有了剛才那種座標對應。",
 "現在給空間中任何一個點。過它、平行於第二與第三軸的那個平面，會交第一軸於一點，於是給出第一個座標；同樣的作法給出另外兩個。所以每個點決定一個三元組，這個對應就叫做這組軸系定義的座標對應。",
 "值得注意的是，三個單位點的座標三元組，正好就是那三個「只有一個位置是一、其他都是零」的向量。這一點等一下會反覆用到。",
 "接下來有四件關於座標對應的基本事實。嚴格說，它們要先當成幾何定理證出來，才能拿座標去處理幾何問題。但書上說這些幾何定理相當棘手，用中學那套幾何幾乎沒辦法講清楚，所以直接假設它們成立。",
 "第一件：這個座標對應是空間到三維座標空間的雙射。第二件：兩條線段等長、平行而且方向相同，若且唯若它們終點座標減起點座標的結果相同。把有向線段這個概念形式化之後，第二件事就寫成「兩條有向線段等價」。",
 "第三件：如果一個點不是原點，那麼另一個點落在過原點與它的那條直線上，若且唯若後者的座標是前者的純量倍數；而且那個純量正好就是後者在這條線上、以前者為單位點時的座標。",
 "第四件要求軸系是笛卡兒的，也就是三軸互相垂直、而且共用同一個長度單位。這時一段從原點出發的線段長度，就由歐氏範數給出——各座標平方和再開根號。這直接來自畢氏定理。",
 "把畢氏定理再用一次到原點與兩個點所成的三角形，就得到另一件事：兩段從原點出發的線段互相垂直，若且唯若它們座標的純量積等於零。純量積就是對應座標相乘再加起來。",
 "還有一個很好用的性質：把純量積的其中一個變數固定住，它對另一個變數是線性的。有了這個，直線的方程就出來了：過某一點、平行於某個方向的直線包含一個點，若且唯若座標差是那個方向的純量倍數。",
]), "en": ("Chapter 1: The Coordinate Correspondence and the Scalar Product", [
 "This section connects the coordinate systems of analytic geometry back to vector spaces. Coordinates let us treat lines and planes in vector terms, and the geometry repays us in intuition about vector spaces. We begin by reviewing how the correspondence is set up.",
 "Start with a line. Choose on it a zero point and a distinct unit point. Then each point gets a number: its size is the distance from the zero point, measured in units of the segment to the unit point, and its sign says which side it lies on.",
 "Three dimensions go the same way. Choose an origin and three unit points, the four not lying in a plane. Each unit point determines a line through the origin, and these three are the coordinate axes, each already carrying a correspondence of the kind just described.",
 "Now take any point of space. The plane through it parallel to the second and third axes meets the first axis, giving the first coordinate; the same construction gives the other two. So every point determines a triple, and that is the correspondence defined by the axis system.",
 "Worth noticing: the coordinate triples of the three unit points are exactly the vectors with a single one and zeros elsewhere. That fact gets used again and again shortly.",
 "There are four basic facts about the correspondence. Strictly they must be proved as geometry before coordinates can be used on geometric questions. But the book calls them tricky and almost impossible to discuss on the usual school treatment, so it simply assumes them.",
 "First: the correspondence is a bijection from space onto coordinate three-space. Second: two segments are equal in length, parallel and similarly directed exactly when endpoint minus starting coordinates agree. Formalized, that says the two directed segments are equivalent.",
 "Third: if a point is not the origin, then another point lies on the line through the origin and it exactly when the second set of coordinates is a scalar multiple of the first. Moreover that scalar is the coordinate of the second point on that line, taking the first as its unit point.",
 "The fourth assumes the axes are Cartesian: mutually perpendicular, with a common unit of distance. Then the length of a segment from the origin is the Euclidean norm, the square root of the sum of the squared coordinates. This follows directly from the Pythagorean theorem.",
 "Applying Pythagoras again, to the triangle on the origin and two points, gives another fact: two segments from the origin are perpendicular exactly when the scalar product of their coordinates is zero, that product being corresponding coordinates multiplied and summed.",
 "One more property is useful: hold either variable of the scalar product fixed and it is linear in the other. Then the equation of a line drops out: the line through a point parallel to a direction contains a point exactly when the coordinate difference is a multiple of that direction.",
])},

# E10 — chapter 1, section 2, second half (book pp. 39-43 = PDF pp. 51-55):
# the equation of a plane, dropping the scalar product for a linear
# functional, parallel translation, affine subspaces and hyperplanes.
10: {"zh": ("第 1 章：平面、平行移動與仿射子空間", [
 "現在換平面。過某一點、而且垂直於某個方向的平面，包含另一個點，若且唯若連接這兩點的線段垂直於那個方向。用上一集的第二與第四件事翻譯過來，就是「座標差與那個方向的純量積等於零」。",
 "把純量積對第一個變數的線性拿來展開，再把定值那一項記成一個數，平面的方程就變成「座標與方向的純量積等於某個常數」，也就是三個係數分別乘上三個座標再加起來等於常數。反過來，只要方向不是零向量，滿足這個方程的點集就是一個平面。",
 "但這裡有個問題。三維座標空間有一個自然的純量積，這在代數與幾何上都非常重要；可是大部分的向量空間並沒有自然的純量積。書上因此刻意在早期的向量理論裡完全不用它，要到第五章才回頭處理。",
 "所以要換一個解讀方式。係數乘座標再加起來這個東西，第一節已經講過：它就是三維座標空間上最一般的線性泛函。於是平面的方程可以完全不提純量積，改寫成「一個非零線性泛函在該點的值等於某個常數」。",
 "反過來也成立：給定任何一個非零線性泛函與任何一個數，滿足那個方程的點集都是一個平面。而係數三元組隨時可以從泛函讀回來——把三個單位向量分別餵進去就是了。",
 "接著找平行移動的向量形式。平面幾何裡談兩個平行而且同向的全等圖形時，常說把其中一個「沿著平面滑動」得到另一個，滑動時所有直線都保持與原來平行。",
 "這個描述可以講得更漂亮：所謂平行移動，就是每一條有向線段都滑到與它等價的線段。如果某個點滑到另一個點、原點滑到某個點，那麼由等價的條件，座標之間差的就是一個固定的向量。",
 "所以平行移動的座標形式，就是「加上一個常向量」。反過來，任何一個常向量給出的這種映射，都確實是一個平行移動。這件事在平面與空間都一樣成立。",
 "幾何上很明顯，平行移動把平面送到平面、直線送到直線；現在也可以給一個純代數的證明。方程是某個泛函等於常數的那個平面，經過平移之後，方程變成同一個泛函等於「原來的常數加上泛函在位移向量的值」，還是一個平面。",
 "現在把這些幾何名詞搬到座標空間上。方程是泛函等於某個常數的那個平面，通過原點若且唯若那個常數是零——而這時它正好是泛函的零空間，是一個子空間。所以座標空間裡的平面與直線，都是子空間的平移。",
 "這些推廣到任意實向量空間，就叫做仿射子空間——子空間的平移。非零線性泛函的零空間永遠是 n 減一維的，這種東西叫超平面。在三維座標空間裡超平面就是普通的幾何平面，但在平面裡，超平面是直線。",
]), "en": ("Chapter 1: Planes, Parallel Translation and Affine Subspaces", [
 "Now for planes. The plane through a point and perpendicular to a direction contains another point exactly when the segment joining them is perpendicular to that direction. By the second and fourth facts of the last episode, that means one scalar product is zero.",
 "Expanding by linearity in the first variable and naming the constant, the equation becomes the scalar product of coordinates with direction equal to that constant: three coefficients times three coordinates, summed. Conversely, if the direction is nonzero, that locus is a plane.",
 "But there is a problem. Coordinate three-space has a natural scalar product, extremely important both algebraically and geometrically; most vector spaces have none at all. The book therefore deliberately neglects it in the early vector theory, returning to it only in chapter five.",
 "So we look for another reading. Coefficients times coordinates, summed, is what section one identified as the most general linear functional on coordinate three-space. So the equation of a plane can drop the scalar product and become a functional taking a constant value.",
 "The converse holds too: given any nonzero linear functional and any number, the locus of that equation is a plane. And the coefficient triple can always be read back off the functional, by feeding in the three unit vectors.",
 "Next, the vector form of parallel translation. In plane geometry, when two congruent figures are parallel and similarly oriented, we often speak of obtaining one from the other by sliding the plane along itself so that every line stays parallel to where it was.",
 "That description can be put more elegantly: a parallel translation is one in which every directed segment slides to an equivalent segment. If one point slides to another and the origin slides to some point, then by the equivalence condition the coordinates differ by one fixed vector.",
 "So in coordinates a parallel translation is simply adding a constant vector. Conversely, the mapping given by any constant vector really is a parallel translation. This holds equally for the plane and for space.",
 "Geometrically it is clear that translations carry planes to planes, and now we can prove it algebraically. Take the plane whose equation is a functional equal to a constant; translating gives the same functional equal to that constant plus the functional at the shift vector.",
 "Now carry the terminology over to coordinate space. A plane whose equation is a functional equal to a constant passes through the origin exactly when that constant is zero, and then it is the null space of the functional. So planes and lines are translates of subspaces.",
 "In any real vector space these are the affine subspaces, translates of subspaces. The null space of a nonzero functional always has dimension n minus one, and such a set is a hyperplane. In coordinate three-space a hyperplane is an ordinary plane, but in the plane it is a line.",
])},

# E11 — chapter 1, section 3, first half (book pp. 43-46 = PDF pp. 55-58):
# product spaces, Theorem 3.1, Hom(V, W) and composition.
11: {"zh": ("第 1 章：積空間與 Hom(V, W)", [
 "前面看過：W 是向量空間、A 是任意集合時，所有從 A 到 W 的函數所成的空間，跟實值函數空間一樣是向量空間。加法逐點做，數乘也逐點做，向量律成立的理由一模一樣。",
 "但沒有理由每個指標都要用同一個 W。給一族用 I 編號的向量空間，它們的笛卡兒積定義成：所有定義域是 I、而且在每個 i 取的值都落在第 i 個空間裡的函數。",
 "書上舉了一個很具體的例子。單位球面上，每一點的切平面平移到原點就是一個子空間。那麼所有這些子空間的乘積裡的一個元素，就是在球面每一點指定一個平行於該點切平面的向量——也就是球面上的一個向量場。",
 "積空間上的第 j 個座標投影，還是在 j 取值。只是這時取到的值落在一個向量空間裡，而不是落在實數裡，所以叫它座標投影，而不是座標泛函。",
 "關鍵的一句是：積空間上的向量運算，被「所有座標投影都要是線性的」這個要求唯一決定。兩個元素的和，必須是那個在每個 j 的值等於兩者在 j 的值相加的元素；數乘也一樣。",
 "所以定理是：一族向量空間的笛卡兒積，恰好只有一種辦法做成向量空間，使得所有座標投影都線性。證明就是把之前那些公理檢查原封不動再走一遍——那些論證從來沒要求被加的函數值都落在同一個空間。",
 "接著是 Hom。當定義域本身是一個向量空間的時候，我們特別把所有線性映射從函數空間裡挑出來，這個子集就寫成 Hom V W。",
 "第一個定理是形式上的：Hom 是所有映射所成空間的一個子空間。兩個線性映射相加還是線性、乘上純量還是線性，而且零變換在裡面，所以非空。",
 "接下來是合成。兩個線性映射合起來還是線性的。這句話很基本，但它需要定義域與上域對得上；這一節的敘述都是這樣，論證簡單，可是被討論的對象會越來越複雜。",
 "同一個定理還說了兩件事：合成對加法有分配律，而且兩邊都成立；另外，合成與純量乘法可以交換次序。",
 "最後一個推論。把某個固定的 T 從右邊合成上去，這件事本身就是一個線性變換，從一個 Hom 空間到另一個 Hom 空間。而且如果 T 是同構，這個變換也是同構——因為拿 T 的反函數去合成就能還原。",
]), "en": ("Chapter 1: Product Spaces and Hom(V, W)", [
 "We have seen that when W is a vector space and A is any set, the space of all functions from A into W is a vector space in the same way the real-valued ones are. Addition is pointwise, and so is multiplication by scalars, for exactly the same reasons.",
 "But there is no reason to use the same W at every index. Given a collection of vector spaces indexed by I, their Cartesian product is defined as all functions with domain I whose value at each i lies in the ith space.",
 "The book gives a concrete example. On the unit sphere, the tangent plane at each point, translated to the origin, is a subspace. An element of the product of all of those assigns to each point of the sphere a vector parallel to the tangent plane there: a vector field.",
 "The jth coordinate projection on a product space is still evaluation at j. Here its values lie in a vector space rather than in the reals, so it is called a coordinate projection rather than a coordinate functional.",
 "The key point is that the vector operations on a product space are uniquely determined by requiring that all the coordinate projections be linear. The sum of two elements must be the one whose value at each j is the sum of their values there, and likewise for scalars.",
 "So the theorem: the Cartesian product of a collection of vector spaces can be made into a vector space in exactly one way so that the coordinate projections are all linear. The proof is the earlier axiom check verbatim, which never asked that the values lie in one space.",
 "Now Hom. When the domain is itself a vector space, we single out from the function space the subset consisting of all the linear mappings, and that subset is written Hom of V and W.",
 "The first theorem is a formality: Hom is a subspace of the space of all mappings. The sum of two linear maps is linear, so is a scalar multiple, and the zero transformation is in there, so it is nonempty.",
 "Next, composition. The composition of two linear maps is linear. The statement is elementary but it needs the obvious hypotheses on domains and codomains, which is the pattern here: simple arguments, but objects of growing complexity.",
 "The same theorem adds two more things: composition distributes over addition, on both sides, and composition commutes with multiplication by scalars.",
 "A last corollary. Composing with a fixed T on the right is itself a linear transformation from one Hom space to another. And if T is an isomorphism then so is that transformation, since composing with the inverse of T undoes it.",
])},

# E12 — chapter 1, section 3, second half (book pp. 46-52 = PDF pp. 58-64):
# Theorem 3.4, Hom(V) as an algebra, injections, and Theorems 3.6 and 3.7.
12: {"zh": ("第 1 章：投影、注入與線性映射的拆裝", [
 "先看一個定理：如果上域是積空間，那麼一個映射是線性的，若且唯若每一個座標投影接在它後面之後都是線性的。這把「往積空間裡送」化約成一堆各自獨立的問題。",
 "這件事把上一節接了回來。從 n 維座標空間到 m 維座標空間的線性映射，第 i 個座標投影接上去之後，得到的線性泛函，它的 skeleton 正好是矩陣的第 i 列。",
 "所以之前把一條向量方程換成 m 條純量方程時，我們做的就是「讀出第 i 個座標」。用代數的話說，是把一個線性映射換成一組線性映射，而剛才的定理保證這兩者等價。",
 "再看定義域與上域都是同一個 V 的情形。這個空間除了是向量空間，還對合成封閉，而合成永遠滿足結合律。加上分配律與純量的相容性，這種結構叫做代數。所以 Hom V 是一個代數。",
 "之前見過的實值函數空間也是代數，但那裡的乘法是可交換的。Hom V 的乘法通常不可交換，除非 V 是零空間，或者跟實數線同構。",
 "除了座標投影，積空間上還有第二類基本的線性映射，叫做注入。第 j 個注入把第 j 個因子裡的一個向量，送到「在第 j 個位置放它、其他位置全放零」的那個元素。",
 "投影與注入的關係就寫成兩條等式：投影接在自己的注入後面是恆等；接在別人的注入後面是零。而如果指標集是有限的，把每一個「注入接投影」加起來，正好就是恆等變換。",
 "舉個例子。一個從三維到二維的線性映射，矩陣是兩列三行。第一個座標投影接上去，得到的線性泛函的 skeleton 就是第一列，所以可以把它拆成兩個線性泛函。",
 "而把它們裝回去，用的正好就是剛才那條等式：兩個「注入接投影」加起來是恆等，套在原來的映射上就把它還原了。",
 "寫成一般形式：給定一族從共同定義域出發、分別到各個因子的線性映射，那麼恰好有一個到積空間的線性映射，使得每個座標投影接上去之後，得到的都是原來那一個。",
 "定義域是積空間的時候，也有一個對稱的說法。這個定理對任意積空間都成立，不管有限無限，而且它其實刻畫了積空間。書上承認這些看起來太形式，但說等到後面要處理更複雜的情況時就會用上。",
]), "en": ("Chapter 1: Projections, Injections and Taking Maps Apart", [
 "Start from a theorem: if the codomain is a product space, a mapping is linear exactly when each coordinate projection composed after it is linear. That reduces mapping into a product to a set of independent questions.",
 "It ties back to the last section. For a linear map from coordinate n-space to coordinate m-space, composing the ith coordinate projection after it gives the linear functional whose skeleton is the ith row of the matrix.",
 "So when we replaced one vector equation by m scalar equations, what we were doing was reading off the ith coordinate. In algebraic terms, replacing one linear map by a set of them, which the theorem says is equivalent.",
 "Now take the case where the domain and codomain are the same V. Besides being a vector space it is closed under composition, and composition is always associative. With the distributive laws and the scalar relation, that structure is called an algebra.",
 "The real-valued function spaces seen earlier are algebras too, but there multiplication is commutative. In Hom of V it is not, unless V is the trivial space or is isomorphic to the real line.",
 "Besides the coordinate projections there is a second class of basic linear maps on a product: the injections. The jth injection takes a vector in the jth factor to the element having that value at index j and zero everywhere else.",
 "Their relationship is two identities: a projection after its own injection is the identity, and after any other injection it is zero. And if the index set is finite, summing injection-after-projection over all indices gives the identity.",
 "An example. Take a linear map from three-space to the plane with a two by three matrix. Composing the first coordinate projection gives the linear functional whose skeleton is the first row, so the map comes apart into two linear functionals.",
 "Putting them back together uses exactly that identity: the two injection-after-projection terms sum to the identity, and applied to the original map they reassemble it.",
 "In general form: given a family of linear maps out of a common domain into the separate factors, there is exactly one linear map into the product such that composing each coordinate projection after it returns the one you started with.",
 "There is a symmetric statement when the domain is the product instead. The theorem holds for all product spaces, finite or not, and in fact characterizes them. The book grants this looks overly formal, but says it helps later in more complicated situations.",
])},

# E13 — chapter 1, section 4 (book pp. 52-56 = PDF pp. 64-68): affine
# subspaces, the quotient space, and Theorems 4.1 through 4.4.
13: {"zh": ("第 1 章：仿射子空間與商空間", [
 "這一節先看向量空間裡的「平面」，問它們被平移、彼此相交、被線性映射送過去之後會怎麼樣。然後把注意力縮到某個固定子空間的所有平移，會發現這一堆東西自己就是一個向量空間。",
 "定義是這樣：N 是子空間、α 是任意一個向量，那麼 N 的每個元素都加上 α 所成的集合，叫做含 α 的陪集，或者說過 α 且平行於 N 的仿射子空間。第二節說的平面，指的就是這種東西。",
 "第一個性質：如果 γ 落在 α 的陪集裡，那麼 γ 的陪集跟 α 的陪集是同一個。第二個：任兩個陪集要嘛完全相同、要嘛不相交。這正是第零章那個等價關係的特例——兩個向量等價，若且唯若它們的差落在 N 裡。",
 "再來幾條。任意多個仿射子空間的交集，要嘛是空的、要嘛還是仿射子空間。兩個仿射子空間的集合和，還是仿射子空間。",
 "線性映射把仿射子空間送到仿射子空間；反過來，仿射子空間的原像要嘛是空的、要嘛還是仿射子空間。",
 "平移本身不是線性的——它把零送到位移向量，而不是送到零。但它確實把仿射子空間送到仿射子空間。而「線性映射後面接一個平移」，就叫做仿射變換。",
 "現在固定一個子空間，看它所有平移所成的集合。書上的例子是：如果它是三維空間裡過原點的一條直線，那麼這個集合就是所有平行於它的直線。",
 "值得注意的是，這些平行直線自己構成一個向量空間：任兩條的集合和還是這一族裡的一條直線，非零倍數也是。這些平移把整個空間纖維化，而纖維所成的集合，自然就是一個向量空間。",
 "加法定義成集合和，數乘定義成集合的倍數，只有乘以零那一種要另外規定成 N 本身。於是「把向量送到它的陪集」這個自然映射，加法與數乘都保持。",
 "有一個定理省下逐條檢查的工夫：如果一個集合上有兩個像向量運算的運算，而且從某個向量空間有一個保持運算的滿射過去，那麼它就是向量空間。用它就知道商空間是向量空間，投影是滿的線性映射。",
 "這一節的重點定理是：如果一個線性映射的零空間包含某個子空間，那麼它可以唯一地分解成「先投影到商空間，再接一個線性映射」。另外，如果某個子空間被 T 送進自己，那麼商空間上就有唯一一個與 T 相容的映射。",
]), "en": ("Chapter 1: Affine Subspaces and Quotient Spaces", [
 "This section looks at the planes in a vector space and asks what happens to them under translation, intersection with each other, and images under linear maps. Then it narrows to the translates of one fixed subspace and finds that set is itself a vector space.",
 "The definition: for a subspace N and any vector, the set of everything in N shifted by that vector is called the coset containing it, or the affine subspace through it parallel to N. These are the general objects section two wanted to call planes.",
 "First property: if one vector lies in the coset of another, the two cosets are the same. Second: any two cosets are either identical or disjoint. This is the equivalence relation of chapter zero in a special case, with two vectors equivalent when their difference lies in N.",
 "More of them: the intersection of any family of affine subspaces is either empty or an affine subspace, and the set sum of two affine subspaces is again an affine subspace.",
 "A linear map carries an affine subspace to an affine subspace; and the preimage of an affine subspace is either empty or an affine subspace.",
 "Translation itself is not linear, since it carries zero to the shift vector rather than to zero. But it does carry affine subspaces to affine subspaces. A linear map followed by a translation is called an affine transformation.",
 "Now fix a subspace and look at the set of all its translates. The book's example: if it is a line through the origin in three-space, that set is all the lines parallel to it.",
 "What is worth noticing is that these parallel lines form a vector space in their own right: the set sum of any two is another line in the family, and so is a nonzero multiple. The translates fiber the space, and the set of fibers is naturally a vector space.",
 "Addition is set addition and scalar multiplication is the set product, with only multiplication by zero needing a separate stipulation, namely the subspace itself. The natural map sending a vector to its coset then preserves both operations.",
 "A theorem saves the work of checking every law: if a set carries two vectorlike operations and some vector space maps onto it preserving them, it is a vector space. So the quotient space is a vector space and the projection is a surjective linear map.",
 "The main theorem here: if the null space of a linear map includes a subspace, the map factors uniquely as the projection onto the quotient followed by a linear map. And if a subspace is carried into itself, there is a unique matching map on the quotient.",
])},

# E14 — chapter 1, section 5, first part (book pp. 56-58 = PDF pp. 68-70):
# direct sums, the even-odd decomposition, independence and complements.
14: {"zh": ("第 1 章：直和與補空間", [
 "書上說，現在到了這一章的核心。經常會發生這種事：研究某個向量空間上的現象時，冒出一族有限多個子空間，使得整個空間自然地同構於它們的乘積。",
 "在這個同構之下，積空間上的「注入接投影」變成 V 上的一族映射，而投影注入的等式就反映成三條：全部加起來是恆等、每一個接自己還是自己、不同的兩個相接是零。而那些子空間，就是它們各自的值域。",
 "定義是這樣：給定 V 的一族子空間，把「每個子空間各取一個向量」的元組送到它們的和，這是一個從乘積到 V 的線性映射。如果它是嵌射，就說這些子空間獨立；如果它是同構，就說 V 是它們的直和。",
 "所以 V 是直和，若且唯若這個映射既是嵌射又是滿射，也就是這些子空間既獨立、又生成整個 V。換個說法：V 裡每一個向量，都能唯一地寫成「每個子空間各出一項」的和。",
 "這樣的寫法存在，是因為它們生成 V；寫法唯一，是因為它們獨立。要兩件事同時成立才是直和。",
 "書上的例子很漂亮。取實數線上所有連續函數，偶函數所成的子集是子空間，奇函數所成的子集也是，而整個空間正好是這兩個的直和。",
 "作法是：任何一個函數，跟自己的鏡像平均起來就得到偶的部分，相減再除以二就得到奇的部分。而分解是唯一的，因為同時是偶又是奇的函數只有零。指數函數的偶奇分量，正好就是雙曲餘弦與雙曲正弦。",
 "因為嵌射等價於零空間只有零向量，獨立性就有一個好用的等價說法：如果每個子空間各取一個向量、加起來等於零，那麼每一個都必須是零。",
 "兩個子空間的情形特別簡單：它們獨立，若且唯若交集只有零向量。所以 V 是兩個子空間的直和，若且唯若 V 等於它們的和、而且它們只在零向量處相交。",
 "這時這兩個子空間互稱補空間。但要小心：一個子空間的補空間通常不唯一。在三維座標空間裡，真子空間就只有過原點的平面與過原點的直線兩種。",
 "如果兩個真子空間裡，一個是平面、另一個是不落在該平面上的直線，那麼它們互為補空間；而且在三維空間裡，這是唯一一種非平凡的互補配對。",
]), "en": ("Chapter 1: Direct Sums and Complements", [
 "The book says we now come to the heart of the chapter. It frequently happens that studying some phenomenon on a vector space turns up a finite collection of subspaces such that the space is naturally isomorphic to their product.",
 "Under that isomorphism, injection-after-projection on the product becomes a family of maps on V, and the identities are reflected as: they sum to the identity, each composed with itself gives itself, and different ones compose to zero. Each subspace is one of their ranges.",
 "The definition: given a family of subspaces, sending a tuple of vectors, one from each, to their sum is a linear map from the product into V. If that map is injective the subspaces are called independent; if it is an isomorphism, V is their direct sum.",
 "So V is the direct sum exactly when the map is both injective and surjective, that is, when the subspaces are both independent and span V. Restated: every vector of V is uniquely expressible as a sum with one term from each subspace.",
 "Such an expression exists because they span V, and it is unique because they are independent. It takes both to have a direct sum.",
 "The book's example is a pretty one. In the space of continuous functions on the line, the even functions form a subspace and so do the odd ones, and the whole space is the direct sum of the two.",
 "Given any function, averaging it with its own reflection gives the even part, and half the difference gives the odd part. The decomposition is unique because the only function both even and odd is zero. The even and odd parts of the exponential are the hyperbolic cosine and sine.",
 "Since injectivity is the same as having only zero in the null space, independence gets a convenient restatement: if one vector is taken from each subspace and they sum to zero, then every one of them is zero.",
 "For two subspaces it is especially simple: they are independent exactly when their intersection is only the zero vector. So V is the direct sum of two subspaces exactly when V is their sum and they meet only at zero.",
 "Two such subspaces are called complements of each other. But a warning: a subspace does not have a unique complement. In coordinate three-space the only proper subspaces are the planes through the origin and the lines through the origin.",
 "If two proper subspaces are one plane and one line not lying in that plane, then they are complementary; and in three-space those are the only nontrivial complementary pairs.",
])},

# E15 — chapter 1, section 5, second part (book pp. 58-61 = PDF pp. 70-73):
# the projection operators, Theorems 5.1 and 5.2, and idempotence.
15: {"zh": ("第 1 章：直和與投影算子", [
 "先補一個技術性的引理：如果兩個子空間獨立，而其中第二個自己又分解成一族獨立的子空間，那麼把它們全部合起來的那一族，在 V 裡也是獨立的。",
 "推論是：V 是前兩者的直和、而第二個又是後面那些的直和，兩件事合起來就得到 V 是全部這些的直和。所以直和可以一層一層拆下去。",
 "現在定義投影。V 是一族子空間的直和時，那個從乘積到 V 的映射是同構，所以有反函數。把第 j 個座標投影接在反函數後面，就得到一個從 V 到第 j 個子空間的線性映射。",
 "因為每個向量都唯一地寫成各子空間各出一項的和，這個映射就是把一個向量送到它在第 j 個子空間裡的那一份。書上把這一份叫做該向量的第 j 個分量，把這個映射叫做 V 到第 j 個子空間的投影。",
 "要注意「投影」這個詞在書裡已經出現三種不同的意思：笛卡兒積上的座標投影、商空間上的投影，還有現在這一個。三者互相有關，但確實不同；靠上下文分辨就好。",
 "定理是：這些投影的值域正好就是那些子空間、不同的兩個相接是零、而且全部加起來是恆等。這三條，正是積空間上那組等式在 V 裡的倒影。",
 "反過來的定理也成立。如果 V 上的一族線性映射滿足「加起來是恆等」與「不同的相接是零」，那麼把它們的值域取出來，V 就是這些值域的直和，而它們正好是對應的投影。",
 "這給了投影一個內在的刻畫。投影是冪等的——自己接自己還是自己；等價地說，它在自己的值域上就是恆等。而它的零空間，正好是其他那些子空間的和。",
 "反過來也對：只要 V 上一個線性映射是冪等的，那麼 V 就是它的值域與零空間的直和，而它正好是值域上的投影。所以「冪等」與「是一個投影」，講的是同一件事。",
 "證明很短。設 Q 是恆等減去 P，那麼 P 接 Q 等於 P 減去 P 的平方，也就是零，於是套用前一個定理；而 Q 的值域正好是 P 的零空間。",
 "兩個相加等於恆等、而且兩邊相接都是零的映射，叫做一對互補投影。最後書上補了一個細節：嚴格說，把那些投影加起來時上域對不上，要引進一個把子空間看成 V 的子集的恆等注入，才算完全嚴密。",
]), "en": ("Chapter 1: Direct Sums and Projection Operators", [
 "First a technically useful lemma: if two subspaces are independent, and the second of them is itself split into an independent family, then the whole collection taken together is independent in V.",
 "The corollary: V being the direct sum of the first two, together with the second being the direct sum of the rest, gives V as the direct sum of all of them. So direct sums can be taken apart a layer at a time.",
 "Now the projections. When V is the direct sum of a family, the map from the product to V is an isomorphism, so it has an inverse. Composing the jth coordinate projection after that inverse gives a linear map from V into the jth subspace.",
 "Since every vector is uniquely a sum with one term from each subspace, that map sends a vector to its own share in the jth one. The book calls that share the jth component, and the map the projection of V onto the jth subspace.",
 "Note that the word projection now has three different meanings in this book: the coordinate projection on a Cartesian product, the projection onto a quotient space, and this one. They are related but distinct, and context settles which is meant.",
 "The theorem: the ranges of these projections are exactly those subspaces, different ones compose to zero, and all of them sum to the identity. Those three are the reflection in V of the identities that held on the product space.",
 "The converse holds as well. If a family of maps on V sums to the identity and different ones compose to zero, then taking their ranges, V is the direct sum of those ranges and the maps are the corresponding projections.",
 "That gives projections an intrinsic characterization. They are idempotent: each composed with itself gives itself, equivalently each is the identity on its own range. And the null space of one is the sum of all the other subspaces.",
 "The converse holds too: if any linear map on V is idempotent, then V is the direct sum of its range and its null space, and the map is the projection onto its range. So being idempotent and being a projection are the same thing.",
 "The proof is short. Set Q to be the identity minus P; then P composed with Q is P minus P squared, which is zero, so the previous theorem applies, and the range of Q is exactly the null space of P.",
 "A pair of maps summing to the identity whose composites both ways are zero is called a pair of complementary projections. The book closes on a fine point: strictly, summing those projections mismatches the codomains, and an identity injection is needed to make it exact.",
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
 # The count was recomputed from 155 to 169 on 2026-08-04 (see OUTLINE.md).
 # It appears in four places for this episode -- here, the scene's own closing
 # caption, the narration (it is spoken aloud), and the manifest description.
 10: "169  ·  2 – 4 pp / ep  ·  Ch 0 § 1 – 3",
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

4: {
 0: "F : A × B → C        hˣ ( y )  =  F ( x , y )",
 1: "φ : A → Cᴮ        θ : B → Cᴬ        F : A × B → C",
 2: "t = { tᵢⱼ }        tᵢ  ↦  ⟨ tᵢ₁ , … , tᵢₙ ⟩        tⱼ  ↦  ⟨ t₁ⱼ , … , tₘⱼ ⟩",
 3: "⟨ f₁ , … , fₙ ⟩        a  ↦  ⟨ f₁ ( a ) , … , fₙ ( a ) ⟩  :  A → Bⁿ",
 4: "F ( p , l ) ∈ { 0 , 1 }        l  ↦  { p : F = 1 }        p  ↦  { l : F = 1 }",
 5: "hˣ  =  F ( x , · )        f  =  f ( · )        Dξ F ( · )",
 6: "⋃ ℱ  =  { x : ( ∃A ∈ ℱ ) ( x ∈ A ) }        x ∈ ⋂ᵢ Aᵢ  ⇔  ( ∀i ) ( x ∈ Aᵢ )",
 7: "A′ = { x ∈ S : x ∉ A }        ( ⋂ᵢ Aᵢ )′  =  ⋃ᵢ ( Aᵢ′ )",
 8: "f ⁻¹ [ ⋃ᵢ Bᵢ ] = ⋃ᵢ f ⁻¹ [ Bᵢ ]        f ⁻¹ [ B′ ] = ( f ⁻¹ [ B ] )′",
 9: "⋃ ℱ = A  ,  Aᵢ ∩ Aⱼ = ∅        π : A → ℱ  ,  x ↦ x̄",
 10: "x ∼ x    x ∼ y ⇒ y ∼ x    x ∼ y & y ∼ z ⇒ x ∼ z        g  =  ḡ ∘ π",
},

5: {
 0: "Ch 1 :  V          Ch 2 :  dim V < ∞",
 1: "OA  +  OB  =  OP",
 2: "x ( OA )  =  OB        | OB |  =  | x | · | OA |",
 3: "( OA + OB ) + OC  =  OA + ( OB + OC )  =  OX",
 4: "⟨ x₁ , x₂ , x₃ ⟩ + ⟨ y₁ , y₂ , y₃ ⟩ = ⟨ x₁+y₁ , x₂+y₂ , x₃+y₃ ⟩",
 5: "x  :  { 1 , 2 , 3 } → ℝ        xᵢ  =  x ( i )",
 6: "A1 ( α+β )+γ = α+( β+γ )   A2 α+β = β+α   A3 α+0 = α   A4 α+β = 0",
 7: "S1 ( xy )α = x( yα )   S2 ( x+y )α = xα+yα   S3 x( α+β ) = xα+xβ   S4 1α = α",
 8: "ℝᴬ  =  { f : A → ℝ }        ( f + g ) ( a )  =  f ( a ) + g ( a )",
 9: "W ⊂ V  ,  W ≠ ∅        α , β ∈ W  ⇒  α + β ∈ W   &   xα ∈ W",
 10: "𝒞 [ a , b ]  ⊂  ℝ [ a , b ]        { x : x₁ + x₂ = 0 }  ⊂  ℝ²",
},

6: {
 0: "( α₁ + α₂ ) + α₃  =  α₁ + ( α₂ + α₃ )  =  α₂ + ( α₃ + α₁ )  =  …",
 1: "Σ αᵢ    ( i ∈ I )",
 2: "I = { 1 , … , n }        Σ cᵢⱼ sⁱ tʲ    ( i + j ≤ 5 )",
 3: "Lⱼₖ  =  Jⱼ ∩ Kₖ        ξⱼₖ  =  Σ αᵢ    ( i ∈ Lⱼₖ )",
 4: "β  =  Σ xᵢ αᵢ    ,    αᵢ ∈ A",
 5: "Σ cᵢ tⁱ        3 · sin t + 0 · cos t + ( −1 ) · eᵗ    →    ⟨ 3 , 0 , −1 ⟩",
 6: "L  =  { ⟨ s , s + t , s − t ⟩  :  ⟨ s , t ⟩ ∈ ℝ² }",
 7: "L ( A )  ⊂  V        A ⊂ M  ⇒  L ( A ) ⊂ M",
 8: "( Σ xᵢαᵢ ) + ( Σ yᵢαᵢ ) = Σ ( xᵢ + yᵢ ) αᵢ        c ( Σ xᵢαᵢ ) = Σ ( cxᵢ ) αᵢ",
 9: "( Σ₁ⁿ xᵢαᵢ ) + ( Σ₁ᵐ yⱼβⱼ )  =  Σ₁ⁿ⁺ᵐ xᵢαᵢ",
 10: "δ ʲ  =  ⟨ 0 , … , 1 , … , 0 ⟩        x  =  Σ₁ⁿ xᵢ δ ⁱ",
},

7: {
 0: "ℝᴬ  :  f + g  ,  x f  ,  f g          V  :  α + β  ,  x α",
 1: "T ( f ) = ∫ f        T ( f + g ) = T f + T g        T ( f g )  ≠  T f · T g",
 2: "y₁ = 2x₁ − x₂ + x₃        y₂ = x₁ + 3x₂ − 5x₃",
 3: "T ( α + β ) = T α + T β    T ( xα ) = x T α        T ( xα + yβ ) = x Tα + y Tβ",
 4: "T ( Σ xᵢ αᵢ )  =  Σ xᵢ T ( αᵢ )",
 5: "x  ↦  Σ₁³ xᵢ fᵢ        f₁ = sin  ,  f₂ = cos  ,  f₃ = exp",
 6: "T ( δ ʲ )  =  fⱼ        skeleton  =  { T ( δ ⁱ ) }₁ⁿ",
 7: "Lα ( x )  =  Σ₁ⁿ xᵢ αᵢ        skeleton ( Lα )  =  α        T  =  L β",
 8: "T ( δ ʲ ) = Σ δ ʲᵢ βᵢ = βⱼ        T ( x ) = T ( Σ xᵢ δ ⁱ ) = Σ xᵢ βᵢ",
 9: "α  ↦  Lα  :  Wⁿ  ⟷  { T : ℝⁿ → W }        T  ↦  skeleton ( T )",
 10: "W = ℝ    ⇒    skeleton  ∈  ℝⁿ",
},

8: {
 0: "bᵢ = F ( δ ⁱ )        F ( x )  =  Σ₁ⁿ bᵢ xᵢ",
 1: "{ F : ℝⁿ → ℝ }   ⟷   ℝⁿ",
 2: "βⱼ  =  T ( δ ʲ )  ∈  ℝᵐ        t  =  { tᵢⱼ }",
 3: "t  :  m × n        columns ( t )  =  skeleton ( T )",
 4: "yᵢ  =  Σⱼ₌₁ⁿ tᵢⱼ xⱼ        ( i = 1 , … , m )",
 5: "{ t : m × n }  ⟷  { T : ℝⁿ → ℝᵐ }        F  :  1 × n",
 6: "πᵢ ( f )  =  f ( i )        πᵢ ( s f + t g ) = s πᵢ ( f ) + t πᵢ ( g )",
 7: "T [ L ( A ) ]  =  L ( T [ A ] )        T ⁻¹ [ Y ]  ⊂  V",
 8: "N ( T ) = T ⁻¹ ( 0 )        R ( T ) = T [ V ]        T  inj  ⇔  N ( T ) = { 0 }",
 9: "⟨ c₁ , … , cₙ ⟩  ↦  Σ₀ⁿ⁻¹ cᵢ₊₁ xⁱ        ℝⁿ  ≅  { deg < n }",
 10: "T ( α )  =  x α        α  :  eigenvector        x  :  eigenvalue",
},

9: {
 0: "𝔼³   ⟷   ℝ³",
 1: "O  ,  Q        X  ↦  x        | x |  =  | OX | / | OQ |",
 2: "O , Q₁ , Q₂ , Q₃        L₁ , L₂ , L₃",
 3: "θ  :  X  ↦  x  =  ⟨ x₁ , x₂ , x₃ ⟩",
 4: "θ ( Q₁ ) = δ ¹    θ ( Q₂ ) = δ ²    θ ( Q₃ ) = δ ³",
 5: "1 )  θ  :  𝔼³ → ℝ³",
 6: "2 )   AB ∼ XY   ⇔   b − a  =  y − x",
 7: "3 )   Y ∈ OX   ⇔   y  =  t x        t  =  coord ( Y )",
 8: "4 )   | OX |  =  ( Σ₁³ xᵢ² ) ¹ᐟ²",
 9: "OX ⊥ OY   ⇔   ( x , y ) = 0        ( x , y )  =  Σ₁³ xᵢ yᵢ",
 10: "( c x + d y , z ) = c ( x , z ) + d ( y , z )        x  =  t a + b",
},

10: {
 0: "( x − b , a )  =  0",
 1: "( x , a )  =  l        Σ₁³ aᵢ xᵢ  =  l",
 2: "ℝ³  :  ( x , y )          V  :  —",
 3: "f ( x )  =  l        f  :  ℝ³ → ℝ  ,  f ≠ 0",
 4: "aᵢ  =  f ( δ ⁱ )        f ( x ) = f ( Σ xᵢ δ ⁱ ) = Σ xᵢ aᵢ",
 5: "OX  ∼  BY",
 6: "x  =  y − b",
 7: "x  ↦  y  =  x + b",
 8: "f ( y − b ) = l   ⇔   f ( y ) = l + f ( b )        N  =  M + b",
 9: "l = 0   ⇔   0 ∈ M        M  =  N ( f )  +  b        { t a + b }  =  { t a } + b",
 10: "dim N ( f )  =  n − 1        ℝ³  :  plane          ℝ²  :  line",
},

11: {
 0: "Wᴬ  =  { f : A → W }        ( f + g ) ( a )  =  f ( a ) + g ( a )",
 1: "∏ᵢ Wᵢ  =  { f  :  dom f = I  ,  f ( i ) ∈ Wᵢ }",
 2: "S = { x : Σ₁³ xᵢ² = 1 }        Wₓ  ⊂  ℝ³        ∏ₓ ∈ S Wₓ",
 3: "πⱼ ( f )  =  f ( j )   ∈   Wⱼ",
 4: "πⱼ ( f + g )  =  πⱼ ( f ) + πⱼ ( g )        πⱼ ( x f )  =  x πⱼ ( f )",
 5: "∏ᵢ Wᵢ   :   unique",
 6: "Hom ( V , W )   ⊂   Wⱽ",
 7: "( S + T ) ( xα + yβ )  =  x ( S + T ) ( α )  +  y ( S + T ) ( β )",
 8: "T ∈ Hom ( V , W )  ,  S ∈ Hom ( W , X )   ⇒   S ∘ T ∈ Hom ( V , X )",
 9: "( S₁ + S₂ ) ∘ T = S₁∘T + S₂∘T        c ( S ∘ T ) = ( cS ) ∘ T = S ∘ ( cT )",
 10: "S  ↦  S ∘ T   :   Hom ( W , X )  →  Hom ( V , X )",
},

12: {
 0: "T : V → ∏ᵢ Wᵢ   linear   ⇔   πᵢ ∘ T   linear   ( ∀i )",
 1: "skeleton ( πᵢ ∘ T )  =  row i of  t",
 2: "y = T ( x )        ⇔        yᵢ = Σⱼ tᵢⱼ xⱼ",
 3: "A ∘ ( B ∘ C ) = ( A ∘ B ) ∘ C        A ∘ ( B + C ) = A∘B + A∘C",
 4: "Hom ( V )   :   algebra        S ∘ T  ≠  T ∘ S",
 5: "θⱼ ( α )  =  ⟨ 0 , … , α , … , 0 ⟩",
 6: "πⱼ ∘ θⱼ = Iⱼ        πⱼ ∘ θᵢ = 0   ( i ≠ j )        Σₖ θₖ ∘ πₖ = I",
 7: "t = [ 2 , −1 , 1 ; 1 , 1 , 4 ]        l₁ = π₁ ∘ T        l₂ = π₂ ∘ T",
 8: "( θ₁ ∘ π₁ + θ₂ ∘ π₂ ) ( T ( x ) )  =  T ( x )",
 9: "Tᵢ ∈ Hom ( V , Wᵢ )   ⇒   ∃ ! T ,   Tᵢ = πᵢ ∘ T        T = Σ θᵢ ∘ Tᵢ",
 10: "T = Σⱼ Tⱼ ∘ πⱼ        Tⱼ ∈ Hom ( Vⱼ , W )",
},

13: {
 0: "N ⊂ V          N + α",
 1: "N + α  =  { ξ + α  :  ξ ∈ N }        ᾱ  =  N + α",
 2: "γ ∈ ᾱ  ⇒  γ̄ = ᾱ        ᾱ = β̄   or   ᾱ ∩ β̄ = ∅        α ∼ β ⇔ α − β ∈ N",
 3: "⋂ᵢ Aᵢ  :  ∅  or  affine        A + B  :  affine",
 4: "T [ A ]  :  affine        T ⁻¹ [ B ]  :  ∅  or  affine",
 5: "Sα ( ξ ) = ξ + α        Sα ( 0 ) = α  ≠  0        ξ ↦ T ( ξ ) + β",
 6: "N  =  { t a }        W  =  { N + α  :  α ∈ V }",
 7: "ᾱ  +ₛ  β̄   =   α + β  ‾",
 8: "π ( α + β ) = π ( α ) + π ( β )        π ( t α ) = t π ( α )        0̄ = N",
 9: "T : V → W   onto ,  T ( sα + tβ ) = s T α + t T β   ⇒   W   vector space",
 10: "M ⊂ N ( T )   ⇒   T = S ∘ π   ,   S ∈ Hom ( V / M , W )",
},

14: {
 0: "V  ≅  ∏₁ⁿ Vᵢ",
 1: "Σ Pᵢ = I        Pⱼ ∘ Pⱼ = Pⱼ        Pᵢ ∘ Pⱼ = 0  ( i ≠ j )        Vᵢ = R ( Pᵢ )",
 2: "π : ⟨ α₁ , … , αₙ ⟩ ↦ Σ₁ⁿ αᵢ        π  inj :  independent",
 3: "V  =  V₁ ⊕ … ⊕ Vₙ   ⇔   π   iso",
 4: "α  =  Σ₁ⁿ αᵢ   ,   αᵢ ∈ Vᵢ   ,   unique",
 5: "V = 𝒞 ( ℝ )        Vₑ : f ( −x ) = f ( x )        Vₒ : f ( −x ) = − f ( x )",
 6: "eˣ  =  ( eˣ + e⁻ˣ ) / 2  +  ( eˣ − e⁻ˣ ) / 2  =  cosh x + sinh x",
 7: "αᵢ ∈ Vᵢ  &  Σ₁ⁿ αᵢ = 0   ⇒   αᵢ = 0   ( ∀i )",
 8: "M , N   independent   ⇔   M ∩ N = { 0 }",
 9: "V = M ⊕ N   ⇔   V = M + N   &   M ∩ N = { 0 }",
 10: "ℝ³  =  N ⊕ L        ξ  =  η + λ",
},

15: {
 0: "V₁ , V₀   ind .        V₀ = ⊕₂ⁿ Vᵢ        ⇒   { Vᵢ }₁ⁿ   ind .",
 1: "V = V₁ ⊕ V₀   &   V₀ = ⊕₂ⁿ Vᵢ    ⇒    V = ⊕₁ⁿ Vᵢ",
 2: "Pⱼ  =  πⱼ ∘ π ⁻¹   :   V → Vⱼ",
 3: "α = Σ₁ⁿ αᵢ        Pⱼ ( α )  =  αⱼ",
 4: "∏ Wᵢ  :  πⱼ          V / N  :  π          ⊕ Vᵢ  :  Pⱼ",
 5: "R ( Pᵢ ) = Vᵢ        Pᵢ ∘ Pⱼ = 0  ( i ≠ j )        Σ₁ⁿ Pᵢ = I",
 6: "Σ₁ⁿ Pᵢ = I  &  Pᵢ ∘ Pⱼ = 0    ⇒    V = ⊕₁ⁿ R ( Pᵢ )",
 7: "Pᵢ ∘ Pᵢ  =  Pᵢ        N ( Pᵢ )  =  Σⱼ ≠ ᵢ Vⱼ",
 8: "P ∘ P = P    ⇒    V  =  R ( P )  ⊕  N ( P )",
 9: "Q = I − P        P ∘ Q  =  P − P ∘ P  =  0        R ( Q ) = N ( P )",
 10: "P + Q = I        P ∘ Q = Q ∘ P = 0        π̄ⱼ = ιⱼ ∘ πⱼ",
},

}
