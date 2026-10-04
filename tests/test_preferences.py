from career_advisor import preferences


def test_default_preferences_are_populated():
    learning_style, career_goals = preferences.default_personalization_preferences()

    assert learning_style == "visual"
    assert career_goals


def test_preferences_module_does_not_write_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    preferences.default_personalization_preferences()

    assert list(tmp_path.iterdir()) == []
