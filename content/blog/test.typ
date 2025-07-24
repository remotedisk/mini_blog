#import "../3rd_party/mathyml/lib.typ": *
#import "../3rd_party/mathyml/lib.typ" as mathyml
#import mathyml.prelude:*

#show math.equation: to-mathml



#metadata("Introduction to Typst") <meta:title>
#metadata("Recent developments in typesetting software have rekindled hope in previously frustrated researchers. This post explores Typst's capabilities and demonstrates various features.") <meta:desc>
#metadata("2024-07-23") <meta:date>
#metadata("Xiaotian Han") <meta:author>
#metadata("typst") <meta:tags>


#set heading(numbering: "1.")

#outline(title: "Table of Contents", depth: 1)

= Introduction <sec:intro>
Recent developments in
typesetting software have
rekindled hope in previously
frustrated researchers. 
#lorem(100)

= Results <sec:results>
We discuss our approach in
comparison with others.
#lorem(100)

== Performance <sec:results:perf>
demonstrates what slow
software looks like #to-mathml($O(n) = 2^n$).
#to-mathml($ O(n) = 2^n $)


== Image <sec:results:image>
#figure(
  image("./glacier.jpg", width: 150pt),
  caption: [
    _Glaciers_ form an important part
    of the earth's climate system.
  ],
) <glaciers>


The @glaciers figure shows a
glacier in the Alps.


= Table <sec:table>

#table(
  columns: (auto, auto, auto, auto, auto),
  align: (center, center, center, center),
  [], [Token/s], [Peak FLOPS], [MFU], [llm.c MFU],
  [A100], [33k], [312], [\~63.5%], [\~40%],
  [H100], [78k], [989], [\~47.3%], [\~39%],
) <tab:tan2>


#table(
  columns: (auto, auto, auto, auto, auto),
  align: (center, center, center, center),
  [], [Token/s], [Peak FLOPS], [MFU], [llm.c MFU],
  [A100], [33k], [312], [\~63.5%], [\~40%],
  [H100], [78k], [989], [\~47.3%], [\~39%],

) <tab:tan1>


= Link <link>

The section @sec:table @sec:results:image @sec:intro shows a table.

#link("https://arxiv.org/pdf/2310.00183")[arXiv]


= Block <sec:block>

#block(
  fill: luma(240),
  inset: 10pt,
  radius: 4pt,
  [
    *TL;DR* \
    - dive into softmax, from math to implementation, from vector to matrix. \
    - torch and triton implementations, with reference code and speed comparison.
  ]
)

#align(center)[
  #block(
    fill: rgb("f0f0f0"),
    inset: 8pt,
    radius: 4pt,
    [*Is there a connection between graph convolution and Mixup?*]
  )
]



= Code <sec:code>

```python
for inputs, labels in data_loader:
    outputs = model(inputs)
    loss = criterion(outputs, labels)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```
