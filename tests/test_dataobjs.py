from httpobjects import WebSearchRequest


def test_init_websearch():
    no_optional = WebSearchRequest(q="Query here")
    assert not no_optional.summary

