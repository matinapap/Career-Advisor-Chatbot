from career_advisor.text_utils import clean_output


def test_clean_output_handles_empty_values():
    assert clean_output("") == "(No output)"
    assert clean_output(None) == "(No output)"


def test_clean_output_strips_basic_html_document():
    raw = "<!DOCTYPE html><html><body><h1>Error</h1><p>Try again</p></body></html>"

    cleaned = clean_output(raw)

    assert "Error" in cleaned
    assert "Try again" in cleaned
    assert "<h1>" not in cleaned


def test_clean_output_keeps_plain_text_unchanged():
    assert clean_output("Plain answer") == "Plain answer"
