def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[4].id, "dir": 1})
    assert res.status_code == 201

def test_vote_on_post_twice(authorized_client, test_posts, test_vote):
    #original vote added in conftest file
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[4].id, "dir": 0})
    assert res.status_code == 201

def test_vote_errors(authorized_client, test_posts):
    #vote on post that does not exist
    res_1 = authorized_client.post("/vote/", json={"post_id": 1000, "dir": 1})
    assert res_1.status_code == 404

    res_2 = authorized_client.post("/vote/", json={"post_id": 1000, "dir": 0})
    assert res_2.status_code == 404

    #delete vote that does not exist
    res_3 = authorized_client.post("/vote/", json={"post_id": test_posts[1].id, "dir": 0})
    assert res_3.status_code == 404
