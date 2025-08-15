import pytest
import os
from flask_auth_service.app import create_app

@pytest.fixture
def app():
    """Create application for the tests."""
    os.environ['VALID_KEYS'] = 'test-key-1:tenant1,tenant2;test-key-2:tenant3'
    app = create_app({'TESTING': True})
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_health_endpoint(client):
    """Test health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['keys_configured'] is True

def test_validate_valid_token(client):
    """Test validation with valid token."""
    response = client.post('/validate', headers={
        'Authorization': 'Bearer test-key-1',
        'tenant': 'tenant1'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['subject'] == 'authorized-user'

def test_validate_invalid_token(client):
    """Test validation with invalid token."""
    response = client.post('/validate', headers={
        'Authorization': 'Bearer invalid-key',
        'tenant': 'tenant1'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'unauthorized'

def test_validate_no_token(client):
    """Test validation without token."""
    response = client.post('/validate', headers={
        'tenant': 'tenant1'
    })
    assert response.status_code == 401

def test_index_endpoint(client):
    """Test index endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['service'] == 'Flask Auth Service'