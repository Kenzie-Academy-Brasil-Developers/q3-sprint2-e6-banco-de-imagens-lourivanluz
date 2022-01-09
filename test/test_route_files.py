from werkzeug.wrappers import response
from app import app
import os

def app_client():
    return app.test_client()

def test_status_code_route_files():
    client = app_client()
    response = client.get('/files')
    assert response.status_code == 200

def test_response_route_all_files():
    list_files = []
    dirs = ['gif', 'jpg', 'png']
    for dir in dirs:
        files = os.listdir(f'/tmp/files_upload/{dir}')
        for file in files:
            list_files.append(file)
    client = app_client()
    response = client.get('/files')
    assert response.json == {'files': list_files}

def test_response_route_files_png():
    list_files = []
    dirs = ['png']
    for dir in dirs:
        files = os.listdir(f'/tmp/files_upload/{dir}')
        for file in files:
            list_files.append(file)
    client = app_client()
    response = client.get('/files/png')
    assert response.json == {'files': list_files}

def test_status_code_route_files_png():
    client = app_client()
    response = client.get('/files/png')
    assert response.status_code == 200

def test_status_code_route_file_with_extension():
    client = app_client()
    response = client.get('/files/bin')
    assert response.status_code == 404