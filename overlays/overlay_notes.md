# Overlay construction notes (the only hand-curated input)

Country names are spelled exactly as in JST R6: Australia, Belgium,
Canada, Denmark, Finland, France, Germany, Ireland, Italy, Japan,
Netherlands, Norway, Portugal, Spain, Sweden, Switzerland, UK, USA.

Austria and Greece appear in many default chronologies but are **not**
in the JST-18 panel, so they are omitted.

## rr_defaults.csv — inclusion decisions

| country | year | include? | reason |
|---|---|---|---|
| Germany | 1932 | yes | Transfer moratorium / standstill on external debt. Named in HANDOFF. |
| Germany | 1948 | yes | Currency reform wiped domestic public debt. Named in HANDOFF (1932/1948). |
| Japan | 1942 | yes | Wartime external default. Named in HANDOFF. |
| Italy | 1940 | yes | Wartime default / suspension of external service. Standard RR 20th-c Europe list. |
| Portugal | 1892 | yes | External default / rescheduling. Standard 19th-c RR list. |
| Spain | 1873 | yes | External default. Standard 19th-c RR list. |
| Spain | 1882 | yes | External default / rescheduling. Standard 19th-c RR list. |
| Spain | 1936 | yes | Civil-war default on external debt. |
| USA | 1933 | **no (base)** | Gold-clause abrogation is a domestic-debt event. HANDOFF says the US produces zero onsets under the base definitions and to run 1933/1971 only as a *named sensitivity*. |
| USA | 1971 | **no (base)** | Nixon shock / gold window. Same named-sensitivity rule. |
| UK | 1932 | **no** | War-debt suspension vis-à-vis the US is sometimes coded as default; HANDOFF's short list of advanced external defaults does not include it. |
| France | 1934 / 1940s | **no as D1** | No clean external default year in the HANDOFF short list. 1940s inflation adjustment is intended to be caught by D2, not forced into D1. |
| Australia, Canada, etc. | — | no | No RR sovereign default/restructuring onset in 1870–present for these JST-18 names that survives the same filter. |

Sources consulted (public chronologies, not a re-coding of crises by eye):
Reinhart–Rogoff *This Time Is Different* appendix tables on external
default/rescheduling (Europe 19th c. and 20th c.) and domestic-debt
episodes; HANDOFF.md's own named examples.

## imf_programs.csv — inclusion decisions

Criterion stated in HANDOFF: *IMF arrangements with fiscal conditionality,
post-1945*. Not every drawing or precautionary line.

| country | year | include? | reason |
|---|---|---|---|
| UK | 1976 | yes | SBA / Letter of Intent with fiscal conditions. Named in HANDOFF. |
| UK | 1967 | **no (base)** | SBA after sterling devaluation; weaker fiscal-conditionality case than 1976. Named-sensitivity candidate. |
| Italy | 1974 | yes | SBA during mid-70s fiscal/external stress. |
| Italy | 1977 | yes | SBA. Named in HANDOFF. May fall inside the 1974 exclusion window at default params — that is a finding, not a reason to drop the row from the overlay. |
| Spain | 1978 | yes | SBA. |
| Portugal | 1977 | yes | SBA (first post-revolution program). |
| Portugal | 1983 | yes | SBA. |
| Portugal | 2011 | yes | EF / Troika program with fiscal conditionality. |
| Ireland | 2010 | yes | EFF / Troika program with fiscal conditionality. |
| Spain | 2012 | **no** | ESM bank-recap facility, not an IMF arrangement. |
| France, Germany, USA, … | — | no | No IMF program with fiscal conditionality. |

Primary source family: IMF history of arrangements / MONA-style program
dates as commonly reported. Years are *arrangement onset years*, not
every review year.

## What this overlay is not

It is not a complete census of every historian's "debt crisis" year.
Banking crises (JST `crisisJST`), ERM 1992, and 2008 banking-system
events are deliberately out of D1/D4. If they belong at all, D2/D3 have
to pick them up from prices.
