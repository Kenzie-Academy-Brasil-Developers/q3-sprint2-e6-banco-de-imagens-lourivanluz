import os

def get_name_files():
    base_dir = os.getenv('FILES_DIRECTORY')
    extension_list = list(os.getenv('ALLOWED_EXTENSIONS').split(','))
    list_files = []
    for extension in extension_list:
        extension_dir = f'{base_dir}/{extension}' 
        for _,_,files in os.walk(extension_dir):
            list_files.append(files)
    return sum(list_files,[])

def get_files_filtred(extension_filter):
    files = get_name_files()
    files_filtred = [file for file in files if extension_filter in file]
    return files_filtred

def save_file(file,extension):
    base_dir = os.getenv('FILES_DIRECTORY')
    extension_dir = f'{base_dir}/{extension}'
    file_name = file.filename
    list_files = get_name_files()

    if file_name in list_files:
        return ('Imagem com um nome ja existente no sistema,',409)
    else:
        file.save(f'{extension_dir}/{file.filename}')
        return ('Imagen salva',201)
        
def upload(file):
    max_size = int(os.getenv('MAX_CONTENT_LENGTH'))
    extension_list = os.getenv('ALLOWED_EXTENSIONS').split(',')
    extension = file.filename.split('.')[-1]
    
    if extension in extension_list:
        file_length = len(file.read())
        file.seek(0)
        if file_length<=max_size:
            mensagem = save_file(file,extension)
            return mensagem

        return (f'Arquivo maior que {max_size/1000000} MB', 413)
        
    return (f'Extensão .{extension} não é suportada', 415)


def create_zip_by_extension(extension,radios):
    base_dir = os.getenv('FILES_DIRECTORY')
    extension_dir = f'{base_dir}/{extension}'
    files = ''.join(os.listdir(f'{base_dir}/{extension}'))
    if files:
        os.system(f'cd {extension_dir} ; zip -{radios} {extension}.zip *.png')
        return f'{extension}.zip'
    return ''