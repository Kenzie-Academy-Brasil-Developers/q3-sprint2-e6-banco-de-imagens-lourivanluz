from app import app
from .test_route_upload import reset_dir,base_dir
import os

def app_client():
    return app.test_client()

def test_status_code_download_zip_with_directory_no_corret_name():
    reset_dir()
    client = app_client()
    response = client.get('/download-zip?file_ex')
    assert response.status_code == 404    

def test_status_code_download_zip_with_directory_corret_name():
    reset_dir()
    os.system(f'cp ./test/img_test/kenzie.png {base_dir}/png')
    client = app_client()
    response = client.get('/download-zip?file_extension=png&compression_ratio=9')
    assert response.status_code == 200

def test_response_download_zip_with_directory_corret_name():
    reset_dir()
    os.system(f'cp ./test/img_test/kenzie.png {base_dir}/png')
    client = app_client()
    os.system(f'cd /tmp/files_upload/png/ ; zip -9 png.zip *.png')
    with open('/tmp/files_upload/png/png.zip','rb') as file:
        zip_file = file.read()
    
    response = client.get('/download-zip?file_extension=png&compression_ratio=9')
    assert response.data == zip_file