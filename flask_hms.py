from flask import Flask, Response
# from flask_cors import CORS
from flask_restful import Api, Resource
import os

# Import modules
from modules.hms import ncdc_stations
from modules.hms import percent_area

app = Flask(__name__)
# CORS(app)
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
       return {"status": "GIS_QED up and running."}


print('Starting hms flask...')
api.add_resource(StatusTest, '/gis/test/')

# HMS endpoints
# TODO: add endpoint for get after converting post endpoint to celery function
api.add_resource(ncdc_stations.HMSNcdcStations, '/gis/ncdc/stations/')
api.add_resource(percent_area.getPercentArea, '/gis/percentage/')


if __name__ == '__main__':
    app.run(port=7777, debug=True)
