# advcalc E85 — 第 7 章：張量積與共變張量

Chapter 7: Tensor Products and Covariant Tensors

依據 Lynn H. Loomis & Shlomo Sternberg, *Advanced Calculus*, revised edition, Jones and Bartlett, 1990。本集對應第 7 章第 1 節「雙線性泛函」與第 2 節「多重線性泛函」（書頁 305–308）。**第 7 章整章沒有習題**：305 到 320 逐頁核過，九節裡一個 EXERCISES 標題都沒有，所以這一集不示範任何習題。章首自己說這一章「主要是備查用的，不期待讀者細讀證明」。

- 場景檔：`manim_lessons/lessons/advcalc/advcalc_e85_tensor.py`（`AdvCalcE85ZH` / `AdvCalcE85EN`）
- 腳本與公式：`manim_lessons/localization/advcalc.py`（`TOPICS_ADVCALC[85]` / `FORMULAS_ADVCALC[85]`）
- 配音：`manim_lessons/samples/audio_e85/`（zh-TW `-4%`、en `-4%`）
- 片長：中文 255.4 秒（4:15）／英文 207.9 秒（3:27）
- YouTube（私人）：中文 —／英文 —（尚未渲染）

## 這兩節在做什麼

**第 1 節只做一件事：把「所有雙線性泛函」這個集合本身當成一個向量空間看。** V 與 W 有限維時，V × W 上的雙線性泛函全體顯然對加法與純量乘法封閉，書上把這個空間記作 V 星與 W 星的**張量積**：

```
V * ⊗ W *   =   { f  :  V × W → ℝ ,  在每一個變數上線性 }
```

「在每一個變數上線性」不等於「線性」。固定 η 之後 ξ ↦ f ( ξ , η ) 是線性的，固定 ξ 之後也是，但兩個一起動就是二次的——這是第 2 拍那條拋物線要講的事。

**定理 1.1** 說，這個空間有三個互相自然同構的描述：

```
V * ⊗ W *   ≅   Hom ( V , W * )   ≅   Hom ( W , V * )
```

對應是 f ↦ ( α ↦ f _ α )，其中 f _ α ( ξ ) = f ( ξ , α )。**第 1 章定理 6.1 已經做掉一半**：它說這個對應是雙射。第 7 章補的只有「這個對應本身是線性的」，也就是 f + g 與 c f 被送到對應的和與純量倍上去——所以它是同構，不只是雙射。把兩個變數的角色對調就得到另外那一個同構，在座標上就是轉置。

**初等張量**定義成

```
( γ ⊗ λ ) ( ξ , η )   =   γ ( ξ )  ·  λ ( η )
```

長這個樣子的雙線性泛函叫做**初等的**。書上順手記下一件事：f 是初等的，若且唯若它在 Hom ( V , W * ) 那邊對應的映射是一個 **dyad**，也就是秩一。這一句在畫面上就是兩個真的算出秩來的矩陣。

**定理 1.2** 給出基底。取 V 與 W 的基底 α ᵢ、β ⱼ 與對偶基底 μ ᵢ、ν ⱼ，那 m n 個初等泛函就是一組基底：

```
f   =   Σ ᵢ ⱼ   t ᵢ ⱼ   ( μ ᵢ ⊗ ν ⱼ )            t ᵢ ⱼ   =   f ( α ᵢ , β ⱼ )
dim ( V * ⊗ W * )   =   m n
```

證明只是把矩陣展開式 f ( ξ , η ) = Σ t ᵢ ⱼ x ᵢ y ⱼ 讀成 ( μ ᵢ ⊗ ν ⱼ ) ( ξ , η ) = x ᵢ y ⱼ 的線性組合。書上還註明這與第 2 章第 4 節末尾談 Hom ( V , W ) 的基底完全是同一件事。

**第 2 節把這一切推到 n 個位置。** f 從 V ₁ × ⋯ × V ₙ 映到 ℝ，固定其他變數時對每一個變數都線性，全體記作 V ₁ * ⊗ ⋯ ⊗ V ₙ *。為了讓記號簡單，也因為這才是後面真正要用的情形，**讓這 n 個空間全是同一個 V**：

