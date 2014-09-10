import bottle, os, sys

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

# Add Django project & parent directory to Python PATH
sys.path.insert(0, '/var/www/ubertool/ubertool_ecorest')
sys.path.insert(0, '/var/www/ubertool')

# ... build or import your bottle application here ...
import REST_EC2.bottle_ec2
# Do NOT use bottle.run() with mod_wsgi

application = bottle.default_app()