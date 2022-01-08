from app import *

def app_client():
    return app.test_client()

def test_home_return_status_code():
    client = app_client()
    responde = client.get('/')
    assert responde.status_code == 200,'status incorreto'
