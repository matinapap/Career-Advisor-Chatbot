import json

from career_advisor import preferences


def test_load_preferences_creates_default_file(tmp_path, monkeypatch):
    prefs_file = tmp_path / "user_personalization.json"
    monkeypatch.setattr(preferences, "DATA_DIR", tmp_path)
    monkeypatch.setattr(preferences, "PREFS_FILE", prefs_file)

    learning_style, career_goals = preferences.load_personalization_preferences()

    assert learning_style == "visual"
    assert career_goals
    assert prefs_file.exists()


def test_save_and_load_preferences_round_trip(tmp_path, monkeypatch):
    prefs_file = tmp_path / "user_personalization.json"
    monkeypatch.setattr(preferences, "DATA_DIR", tmp_path)
    monkeypatch.setattr(preferences, "PREFS_FILE", prefs_file)

    preferences.save_user_preferences("hands-on", "Work remotely")

    assert preferences.load_personalization_preferences() == ("hands-on", "Work remotely")
    assert json.loads(prefs_file.read_text(encoding="utf-8")) == {
        "learning_style": "hands-on",
        "career_goals": "Work remotely",
    }
