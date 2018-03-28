from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

import flask_pram as pram
import flask_hms as hms


app = DispatcherMiddleware(pram.app, {
    '/hms': hms.app,
})

if __name__ == "__main__":
    run_simple('localhost', 7777, app, use_reloader=True, use_debugger=True, use_evalex=True)
