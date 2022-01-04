import os


base_dir = os.getenv('FILES_DIRECTORY')

def save_file(file,extencion):
    extension_dir = f'{base_dir}/{extencion}'
    file_name = file.filename
    list_files = []
    for _,_,files in os.walk(extension_dir):
        list_files.append(files)

    if file_name in list_files[0]:
        return ('Imagem com um nome ja existente no sistema,',409)
    else:
        file.save(f'{extension_dir}/{file_name}')
        return ('Imagen salva',201)
        
def upload(file):
    max_size = int(os.getenv('MAX_CONTENT_LENGTH'))
    extension_list = os.getenv('ALLOWED_EXTENSIONS').split(',')
    extension = file.filename.split('.')[-1]
    
    if extension in extension_list:
        size = len(file.read())
        if size<=max_size:
            mensagem = save_file(file,extension)
            return mensagem

        return (f'Arquivo maior que {max_size/1000000} MB', 413)
        
    return (f'Extensão .{extension} não é suportada', 415)
