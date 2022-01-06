from flask import Flask,request,send_from_directory
from kenzie import *
import os

app = Flask(__name__)


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

@app.post('/upload')
def file_upload():
    file = request.files['file']
    (mensagem,status) = upload(file)
    return {'mensagem': mensagem},status

@app.get('/files')
def file_listed():
    return {'files': get_name_files()},200

@app.get('/files/<extension>')
def files_filtred(extension):
    return {'files': get_files_filtred(extension)},200

@app.get('/download-zip')
def download_zip():
    try:
        extension = request.args.get('file_extension')
        radios = int(request.args.get('compression_ratio'))
        
        file = create_zip_by_extension(extension,radios)
        return send_from_directory(
            directory= f'../files_upload/{extension}/',
            path= file,
            as_attachment=True
        )
    except:
        if radios<=1 and radios >=9:
            return {'mensagem': 'compression_ratio deve ser um inteiro entre 1 e 9'},401
        if extension not in extension_list:
            return {'mensagem': 'aplicasão não suporta essa extensão'},401
        return {'mensagem': 'file_extension e compression_ratio necessarios'},401