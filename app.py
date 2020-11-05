from flask import Flask

app = Flask(__name__)

from bills import app as bills_blueprint
from senders import app as senders_blueprint
from receivers import app as receivers_blueprint

app.register_blueprint(bills_blueprint)
app.register_blueprint(senders_blueprint)
app.register_blueprint(receivers_blueprint)
