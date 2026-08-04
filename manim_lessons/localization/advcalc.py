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
 # The uploaded E00 still shows 155 here; the count was recomputed to 169 on
 # 2026-08-04 (see series/advcalc/OUTLINE.md). Corrected for any re-render.
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

}
