from app import app
from .test_route_upload import reset_dir,base_dir
import os

def app_client():
    return app.test_client()

def test_status_code_route_download_with_valid_name():
    reset_dir()
    os.system(f'cp ./test/img_test/kenzie.png {base_dir}/png')

    client = app_client()
    response = client.get('/download/kenzie.png')
    assert response.status_code == 200

def test_response_route_download_with_valid_name():
    reset_dir()
    os.system(f'cp ./test/img_test/kenzie.png {base_dir}/png')
    with open('./test/img_test/kenzie.png','rb') as file:
        img_test = file.read()
    client = app_client()
    response = client.get('/download/kenzie.png')
    assert response.data == img_test

def test_status_code_route_download_with_no_valid_name():
    reset_dir()
    client = app_client()
    response = client.get('/download/kenzie.png')
    assert response.status_code == 404
