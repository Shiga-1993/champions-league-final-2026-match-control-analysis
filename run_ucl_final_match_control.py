from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"
TABLE_DIR = OUTPUT_DIR / "tables"
REPORT_DIR = OUTPUT_DIR / "report"

PARIS = "Paris Saint-Germain"
ARSENAL = "Arsenal"

COLORS = {
    PARIS: "#2447A9",
    ARSENAL: "#C13B3A",
    "score": "#56616f",
    "grid": "#d7dde5",
    "text": "#17202a",
    "muted": "#667085",
    "paper": "#f7f9fc",
}


CONTROL_STATS = [
    {
        "metric": "Possession share",
        "unit": "%",
        "paris": 75.3,
        "arsenal": 24.7,
        "source": "Opta Analyst / OptaJoe",
        "note": "Arsenal possession was reported as 24.7%; Paris share is inferred as 100 minus Arsenal.",
    },
    {
        "metric": "Total shots",
        "unit": "shots",
        "paris": 21.0,
        "arsenal": 7.0,
        "source": "Opta Analyst",
        "note": "Opta Analyst reported Paris with 21 shots and Arsenal with seven attempts.",
    },
    {
        "metric": "Completed passes",
        "unit": "passes",
        "paris": 806.0,
        "arsenal": 196.0,
        "source": "Sports Illustrated summary of match statistics",
        "note": "Provider-specific completed-pass count; other public stat feeds list slightly different pass totals.",
    },
    {
        "metric": "Goals after extra time",
        "unit": "goals",
        "paris": 1.0,
        "arsenal": 1.0,
        "source": "UEFA official match report",
        "note": "The final was 1-1 after extra time before Paris won 4-3 on penalties.",
    },
]

MATCH_EVENTS = [
    {
        "minute": 6,
        "phase": "First half",
        "team": ARSENAL,
        "event": "Kai Havertz goal",
        "score": "Paris 0-1 Arsenal",
    },
    {
        "minute": 65,
        "phase": "Second half",
        "team": PARIS,
        "event": "Ousmane Dembele penalty",
        "score": "Paris 1-1 Arsenal",
    },
    {
        "minute": 77,
        "phase": "Second half",
        "team": PARIS,
        "event": "Kvaratskhelia effort deflects onto post",
        "score": "Paris 1-1 Arsenal",
    },
    {
        "minute": 89,
        "phase": "Second half",
        "team": PARIS,
        "event": "Vitinha late chance",
        "score": "Paris 1-1 Arsenal",
    },
    {
        "minute": 120,
        "phase": "After extra time",
        "team": "Both",
        "event": "Level after extra time",
        "score": "Paris 1-1 Arsenal",
    },
]

SHOOTOUT = [
    {"order": 1, "team": PARIS, "player": "Goncalo Ramos", "result": "Scored", "running_score": "1-0"},
    {"order": 2, "team": ARSENAL, "player": "Viktor Gyokeres", "result": "Scored", "running_score": "1-1"},
    {"order": 3, "team": PARIS, "player": "Desire Doue", "result": "Scored", "running_score": "2-1"},
    {"order": 4, "team": ARSENAL, "player": "Eberechi Eze", "result": "Missed", "running_score": "2-1"},
    {"order": 5, "team": PARIS, "player": "Nuno Mendes", "result": "Saved", "running_score": "2-1"},
    {"order": 6, "team": ARSENAL, "player": "Declan Rice", "result": "Scored", "running_score": "2-2"},
    {"order": 7, "team": PARIS, "player": "Achraf Hakimi", "result": "Scored", "running_score": "3-2"},
    {"order": 8, "team": ARSENAL, "player": "Gabriel Martinelli", "result": "Scored", "running_score": "3-3"},
    {"order": 9, "team": PARIS, "player": "Lucas Beraldo", "result": "Scored", "running_score": "4-3"},
    {"order": 10, "team": ARSENAL, "player": "Gabriel Magalhaes", "result": "Missed", "running_score": "4-3"},
]

SOURCES = [
    {
        "name": "UEFA official match report",
        "url": "https://www.uefa.com/uefachampionsleague/news/02a5-20c02e59f219-15e92acdc717-1000--paris-retain-champions-league-holders-edge-arsenal-on-pena/",
        "used_for": "Final score, timeline events, penalty failures, and player of the match.",
    },
    {
        "name": "Opta Analyst match report",
        "url": "https://theanalyst.com/articles/psg-vs-arsenal-champions-league-final-stats",
        "used_for": "Shots, possession record, first-half pass fact, and shootout sequence.",
    },
    {
        "name": "Sports Illustrated match-stat summary",
        "url": "https://www.si.com/soccer/arsenal-extend-unwanted-champions-league-record-after-heartbreaking-final-defeat",
        "used_for": "Completed-pass comparison and Opta possession note.",
    },
]


