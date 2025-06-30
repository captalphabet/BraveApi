from httpobjects import WebSearchRequest, ForumData, DiscussionResult


def test_init_websearch():
    no_optional = WebSearchRequest(q="Query here")
    assert not no_optional.summary

def test_forumdata_model():
    raw = {
        "forum_name": "StackOverflow",
        "num_answers": 5,
        "score": "10",
        "title": "How to test?",
        "question": "Testing forum post",
        "top_comment": "This is the answer",
    }
    fd = ForumData.model_validate(raw)
    assert fd.forum_name == "StackOverflow"
    assert fd.num_answers == 5
    assert fd.score == "10"
    assert fd.title == "How to test?"
    assert fd.question == "Testing forum post"
    assert fd.top_comment == "This is the answer"

def test_discussionresult_model():
    raw = {
        "type": "discussion",
        "subtype": "generic",
        "is_live": False,
        "language": "en",
        "data": {"forum_name": "TestForum"},
    }
    dr = DiscussionResult.model_validate(raw)
    assert dr.type == "discussion"
    assert dr.subtype == "generic"
    assert dr.data and dr.data.forum_name == "TestForum"

