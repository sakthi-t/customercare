from agent.workflow import handle_query

def test_basic_query():
    response = handle_query("admin", "How many orders are cancelled?")
    assert "cancelled" in response.lower()