```
( V * ) ⊗ ⁿ   =   V *  ⊗  ⋯  ⊗  V *            （n 個因子）
```

叫做 **n 階共變張量空間**。把每個 ξ ᵢ 照基底展開，再逐個變數用線性，就得到

```
f ( ξ ₁ , … , ξ ₙ )   =   Σ ₚ ∈ m̄ ⁿ   x ¹ ₚ ₁ ⋯ x ⁿ ₚ ₙ   f ( α ₚ ₁ , … , α ₚ ₙ )
```

和式跑遍所有 n 元組 p，而 m̄ ⁿ 就是「從 1 到 n 映到 1 到 m 的所有函數」這個集合。用對偶基底做出的初等多重線性泛函，在基底上就是 Kronecker 符號：

```
μ ᵣ ( α ₚ ₁ , … , α ₚ ₙ )   =   0   ( p ≠ r )            =   1   ( p = r )
```

（書上這個下標用 q，畫面上寫 r，理由見下面。）這一條就是為什麼係數可以一眼讀出來：把展開式代進第 r 組基底向量，除了第 r 項以外全被殺掉。於是有**定理 2.1 與它的推論**：

```
f   =   Σ ₚ   c ₚ  μ ₚ            c ₚ   =   f ( α ₚ ₁ , … , α ₚ ₙ )
dim ( V * ) ⊗ ⁿ   =   m ⁿ
```

書上明說嚴格的證明要對 n 做歸納，而歸納那一步得把一個雙重和寫成單一和，靠的是 m̄ ⁿ × m̄ 與 m̄ ⁿ ⁺ ¹ 之間的一一對應：一個 n 元組配上一個指標，就是一個 n 加一元組。

**為什麼下一集從置換開始**：有了基底就可以問哪些張量是對稱的、哪些是交錯的，而「交錯」是用置換的正負號定義的，所以第 3 節得先把 S ₙ 與正負號建起來。

### 下標為什麼寫 r 不寫 q

Unicode 有下標的 r（U+1D63 ᵣ），**沒有下標的 q**。畫面上第 8 到第 10 拍整片都是真正的上下標，照書寫 q 就只能寫成字面上的底線 `μ _ q`。所以場景檔與公式列一律把第二個元組指標寫成 r，數學內容不變。

## 這一集用的例子

整集跑同一個具體例子：**V 是三維、W 是二維**，f 是矩陣 T 給的雙線性泛函。

```
T   =   ( +2  −1  ;   0  +3  ;  +1  +2 )              m = 3 ,  n = 2 ,  m n = 6
```

雙線性泛函在模組裡一律以「兩個座標向量的函數」存在，從來不以矩陣存在；矩陣是用 `gram` 把函數代到基底對上**算回來**的（就是書上的 t ᵢ ⱼ = f ( α ᵢ , β ⱼ )）。所以下表每一列的兩邊都是分別算出來的，相等才有意義。

