# UEFA Champions League Final 2026 Match Control Analysis

Status: analysis run completed; review report generated and published to GitHub Pages.

Published report: https://shiga-1993.github.io/champions-league-final-2026-match-control-analysis/

GitHub repository: https://github.com/Shiga-1993/champions-league-final-2026-match-control-analysis

## Analytical Question

How could Paris Saint-Germain control the 2026 UEFA Champions League final so strongly in possession, shots, and passing volume while Arsenal still kept the match level until penalties?

## Data Sources

- Union of European Football Associations: official match report for the scoreline, main events, and penalty failures.
- Opta Analyst: match-control statistics and post-match facts.
- Sports Illustrated: public match-stat summary including the completed-pass comparison and Opta possession note.

## Method

- Keep a small source-cited table rather than storing a heavy raw match feed.
- Compare possession share, total shots, completed passes, and the score after extra time.
- Convert each metric into a Paris Saint-Germain to Arsenal ratio.
- Plot the control indicators next to the 120-minute scoreline to make the gap visible.
- Build a timeline and penalty-shootout sequence for context.

## Outputs

- `outputs/report/review_report.html`
- `outputs/figures/team_control_snapshot.png`
- `outputs/figures/control_gap_vs_scoreline.png`
- `outputs/figures/match_timeline.png`
- `outputs/figures/penalty_shootout_sequence.png`
- `outputs/tables/match_control_stats.csv`
- `outputs/tables/match_events.csv`
- `outputs/tables/penalty_shootout_sequence.csv`
- `outputs/tables/source_notes.csv`

## Reproduce

From this directory:

```bash
python3 run_ucl_final_match_control.py
python3 -m pytest -q
```

## Limitations

- Possession, pass, and shot totals vary by provider definition. The report treats them as provider-specific control indicators, not as universal physical measurements.
- This is a descriptive analysis of one match, not a tactical model.
- Expected goals and shot maps are intentionally excluded until a stable public source can be cited cleanly.
