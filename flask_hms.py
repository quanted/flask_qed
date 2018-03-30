from flask import Flask
from flask_restful import Api, Resource
import os
import logging

# Import modules
from modules.hms import ncdc_stations
from modules.hms import percent_area

app = Flask(__name__)
app.config.update(
    DEBUG=True
)

api = Api(app)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.update({
    'PROJECT_ROOT': PROJECT_ROOT
})


class StatusTest(Resource):
    def get(self):
        return {"status": "flask_hms up and running."}


base_url = "https://localhost:7777/hms"
logging.debug("flask_hms started: live endpoints")
logging.debug(base_url + "/gis")
api.add_resource(StatusTest, '/gis/test/')

# HMS endpoints
# TODO: add endpoint for get after converting post endpoint to celery function
logging.debug(base_url + "/gis/ncdc/stations/")
api.add_resource(ncdc_stations.HMSNcdcStations, '/gis/ncdc/stations/')
logging.debug(base_url + "/gis/percentage/")
api.add_resource(percent_area.getPercentArea, '/gis/percentage/')


if __name__ == '__main__':
    app.run(port=7777, debug=True)
