from flask import send_file, Response, send_from_directory
import os
from templates.RobinHoodCasino.spil.find_the_thai.main import *

def rhc_index():
    return send_file(os.path.join('templates','RobinHoodCasino','index.html'))

def rhc_sellCoke():
    return send_file(os.path.join('templates','RobinHoodCasino','spil','sell_coke','index.html'))

def rhc_sell_coke_javascript():
    return send_file(os.path.join('templates','RobinHoodCasino','spil','sell_coke','script.js'))

def rhc_sell_coke_style():
    return send_file(os.path.join('templates','RobinHoodCasino','spil','sell_coke','styles.css'))

def rhc_ftt_index():
    return find_the_thai(os.path.join('templates','RobinHoodCasino','spil','find_the_thai'))

def rhc_ftt_serve_image(image_path):
    folder_path = os.path.join('templates','RobinHoodCasino','spil','find_the_thai','static')
    return send_from_directory(folder_path, image_path)

# Crash and bumle
def rhc_crash_and_index():
    return send_file(os.path.join('templates','RobinHoodCasino','spil','crash_and_bumle','index.html'))

def rhc_bumle():
    return send_file(os.path.join('templates','RobinHoodCasino','spil','crash_and_bumle','racerspil.html'))

def rhc_crash_and_bumle_style():
    return send_file(os.path.join('templates','RobinHoodCasino','spil','crash_and_bumle','style.css'))

def rhc_crash_and_bumle_serve_image(filename):
    print(filename,"FILENAME:")
    folder_path = os.path.join('templates','RobinHoodCasino','spil','crash_and_bumle','photo')
    return send_from_directory(folder_path, filename)

