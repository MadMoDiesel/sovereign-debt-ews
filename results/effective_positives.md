# Effective positives — complete indicator vector before onset

E0 labels, full 14-column vector, JST R6. A training row at year s is
usable for an h-year-ahead model only if the outcome window closes
(`labels_usable_at`) *and* the feature vector at s is complete. The
relevant feature years for a 3-year-ahead onset at τ are s ∈ {τ−1, τ−2, τ−3}.

## Headline

| | n / 34 |
|---|---|
| Complete vector at s (onset year itself) | 20 |
| Complete vector at **s−1** | **22** |
| Complete at s−2 | 22 |
| Complete at s−3 | 21 |
| Complete at any of s−1..s−3 | 24 |
| Complete at all of s−1..s−3 | 19 |

**Effective positives for the primary 3-year-ahead spec: 22.**
Not 34. Model complexity is capped by 22, not by the raw onset count.

## Event-by-event (1 = complete)

| country | year | rule | s | s−1 | s−2 | s−3 | n leads |
|---|---|---|---|---|---|---|---|
| Belgium | 1923 | D3 | 0 | 0 | 0 | 0 | 0 |
| Belgium | 1938 | D3 | 1 | 1 | 1 | 1 | 3 |
| Finland | 1945 | D2,D3 | 0 | 0 | 0 | 0 | 0 |
| France | 1914 | D3 | 0 | 1 | 1 | 1 | 3 |
| France | 1924 | D3 | 1 | 1 | 0 | 0 | 1 |
| France | 1937 | D2,D3 | 1 | 1 | 1 | 1 | 3 |
| Germany | 1932 | D1 | 1 | 1 | 1 | 0 | 2 |
| Germany | 1948 | D1 | 0 | 0 | 0 | 0 | 0 |
| Ireland | 1981 | D2 | 1 | 1 | 1 | 1 | 3 |
| Ireland | 2010 | D4 | 1 | 1 | 1 | 1 | 3 |
| Italy | 1915 | D3 | 0 | 1 | 1 | 1 | 3 |
| Italy | 1940 | D1 | 1 | 1 | 1 | 1 | 3 |
| Italy | 1974 | D4 | 1 | 1 | 1 | 1 | 3 |
| Japan | 1942 | D1 | 0 | 0 | 0 | 0 | 0 |
| Netherlands | 1915 | D3 | 0 | 0 | 1 | 1 | 2 |
| Netherlands | 1939 | D3 | 1 | 1 | 1 | 1 | 3 |
| Netherlands | 1951 | D3 | 1 | 1 | 0 | 0 | 1 |
| Netherlands | 1957 | D3 | 1 | 1 | 1 | 1 | 3 |
| Portugal | 1873 | D2,D3 | 0 | 0 | 0 | 0 | 0 |
| Portugal | 1890 | D3 | 1 | 1 | 1 | 1 | 3 |
| Portugal | 1916 | D2 | 0 | 0 | 0 | 0 | 0 |
| Portugal | 1922 | D2 | 0 | 0 | 0 | 0 | 0 |
| Portugal | 1977 | D4 | 1 | 1 | 1 | 1 | 3 |
| Portugal | 1983 | D4 | 1 | 1 | 1 | 1 | 3 |
| Portugal | 2011 | D3,D4 | 1 | 1 | 1 | 1 | 3 |
| Spain | 1873 | D1 | 0 | 0 | 0 | 0 | 0 |
| Spain | 1882 | D1 | 0 | 0 | 0 | 0 | 0 |
| Spain | 1936 | D1 | 0 | 0 | 1 | 1 | 2 |
| Spain | 1947 | D2,D3 | 0 | 0 | 0 | 0 | 0 |
| Spain | 1978 | D4 | 1 | 1 | 1 | 1 | 3 |
| UK | 1917 | D2,D3 | 1 | 1 | 1 | 1 | 3 |
| UK | 1947 | D3 | 1 | 1 | 1 | 1 | 3 |
| UK | 1973 | D3 | 1 | 1 | 1 | 1 | 3 |
| USA | 1947 | D3 | 1 | 1 | 1 | 1 | 3 |

Zero-lead events (no usable pre-onset vector at all): Belgium 1923,
Finland 1945, Germany 1948, Japan 1942, Portugal 1873/1916/1922,
Spain 1873/1882/1947. Ten events. They remain in the onset list; they
do not contribute a positive training row under complete-case features.

s−1 misses that *are* recoverable by dropping only `credit_gap_5y`:
Portugal 1916, 1922, Spain 1947 (22 → 25). Japan 1942 is only `slope`.
The rest are multi-series wartime/19th-century holes.

## Implication for §5

22 positives, 13 indicators, country FE on top: L1 is not optional.
M1 failing to beat M2 (debt/GDP alone) is the expected null as often
as not. Do not add interactions beyond the one already declared.
Do not build the fold engine against a 34-positive fantasy sample.
