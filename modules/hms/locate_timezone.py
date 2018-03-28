"""
HMS Locate Timezone from lat/lon coordinates
Google Earth Engine Script
"""

# import ee
import json
# ee.Initialize()


def get_timezone(latitude, longitude):
    tzInfo = ee.FeatureCollection('ft:12EZLvV1mM8iGQiF41Z6isKip8ObYsn4IgT6c1ApJ')
    timeZones = ee.FeatureCollection('ft:1W4iGwwnWg0sW1POUnSVfbT_yj8aDvKa8rOb9XgL5')
    coordinate = ee.Geometry.Point(ee.List([float(longitude), float(latitude)]))
    tzName = timeZones.filterBounds(coordinate).first().get('TZID').getInfo()
    tzOffset = tzInfo.filter(ee.Filter.eq('Name', tzName)).first().get('offset').getInfo()
    timezone_details = {"latitude": float(latitude), "longitude": float(longitude), "tzName": str(tzName), "tzOffset": str(tzOffset)}
    return json.dumps(timezone_details)