| 要驗的事 | 算出來的數字 |
|---|---|
| 把 f 代到基底對上再組回矩陣，等於原來的 T | 差 0.0e+00 |
| 固定第二個變數，f 沿參數走是一條直線 | 斜率 f ( ξ ′ , η ) = +2 |
| 固定第一個變數，f 沿參數走是一條直線 | 斜率 f ( ξ , η ′ ) = +1 |
| **那兩條線憑什麼不一樣** | **斜率 +2 ≠ +1**，所以是兩條線，不是一條畫兩次 |
| 兩個變數一起動是二次的 | c ₀ = +3、c ₁ = +3、c ₂ = f ( ξ ′ , η ′ ) = +2 ≠ 0 |
| Φ ( f + g ) = Φ f + Φ g | 殘差 0.0e+00 |
| Φ ( c f ) = c Φ f（c = -1.5） | 殘差 0.0e+00 |
| 角色對調就是轉置 | 殘差 0.0e+00 |
| 從係數表組回 f 就是 f（所以 Φ 是雙射） | 243 對整數向量上最大差 0.0e+00 |
| γ ⊗ λ 的表就是外積 | γ = ( +1 −2 +3 )、λ = ( +2 +1 ) → ( +2 +1 ; −4 −2 ; +6 +3 ) |
| **初等（dyad）的秩是一** | rank = 1，σ ₂ = 7.3e-16 |
| **例子裡那個 f 不是初等的** | rank = 2，σ ₂ = 2.236 |
| f = Σ t ᵢ ⱼ ( μ ᵢ ⊗ ν ⱼ ) 逐點成立 | 243 對整數向量上最大差 0.0e+00 |
| 六個初等泛函獨立（6 × 6 取值矩陣） | det = +544 |
| 初等三重線性泛函在三個位置上各自線性 | 二階差 0.0e+00 |
| **三個位置真的是三個不同的映射** | Δ ⱼ = -10 , +4 , -4，三個都不同 |
| n 元組的個數是一個一個數出來的，不是幂算的 | \| m̄ ¹ \| = 3、\| m̄ ² \| = 9、\| m̄ ³ \| = 27 |
| 跑遍 9 個二元組的和式 = 直接算的值 | -6 與 -6，差 0.0e+00 |
| μ ᵣ 在 p ≠ r 時是零 | 七十二個非對角格的最大值 0.0e+00 |
| μ ᵣ 在 p = r 時是一 | 九個對角格的最小值 1 |
| 那張 9 × 9 的表是單位矩陣 | det = +1 |
| 係數 c ᵣ 真的還原 f 在第 r 組基底上的值 | 九個 r 全部相符 |
| 雙重和 = 單一和（27 個隨機整數） | +5 與 +5，差 0.0e+00 |
| ⟨ p , j ⟩ ↦ r 真的是一一對應 | 排序後的 9 × 3 個 ⟨ p , j ⟩ 與 27 個三元組逐項相同 |
| 二階張量唯一拆成對稱加反對稱 | \| S + A − C \| = 0.0e+00、\| S ᵗ − S \| = 0.0e+00、\| A ᵗ + A \| = 0.0e+00 |
| 兩塊的維數加起來是 m ² | 6 + 3 = 9 |

**沒有有限差分，也沒有容差。** 這一集的每一個殘差都是整數算術或精確的線性代數，所以表裡的 0.0e+00 就是字面上的零；唯一不是零的是 σ ₂ 的 7.3e-16，那是 SVD 的浮點誤差。

## 這一輪抓到的錯

- **第 2 拍原本把兩條直線畫成同一條。** 一開始取 ξ = ( 1 , 0 , 1 )、ξ ′ = ( 0 , 1 , 1 )、
  η = ( 1 , 0 )、η ′ = ( 0 , 1 )，算出來 f ( ξ ′ , η ) 與 f ( ξ , η ′ ) **都等於 1**，
  兩條線會完全重合——正是 PLAYBOOK 記了五次的那個錯。改成 ξ ′ = ( 1 , 1 , 0 ) 之後斜率是
  2 與 1。現在這件事由 `assert SLA != SLB` 釘在模組層，訊息就寫
  「兩條線斜率不同，所以是兩條線不是一條畫兩次」。
- **第 6 拍（三重線性）原本三個斜率有兩個是零。** 選的第三個向量剛好讓 λ ₃ ( u ₃ ) = 0，
  於是前兩個位置的增量整個被乘成零，右表會印出兩個 0 卻看不出哪裡不對。
  換掉 u ₃ 之後是 −10、+4、−4，並加上 `assert len(set(SLOPE3)) == 3`。
- **第 5 拍（定理 1.2）的 6 × 6 取值矩陣原本是奇異的。** 用亂數挑六對 ( ξ , η ) 時抽到了
  一對零向量，det 正好是 0，而那一列本來是要用來說「六個基底元素獨立」的——
  等於在畫面上印一個 0 然後說它證明了獨立性。改成挑的時候就排掉零向量，並且
  `assert abs(DET6) > 1.0`。
- **不是錯但先查掉的：⊗ 這個字元在這個系列從來沒用過。** 照 PLAYBOOK 裡 ‴ 的教訓，
  先掃了系統所有 157 個字型檔的 cmap：預設的 wqy-zenhei **有 ‴ 卻把它畫成兩撇**
  （這正是當初那個坑的成因），而 **wqy-zenhei 根本沒有 ⊗**，所以 Pango 一定會退到
  DejaVu 或 wqy-microhei，兩者的 ⊗ 都是正常的圈叉。同一輪順手確認了 ∗、𝒜、ₚ、ᵣ
  四個字元也都只存在於會被退回去的字型裡。
