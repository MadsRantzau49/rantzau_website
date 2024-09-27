from flask import send_file
import os

def music_indexx():
    return send_file(os.path.join('templates', 'music','index.html'))
