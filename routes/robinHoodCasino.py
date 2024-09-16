from flask import send_file
import os
from websites.RobinHoodCasino.spil.find_the_thai.main import *


def rhc_index():
    return send_file(os.path.join('websites','RobinHoodCasino','index.html'))

def rhc_sellCoke():
    return send_file(os.path.join('websites','RobinHoodCasino','spil','sell_coke','index.html'))

def rhc_sell_coke_javascript():
    return send_file(os.path.join('websites','RobinHoodCasino','spil','sell_coke','script.js'))

def rhc_sell_coke_style():
    return send_file(os.path.join('websites','RobinHoodCasino','spil','sell_coke','styles.css'))

def rhc_ftt_index():
    return find_the_thai(os.path.join('websites','RobinHoodCasino','spil','find_the_thai'))

