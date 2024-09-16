from flask import send_file, request
import os

def oeb_index():
    return send_file(os.path.join('templates','OB_Boedekasse','public','index.html'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls'}

def upload_trans():
    if 'fileUpload' not in request.files:
        return 'No file part'
    file = request.files['fileUpload']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join('templates','OB_Boedekasse','database', "trans.xlsx"))
        return 'File uploaded successfully!'
    else:
        return 'Invalid file type'