# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

import bottle
import REST_EC2.bottle_ec2
# ... build or import your bottle application here ...
# Do NOT use bottle.run() with mod_wsgi

# application = bottle.default_app()
application = REST_EC2.bottle_ec2.application