- **第 9 拍的樹原本留了一段除錯殘留**：邊的索引寫成一個 `if False else` 的死碼。
  取到的值是對的，但那是除錯痕跡，交稿前刪掉了。
- **第 2 拍的縱向比例原本只有一個沒有訊息、也沒在保證什麼的 assert。**
  換成 PLAYBOOK 第 3 節那條規則本身：三條曲線裡最平的那一條，在畫面上的升幅必須
  超過畫帶高度的四分之一（`FLAT1 > 0.25`，實際是 0.286）。這樣調 t 範圍或縱向比例時，
  「主角貼在軸上」會在 import 當下就失敗，而不是等到看 1080p 的幀。

## 十一拍

### 第 1 拍 — 第 7 章：備查章節，整章沒有習題 / chapter 7: a reference chapter, and no exercises in it

公式列：

```
V * ⊗ W *            ( V * ) ⊗ ⁿ            dim   =   m ⁿ
```

中文旁白：第 7 章開宗明義就說，這一章主要是備查用的，大部分的證明雖然都寫出來了，但並不期待讀者細讀。它的目標是把交錯多重線性泛函，也就是外形式，那一整套工具備齊，而行列式正是其中一項收穫。整章九節，一題習題也沒有。

English: Chapter 7 says so itself: it is principally for reference, and although most of the proofs are included, the reader is not expected to study them. The goal is a collection of theorems on alternating multilinear functionals, and the determinant is one of the rewards. No exercises.

### 第 2 拍 — 雙線性泛函自成一個向量空間 / the bilinear functionals form a vector space

公式列：

```
f ( a ξ + ξ ′ , η )   =   a  f ( ξ , η )   +   f ( ξ ′ , η )
```

中文旁白：先看雙線性的情形。V 和 W 都是有限維的時候，兩者的乘積上所有雙線性泛函合起來，很顯然就是一個向量空間，書上把它記作 V 星與 W 星的張量積。左圖是兩條直線加一條拋物線：固定一個變數時另一個是線性的，兩個一起動就不是。

English: Start with the bilinear case. For finite dimensional V and W, all bilinear functionals on their product pretty clearly form a vector space, written as the tensor product of the two dual spaces. The figure draws two lines and a parabola: linear in each slot, not in both.

### 第 3 拍 — 定理 1.1：三個空間自然同構 / theorem 1.1: three spaces, naturally isomorphic

公式列：

```
V * ⊗ W *   ≅   Hom ( V , W * )   ≅   Hom ( W , V * )
```

中文旁白：定理 1.1 說，V 星與 W 星的張量積、從 V 到 W 星的線性映射全體、從 W 到 V 星的線性映射全體，這三個空間自然同構。證明其實第 1 章定理 6.1 就做掉一半了：每個雙線性泛函都決定一個對應，而這一章要補的只是那個對應本身是線性的。

English: Theorem 1.1: the tensor product, the linear maps from V to the dual of W, and the linear maps from W to the dual of V are naturally isomorphic. Theorem 6.1 of chapter one already did half of it. All that is added here is that the correspondence is itself a linear one.

### 第 4 拍 — 初等張量：秩一 / elementary tensors: rank one

公式列：

```
( γ ⊗ λ ) ( ξ , η )   =   γ ( ξ )  ·  λ ( η )
```

中文旁白：接著定義初等張量。γ 張量 λ 在一對向量上的值，就是 γ 作用在第一個上面，乘以 λ 作用在第二個上面。一個雙線性泛函是初等的，若且唯若它對應的那個線性映射的秩是一。左圖上面那個矩陣的第二個奇異值是零，下面那個不是。

English: Now the elementary tensors. The value of gamma tensor lambda on a pair of vectors is gamma on the first times lambda on the second. A bilinear functional is elementary exactly when the corresponding linear map has rank one. The upper matrix has second singular value zero.

### 第 5 拍 — 定理 1.2：維數是 m 乘 n / theorem 1.2: the dimension is m times n

公式列：

