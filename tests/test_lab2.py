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

def test_predict():
    test_features = {
        "MedInc":22.01,
        "HouseAge":4.5,
        "AveRooms":3.5,
        "AveBedrms":1.5,
        "Population":200.5,
        "AveOccup":2.5,
        "Latitude":34.5,
        "Longitude":90.5
    }
    response = client.post(
        "/predict",
        json=test_features
    )
    assert response.status_code == 200
    assert type(response.json()) == float

def test_invalid_predict():
    test_features_1 = {
        "MedInc":'try',
        "HouseAge":7.9,
        "AveRooms":3.5,
        "AveBedrms":3.4,
        "Population":20.5,
        "AveOccup":12.5,
        "Latitude":70.5,
        "Longitude":-120.5
    }
    test_features_2 = {
        "MedInc":11.0,
        "HouseAge":7.9,
        "AveRooms":3.5,
        "AveBedrms":3.4,
        "Population":20.5,
        "AveOccup":12.5,
        "Latitude":-337.5,
        "Longitude":-120.5
    }
    test_features_3 = {
        "MedInc":22.0,
        "HouseAge":7.9,
        "AveRooms":3.5,
        "AveBedrms":3.4,
        "Population":20.5,
        "AveOccup":12.5,
        "Latitude":75.1,
        "Longitude":-1120.5
    }
    response = client.post(
        "/predict",
        json=test_features_1
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'][1] == 'MedInc'
    assert response.json()['detail'][0]['msg'] == "value is not a valid float"

    response = client.post(
        "/predict",
        json=test_features_2
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'][1] == 'Latitude'
    assert response.json()['detail'][0]['msg'] == "Must lie within -90 to 90"

    response = client.post(
        "/predict",
        json=test_features_3
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'][1] == 'Longitude'
    assert response.json()['detail'][0]['msg'] == "Must lie within -180 to 180"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200