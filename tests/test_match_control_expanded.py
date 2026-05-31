import math

from run_ucl_final_match_control_expanded import build_tables


def test_control_ratio_highlights_score_gap():
    control, _, _, _, _, _, _ = build_tables()
    ratios = dict(zip(control["metric"], control["paris_to_arsenal_ratio"]))

    assert ratios["Goals after extra time"] == 1
    assert ratios["Total shots"] == 3
    assert ratios["Completed passes"] > 4
    assert ratios["Possession share"] > 3


def test_paris_possession_is_inferred_complement():
    control, _, _, _, _, _, _ = build_tables()
    possession = control[control["metric"] == "Possession share"].iloc[0]

    assert math.isclose(possession["paris"] + possession["arsenal"], 100.0)


def test_shootout_final_running_score():
    _, _, shootout, _, _, _, _ = build_tables()

    assert shootout.iloc[-1]["running_score"] == "4-3"
    assert shootout[shootout["result"] != "Scored"].shape[0] == 3


def test_win_probability_moves_with_score_state():
    _, _, _, _, win_probability, _, _ = build_tables()
    kickoff = win_probability[win_probability["timeline_x"] == 0].iloc[0]
    after_arsenal_goal = win_probability[win_probability["timeline_x"] == 6].iloc[0]
    after_paris_equalizer = win_probability[win_probability["timeline_x"] == 65].iloc[0]
    after_extra_time = win_probability[win_probability["timeline_x"] == 120].iloc[0]

    assert kickoff["paris_win_probability"] > 0.5
    assert after_arsenal_goal["paris_win_probability"] < kickoff["paris_win_probability"]
    assert after_paris_equalizer["paris_win_probability"] > after_arsenal_goal["paris_win_probability"]
    assert math.isclose(after_extra_time["paris_win_probability"], 0.5, abs_tol=0.01)
