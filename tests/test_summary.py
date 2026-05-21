import pytest
from fastapi.testclient import TestClient
from main import app
from services.classes import SummaryService
from storage.database import delete_user, get_user_by_username



client = TestClient(app)
def get_testdata():
    data = {
        'username': 'user95',
        'password': 'pass1',
    }
    return data
def get_test_user():
    data = get_testdata()
    return data['username']

def test_calculate_earned():
    result = SummaryService.calculate_earned(8.0, 15.0)
    assert result == 120

def test_calculate_earned_zero_hours():
    result = SummaryService.calculate_earned(0.0, 15.0)
    assert result == 0

def test_calculate_earned_float():
    result = SummaryService.calculate_earned(7.5, 10.0)
    assert result == 75

def test_auth_flow():
    response = client.post('/auth/register', data=get_testdata())
    assert response.status_code == 200
    assert 'access_token' in response.json()

    response = client.post('/auth/login', data=get_testdata())
    assert response.status_code == 200
    assert 'access_token' in response.json()
    user = get_user_by_username(get_test_user())
    delete_user(user['id'])

def test_get_shifts():
    response = client.post('/auth/register', data=get_testdata())
    assert response.status_code == 200
    assert 'access_token' in response.json()
    token = response.json()['access_token']

    response = client.get('/shifts', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    user = get_user_by_username(get_test_user())
    delete_user(user['id'])

def test_get_summary():
    response = client.post('/auth/register', data=get_testdata())
    assert response.status_code == 200
    assert 'access_token' in response.json()
    token = response.json()['access_token']
    response = client.get('/summary', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    user = get_user_by_username(get_test_user())
    delete_user(user['id'])