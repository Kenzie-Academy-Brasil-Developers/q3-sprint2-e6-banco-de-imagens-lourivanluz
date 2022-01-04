from flask import Flask,request
from kenzie import upload
import os

app = Flask(__name__)


app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH'))

base_dir = os.getenv('FILES_DIRECTORY')
extension_list = os.getenv('ALLOWED_EXTENSIONS').split(',')

try:
    os.mkdir(f'{base_dir}')
except:
    ...

for extension in extension_list:
    try:
       os.mkdir(f'{base_dir}/{extension}')
    except:
        pass


@app.post('/upload')
def file_upload():
    file = request.files['file']
    (mensagem,status) = upload(file)
    return {'mensagem': mensagem},status