from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    post = schemas.PostOut(**res.json()[0])
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert post.Post.title == "1st title"
    assert post.Post.content == "1st content"
    assert post.Post.owner_id == 1

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[1].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.title == "2nd title"
    assert post.Post.content == "2nd content"
    assert post.Post.owner_id == 1

def test_get_one_post_errors(authorized_client):
    res = authorized_client.get("/posts/1000")
    assert res.status_code == 404

def test_create_post(authorized_client, test_user):
    #Published is False
    res_1 = authorized_client.post("/posts/", json={"title": "test_post 1", "content": "test_post content 1", "published": False})
    assert res_1.status_code == 201
    post_1 = schemas.Post(**res_1.json())
    assert post_1.title == "test_post 1"
    assert post_1.content == "test_post content 1"
    assert post_1.owner_id == 1
    assert post_1.published == False

    #Published is True
    res_2 = authorized_client.post("/posts/", json={"title": "test_post 2", "content": "test_post content 2", "published": True})
    assert res_2.status_code == 201
    post_2 = schemas.Post(**res_2.json())
    assert post_2.published == True

    #Published is defaulted
    res_3 = authorized_client.post("/posts/", json={"title": "test_post 3", "content": "test_post content 3"})
    assert res_3.status_code == 201
    post_3 = schemas.Post(**res_3.json())
    assert post_3.published == True

@pytest.mark.parametrize("title, content, published", [
    (None, "test_post content 4", True),
    ("test_post 4", "test_post content 4", 12),
    ("test_post 4", "test_post content 4", "string"),
    (None, None, None),
])

def test_create_post_errors(authorized_client, title, content, published):
 res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
 assert res.status_code == 422


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_errors(authorized_client):
    res_1 = authorized_client.delete("/posts/1000")
    assert res_1.status_code == 404

    res_2 = authorized_client.delete("/posts/asdfg")
    assert res_2.status_code == 422

def test_delete_other_users_post(authorized_client):
    res = authorized_client.delete("/posts/4")
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": False
    }
    authorized_client.put(f"/posts/{test_posts[1].id}", json=data)
    res = authorized_client.get(f"/posts/{test_posts[1].id}")
    updated_post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert updated_post.Post.title == data['title']
    assert updated_post.Post.content == data['content']
    assert updated_post.Post.published == data['published']

def test_update_other_users_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": False
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

@pytest.mark.parametrize("title, content, published", [
(None, "updated content", False),
("updated title", None, False),
("updated title", "updated content", "asfgjh"),
("updated title", "updated content", 123),
(None, None, None)
])
def test_update_post_errors(authorized_client, test_posts, title, content, published):
    data = {
        "title": title,
        "content": content,
        "published": published
    }
    res_1 = authorized_client.put(f"/posts/{test_posts[1].id}", json=data)
    assert res_1.status_code == 422

    #update non-existant post
    res_2 = authorized_client.put("/posts/1000", json={"title": "updated title", "content": "updated content", "published": False})
    assert res_2.status_code == 404