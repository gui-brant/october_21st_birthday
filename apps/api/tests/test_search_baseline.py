def whitespace_insensitive_match(query: str, title: str) -> bool:
    needle = "".join(query.lower().split())
    hay = "".join(title.lower().split())
    return needle in hay


def test_whitespace_insensitive_matching():
    assert whitespace_insensitive_match("Arm 1", "Arm1")
    assert whitespace_insensitive_match("Arm ", "Arm 2")
    assert not whitespace_insensitive_match("Leg", "Arm 2")
