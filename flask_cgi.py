from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import logging
import os

import pram_flask.flask_pram as pram
import hms_flask.flask_hms as hms


from temp_config.set_environment import DeployEnv
runtime_env = DeployEnv()
runtime_env.load_deployment_environment()

if not os.environ.get('OPENCPU_REST_SERVER'):
    os.environ.update({'OPENCPU_REST_SERVER': 'http://172.20.100.18:5656'})
    
# logging.info("OPENCPU_REST_SERVER: {}".format(OPENCPU_REST_SERVER))

logging.info("flask_cgi started: live flask apps")
app = DispatcherMiddleware(pram.app, {
    '/hms': hms.app,
})

if __name__ == "__main__":
    run_simple('localhost', 7777, app, use_reloader=True, use_debugger=True, use_evalex=True)
