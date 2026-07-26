# 特別篇 S01 — 可被說出的表徵：語言模型裡的全域工作空間

Verbalizable Representations: A Global Workspace

依據 Gurnee et al., *Verbalizable Representations Form a Global Workspace in Language Models*, Anthropic, 2026 — https://transformer-circuits.pub/2026/workspace/index.html

- 場景檔：`manim_lessons/lessons/special_s01_workspace.py`（`SpecialS01ZH` / `SpecialS01EN`）
- 腳本與公式：`manim_lessons/localization/special_topics.py`（`TOPICS_SPECIAL[1]` / `FORMULAS_SPECIAL[1]`）
- 配音：`manim_lessons/samples/audio_s01/`（zh-TW `-4%`、en `-8%`）
- 片長：中文 4.19 分（251 秒）／英文 3.26 分（196 秒）

---

## Beat 0 — 內部表徵很多，說得出口的很少 / many representations, few of them spoken
*配音長度：中文 19.3s ／ 英文 17.7s*

**畫面公式**

```
內部表徵很多，說得出口的很少   |   many representations, few of them spoken
Claude Sonnet 4.5   ·   layer 0 → 100
```

**旁白（繁中）**

> 一個語言模型在回答問題時，內部會產生龐大的表徵；但其中只有一小部分，是它真的能說出口的。這篇來自 Anthropic 的研究主張，這些可以被說出來的表徵，在模型裡構成了一個類似全域工作空間的東西。

**Narration (EN)**

> When a language model answers a question, it builds an enormous number of internal representations, yet only a small part of them can ever be spoken. This work from Anthropic argues that those verbalizable representations form a global workspace inside the model.

**動畫**

層塔（layer 0 → 100）+ 內部表徵點雲：84 個點只有 7 個是 ACCENT_C（可被說出），箭頭把它們送進右邊的「說得出口的」框。

## Beat 1 — 雅可比透鏡：直接把中層讀成詞彙 / the Jacobian lens: read a middle layer as vocabulary
*配音長度：中文 20.1s ／ 英文 18.4s*

**畫面公式**

```
雅可比透鏡：直接把中層讀成詞彙   |   the Jacobian lens: read a middle layer as vocabulary
J = avg ∂h_final/∂h_layer  ,  lens = softmax( W_U norm( J h ) )
```

**旁白（繁中）**

> 要看見模型能說什麼，作者提出了雅可比透鏡。他們把最終輸出對某一層的活化取梯度，再在一千個提示與各個位置上平均，得到一個線性映射；用它取代上面所有的層，就能把中間層的活化直接讀成詞彙分數。

**Narration (EN)**

> To see what a model could say, the authors build the Jacobian lens. They differentiate the final output with respect to one layer, average that over a thousand prompts, and use the resulting linear map in place of every layer above, reading the activation as vocabulary scores.

**動畫**

在第 60 層點亮一塊（tap），上面的層被虛線標成「被 J 取代」；一道 ACCENT_C 光束帶著脈衝點射向右邊的 J-lens 讀數面板（Paris / France / capital / city / Lyon）。

## Beat 2 — 工作空間座標：稀疏、非負、佔比很小 / workspace coordinates: sparse, non-negative, small
*配音長度：中文 22.1s ／ 英文 17.8s*

**畫面公式**

```
工作空間座標：稀疏、非負、佔比很小   |   workspace coordinates: sparse, non-negative, small
h ≈ c₁j₁ + … + c₂₅j₂₅  ,  cᵢ ≥ 0  ,  variance under 10 %
```

**旁白（繁中）**

> 這些透鏡向量的數量遠多於模型的維度，所以是一組過完備的基底。把任一個活化分解成大約二十五個透鏡向量的稀疏非負組合，就得到它在工作空間裡的座標。關鍵是，這個成分佔全部變異不到一成，卻承擔了不成比例的功能。

**Narration (EN)**

> There are far more lens vectors than dimensions, so the set is overcomplete. Decomposing an activation into a sparse combination of about twenty-five of them gives its workspace coordinates. That component holds under a tenth of the variance, yet does far more.

**動畫**

左邊一根活化變異柱：頂端 10% 是 ACCENT_C 的 J-space，其餘是灰色；右邊列出 j₁…j₂₅ 的非負係數長條，標註 k ≈ 25。