def ensure_dirs() -> None:
    for directory in [FIGURE_DIR, TABLE_DIR, REPORT_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#9aa4b2",
            "axes.labelcolor": COLORS["text"],
            "axes.titlesize": 14,
            "axes.labelsize": 12,
            "xtick.color": COLORS["muted"],
            "ytick.color": COLORS["text"],
            "font.size": 11,
            "font.family": "DejaVu Sans",
            "savefig.bbox": "tight",
            "savefig.dpi": 180,
        }
    )


def build_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    control = pd.DataFrame(CONTROL_STATS)
    control["paris_to_arsenal_ratio"] = control["paris"] / control["arsenal"].replace(0, np.nan)
    control["difference"] = control["paris"] - control["arsenal"]

    events = pd.DataFrame(MATCH_EVENTS)
    shootout = pd.DataFrame(SHOOTOUT)
    sources = pd.DataFrame(SOURCES)
    return control, events, shootout, sources


def save_tables(
    control: pd.DataFrame, events: pd.DataFrame, shootout: pd.DataFrame, sources: pd.DataFrame
) -> None:
    control.to_csv(TABLE_DIR / "match_control_stats.csv", index=False)
    events.to_csv(TABLE_DIR / "match_events.csv", index=False)
    shootout.to_csv(TABLE_DIR / "penalty_shootout_sequence.csv", index=False)
    sources.to_csv(TABLE_DIR / "source_notes.csv", index=False)
    metadata = {
        "project": "uefa_champions_league_final_2026_match_control",
        "source_checked_date": date.today().isoformat(),
        "match_date": "2026-05-30",
        "match": f"{PARIS} vs {ARSENAL}",
        "result": "1-1 after extra time; Paris Saint-Germain won 4-3 on penalties.",
        "method": "Descriptive comparison of match-control indicators and outcome metrics.",
    }
    (TABLE_DIR / "run_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")


def add_value_label(ax: plt.Axes, value: float, y: float, unit: str) -> None:
    if unit == "%":
        text = f"{value:.1f}%"
    elif value.is_integer():
        text = f"{int(value):,}"
    else:
        text = f"{value:.1f}"
    ax.text(value, y, f"  {text}", va="center", ha="left", color=COLORS["text"], fontsize=11)


def plot_team_control_snapshot(control: pd.DataFrame) -> Path:
    metrics = control[control["metric"] != "Goals after extra time"].reset_index(drop=True)
    fig, axes = plt.subplots(1, len(metrics), figsize=(14, 5), gridspec_kw={"wspace": 0.62})
    for ax, row in zip(axes, metrics.to_dict("records")):
        values = [row["paris"], row["arsenal"]]
        teams = [PARIS, ARSENAL]
        team_labels = ["Paris", "Arsenal"]
        y = np.arange(len(teams))
        ax.barh(y, values, color=[COLORS[PARIS], COLORS[ARSENAL]], height=0.45)
        ax.set_yticks(y, team_labels)
        ax.invert_yaxis()
        ax.set_xlabel(row["unit"])
        ax.set_xlim(0, max(values) * 1.28)
        ax.grid(axis="x", color=COLORS["grid"], linewidth=0.8, alpha=0.8)
        ax.set_axisbelow(True)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.set_title(
            row["metric"],
            loc="left",
            pad=12,
            fontsize=11.5,
            fontweight="semibold",
            color=COLORS["text"],
        )
        for yi, value in zip(y, values):
            add_value_label(ax, float(value), yi, row["unit"])
    output = FIGURE_DIR / "team_control_snapshot.png"
    fig.savefig(output)
    plt.close(fig)
    return output


