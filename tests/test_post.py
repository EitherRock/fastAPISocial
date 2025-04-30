import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get('/posts/')

    def validate(post): 
        return schemas.PostResponse(**post)
    
    # posts_map = map(validate, response.json())
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200
    

def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get('/posts/')
    assert response.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    response = client.get(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get('/posts/88888')
    print(response.json())
    assert response.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostVote(**response.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize('title, content, published', [
    ('new title test', 'new contetnt test', True),
    ('anopteorh new title test', 'more new contetnt test', False),
    ('new titledasfsdfsd test', 'new casdfasdfontetnt test', True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post('/posts/', json={'title': title, 'content': content, 'published': published})

    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content 
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    response = authorized_client.post('/posts/', json={'title': 'title', 'content': 'content'})

    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == 'title'
    assert created_post.content == 'content' 
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_posts(client, test_user, test_posts):
    response = client.post('/posts/', json={'title': 'title', 'content': 'content'})
    assert response.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    response = client.delete('/posts/{test_post[0].id}')
    assert response.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    response = authorized_client.delete('/posts/{test_post[0].id}')
    assert response.status_code == 204
