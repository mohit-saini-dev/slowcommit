from slowcommit.core import bounded_diff, build_prompt, clean_message, redact_secrets

def test_redacts_common_assignment_secret():
    result = redact_secrets('api_key = "abcdefgh1234567890"')
    assert "abcdefgh1234567890" not in result
    assert "[REDACTED]" in result

def test_redacts_github_token_shape():
    result = redact_secrets("token ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456")
    assert "ghp_" not in result
    assert "[REDACTED_TOKEN]" in result

def test_bounded_diff_marks_truncation():
    result = bounded_diff("x" * 100, max_chars=40)
    assert len(result) <= 40
    assert "truncated" in result

def test_build_prompt_marks_diff_untrusted():
    prompt = build_prompt("diff --git a/a.py b/a.py\n+print('hello')")
    assert "STAGED DIFF START" in prompt
    assert "untrusted" in prompt

def test_clean_message_uses_first_nonempty_line():
    assert clean_message("\n```text\nfix: handle empty input\nextra details\n```") == "fix: handle empty input"

def test_clean_message_empty():
    assert clean_message(" \n ") == ""