```
f   =   Σ ᵢ ⱼ   t ᵢ ⱼ   ( μ ᵢ ⊗ ν ⱼ )            dim   =   m n
```

中文旁白：定理 1.2：取 V 與 W 的基底和它們的對偶基底，那 m 乘 n 個 μ i 張量 ν j 就構成張量積的一組基底，所以維數是 m 乘 n。左圖是一個具體的三乘二係數表，每一格就是 f 在那一對基底向量上的值，右表把展開式與逐點的核對放在一起。

English: Theorem 1.2: take bases of V and W and their dual bases, and the m times n elementary functionals form a basis of the tensor product, so the dimension is m times n. The figure is a concrete three by two table of coefficients, each entry a value of f on a pair of basis vectors.

### 第 6 拍 — 推廣到 n 重線性 / on to n slots

公式列：

```
f   :   V ₁  ×  ⋯  ×  V ₙ   →   ℝ
```

中文旁白：以上整套都推廣到多重線性。f 從 n 個空間的乘積映到實數，要求是固定其他變數的時候，對每一個變數都線性。全體一樣是個向量空間，記作那 n 個對偶空間的張量積。左圖只把第二個位置點亮，表示其他位置都先凍結住，只讓它動。

English: All of that generalises to multilinear functionals. Here f runs from a product of n spaces to the reals, and is required to be linear in each variable when the others are held fixed. The figure lights up the second slot alone, to say the others are frozen while it moves.

### 第 7 拍 — 都取同一個 V：n 階共變張量 / all slots the same V: covariant tensors of order n

公式列：

```
f ( ξ ₁ , … , ξ ₙ )   =   Σ ₚ   x ¹ ₚ ₁ ⋯ x ⁿ ₚ ₙ   f ( α ₚ ₁ , … , α ₚ ₙ )
```

中文旁白：為了讓記號簡單，也因為這才是最有用的情形，以下讓這 n 個空間全都是同一個 V。這時候空間記作 V 星的 n 次張量冪，叫做 n 階共變張量空間。把每個變數照基底展開，再逐個變數用線性，就得到一個跑遍所有 n 元組的和式。

English: To keep the notation simple, and because it is the case of most interest, let all n of the spaces be one and the same V. The space is then a tensor power of the dual, called the covariant tensors of order n. Expanding each variable gives a sum over all tuples of length n.

### 第 8 拍 — 初等多重線性泛函 / the elementary multilinear functionals

公式列：

```
μ ᵣ ( α ₚ ₁ , … , α ₚ ₙ )   =   0   ( p ≠ r )            =   1   ( p = r )
```

中文旁白：那些 n 元組的集合，書上記作 m 上面加一槓再 n 次方，意思是從 1 到 n 映到 1 到 m 的所有函數。用對偶基底做出的初等多重線性泛函，在基底的 n 元組上只有指標完全一樣時才是一，其他全是零。左圖那個九乘九的矩陣就是單位矩陣。

English: The set of those tuples is written m bar to the n: all the functions from one to n into one to m. The dual basis builds elementary multilinear functionals, one per tuple, worth one when the two index tuples agree and zero otherwise. The matrix on the left is the identity.

### 第 9 拍 — 定理 2.1 與推論：維數是 m 的 n 次方 / theorem 2.1 and its corollary: the dimension is m to the n

公式列：

```
f   =   Σ ₚ   c ₚ  μ ₚ            dim ( V * ) ⊗ ⁿ   =   m ⁿ
```

中文旁白：於是有定理 2.1：這些初等泛函構成 n 階共變張量空間的一組基底，而係數就是 f 在對應的那組基底向量上的值。推論是維數等於 m 的 n 次方。左圖那棵樹每一層都分三叉，m 等於三的時候三層剛好是三個、九個、二十七個。

English: Theorem 2.1: those elementary functionals are a basis of the covariant tensors of order n, with coordinates the values of f on the matching tuples of basis vectors. The corollary is that the dimension is m to the n. The tree branches three ways: three, nine, twenty-seven.

### 第 10 拍 — 歸納那一步：雙重和寫成單一和 / the inductive step: a double sum as a single one

公式列：