def plot_control_gap_vs_scoreline(control: pd.DataFrame) -> Path:
    plot_data = control.copy()
    plot_data["label"] = plot_data["metric"].replace(
        {
            "Possession share": "Possession",
            "Total shots": "Shots",
            "Completed passes": "Completed passes",
            "Goals after extra time": "Score after 120 min",
        }
    )
    fig, ax = plt.subplots(figsize=(11.5, 6.2))
    colors = [
        COLORS["score"] if metric == "Goals after extra time" else COLORS[PARIS]
        for metric in plot_data["metric"]
    ]
    y = np.arange(len(plot_data))
    ax.barh(y, plot_data["paris_to_arsenal_ratio"], color=colors, height=0.55)
    ax.axvline(1, color="#111827", linewidth=1.2)
    ax.set_yticks(y, plot_data["label"])
    ax.invert_yaxis()
    ax.set_xlabel("Paris Saint-Germain value / Arsenal value")
    ax.set_xlim(0, max(plot_data["paris_to_arsenal_ratio"]) * 1.24)
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.8, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    for yi, value in zip(y, plot_data["paris_to_arsenal_ratio"]):
        ax.text(value, yi, f"  {value:.1f}x", va="center", ha="left", fontsize=12)
    ax.text(
        1.02,
        len(plot_data) - 0.05,
        "equal",
        color=COLORS["muted"],
        fontsize=10,
        ha="left",
        va="bottom",
    )
    output = FIGURE_DIR / "control_gap_vs_scoreline.png"
    fig.savefig(output)
    plt.close(fig)
    return output


def plot_match_timeline(events: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(13, 5.8))
    ax.hlines(0, 0, 120, color="#a8b3c2", linewidth=3)
    ax.scatter([0, 45, 90, 120], [0, 0, 0, 0], s=55, color="#344054", zorder=3)
    for minute, label in [(0, "Kickoff"), (45, "Half-time"), (90, "Full-time"), (120, "120 min")]:
        ax.text(minute, -0.18, label, ha="center", va="top", color=COLORS["muted"], fontsize=10)

    label_overrides = {
        "Kai Havertz goal": "6'  Havertz goal\nParis 0-1 Arsenal",
        "Ousmane Dembele penalty": "65'  Dembele penalty\nParis 1-1 Arsenal",
        "Kvaratskhelia effort deflects onto post": "77'  Shot onto post\nParis pressure",
        "Vitinha late chance": "89'  Vitinha chance\nStill 1-1",
        "Level after extra time": "120'  After extra time\nParis 1-1 Arsenal",
    }
    label_positions = {
        "Kai Havertz goal": (8, 0.88, "left"),
        "Ousmane Dembele penalty": (58, -0.9, "right"),
        "Kvaratskhelia effort deflects onto post": (78, 0.95, "left"),
        "Vitinha late chance": (88, -0.9, "left"),
        "Level after extra time": (116, 0.43, "right"),
    }
    for idx, row in enumerate(events.to_dict("records")):
        minute = row["minute"]
        team = row["team"]
        color = COLORS.get(team, COLORS["score"])
        text_x, ypos, ha = label_positions[row["event"]]
        ax.vlines(minute, 0, ypos * 0.76, color=color, linewidth=2, alpha=0.9)
        ax.scatter(minute, 0, s=95, color=color, zorder=4)
        label = label_overrides[row["event"]]
        ax.text(
            text_x,
            ypos,
            label,
            ha=ha,
            va="center",
            fontsize=10.2,
            color=COLORS["text"],
            bbox={
                "boxstyle": "round,pad=0.35",
                "facecolor": "white",
                "edgecolor": "#d0d5dd",
                "linewidth": 0.8,
            },
        )
    ax.set_xlim(-3, 123)
    ax.set_ylim(-1.2, 1.24)
    ax.set_yticks([])
    ax.set_xlabel("Match minute")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#c7ced8")
    ax.grid(False)
    output = FIGURE_DIR / "match_timeline.png"
    fig.savefig(output)
    plt.close(fig)
    return output


