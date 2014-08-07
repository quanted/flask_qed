import bottle, os, sys

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

# ... build or import your bottle application here ...
import REST_EC2.bottle_ec2
# Do NOT use bottle.run() with mod_wsgi

application = bottle.default_app()