```
Σ ₚ ∈ m̄ ⁿ   Σ ⱼ ∈ m̄      =      Σ ᵣ ∈ m̄ ⁿ ⁺ ¹
```

中文旁白：為什麼要堆這麼多記號？因為嚴格的證明要對 n 做歸納，而歸納那一步得把一個雙重和寫成單一和。用到的事實是：一個 n 元組再配上一個指標，和一個 n 加一元組是一一對應的。左圖把三個配上三個變成九個，右表把兩種加法算出來對照。

English: Why pile up so much notation? A strict proof needs an induction on n, and the inductive step has to rewrite a double sum as a single one. The fact it uses is that a tuple together with one more index is the same thing as a tuple one longer. Three times three become nine.

### 第 11 拍 — 收尾：對稱與交錯，下一集從置換開始 / closing: symmetry and alternation, and permutations next

公式列：

```
C   =   S   +   A            S ᵗ  =  S   ,   A ᵗ  =  − A
```

中文旁白：有了基底就可以談對稱與交錯了。二階的時候，任何一個係數矩陣都能拆成對稱的一半加上反對稱的一半，維數六加三剛好是九。但交錯這個詞是用置換的正負號定義的，所以下一集得先從置換群與正負號講起。

English: With a basis in hand one can speak of symmetry and alternation. In order two every coefficient matrix splits into a symmetric half and a skew half, and six plus three is nine. But alternating is defined by the sign of a permutation, so the next episode starts with those.

## 動畫說明

| 拍 | 畫面 |
|---|---|
| 1 | 左圖是這一章九節的地圖，九個方塊標 § 1 到 § 9，§ 1 與 § 2 是橘的並畫了底線；右表每一列是那一節做出來的東西（V * ⊗ W *、S ₙ、𝒜 ⁿ、det、∧、∗） |
| 2 | 三條曲線對同一個參數 s：橘線固定 η、青線固定 ξ，兩條都是直線但斜率是 2 與 1；紫線兩個變數一起動，是拋物線。三條在 s = 0 交於同一個白點，虛線標出 s = 0，底下是 s 軸與 −1、0、+1 三個刻度 |
| 3 | V * ⊗ W * 在上，Hom ( V , W * ) 與 Hom ( W , V * ) 在下，三條雙向箭頭圍成一個三角形，每條旁邊標 ≅；底下那條從兩個名字各拉一小段虛線下來，再往左右指回去 |
| 4 | 兩個 3 × 2 的數字陣列並排：左邊是 γ ⊗ λ 的外積（秩一），右邊是例子 f 的矩陣（秩二），各自底下寫真的算出來的 rank |
| 5 | f 的係數表畫成 3 × 2 的數字陣列，左側三列標 μ ₁ μ ₂ μ ₃、上方兩行標 ν ₁ ν ₂，底下寫 t ᵢ ⱼ = f ( α ᵢ , β ⱼ ) |
| 6 | V ₁ × V ₂ × ⋯ × V ₙ 四個方塊串成一排，只有 V ₂ 是橘的、底下掛 α ⱼ，其餘掛 α ᵢ 而且是灰的；一支標著 f 的箭頭從 V ₂ 底下斜指到 ℝ 那個方塊 |
| 7 | 3 × 3 的格子，每一格寫著它自己那個二元組 ⟨ i , j ⟩，上面標 m̄ ²、底下標 \| m̄ ² \| = 9 |
| 8 | 9 × 9 的 0 與 1 陣列，就是真的算出來的 μ ᵣ ( α ₚ ) 表：對角線九格是橘色的 1，其餘七十二格是灰色的 0 |
| 9 | 一棵往下長的樹，每一層分三叉：1 → 3 → 9 → 27 個點，右側標上 3、9、27 三個數 |
| 10 | 左邊三個 ⟨ p ⟩ 各拉出三條線到右邊九個 ⟨ p , j ⟩，上方兩個標頭是 m̄ ¹ × m̄ 與 m̄ ² |
| 11 | 兩個 3 × 3 數字陣列並排，中間一個橘色的 +：左邊是對稱部分 S、右邊是反對稱部分 A，各自底下寫 S ᵗ = S 與 A ᵗ = − A，最底下寫 6 + 3 = 9 = m ² |