## Beat 3 — 性質一　口語報告 / property 1 — verbal report
*配音長度：中文 25.8s ／ 英文 18.7s*

**畫面公式**

```
性質一　口語報告   |   property 1 — verbal report
soccer → rugby        J-space 59 %   |   remainder 5 %
```

**旁白（繁中）**

> 第一個性質是口語報告。請模型心裡先想一個運動，在它還沒說出來以前，透鏡在中層就已經讀出足球。把足球的座標換成橄欖球，模型說出口的就變成橄欖球。而且只換工作空間那一小塊成分，成功率有五成九；換掉剩下的九成多，只有五趴。

**Narration (EN)**

> The first property is verbal report. Ask the model to think of a sport: before it says anything, the lens already reads soccer in the middle layers. Swap those coordinates for rugby and it says rugby. The workspace part alone drives fifty-nine percent of swaps, the rest five.

**動畫**

三面板流程 提示 → J-lens 讀數 → 模型輸出。讀數首列 soccer 在句中被換成 rugby（轉紅），輸出從 Soccer 變成 Rugby。

## Beat 4 — 性質二　指向性調控 / property 2 — directed modulation
*配音長度：中文 22.7s ／ 英文 18.2s*

**畫面公式**

```
性質二　指向性調控   |   property 2 — directed modulation
hold citrus in mind → orange , lemon      suppress → not zero
```

**旁白（繁中）**

> 第二個性質是指向性調控。讓模型一邊逐字抄寫一句無關的句子，一邊在心裡專注想著柑橘類水果；透鏡就在抄寫的位置上讀出柳橙和檸檬。反過來叫它不要去想，出現率明顯下降，卻不會歸零，就像人被叫做不要想白熊一樣。

**Narration (EN)**

> The second is directed modulation. Ask the model to copy an unrelated sentence word by word while holding citrus fruit in mind, and the lens reads orange and lemon right at the copying positions. Tell it not to think of them and the rate drops sharply, but never to zero.

**動畫**

提示卡是逐字抄寫任務＋「心裡想著柑橘」；讀數出現 orange / lemon / citrus。句中改成「不要去想」，所有長條縮到約四成、轉灰但不歸零。

## Beat 5 — 性質三　內部推理 / property 3 — internal reasoning
*配音長度：中文 23.7s ／ 英文 16.8s*

**畫面公式**

```
性質三　內部推理   |   property 3 — internal reasoning
spins webs → [ spider ] → 8        spider → ant  ⟹  6
```

**旁白（繁中）**

> 第三個性質是內部推理。問模型會結網的動物有幾條腿，蜘蛛這個詞從頭到尾沒出現在題目或答案裡，卻清楚出現在中層的透鏡讀數上。把蜘蛛換成螞蟻，答案就從八變成六；在兩跳推理題上，這種替換的成功率大約在五成到七成之間。

**Narration (EN)**

> The third is internal reasoning. Ask how many legs the animal that spins webs has: the word spider never appears in the question or the answer, yet it stands out in the middle-layer readout. Swap spider for ant and the answer turns from eight into six.

**動畫**

提示是「會結網的動物有幾條腿」；讀數首列 spider（題目與答案都沒有這個字）。換成 ant 後輸出由 8 變 6。

## Beat 6 — 性質四　彈性泛化 / property 4 — flexible generalization
*配音長度：中文 23.3s ／ 英文 18.1s*

**畫面公式**

```
性質四　彈性泛化   |   property 4 — flexible generalization
France → China        capital  |  language  |  continent
```

**旁白（繁中）**

> 第四個性質是彈性泛化。同一個代表法國的向量，被換成代表中國以後，接著問首都、問語言、問位在哪一洲，三個完全不同的下游運算全都跟著改。所以工作空間裡放的是一個可以被任意取用的概念，而不是為某一題預先算好的答案。

**Narration (EN)**

> The fourth is flexible generalization. Take the one vector standing for France, swap it to China, then ask for the capital, the language, or the continent: all three different downstream operations follow the swap. The workspace holds a concept, not a precomputed answer.

**動畫**

提示卡列出三個不同下游問句（首都 / 語言 / 洲）；把 France 換成 China 後，輸出三列同時變成 Beijing / Chinese / Asia。

