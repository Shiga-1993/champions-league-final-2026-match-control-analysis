# UEFA Champions League Final 2026 Match Control Analysis

Status: analysis run completed; review report generated and published to GitHub Pages.

Published report: https://shiga-1993.github.io/champions-league-final-2026-match-control-analysis/

GitHub repository: https://github.com/Shiga-1993/champions-league-final-2026-match-control-analysis

## Analytical Question

How could Paris Saint-Germain control the 2026 UEFA Champions League final so strongly in possession, shots, and passing volume while Arsenal still kept the match level until penalties?

## Data Sources

- Union of European Football Associations: official match report for the scoreline, main events, substitutions, penalty failures, and Player of the Match context.
- Opta Analyst: match-control statistics, pre-match win-probability note, and Vitinha's Champions League profile.
- Sports Illustrated: public match-stat summary including the completed-pass comparison and Opta possession note.
- VG live report: penalty shootout sequence cross-check.

## Method

- Keep small source-cited tables rather than storing a heavy raw match feed.
- Compare possession share, total shots, completed passes, and the score after extra time.
- Convert each control metric into a Paris Saint-Germain to Arsenal ratio.
- Build a score-state win-probability estimate from match events and the penalty sequence.
- Add Vitinha's Champions League profile and substitution leverage analysis.
- Build a numbered timeline and penalty-shootout sequence for context.

## Outputs

- `outputs/report/review_report.html`
- `outputs/figures/team_control_snapshot.png`
- `outputs/figures/control_gap_vs_scoreline.png`
- `outputs/figures/win_probability_timeline.png`
- `outputs/figures/match_timeline_numbered.png`
- `outputs/figures/vitinha_profile.png`
- `outputs/figures/substitution_leverage.png`
- `outputs/figures/penalty_shootout_sequence.png`
- `outputs/tables/match_control_stats.csv`
- `outputs/tables/match_events.csv`
- `outputs/tables/penalty_shootout_sequence.csv`
- `outputs/tables/win_probability_timeline.csv`
- `outputs/tables/substitution_summary.csv`
- `outputs/tables/vitinha_profile.csv`
- `outputs/tables/source_notes.csv`

## Reproduce

From this directory:

```bash
python3 run_ucl_final_match_control.py
python3 -m pytest -q
```

## Limitations

- Possession, pass, and shot totals vary by provider definition. The report treats them as provider-specific control indicators, not universal physical measurements.
- The win-probability curve is a transparent score-state model, not a bookmaker line or an official live feed.
- This is a descriptive analysis of one match, not a tactical model.
- Expected goals and shot maps are intentionally excluded until a stable public source can be cited cleanly.
