from dotenv.main import load_dotenv
from flask import Flask,request,send_from_directory
from kenzie import upload,get_files_filtred,get_name_files,create_zip_by_extension

import os

app = Flask(__name__)

load_dotenv()

app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH'))

base_dir = os.getenv('FILES_DIRECTORY')
extension_list = os.getenv('ALLOWED_EXTENSIONS').split(',')

try:
    os.mkdir(f'{base_dir}')
    for extension in extension_list:
        try:
            os.mkdir(f'{base_dir}/{extension}')
        except:
            pass
except:
    pass


@app.get('/')
def home():
    return{'mensagem':'ta na home'},200

@app.post('/upload')
def file_upload():
    file = request.files['file']
    # "file": "<class 'werkzeug.datastructures.FileStorage'>"
    (mensagem,status) = upload(file)
    return {'mensagem': mensagem},status

@app.get('/files')
def file_listed():
    return {'files': get_name_files()},200

@app.get('/files/<extension>')
def files_filtred(extension):
    if extension in extension_list:
        list_files = get_files_filtred(extension)
        return {'files': list_files},200
    return {'mensagem':'Extensão invalida'},404

@app.get('/download/<file_name>')
def download_file(file_name):
    extension = file_name.split('.')[1]
    try:
        return send_from_directory(
            directory= f'{base_dir}/{extension}/',
            path= file_name,
            as_attachment=True
        )
    except:
        return  {'mensagem':'Nome de arquivo inválido'},404

@app.get('/download-zip')
def download_zip():
    try:
        extension = request.args.get('file_extension')
        radios = int(request.args.get('compression_ratio'))
        
        response = create_zip_by_extension(extension,radios)
        if response:
            file_download = send_from_directory(
                directory= f'{base_dir}/{extension}/',
                path= response,
                as_attachment=True
            )
            os.system(f'rm /tmp/files_upload/{extension}/{extension}.zip')
            return file_download
        return {'mensagem':'pasta vazia'},404
    except:
        mensagem = 'file_extension e compression_ratio necessarios'
        if extension not in extension_list:
            mensagem ='aplicasão não suporta essa extensão'
        return {'mensagem': mensagem},404
