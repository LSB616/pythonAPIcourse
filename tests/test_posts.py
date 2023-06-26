from app import schemas
from typing import List

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    post = schemas.PostOut(**res.json()[0])
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert post.Post.title == "1st title"
    assert post.Post.content == "1st content"
    assert post.Post.owner_id == 1