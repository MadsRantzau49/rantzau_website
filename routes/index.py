from flask import send_file
import os

def index():
    return send_file(os.path.join('public', 'index.html'))
