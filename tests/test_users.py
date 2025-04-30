import pytest
from jose import jwt
from app.schemas import UserResponse, Token 
from app.config import settings


# def test_root(client):
#     response = client.get('/')
#     print(response.json().get('message'))
#     assert response.json().get('message') == 'Hello world!!!!'
#     assert response.status_code == 200

def test_create_user(client):
    response = client.post('/users/', json={"email": "hello@gmail.com", "password": "password123"})
    
    new_user = UserResponse(**response.json())

    assert new_user.email == 'hello@gmail.com'
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post(
        '/login', 
        data={
            "username": test_user['email'], 
            "password": test_user['password']
        }
    )

    login_response = Token(**response.json())

    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    print(response.json())
    assert id == test_user['id']
    assert login_response.token_type == 'bearer'
    assert response.status_code == 200


@pytest.mark.parametrize('email, password, status_code', [
    ('wrongemail@gmail.com', 'password123', 403),
    ('email@email.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('email@email.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):

    form_data = {}
    if email is not None:
        form_data['username'] = email
    
    if password is not None:
        form_data['password'] = password

    print(form_data)
    response = client.post(
        '/login', 
        data=form_data
    )

    assert response.status_code == status_code
    # assert response.json().get('detail') == 'Invalid Credentials'

