import pytest
from flask_jwt_extended import create_access_token
from app import create_app
from db_models import db, Szamla, Befizetes, Ugyfel, Penzfelvetel, Utalas
from flask.testing import FlaskClient
import json


@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def adatbazis_generalasa(app):
    with app.app_context():
        admin_ugyfel = Ugyfel(id=1, email='admin@a.a', jelszo_hash='jelszo', admin=True)
        ugyfel = Ugyfel(id=2, email='user@a.a', jelszo_hash='jelszo', admin=False)
        szamla1 = Szamla(id=1, ugyfel_id=2, egyenleg=1000)
        szamla2 = Szamla(id = 2, ugyfel_id=2, egyenleg=1000)
        befizetes = Befizetes(id=1, osszeg=1000, szamla=1)
        penzfelvetel = Penzfelvetel(id=1, osszeg=500, szamla=1)
        utalas = Utalas(id=1, osszeg=100, utalo_szamla=1, fogado_szamla=1)

        db.session.add(admin_ugyfel)
        db.session.add(ugyfel)
        db.session.add(szamla1)
        db.session.add(szamla2)
        db.session.add(befizetes)
        db.session.add(penzfelvetel)
        db.session.add(utalas)
        db.session.commit()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture
def hozzaferesi_kulcs_admin_ugyfel(app):
    with app.app_context():
        admin_ugyfel = db.session.get(Ugyfel, 1)
        kulcs = create_access_token(identity=admin_ugyfel)
        return kulcs


@pytest.fixture
def hozzaferesi_kulcs_ugyfel(app):
    with app.app_context():
        ugyfel = db.session.get(Ugyfel, 2)
        kulcs = create_access_token(identity=ugyfel)
        return kulcs


def test_befizetes_lekerdezese_admin_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}'
    }
    response = client.get('/befizetesek/', headers=headers)
    assert response.status_code in [200, 404]

def test_befizetes_lekerdezese_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}'
    }
    response = client.get('/befizetesek/', headers=headers)
    assert response.status_code in [200, 404]


def test_befizetes_letrehozasa_admin_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 1000,
        "szamla": 1
    }
    response = client.post('/befizetesek/', data=json.dumps(data), headers=headers)
    assert response.status_code in [201, 404, 400, 423]


def test_befizetes_letrehozasa(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 1000,
        "szamla": 1
    }
    response = client.post('/befizetesek/', data=json.dumps(data), headers=headers)
    assert response.status_code in [201, 404, 400, 423]


def test_befizetes_lekerdezese_id_alapjan(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}'
    }
    response = client.get('/befizetesek/1', headers=headers)
    assert response.status_code in [200, 404]


def test_befizetes_lekerdezese_id_alapjan_admin_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}'
    }
    response = client.get('/befizetesek/1', headers=headers)
    assert response.status_code in [200, 404]

def test_befizetes_lekerdezese_id_alapjan_ugyfel_fail(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}'
    }
    response = client.get('/befizetesek/2', headers=headers)
    assert response.status_code in [404, 423]


def test_befizetes_modositasa(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 2000
    }
    response = client.put('/befizetesek/1', data=json.dumps(data), headers=headers)
    assert response.status_code in [200, 404, 400]


def test_befizetes_modositasa_fail(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 2000
    }
    response = client.put('/befizetesek/1', data=json.dumps(data), headers=headers)
    assert response.status_code in [423]


def test_befizetes_torlese_fail(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}'
    }
    response = client.delete('/befizetesek/1', headers=headers)
    assert response.status_code in [423]


def test_befizetes_torlese(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}'
    }
    response = client.delete('/befizetesek/1', headers=headers)
    assert response.status_code in [204, 404]


def test_unauthorized_access(client: FlaskClient, adatbazis_generalas):
    response = client.get('/befizetesek/')
    assert response.status_code == 401


def test_befizetes_letrehozasa_ervenytelen(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": "asdasd",
        "szamla": 1
    }
    response = client.post('/befizetesek/', data=json.dumps(data), headers=headers)
    assert response.status_code in [400, 404]


def test_penzfelvetel_lekerdezese_admin_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}'
    }
    response = client.get('/penzfelvetel/', headers=headers)
    assert response.status_code in [200, 404]