## Beat 7 — 性質五　選擇性 / property 5 — selectivity
*配音長度：中文 23.3s ／ 英文 16.7s*

**畫面公式**

```
性質五　選擇性   |   property 5 — selectivity
Spanish → French        automatic  ≠  report and inference
```

**旁白（繁中）**

> 第五個性質是選擇性。拿同一段西班牙文，把代表西班牙文的向量換成法文。要模型往下續寫時，它照樣寫出流暢的西班牙文；要它偵測夾雜進來的外語時，也照樣抓得到。但只要問它這是什麼語言，答案就跟著換過去了。

**Narration (EN)**

> The fifth is selectivity. Take a Spanish passage and swap the vector for Spanish to French. Asked to continue, the model still writes fluent Spanish, and it still spots a foreign intrusion. But ask it to name the language, and the answer follows the swap.

**動畫**

提示卡是一段西班牙文，讀數 Spanish 換成 French；右邊四列任務表：續寫與偵測外語標「不變」（青），說出語言與舉作家標「跟著換」（紅）。

## Beat 8 — 結構：深度、容量、消融 / structure: depth, capacity, ablation
*配音長度：中文 25.3s ／ 英文 18.1s*

**畫面公式**

```
結構：深度、容量、消融   |   structure: depth, capacity, ablation
workspace layers ≈ 38 → 92        10 – 25 concepts at once
```

**旁白（繁中）**

> 這個工作空間還有很明顯的結構。它只在中間大約三分之一的層裡運作，太早或太晚都不行；同時活躍的概念大約只有十到二十五個，容量非常有限。把它壓制掉之後，分類、抽取、情感判斷這些淺層任務幾乎不受影響，多跳推理的正確率卻掉到接近零。

**Narration (EN)**

> The workspace has a clear structure. It works only in the middle third of the layers, and only about ten to twenty-five concepts are active at once. Suppress it and shallow tasks like classification and sentiment barely change, while multi-hop reasoning drops to near zero.

**動畫**

結構板：左邊層深剖面曲線與 38–92 的 ACCENT_C 帶；右上 25 顆點代表容量；右下消融長條，淺層任務接近滿格（青）、多跳推理接近零（紅）。

## Beat 9 — 廣播樞紐與點火動態 / a broadcast hub, and ignition
*配音長度：中文 21.1s ／ 英文 17.6s*

**畫面公式**

```
廣播樞紐與點火動態   |   a broadcast hub, and ignition
broadcast hub   ·   ignition at the workspace onset
```

**旁白（繁中）**

> 還有兩個很像大腦的跡象。工作空間裡的向量比其他方向更容易被下游的權重接上，像是一個樞紐；而且遇到有歧義的輸入時，模型會在工作空間開始的那一層附近，突然收斂到單一種解讀，很像神經科學裡說的點火現象。

**Narration (EN)**

> Two more signatures look brain-like. Workspace vectors compose with downstream weights far more broadly than other directions, like a hub. And on an ambiguous input the model commits sharply to one reading right where the workspace begins, much like neural ignition.

**動畫**

左邊 J 樞紐向 12 個下游權重塊放射，對照旁邊只接 2 條的一般方向；右邊點火圖：兩條解讀曲線在第 38 層附近急遽分離，虛線標出工作空間起點。

## Beat 10 — 功能上的工作空間 / a workspace in the functional sense
*配音長度：中文 24.5s ／ 英文 17.5s*

**畫面公式**

```
功能上的工作空間   |   a workspace in the functional sense
functional workspace   ≠   subjective experience
```

**旁白（繁中）**

> 作者說得很清楚：這些結果並沒有回答模型有沒有主觀經驗。但在功能的層次上，一組容量有限、可以被報告、可以被指揮、又能廣播給各種下游運算的表徵，確實存在於模型內部。這也讓透鏡成為一種稽核工具，讓我們看見模型沒有說出口的東西。

**Narration (EN)**

> The authors are explicit that this says nothing about subjective experience. But functionally, a limited set of representations that can be reported, directed, and broadcast to many downstream operations does exist inside the model. That makes the lens an auditing tool.

**動畫**

收尾：中央「全域工作空間」圓，五條輻條連到五個功能性質；公式區點出功能上的工作空間不等於主觀經驗。
