def test_unauthorized_vote_on_post(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[2].id, "dir": 1})
    assert res.status_code == 401

def test_unauthorized_delete_vote_on_post(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 401