def test_penzfelvetel_lekerdezese_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}'
    }
    response = client.get('/penzfelvetel/', headers=headers)
    assert response.status_code in [200, 404]


def test_penzfelvetel_letrehozasa_admin_ugyfel_fail(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 500,
        "szamla": 4
    }
    response = client.post('/penzfelvetel/', data=json.dumps(data), headers=headers)
    assert response.status_code in [404]


def test_penzfelvetel_letrehozasa_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 500,
        "szamla": 1
    }
    response = client.post('/penzfelvetel/', data=json.dumps(data), headers=headers)
    assert response.status_code in [201, 404, 400, 423]


def test_penzfelvetel_lekerdezese_id_alapjan_admin_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}'
    }
    response = client.get('/penzfelvetel/1', headers=headers)
    assert response.status_code in [200, 404]


def test_penzfelvetel_lekerdezese_id_alapjan_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}'
    }
    response = client.get('/penzfelvetel/1', headers=headers)
    assert response.status_code in [200, 404]


def test_penzfelvetel_modositasa(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 700
    }
    response = client.put('/penzfelvetel/1', data=json.dumps(data), headers=headers)
    assert response.status_code in [200, 404, 400]


def test_penzfelvetel_modositasa_fail(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 700
    }
    response = client.put('/penzfelvetel/1', data=json.dumps(data), headers=headers)
    assert response.status_code in [423]


def test_penzfelvetel_torlese_fail(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}'
    }
    response = client.delete('/penzfelvetel/1', headers=headers)
    assert response.status_code in [423]


def test_penzfelvetel_torlese(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}'
    }
    response = client.delete('/penzfelvetel/1', headers=headers)
    assert response.status_code in [204, 404]


# Additional tests for Utalasok

def test_utalasok_lekerdezese_admin_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}'
    }
    response = client.get('/utalasok/', headers=headers)
    assert response.status_code in [200, 404]


def test_utalasok_lekerdezese_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}'
    }
    response = client.get('/utalasok/', headers=headers)
    assert response.status_code in [200, 404]


def test_utalasok_letrehozasa(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 100,
        "utalo_szamla": 1,
        "fogado_szamla": 2
    }
    response = client.post('/utalasok/', data=json.dumps(data), headers=headers)
    assert response.status_code in [201, 404, 400, 405, 423]


def test_utalasok_letrehozasa_fail(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 100000,
        "utalo_szamla": 1,
        "fogado_szamla": 2
    }
    response = client.post('/utalasok/', data=json.dumps(data), headers=headers)
    assert response.status_code in [405]


def test_utalasok_letrehozasa(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 100,
        "utalo_szamla": 1,
        "fogado_szamla": 2
    }
    response = client.post('/utalasok/', data=json.dumps(data), headers=headers)
    assert response.status_code in [201, 404, 400, 405, 423]


def test_utalas_lekerdezese_id_alapjan_admin_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}'
    }
    response = client.get('/utalasok/1', headers=headers)
    assert response.status_code in [200, 404]


def test_utalas_lekerdezese_id_alapjan_ugyfel(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}'
    }
    response = client.get('/utalasok/1', headers=headers)
    assert response.status_code in [200, 404]


def test_utalasok_modositasa_fail(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 200
    }
    response = client.put('/utalasok/1', data=json.dumps(data), headers=headers)
    assert response.status_code in [423]


def test_utalasok_modositasa(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}',
        'Content-Type': 'application/json'
    }
    data = {
        "osszeg": 200
    }
    response = client.put('/utalasok/1', data=json.dumps(data), headers=headers)
    assert response.status_code in [200, 404, 400, 405]


def test_utalasok_torlese_fail(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_ugyfel}'
    }
    response = client.delete('/utalasok/1', headers=headers)
    assert response.status_code in [423]


def test_utalasok_torlese(client: FlaskClient, adatbazis_generalas, hozzaferesi_kulcs_admin_ugyfel):
    headers = {
        'Authorization': f'Bearer {hozzaferesi_kulcs_admin_ugyfel}'
    }
    response = client.delete('/utalasok/1', headers=headers)
    assert response.status_code in [204, 404]
