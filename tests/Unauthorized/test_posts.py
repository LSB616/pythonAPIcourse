def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_unauthorized_create_post(client):
    res = client.post("/posts/", json={"title": "test_post 1", "content": "test_post content 1", "published": False})
    assert res.status_code == 401

def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_unauthorized_put_post(client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": False
    }
    res = client.put(f"/posts/{test_posts[2].id}", json=data)
    assert res.status_code == 401