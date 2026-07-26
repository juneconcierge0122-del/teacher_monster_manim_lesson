"""Bilingual source copy for the special (non-Landau) episodes.

S01 — "Verbalizable Representations Form a Global Workspace in Language Models"
(Gurnee et al., Anthropic, 2026) https://transformer-circuits.pub/2026/workspace/
"""

TOPICS_SPECIAL = {
1: {"zh": ("可被說出的表徵：語言模型裡的全域工作空間", [
 "一個語言模型在回答問題時，內部會產生龐大的表徵；但其中只有一小部分，是它真的能說出口的。這篇來自 Anthropic 的研究主張，這些可以被說出來的表徵，在模型裡構成了一個類似全域工作空間的東西。",
 "要看見模型能說什麼，作者提出了雅可比透鏡。他們把最終輸出對某一層的活化取梯度，再在一千個提示與各個位置上平均，得到一個線性映射；用它取代上面所有的層，就能把中間層的活化直接讀成詞彙分數。",
 "這些透鏡向量的數量遠多於模型的維度，所以是一組過完備的基底。把任一個活化分解成大約二十五個透鏡向量的稀疏非負組合，就得到它在工作空間裡的座標。關鍵是，這個成分佔全部變異不到一成，卻承擔了不成比例的功能。",
 "第一個性質是口語報告。請模型心裡先想一個運動，在它還沒說出來以前，透鏡在中層就已經讀出足球。把足球的座標換成橄欖球，模型說出口的就變成橄欖球。而且只換工作空間那一小塊成分，成功率有五成九；換掉剩下的九成多，只有五趴。",
 "第二個性質是指向性調控。讓模型一邊逐字抄寫一句無關的句子，一邊在心裡專注想著柑橘類水果；透鏡就在抄寫的位置上讀出柳橙和檸檬。反過來叫它不要去想，出現率明顯下降，卻不會歸零，就像人被叫做不要想白熊一樣。",
 "第三個性質是內部推理。問模型會結網的動物有幾條腿，蜘蛛這個詞從頭到尾沒出現在題目或答案裡，卻清楚出現在中層的透鏡讀數上。把蜘蛛換成螞蟻，答案就從八變成六；在兩跳推理題上，這種替換的成功率大約在五成到七成之間。",
 "第四個性質是彈性泛化。同一個代表法國的向量，被換成代表中國以後，接著問首都、問語言、問位在哪一洲，三個完全不同的下游運算全都跟著改。所以工作空間裡放的是一個可以被任意取用的概念，而不是為某一題預先算好的答案。",
 "第五個性質是選擇性。拿同一段西班牙文，把代表西班牙文的向量換成法文。要模型往下續寫時，它照樣寫出流暢的西班牙文；要它偵測夾雜進來的外語時，也照樣抓得到。但只要問它這是什麼語言，答案就跟著換過去了。",
 "這個工作空間還有很明顯的結構。它只在中間大約三分之一的層裡運作，太早或太晚都不行；同時活躍的概念大約只有十到二十五個，容量非常有限。把它壓制掉之後，分類、抽取、情感判斷這些淺層任務幾乎不受影響，多跳推理的正確率卻掉到接近零。",
 "還有兩個很像大腦的跡象。工作空間裡的向量比其他方向更容易被下游的權重接上，像是一個樞紐；而且遇到有歧義的輸入時，模型會在工作空間開始的那一層附近，突然收斂到單一種解讀，很像神經科學裡說的點火現象。",
 "作者說得很清楚：這些結果並沒有回答模型有沒有主觀經驗。但在功能的層次上，一組容量有限、可以被報告、可以被指揮、又能廣播給各種下游運算的表徵，確實存在於模型內部。這也讓透鏡成為一種稽核工具，讓我們看見模型沒有說出口的東西。",
]), "en": ("Verbalizable Representations: A Global Workspace", [
 "When a language model answers a question, it builds an enormous number of internal representations, yet only a small part of them can ever be spoken. This work from Anthropic argues that those verbalizable representations form a global workspace inside the model.",
 "To see what a model could say, the authors build the Jacobian lens. They differentiate the final output with respect to one layer, average that over a thousand prompts, and use the resulting linear map in place of every layer above, reading the activation as vocabulary scores.",
 "There are far more lens vectors than dimensions, so the set is overcomplete. Decomposing an activation into a sparse combination of about twenty-five of them gives its workspace coordinates. That component holds under a tenth of the variance, yet does far more.",
 "The first property is verbal report. Ask the model to think of a sport: before it says anything, the lens already reads soccer in the middle layers. Swap those coordinates for rugby and it says rugby. The workspace part alone drives fifty-nine percent of swaps, the rest five.",
 "The second is directed modulation. Ask the model to copy an unrelated sentence word by word while holding citrus fruit in mind, and the lens reads orange and lemon right at the copying positions. Tell it not to think of them and the rate drops sharply, but never to zero.",
 "The third is internal reasoning. Ask how many legs the animal that spins webs has: the word spider never appears in the question or the answer, yet it stands out in the middle-layer readout. Swap spider for ant and the answer turns from eight into six.",
 "The fourth is flexible generalization. Take the one vector standing for France, swap it to China, then ask for the capital, the language, or the continent: all three different downstream operations follow the swap. The workspace holds a concept, not a precomputed answer.",
 "The fifth is selectivity. Take a Spanish passage and swap the vector for Spanish to French. Asked to continue, the model still writes fluent Spanish, and it still spots a foreign intrusion. But ask it to name the language, and the answer follows the swap.",
 "The workspace has a clear structure. It works only in the middle third of the layers, and only about ten to twenty-five concepts are active at once. Suppress it and shallow tasks like classification and sentiment barely change, while multi-hop reasoning drops to near zero.",
 "Two more signatures look brain-like. Workspace vectors compose with downstream weights far more broadly than other directions, like a hub. And on an ambiguous input the model commits sharply to one reading right where the workspace begins, much like neural ignition.",
 "The authors are explicit that this says nothing about subjective experience. But functionally, a limited set of representations that can be reported, directed, and broadcast to many downstream operations does exist inside the model. That makes the lens an auditing tool.",
])},
}

# On-screen formulas (enlarged unicode Text, shown above the animation stage).
# Language-independent; anything language-dependent lives in MODE_LABEL.
# Keep every entry to ONE line: MODE_LABEL supplies a second one, and a third
# line drops the block to y ≈ 1.3 where it covers the panel headers.
FORMULAS_SPECIAL = {
1: {
 0: "Claude Sonnet 4.5   ·   layer 0 → 100",
 1: "J = avg ∂h_final/∂h_layer  ,  lens = softmax( W_U norm( J h ) )",
 2: "h ≈ c₁j₁ + … + c₂₅j₂₅  ,  cᵢ ≥ 0  ,  variance under 10 %",
 3: "soccer → rugby        J-space 59 %   |   remainder 5 %",
 4: "hold citrus in mind → orange , lemon      suppress → not zero",
 5: "spins webs → [ spider ] → 8        spider → ant  ⟹  6",
 6: "France → China        capital  |  language  |  continent",
 7: "Spanish → French        automatic  ≠  report and inference",
 8: "workspace layers ≈ 38 → 92        10 – 25 concepts at once",
 9: "broadcast hub   ·   ignition at the workspace onset",
 10: "functional workspace   ≠   subjective experience",
},
}
