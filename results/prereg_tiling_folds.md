# Tiling fold grid — coverage correction, 2026-08-31

Rationale is a priori and does not depend on any AUC:

The original §6 grid T ∈ {1950, 1960, …, 2015} with test (T, T+5]
scores 1951–55, 1961–65, … and never scores 1956–60, 1966–70, 1976–80,
1986–90, 1996–00, 2006–10. Half the post-1950 country-years are
discarded by construction. That is a coverage bug, not a data limit.

Correction: T steps of 5 years so test windows abut and tile 1951–2020.
T ∈ {1950, 1955, …, 2015}.

This is a post-hoc coverage correction, not a pre-registered fold grid.
The original eight-fold design had already been run when this cut was
written down. Both grids are reported. The original remains the primary
declared design. Neither grid's AUC is used to choose a winner.
