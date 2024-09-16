from flask import send_file
import os

def rhc_index():
    return send_file(os.path.join('websites','RobinHoodCasino','index.html'))

def rhc_sellCoke():
    return send_file(os.path.join('websites','RobinHoodCasino','spil','sell_coke','index.html'))