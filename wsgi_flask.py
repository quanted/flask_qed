import os
import sys


# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

# Add Flask app & parent directory to Python PATH
sys.path.insert(0, '/var/www/ubertool/ubertool_ecorest/REST_UBER')
sys.path.insert(0, '/var/www/ubertool/ubertool_ecorest')
# sys.path.insert(0, '/var/www/ubertool')

# ... build or import your bottle application here ...
import flask_cgi

application = flask_cgi.app
