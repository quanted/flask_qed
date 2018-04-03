from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
import logging

import pram_flask.flask_pram as pram
import hms_flask.flask_hms as hms

logging.debug("flask_cgi started: live flask apps")
app = DispatcherMiddleware(pram.app, {
    '/hms': hms.app,
})
logging.debug("flask_pram")
logging.debug("flask_hms")

if __name__ == "__main__":
    run_simple('localhost', 7777, app, use_reloader=True, use_debugger=True, use_evalex=True)
