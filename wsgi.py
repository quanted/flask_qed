import bottle, os, sys

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

# Add Django project & parent directory to Python PATH
sys.path.insert(0, '/var/www/ubertool/ubertool_ecorest/REST_UBER')
sys.path.insert(0, '/var/www/ubertool/ubertool_ecorest')
# sys.path.insert(0, '/var/www/ubertool')

# ... build or import your bottle application here ...
# import REST_UBER.bottle_ec2
import REST_UBER.bottle_cgi

# Do NOT use bottle.run() with mod_wsgi/uwsgi

application = bottle.default_app()
