from http import HTTPStatus

from fastapi import status
from fastapi.testclient import TestClient

from tech_clg.app import app

correct_headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer teste',
    'Content-Type': 'application/json',
}
client = TestClient(app)


def test_min_ano():
    data = {'df_key': 'Producao', 'year': 1970}

    response = client.post('/retorna_dados/', headers=correct_headers, json=data)

    assert response.status_code == HTTPStatus.OK


def test_max_ano():
    data = {'df_key': 'Producao', 'year': 2023}

    response = client.post('/retorna_dados/', headers=correct_headers, json=data)

    assert response.status_code == HTTPStatus.OK


def test_no_year():
    data = {
        'df_key': 'Producao',
    }

    response = client.post('/retorna_dados/', headers=correct_headers, json=data)

    assert response.status_code == HTTPStatus.OK


def test_cultivar_tables():
    data = {
        'df_key': 'ExpSuco',
    }
    response = client.post('/retorna_dados/', headers=correct_headers, json=data)

    assert response.status_code == HTTPStatus.OK


def test_cultivar_tables_year():
    data = {'df_key': 'ExpSuco', 'year': 2013}

    response = client.post('/retorna_dados/', headers=correct_headers, json=data)

    assert response.status_code == HTTPStatus.OK


def test_pais_tables():
    data = {'df_key': 'ImpSuco', 'year': 2013}

    response = client.post('/retorna_dados/', headers=correct_headers, json=data)

    assert response.status_code == HTTPStatus.OK


def test_pais_tables_year():
    data = {'df_key': 'ImpSuco', 'year': 2013}

    response = client.post('/retorna_dados/', headers=correct_headers, json=data)

    assert response.status_code == HTTPStatus.OK


def test_auth():
    wrong_headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer senha_errada',
        'Content-Type': 'application/json',
    }
    data = {
        'df_key': 'Producao',
    }
    response = client.post('/retorna_dados/', headers=wrong_headers, json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
