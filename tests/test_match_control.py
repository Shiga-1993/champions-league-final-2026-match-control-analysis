import math

from run_ucl_final_match_control import build_tables


def test_control_ratio_highlights_score_gap():
    control, _, _, _ = build_tables()
    ratios = dict(zip(control["metric"], control["paris_to_arsenal_ratio"]))

    assert ratios["Goals after extra time"] == 1
    assert ratios["Total shots"] == 3
    assert ratios["Completed passes"] > 4
    assert ratios["Possession share"] > 3


def test_paris_possession_is_inferred_complement():
    control, _, _, _ = build_tables()
    possession = control[control["metric"] == "Possession share"].iloc[0]

    assert math.isclose(possession["paris"] + possession["arsenal"], 100.0)


def test_shootout_final_running_score():
    _, _, shootout, _ = build_tables()

    assert shootout.iloc[-1]["running_score"] == "4-3"
    assert shootout[shootout["result"] != "Scored"].shape[0] == 3