def plot_penalty_shootout(shootout: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(13, 5.8))
    y_positions = {PARIS: 1, ARSENAL: 0}
    for team, y in y_positions.items():
        team_data = shootout[shootout["team"] == team]
        ax.scatter(
            team_data["order"],
            [y] * len(team_data),
            s=440,
            color=COLORS[team],
            alpha=0.13,
            edgecolor=COLORS[team],
            linewidth=2,
        )
        ax.text(0.55, y, team, ha="right", va="center", fontsize=12, color=COLORS["text"])

    for row in shootout.to_dict("records"):
        y = y_positions[row["team"]]
        result = row["result"]
        marker = "o" if result == "Scored" else "X"
        color = COLORS[row["team"]] if result == "Scored" else "#111827"
        ax.scatter(row["order"], y, marker=marker, s=130, color=color, zorder=4)
        ax.text(
            row["order"],
            y - 0.23 if y == 1 else y + 0.23,
            f"{row['player']}\n{result}",
            ha="center",
            va="top" if y == 1 else "bottom",
            fontsize=9.2,
            color=COLORS["text"],
        )
        ax.text(
            row["order"],
            -0.62,
            row["running_score"],
            ha="center",
            va="center",
            fontsize=9.5,
            color=COLORS["muted"],
        )
    ax.text(0.55, -0.62, "Score", ha="right", va="center", fontsize=10, color=COLORS["muted"])
    ax.set_xlim(0.15, 10.85)
    ax.set_ylim(-0.82, 1.42)
    ax.set_xticks(range(1, 11))
    ax.set_xlabel("Penalty order")
    ax.set_yticks([])
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#c7ced8")
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.7, alpha=0.55)
    ax.set_axisbelow(True)
    output = FIGURE_DIR / "penalty_shootout_sequence.png"
    fig.savefig(output)
    plt.close(fig)
    return output


def format_value(value: float, unit: str) -> str:
    if unit == "%":
        return f"{value:.1f}%"
    if float(value).is_integer():
        return f"{int(value):,}"
    return f"{value:.1f}"


def render_table(df: pd.DataFrame, columns: list[str]) -> str:
    rows = []
    header = "".join(f"<th>{html.escape(col)}</th>" for col in columns)
    rows.append(f"<tr>{header}</tr>")
    for _, row in df[columns].iterrows():
        cells = "".join(f"<td>{html.escape(str(row[col]))}</td>" for col in columns)
        rows.append(f"<tr>{cells}</tr>")
    return "<table>" + "\n".join(rows) + "</table>"


def build_report(control: pd.DataFrame, events: pd.DataFrame, shootout: pd.DataFrame) -> Path:
    control_rows = []
    for row in control.to_dict("records"):
        control_rows.append(
            {
                "Metric": row["metric"],
                PARIS: format_value(row["paris"], row["unit"]),
                ARSENAL: format_value(row["arsenal"], row["unit"]),
                "Paris / Arsenal": f"{row['paris_to_arsenal_ratio']:.2f}x",
                "Source": row["source"],
            }
        )
    control_display = pd.DataFrame(control_rows)
    source_items = "\n".join(
        f"<li><a href=\"{html.escape(source['url'])}\">{html.escape(source['name'])}</a>: "
        f"{html.escape(source['used_for'])}</li>"
        for source in SOURCES
    )
    figure_blocks = "\n".join(
        [
            '<figure><img src="../figures/team_control_snapshot.png" alt="Team control metrics for Paris Saint-Germain and Arsenal"><figcaption>Paris led the main match-control indicators by a wide margin.</figcaption></figure>',
            '<figure><img src="../figures/control_gap_vs_scoreline.png" alt="Paris to Arsenal ratio for control metrics and score after extra time"><figcaption>The control gap was roughly three to four times larger, while the 120-minute score stayed level.</figcaption></figure>',
            '<figure><img src="../figures/match_timeline.png" alt="Timeline of main events in the 2026 UEFA Champions League final"><figcaption>Arsenal scored early; Paris equalized from a second-half penalty and kept pressing without breaking the 1-1 scoreline.</figcaption></figure>',
            '<figure><img src="../figures/penalty_shootout_sequence.png" alt="Penalty shootout sequence for Paris Saint-Germain and Arsenal"><figcaption>The trophy was decided by a narrow shootout after a lopsided control profile.</figcaption></figure>',
        ]
    )
    report_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>UEFA Champions League Final 2026 Match Control Analysis</title>
  <style>
    :root {{
      --text: #17202a;
      --muted: #667085;
      --line: #d0d5dd;
      --paper: #f7f9fc;
      --accent: #2447a9;
    }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--text);
      background: white;
      line-height: 1.55;
    }}
    main {{
      max-width: 1040px;
      margin: 0 auto;
      padding: 40px 22px 64px;
    }}
    h1 {{
      font-size: clamp(2rem, 4vw, 3.4rem);
      line-height: 1.05;
      margin: 0 0 16px;
      letter-spacing: 0;
    }}
    h2 {{
      font-size: 1.35rem;
      margin: 36px 0 10px;
    }}
    p {{
      max-width: 860px;
      margin: 0 0 16px;
    }}
    .lead {{
      font-size: 1.12rem;
      color: #344054;
    }}
    .callout {{
      border-left: 5px solid var(--accent);
      background: var(--paper);
      padding: 18px 20px;
      margin: 24px 0 28px;
      font-size: 1.1rem;
    }}
    figure {{
      margin: 28px 0 34px;
      padding: 0;
    }}
    img {{
      width: 100%;
      height: auto;
      display: block;
      border: 1px solid var(--line);
    }}
    figcaption {{
      margin-top: 8px;
      color: var(--muted);
      font-size: 0.95rem;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      margin: 18px 0;
      font-size: 0.95rem;
    }}
    th, td {{
      border-bottom: 1px solid var(--line);
      padding: 10px 8px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: var(--paper);
      font-weight: 650;
    }}
    ul {{
      padding-left: 22px;
    }}
    a {{
      color: var(--accent);
    }}
    .meta {{
      color: var(--muted);
      font-size: 0.92rem;
      margin-top: 36px;
    }}
  </style>
