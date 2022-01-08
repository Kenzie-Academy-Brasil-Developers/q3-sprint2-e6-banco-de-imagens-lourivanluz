import os
from werkzeug.datastructures import FileStorage
from app import app

def app_client():
    return app.test_client()

def creat_mock_img(file_name):
    img = os.path.join(f'./test/img_test/{file_name}')
    extension = file_name.split('.')[1]
    mocked_img =  FileStorage(
        stream = open(img,'rb'),
        filename= file_name,
        content_type=f'image/{extension}'
    )
    return mocked_img

def test_status_code_large_image():
    client = app_client()
    data = creat_mock_img('kenzie-large.png')
    response = client.post('/upload',data={'file':data},content_type ='multipart/form-data')
    assert response.status_code == 413,'o status code não esta correto'

def test_status_code_no_extesion_support():
    client = app_client()
    data = creat_mock_img('kenzie.bin')
    response = client.post('/upload',data={'file':data},content_type ='multipart/form-data')
    assert response.status_code == 415,'o status code não esta correto'


def test_status_code_png_less_1kb():
    client = app_client()
    data = creat_mock_img('kenzie.png')
    response = client.post('/upload',data={'file':data},content_type='multipart/form-data')
    assert response.status_code == 201

def test_same_file_in_dir():
    client = app_client()
    data = creat_mock_img('kenzie.png')
    response = client.post('/upload',data={'file':data},content_type='multipart/form-data')
    if 'kenzie.png' in os.listdir('/tmp/files_upload/png'):
        assert response.status_code == 409
  