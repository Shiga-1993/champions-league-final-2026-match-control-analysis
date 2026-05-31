# Data Notes

This project does not store heavy raw feeds.

The analysis table is manually defined in `run_ucl_final_match_control.py` from checked public sources:

- UEFA official match report: result, match events, penalty failures, player of the match.
- Opta Analyst: shot count, possession record, first-half pass note, penalty sequence.
- Sports Illustrated: completed-pass comparison and Opta possession note.

Generated CSVs are stored under `outputs/tables/`.
