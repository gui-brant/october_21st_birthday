from app.services.leveling import apply_exp, exp_required_for_level, hours_required_for_level


def test_level_milestones():
    assert hours_required_for_level(1) == 1.0
    assert hours_required_for_level(28) == 4.0
    assert round(hours_required_for_level(756), 2) == 8.0
    assert round(hours_required_for_level(1848), 2) == 16.0


def test_exp_formula():
    assert exp_required_for_level(1) == 100.0
    assert exp_required_for_level(14) == 200.0


def test_apply_exp_level_up():
    required = exp_required_for_level(1)
    progress = apply_exp(current_level=1, current_exp=0.0, gained_exp=required + 10.0)
    assert progress.level_before == 1
    assert progress.level_after == 2
    assert progress.exp_after == 10.0
