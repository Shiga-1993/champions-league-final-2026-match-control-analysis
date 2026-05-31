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

PREMATCH_PARIS_TROPHY_PROBABILITY = 0.56
ASSUMED_TOTAL_GOALS_TO_120 = 2.6
PENALTY_CONVERSION_PROBABILITY = 0.75


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
        "event_id": 1,
        "minute": 6,
        "phase": "First half",
        "team": ARSENAL,
        "event": "Kai Havertz goal",
        "score": "Paris 0-1 Arsenal",
    },
    {
        "event_id": 2,
        "minute": 65,
        "phase": "Second half",
        "team": PARIS,
        "event": "Ousmane Dembele penalty",
        "score": "Paris 1-1 Arsenal",
    },
    {
        "event_id": 3,
        "minute": 77,
        "phase": "Second half",
        "team": PARIS,
        "event": "Kvaratskhelia effort deflects onto post",
        "score": "Paris 1-1 Arsenal",
    },
    {
        "event_id": 4,
        "minute": 89,
        "phase": "Second half",
        "team": PARIS,
        "event": "Vitinha late chance",
        "score": "Paris 1-1 Arsenal",
    },
    {
        "event_id": 5,
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

SUBSTITUTIONS = [
    {
        "team": PARIS,
        "minute": 83,
        "player_on": "Bradley Barcola",
        "player_off": "Khvicha Kvaratskhelia",
        "penalty_role": "No penalty",
        "contribution": "Fresh wide runner during Paris' late push.",
    },
    {
        "team": ARSENAL,
        "minute": 66,
        "player_on": "Jurrien Timber",
        "player_off": "Cristhian Mosquera",
        "penalty_role": "No penalty",
        "contribution": "Defensive substitution before Paris equalized.",
    },
    {
        "team": ARSENAL,
        "minute": 67,
        "player_on": "Viktor Gyokeres",
        "player_off": "Martin Odegaard",
        "penalty_role": "Scored",
        "contribution": "Converted Arsenal's first shootout kick.",
    },
    {
        "team": ARSENAL,
        "minute": 83,
        "player_on": "Gabriel Martinelli",
        "player_off": "Leandro Trossard",
        "penalty_role": "Scored",
        "contribution": "Converted Arsenal's fourth shootout kick.",
    },
    {
        "team": ARSENAL,
        "minute": 83,
        "player_on": "Noni Madueke",
        "player_off": "Bukayo Saka",
        "penalty_role": "No penalty",
        "contribution": "Added a late direct option on the right side.",
    },
    {
        "team": ARSENAL,
        "minute": 91,
        "player_on": "Eberechi Eze",
        "player_off": "Kai Havertz",
        "penalty_role": "Missed",
        "contribution": "Missed Arsenal's second shootout kick.",
    },
    {
        "team": ARSENAL,
        "minute": 91,
        "player_on": "Martin Zubimendi",
        "player_off": "Myles Lewis-Skelly",
        "penalty_role": "No penalty",
        "contribution": "Extra-time midfield stability.",
    },
    {
        "team": PARIS,
        "minute": 96,
        "player_on": "Goncalo Ramos",
        "player_off": "Ousmane Dembele",
        "penalty_role": "Scored",
        "contribution": "Converted Paris' first shootout kick after entering late.",
    },
    {
        "team": PARIS,
        "minute": 95,
        "player_on": "Warren Zaire-Emery",
        "player_off": "Fabian Ruiz",
        "penalty_role": "No penalty",
        "contribution": "Fresh legs in midfield during extra time.",
    },
    {
        "team": PARIS,
        "minute": 106,
        "player_on": "Illya Zabarnyi",
        "player_off": "Marquinhos",
        "penalty_role": "No penalty",
        "contribution": "Late defensive reset before the shootout.",
    },
    {
        "team": PARIS,
        "minute": 106,
        "player_on": "Lucas Beraldo",
        "player_off": "Vitinha",
        "penalty_role": "Scored",
        "contribution": "Converted Paris' fifth shootout kick.",
    },
]

VITINHA_PROFILE = [
    {
        "metric": "Official final award",
        "value": "Player of the Match",
        "interpretation": "The Union of European Football Associations technical observer panel singled out his control of the game.",
    },
    {
        "metric": "Successful passes per 90",
        "value": "90.6",
        "interpretation": "Season-long Champions League passing volume shows why Paris could sustain possession through midfield.",
    },
    {
        "metric": "Line-breaking passes per 90",
        "value": "14.2",
        "interpretation": "He was not just recycling possession; he repeatedly moved the ball through pressure lines.",
    },
    {
        "metric": "Build-up involvements per 90",
        "value": "50.3",
        "interpretation": "High build-up involvement fits the final's control profile.",
    },
    {
        "metric": "Progressive carries per 90",
        "value": "11.6",
        "interpretation": "Ball-carrying gave Paris another way to advance play when passing lanes narrowed.",
    },
    {
        "metric": "Final event note",
        "value": "89' chance; off 106'",
        "interpretation": "He remained involved late, then Paris used Lucas Beraldo as a shootout option after substituting him.",
    },
]

SOURCES = [
    {
        "name": "UEFA official match report",
        "url": "https://www.uefa.com/uefachampionsleague/news/02a5-20c02e59f219-15e92acdc717-1000--paris-retain-champions-league-holders-edge-arsenal-on-pena/",
        "used_for": "Final score, timeline events, substitution list, penalty failures, and player of the match.",
    },
    {
        "name": "Opta Analyst match report",
        "url": "https://theanalyst.com/articles/psg-vs-arsenal-champions-league-final-stats",
        "used_for": "Shots, possession record, pre-match win probability, first-half pass fact, and Vitinha's Champions League profile.",
    },
    {
        "name": "Sports Illustrated match-stat summary",
        "url": "https://www.si.com/soccer/arsenal-extend-unwanted-champions-league-record-after-heartbreaking-final-defeat",
        "used_for": "Completed-pass comparison and Opta possession note.",
    },
    {
        "name": "UEFA Player of the Match article",
        "url": "https://www.uefa.com/uefachampionsleague/news/02a5-20c0324a93c4-a269d65f5aeb-1000--vitinha-named-official-2026-uefa-champions-league-final-play/",
        "used_for": "Vitinha official Player of the Match context.",
    },
    {
        "name": "VG live report",
        "url": "https://www.vg.no/sport/i/L4Px4Q/champions-league-finalen-arsenal-leiren-reagerer-etter-omdiskutert-straffesituasjon-mot-psg",
        "used_for": "Penalty shootout sequence cross-check.",
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


def poisson_probs(mu: float, max_goals: int = 12) -> np.ndarray:
    probs = np.zeros(max_goals + 1)
    probs[0] = np.exp(-mu)
    for goals in range(1, max_goals + 1):
        probs[goals] = probs[goals - 1] * mu / goals
    probs[-1] += max(0.0, 1.0 - probs.sum())
    return probs


def trophy_probability_from_state(
    paris_score: int,
    arsenal_score: int,
    minute: float,
    paris_goal_rate_120: float,
    arsenal_goal_rate_120: float,
    max_goals: int = 12,
) -> float:
    remaining_share = max(0.0, 120.0 - minute) / 120.0
    paris_future = poisson_probs(paris_goal_rate_120 * remaining_share, max_goals=max_goals)
    arsenal_future = poisson_probs(arsenal_goal_rate_120 * remaining_share, max_goals=max_goals)
    probability = 0.0
    for paris_goals, paris_prob in enumerate(paris_future):
        for arsenal_goals, arsenal_prob in enumerate(arsenal_future):
            final_paris = paris_score + paris_goals
            final_arsenal = arsenal_score + arsenal_goals
            joint = paris_prob * arsenal_prob
            if final_paris > final_arsenal:
                probability += joint
            elif final_paris == final_arsenal:
                probability += 0.5 * joint
    return float(probability)


def fit_goal_rates_for_prematch(
    target_probability: float = PREMATCH_PARIS_TROPHY_PROBABILITY,
    total_goals_120: float = ASSUMED_TOTAL_GOALS_TO_120,
) -> tuple[float, float]:
    low = -total_goals_120 + 0.02
    high = total_goals_120 - 0.02
    for _ in range(60):
        diff = (low + high) / 2
        paris_rate = (total_goals_120 + diff) / 2
        arsenal_rate = (total_goals_120 - diff) / 2
        probability = trophy_probability_from_state(0, 0, 0, paris_rate, arsenal_rate)
        if probability < target_probability:
            low = diff
        else:
            high = diff
    diff = (low + high) / 2
    return (total_goals_120 + diff) / 2, (total_goals_120 - diff) / 2


def shootout_probability(
    completed: list[dict[str, str | int]],
    conversion_probability: float = PENALTY_CONVERSION_PROBABILITY,
) -> float:
    score = {PARIS: 0, ARSENAL: 0}
    attempts = {PARIS: 0, ARSENAL: 0}
    for kick in completed:
        team = str(kick["team"])
        attempts[team] += 1
        if kick["result"] == "Scored":
            score[team] += 1

    next_team_by_order = [PARIS, ARSENAL] * 5

    def recurse(order_index: int, paris_score: int, arsenal_score: int) -> float:
        paris_taken = (order_index + 1) // 2
        arsenal_taken = order_index // 2
        paris_remaining = 5 - paris_taken
        arsenal_remaining = 5 - arsenal_taken
        if paris_score > arsenal_score + arsenal_remaining:
            return 1.0
        if arsenal_score > paris_score + paris_remaining:
            return 0.0
        if order_index >= 10:
            if paris_score > arsenal_score:
                return 1.0
            if paris_score < arsenal_score:
                return 0.0
            return 0.5
        team = next_team_by_order[order_index]
        if team == PARIS:
            made = recurse(order_index + 1, paris_score + 1, arsenal_score)
            missed = recurse(order_index + 1, paris_score, arsenal_score)
        else:
            made = recurse(order_index + 1, paris_score, arsenal_score + 1)
            missed = recurse(order_index + 1, paris_score, arsenal_score)
        return conversion_probability * made + (1 - conversion_probability) * missed

    order_index = len(completed)
    return float(recurse(order_index, score[PARIS], score[ARSENAL]))


def build_win_probability_timeline(shootout: pd.DataFrame) -> pd.DataFrame:
    paris_rate, arsenal_rate = fit_goal_rates_for_prematch()
    rows = []
    for minute in range(0, 121):
        if minute < 6:
            paris_score, arsenal_score = 0, 0
            event = "Kickoff score state"
        elif minute < 65:
            paris_score, arsenal_score = 0, 1
            event = "Arsenal led 1-0"
        else:
            paris_score, arsenal_score = 1, 1
            event = "Match level 1-1"
        paris_probability = trophy_probability_from_state(
            paris_score, arsenal_score, minute, paris_rate, arsenal_rate
        )
        rows.append(
            {
                "timeline_x": float(minute),
                "phase": "match",
                "minute": minute,
                "event": event,
                "paris_win_probability": paris_probability,
                "arsenal_win_probability": 1 - paris_probability,
                "model_note": "Score-state Poisson model calibrated to a 56% pre-match Paris probability.",
            }
        )
    completed: list[dict[str, str | int]] = []
    rows.append(
        {
            "timeline_x": 120.25,
            "phase": "shootout",
            "minute": 120,
            "event": "Before shootout",
            "paris_win_probability": 0.5,
            "arsenal_win_probability": 0.5,
            "model_note": "Shootout model assumes equal teams and 75% conversion for each remaining kick.",
        }
    )
    for _, row in shootout.iterrows():
        completed.append(row.to_dict())
        paris_probability = shootout_probability(completed)
        rows.append(
            {
                "timeline_x": 121 + int(row["order"]) - 1,
                "phase": "shootout",
                "minute": 120,
                "event": f"Penalty {int(row['order'])}: {row['team']} {row['result']}",
                "paris_win_probability": paris_probability,
                "arsenal_win_probability": 1 - paris_probability,
                "model_note": "Shootout model assumes equal teams and 75% conversion for each remaining kick.",
            }
        )
    return pd.DataFrame(rows)


def build_tables() -> tuple[
    pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame
]:
    control = pd.DataFrame(CONTROL_STATS)
    control["paris_to_arsenal_ratio"] = control["paris"] / control["arsenal"].replace(0, np.nan)
    control["difference"] = control["paris"] - control["arsenal"]

    events = pd.DataFrame(MATCH_EVENTS)
    shootout = pd.DataFrame(SHOOTOUT)
    sources = pd.DataFrame(SOURCES)
    win_probability = build_win_probability_timeline(shootout)
    substitutions = pd.DataFrame(SUBSTITUTIONS)
    substitutions["minutes_after_entry_to_120"] = 120 - substitutions["minute"]
    vitinha = pd.DataFrame(VITINHA_PROFILE)
    return control, events, shootout, sources, win_probability, substitutions, vitinha


def save_tables(
    control: pd.DataFrame,
    events: pd.DataFrame,
    shootout: pd.DataFrame,
    sources: pd.DataFrame,
    win_probability: pd.DataFrame,
    substitutions: pd.DataFrame,
    vitinha: pd.DataFrame,
) -> None:
    control.to_csv(TABLE_DIR / "match_control_stats.csv", index=False)
    events.to_csv(TABLE_DIR / "match_events.csv", index=False)
    shootout.to_csv(TABLE_DIR / "penalty_shootout_sequence.csv", index=False)
    win_probability.to_csv(TABLE_DIR / "win_probability_timeline.csv", index=False)
    substitutions.to_csv(TABLE_DIR / "substitution_summary.csv", index=False)
    vitinha.to_csv(TABLE_DIR / "vitinha_profile.csv", index=False)
    sources.to_csv(TABLE_DIR / "source_notes.csv", index=False)
    metadata = {
        "project": "uefa_champions_league_final_2026_match_control",
        "source_checked_date": date.today().isoformat(),
        "match_date": "2026-05-30",
        "match": f"{PARIS} vs {ARSENAL}",
        "result": "1-1 after extra time; Paris Saint-Germain won 4-3 on penalties.",
        "method": "Descriptive comparison of match-control indicators, score-state win probability, player profile, and substitution leverage.",
        "win_probability_model": {
            "prematch_paris_probability": PREMATCH_PARIS_TROPHY_PROBABILITY,
            "assumed_total_goals_to_120": ASSUMED_TOTAL_GOALS_TO_120,
            "penalty_conversion_probability": PENALTY_CONVERSION_PROBABILITY,
            "caveat": "Model estimate from public events, not an official live win-probability feed.",
        },
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
    fig, ax = plt.subplots(figsize=(13, 3.6))
    ax.hlines(0, 0, 120, color="#a8b3c2", linewidth=3)
    ax.scatter([0, 45, 90, 120], [0, 0, 0, 0], s=55, color="#344054", zorder=3)
    for minute, label in [(0, "Kickoff"), (45, "Half-time"), (90, "Full-time"), (120, "120 min")]:
        ax.text(minute, -0.58, label, ha="center", va="top", color=COLORS["muted"], fontsize=10)

    for row in events.to_dict("records"):
        minute = row["minute"]
        team = row["team"]
        color = COLORS.get(team, COLORS["score"])
        marker_y = 0.28 if row["event_id"] % 2 else -0.28
        ax.vlines(minute, 0, marker_y, color=color, linewidth=2, alpha=0.9)
        ax.scatter(minute, marker_y, s=420, color=color, zorder=4)
        ax.text(
            minute,
            marker_y,
            str(row["event_id"]),
            ha="center",
            va="center",
            fontsize=11,
            color="white",
            fontweight="bold",
            zorder=5,
        )
    ax.set_xlim(-3, 123)
    ax.set_ylim(-0.95, 0.78)
    ax.set_yticks([])
    ax.set_xlabel("Match minute")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#c7ced8")
    ax.grid(False)
    output = FIGURE_DIR / "match_timeline_numbered.png"
    fig.savefig(output)
    plt.close(fig)
    return output


def plot_win_probability(win_probability: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    ax.plot(
        win_probability["timeline_x"],
        win_probability["paris_win_probability"] * 100,
        color=COLORS[PARIS],
        linewidth=2.4,
        label="Paris",
    )
    ax.plot(
        win_probability["timeline_x"],
        win_probability["arsenal_win_probability"] * 100,
        color=COLORS[ARSENAL],
        linewidth=2.4,
        label="Arsenal",
    )
    for x in [6, 65, 120]:
        ax.axvline(x, color="#9aa4b2", linewidth=0.9, linestyle="--", alpha=0.8)
    key_points = win_probability[
        win_probability["event"].isin(
            [
                "Kickoff score state",
                "Arsenal led 1-0",
                "Match level 1-1",
                "Before shootout",
                "Penalty 10: Arsenal Missed",
            ]
        )
    ].drop_duplicates("event", keep="first")
    ax.scatter(
        key_points["timeline_x"],
        key_points["paris_win_probability"] * 100,
        s=36,
        color=COLORS[PARIS],
        zorder=4,
    )
    ax.set_ylim(0, 100)
    ax.set_xlim(0, 130)
    ax.set_ylabel("Estimated trophy probability (%)")
    ax.set_xlabel("Match minute; penalty kicks are spread from 121 to 130")
    ax.grid(axis="y", color=COLORS["grid"], linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=2, frameon=False)
    output = FIGURE_DIR / "win_probability_timeline.png"
    fig.savefig(output)
    plt.close(fig)
    return output


def plot_substitution_leverage(substitutions: pd.DataFrame) -> Path:
    data = substitutions.sort_values(["team", "minute", "player_on"]).reset_index(drop=True)
    labels = [name.replace(" ", "\n", 1) for name in data["player_on"]]
    y = np.arange(len(data))
    fig, ax = plt.subplots(figsize=(11.5, 8.8))
    colors = [COLORS[team] for team in data["team"]]
    ax.hlines(y, data["minute"], 120, color=colors, linewidth=5, alpha=0.24)
    marker_map = {"Scored": "o", "Missed": "X", "Saved": "X", "No penalty": "s"}
    for idx, row in data.iterrows():
        marker = marker_map[row["penalty_role"]]
        face = COLORS[row["team"]] if row["penalty_role"] == "Scored" else "white"
        edge = COLORS[row["team"]] if row["penalty_role"] != "Missed" else "#111827"
        ax.scatter(
            row["minute"],
            idx,
            marker=marker,
            s=130,
            facecolor=face,
            edgecolor=edge,
            linewidth=1.8,
            zorder=3,
        )
    ax.set_yticks(y, labels)
    ax.set_xlim(60, 121)
    ax.set_xlabel("Substitution minute")
    ax.set_ylabel("Player entering")
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.8, alpha=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    legend_handles = [
        plt.Line2D([0], [0], marker="o", color="none", markerfacecolor="#6b7280", markeredgecolor="#6b7280", markersize=8, label="Penalty scored"),
        plt.Line2D([0], [0], marker="X", color="none", markerfacecolor="#111827", markeredgecolor="#111827", markersize=8, label="Penalty missed/saved"),
        plt.Line2D([0], [0], marker="s", color="none", markerfacecolor="white", markeredgecolor="#6b7280", markersize=8, label="No penalty kick"),
    ]
    ax.legend(handles=legend_handles, loc="upper center", bbox_to_anchor=(0.5, 1.08), ncol=3, frameon=False)
    output = FIGURE_DIR / "substitution_leverage.png"
    fig.savefig(output)
    plt.close(fig)
    return output


def plot_vitinha_profile(vitinha: pd.DataFrame) -> Path:
    metric_values = (
        vitinha[vitinha["metric"].str.contains("per 90")]
        .assign(numeric_value=lambda data: pd.to_numeric(data["value"], errors="coerce"))
        .dropna(subset=["numeric_value"])
        .sort_values("numeric_value")
    )
    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    y = np.arange(len(metric_values))
    ax.barh(y, metric_values["numeric_value"], color=COLORS[PARIS], height=0.5)
    ax.set_yticks(y, metric_values["metric"])
    ax.set_xlabel("Per 90 minutes, Champions League season")
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.8, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    xmax = metric_values["numeric_value"].max() * 1.18
    ax.set_xlim(0, xmax)
    for yi, value in zip(y, metric_values["numeric_value"]):
        ax.text(value, yi, f"  {value:.1f}", va="center", ha="left", fontsize=10.5)
    output = FIGURE_DIR / "vitinha_profile.png"
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


def build_report(
    control: pd.DataFrame,
    events: pd.DataFrame,
    shootout: pd.DataFrame,
    win_probability: pd.DataFrame,
    substitutions: pd.DataFrame,
    vitinha: pd.DataFrame,
) -> Path:
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
    event_display = events[["event_id", "minute", "phase", "team", "event", "score"]].rename(
        columns={
            "event_id": "#",
            "minute": "Minute",
            "phase": "Phase",
            "team": "Team",
            "event": "Event",
            "score": "Score",
        }
    )
    key_win_probability = win_probability[
        (win_probability["timeline_x"].isin([0.0, 6.0, 65.0, 90.0, 120.0]))
        | (win_probability["event"].isin(["Before shootout", "Penalty 10: Arsenal Missed"]))
    ].copy()
    key_win_probability["Paris"] = (key_win_probability["paris_win_probability"] * 100).map(
        lambda value: f"{value:.1f}%"
    )
    key_win_probability["Arsenal"] = (key_win_probability["arsenal_win_probability"] * 100).map(
        lambda value: f"{value:.1f}%"
    )
    key_win_probability["Point"] = key_win_probability["event"]
    key_win_probability.loc[key_win_probability["timeline_x"] == 0, "Point"] = "Kickoff"
    key_win_probability.loc[key_win_probability["timeline_x"] == 6, "Point"] = "After Arsenal goal"
    key_win_probability.loc[key_win_probability["timeline_x"] == 65, "Point"] = "After Paris equalizer"
    key_win_probability.loc[key_win_probability["timeline_x"] == 90, "Point"] = "End of normal time"
    key_win_probability.loc[key_win_probability["timeline_x"] == 120, "Point"] = "After extra time"
    key_win_probability_display = key_win_probability[["Point", "Paris", "Arsenal"]]
    substitution_display = substitutions[
        ["team", "minute", "player_on", "player_off", "penalty_role", "contribution"]
    ].rename(
        columns={
            "team": "Team",
            "minute": "Minute",
            "player_on": "Player on",
            "player_off": "Player off",
            "penalty_role": "Penalty role",
            "contribution": "Contribution note",
        }
    )
    vitinha_display = vitinha.rename(
        columns={"metric": "Metric", "value": "Value", "interpretation": "Interpretation"}
    )
    source_items = "\n".join(
        f"<li><a href=\"{html.escape(source['url'])}\">{html.escape(source['name'])}</a>: "
        f"{html.escape(source['used_for'])}</li>"
        for source in SOURCES
    )
    figure_blocks = "\n".join(
        [
            '<figure><img src="../figures/team_control_snapshot.png" alt="Team control metrics for Paris Saint-Germain and Arsenal"><figcaption>Paris led the main match-control indicators by a wide margin.</figcaption></figure>',
            '<figure><img src="../figures/control_gap_vs_scoreline.png" alt="Paris to Arsenal ratio for control metrics and score after extra time"><figcaption>The control gap was roughly three to four times larger, while the 120-minute score stayed level.</figcaption></figure>',
            '<figure><img src="../figures/win_probability_timeline.png" alt="Estimated trophy probability timeline for Paris Saint-Germain and Arsenal"><figcaption>Model estimate from score state and shootout state. This is not an official live win-probability feed.</figcaption></figure>',
            '<figure><img src="../figures/match_timeline_numbered.png" alt="Numbered timeline of main events in the 2026 UEFA Champions League final"><figcaption>Numbered markers avoid placing long labels over the event timeline. Details are listed below.</figcaption></figure>',
            '<figure><img src="../figures/vitinha_profile.png" alt="Vitinha Champions League per 90 profile"><figcaption>Vitinha season profile explains why his Player of the Match selection fits the match-control story.</figcaption></figure>',
            '<figure><img src="../figures/substitution_leverage.png" alt="Substitution timing and penalty contribution"><figcaption>Several late substitutions mattered most through penalty responsibilities rather than open-play volume.</figcaption></figure>',
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

  <div class="callout"><strong>Punchline:</strong> Paris had about three times Arsenal's possession share and shot volume, and more than four times the completed passes, but the final still reached penalties at 1-1. A simple score-state win-probability model flips toward Arsenal after the sixth-minute goal, then returns toward a coin flip after Paris equalizes.</div>

  <h2>Background</h2>
  <p>The Union of European Football Associations (UEFA) match report records the final as Paris Saint-Germain 1-1 Arsenal after extra time, with Paris winning 4-3 on penalties at the Puskas Arena in Budapest. Arsenal led through Kai Havertz in the sixth minute. Paris equalized through an Ousmane Dembele penalty in the 65th minute.</p>

  <h2>Purpose</h2>
  <p>This analysis separates match control from match outcome. The goal is to show, in a few readable figures, how a final can be statistically one-sided in possession, shots, and passing volume, while still being decided by one kick in a shootout.</p>

  <h2>Method</h2>
  <p>The project uses small, source-cited tables rather than storing a heavy raw feed. Match outcome, key events, substitutions, and Player of the Match context come from UEFA. Control indicators come from public Opta-derived reporting: Arsenal's 24.7% possession figure, Paris' 21-7 shot advantage, and the 806-196 completed-pass comparison. Paris' possession share is inferred as 100% minus Arsenal's reported share.</p>
  <p>The win-probability curve is a simple model, not an official live feed. It starts from an Opta pre-match forecast of 56% for Paris, uses a Poisson score-state model to 120 minutes, and treats a tied match after extra time as a 50/50 shootout before applying the actual penalty sequence with a neutral 75% conversion assumption for remaining kicks.</p>

  <h2>Results</h2>
  {render_table(control_display, ["Metric", PARIS, ARSENAL, "Paris / Arsenal", "Source"])}
  {figure_blocks}
  <h2>Event Key</h2>
  {render_table(event_display, ["#", "Minute", "Phase", "Team", "Event", "Score"])}

  <h2>Win Probability Read</h2>
  {render_table(key_win_probability_display, ["Point", "Paris", "Arsenal"])}
  <p>The model view says Arsenal's early goal mattered more than the aggregate control numbers at that moment. Paris still had the stronger underlying profile, but the clock and score state moved the estimated trophy probability toward Arsenal until the 65th-minute equalizer. Once the match reached penalties at 1-1, the model resets to roughly even before the actual shootout sequence separates the teams.</p>

  <h2>Vitinha</h2>
  {render_table(vitinha_display, ["Metric", "Value", "Interpretation"])}
  <p>Vitinha's role is the bridge between the team-level data and the player-level story. Paris' control was not only possession for possession's sake. His season profile shows high passing volume, line-breaking passes, build-up involvement, and progressive carries. That makes his Player of the Match selection consistent with the way Paris pinned Arsenal into a low-possession final.</p>

  <h2>Substitutions</h2>
  {render_table(substitution_display, ["Team", "Minute", "Player on", "Player off", "Penalty role", "Contribution note"])}
  <p>The substitutes changed the match less through open-play goals than through the shootout. Paris got converted penalties from late entrants Goncalo Ramos and Lucas Beraldo. Arsenal got converted penalties from Viktor Gyokeres and Gabriel Martinelli, but Eberechi Eze's miss created the first major shootout break toward Paris.</p>

  <h2>Interpretation</h2>
  <p>The clearest read is that Paris controlled the match environment, but did not turn that control into scoreboard separation. Arsenal scored early, defended deep, and kept Paris to one goal across normal and extra time. The win-probability model adds the time dimension: control was one-sided in aggregate, but the game state was not stable for Paris until the equalizer.</p>
  <p>The completed-pass gap is especially strong: Paris completed more than four passes for every one Arsenal completed. The shot gap is also large, but the 120-minute score stayed 1-1. That tension is the main story for a public data post.</p>

  <h2>Limitations</h2>
  <ul>
    <li>Possession, pass, and shot counts can differ by provider definitions. This report keeps the provider notes visible rather than blending incompatible feeds.</li>
    <li>The win-probability curve is a transparent model from score state and penalty state. It is not a bookmaker probability, an Opta live probability feed, or a tactical simulation.</li>
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
    control, events, shootout, sources, win_probability, substitutions, vitinha = build_tables()
    save_tables(control, events, shootout, sources, win_probability, substitutions, vitinha)
    plot_team_control_snapshot(control)
    plot_control_gap_vs_scoreline(control)
    plot_win_probability(win_probability)
    plot_match_timeline(events)
    plot_vitinha_profile(vitinha)
    plot_substitution_leverage(substitutions)
    plot_penalty_shootout(shootout)
    build_report(control, events, shootout, win_probability, substitutions, vitinha)


if __name__ == "__main__":
    main()