</head>
<body>
<main>
  <h1>UEFA Champions League Final 2026 Match Control Analysis</h1>
  <p class="lead">Paris Saint-Germain and Arsenal finished 1-1 after extra time on May 30, 2026, before Paris won the penalty shootout 4-3. The data story is not just who won. It is how much match control Paris had before the scoreboard still stayed level for 120 minutes.</p>

  <div class="callout"><strong>Punchline:</strong> Paris had about three times Arsenal's possession share and shot volume, and more than four times the completed passes, but the final still reached penalties at 1-1.</div>

  <h2>Background</h2>
  <p>The Union of European Football Associations (UEFA) match report records the final as Paris Saint-Germain 1-1 Arsenal after extra time, with Paris winning 4-3 on penalties at the Puskas Arena in Budapest. Arsenal led through Kai Havertz in the sixth minute. Paris equalized through an Ousmane Dembele penalty in the 65th minute.</p>

  <h2>Purpose</h2>
  <p>This analysis separates match control from match outcome. The goal is to show, in a few readable figures, how a final can be statistically one-sided in possession, shots, and passing volume, while still being decided by one kick in a shootout.</p>

  <h2>Method</h2>
  <p>The project uses a small, source-cited table rather than storing a heavy raw feed. Match outcome and key events come from UEFA. Control indicators come from public Opta-derived reporting: Arsenal's 24.7% possession figure, Paris' 21-7 shot advantage, and the 806-196 completed-pass comparison. Paris' possession share is inferred as 100% minus Arsenal's reported share.</p>

  <h2>Results</h2>
  {render_table(control_display, ["Metric", PARIS, ARSENAL, "Paris / Arsenal", "Source"])}
  {figure_blocks}

  <h2>Interpretation</h2>
  <p>The clearest read is that Paris controlled the match environment, but did not turn that control into scoreboard separation. Arsenal scored early, defended deep, and kept Paris to one goal across normal and extra time. That makes the final a useful example of the gap between territorial control and outcome control.</p>
  <p>The completed-pass gap is especially strong: Paris completed more than four passes for every one Arsenal completed. The shot gap is also large, but the 120-minute score stayed 1-1. That tension is the main story for a public data post.</p>

  <h2>Limitations</h2>
  <ul>
    <li>Possession, pass, and shot counts can differ by provider definitions. This report keeps the provider notes visible rather than blending incompatible feeds.</li>
    <li>This is a descriptive analysis of one final, not a tactical model or player-evaluation model.</li>
    <li>Expected goals and shot locations are not included because the most accessible public xG values were less directly sourceable than the control metrics used here.</li>
  </ul>

  <h2>Next Steps</h2>
  <ul>
    <li>Add shot-location or expected-goals data if a stable public source is available.</li>
    <li>Compare this final with other Champions League finals that reached penalties.</li>
    <li>Build a small benchmark of finals where control metrics and final score diverged sharply.</li>
  </ul>

  <h2>Sources</h2>
  <ul>
    {source_items}
  </ul>

  <p class="meta">Source check date: {date.today().isoformat()}. Generated from <code>run_ucl_final_match_control.py</code>.</p>
</main>
</body>
</html>
"""
    output = REPORT_DIR / "review_report.html"
    output.write_text(report_html)
    return output


def main() -> None:
    ensure_dirs()
    setup_style()
    control, events, shootout, sources = build_tables()
    save_tables(control, events, shootout, sources)
    plot_team_control_snapshot(control)
    plot_control_gap_vs_scoreline(control)
    plot_match_timeline(events)
    plot_penalty_shootout(shootout)
    build_report(control, events, shootout)


if __name__ == "__main__":
    main()
