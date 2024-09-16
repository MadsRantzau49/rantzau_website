from flask import Flask
from routes.index import *
from routes.robinHoodCasino import *
from routes.boedekasse import *


app = Flask(__name__)
PORT = 10000

# Add routes
app.add_url_rule('/', 'index', index)
app.add_url_rule('/RobinHoodCasino', 'rhc_index', rhc_index)
app.add_url_rule('/SellCoke', 'rhc_sellCoke', rhc_sellCoke)
app.add_url_rule('/OEB', 'oeb_index', oeb_index)
app.add_url_rule('/OEB_upload_trans', 'upload_trans', upload_trans , methods=['POST'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
