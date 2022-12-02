from email import header
from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest

from src.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 501
    assert response.json() == {'detail': 'The Endpoint is not implemented'}
    
def test_hello_name():
    name = 'Josh'
    response = client.get(f"/hello/?name={name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello {name}"}

def test_invalid_hello_name():
    name = ''
    response = client.get(f"/hello/?name={name}")
    assert response.status_code == 422

def test_get_docs():
    response = client.get(f"/docs")
    assert response.status_code == 200

def test_get_json():
    response = client.get(f"/openapi.json")
    assert response.status_code == 200

def test_health():
    response = client.get("/health")
    assert response.status_code == 200