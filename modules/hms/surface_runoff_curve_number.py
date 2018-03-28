"""
HMS Curve Number Runoff module
Google Earth Engine Script
- all fusion tables have been made public.
"""

# import ee
import json

result_metadata = {}
# ee.Initialize()

# NLCD landcover image
nlcd_landcover = ee.Image('USGS/NLCD/NLCD2011').select("landcover")

# NLCD landcover legend
nlcd_legend = ee.FeatureCollection('ft:1Ji3CTnGa3rRy5Te3mXdFmLusmbKBR6tWeaCXpBW1')

# STATSGO soil details table
statsgo_soil_details = ee.FeatureCollection('ft:18lBl-j1mfqDlgAJe_hUP9XVRUYTXojvUeVZJAS_l')

# STATSGO region boundary outlines
# OBSOLETE with updated get_statsgo_region function
# statsgo_outline = ee.FeatureCollection('ft:1IihDoAf456zaFqKe3HwSs3iWjbhzRCCkEp0bIH7V', 'geometry')


def get_statsgo_region(geometry):
    """
    Gets the statsgo geometries that intersect with the provided geometry.
    :param geometry: Input geometry.
    :return: FeatureCollection containing all intersecting geomteries.
    """
    # region = statsgo_outline.filterBounds(point).first().get('name').getInfo()
    # if (region == "East"):
    #     return ee.FeatureCollection('ft:1oP38-oNfwi63LGT6zmLRIzdYNrKXlehCh72PUrxp', 'geometry').filterBounds(point)
    # elif (region == "MidEast"):
    #     return ee.FeatureCollection('ft:12pF1gr-Emrv2pbu0-0NLpCvCB0ubgFD2oz_OETqx', 'geometry').filterBounds(point)
    # elif (region == "Mid"):
    #     return ee.FeatureCollection('ft:1p16uUd4oPisU-wcJMG5beBaHQUcbQ4i7vOkgAGrH', 'geometry').filterBounds(point)
    # elif (region == "MidWest"):
    #     return ee.FeatureCollection('ft:1FsTaBtg8Xig38Y6Hcp7gbe2KFAT0kD0JRLNSnI7C', 'geometry').filterBounds(point)
    # elif (region == "West"):
    #     return ee.FeatureCollection('ft:1BilByJX_OWOy0X1OqSAOwKfRlUpioVumKbSs8jRM', 'geometry').filterBounds(point)
    # else:
    #     return

    # Checks all statsgo regions if they contain any intersecting geometries with the given geometry.
    # Resolves possible boundary errors.
    statsgo_east = ee.FeatureCollection("ft:1oP38-oNfwi63LGT6zmLRIzdYNrKXlehCh72PUrxp", 'geometry').filterBounds(geometry)
    statsgo_mideast = ee.FeatureCollection("ft:12pF1gr-Emrv2pbu0-0NLpCvCB0ubgFD2oz_OETqx", 'geometry').filterBounds(geometry)
    statsgo_mid = ee.FeatureCollection('ft:1p16uUd4oPisU-wcJMG5beBaHQUcbQ4i7vOkgAGrH', 'geometry').filterBounds(geometry)
    statsgo_midwest = ee.FeatureCollection('ft:1FsTaBtg8Xig38Y6Hcp7gbe2KFAT0kD0JRLNSnI7C', 'geometry').filterBounds(geometry)
    statsgo_west = ee.FeatureCollection('ft:1BilByJX_OWOy0X1OqSAOwKfRlUpioVumKbSs8jRM', 'geometry').filterBounds(geometry)

    # Merges all the FeatureCollections of statsgo geometries into a single FeatureCollection.
    return statsgo_east.merge(statsgo_mideast).merge(statsgo_mid).merge(statsgo_midwest).merge(statsgo_west)


def get_hydrologic_group(musym):
    """
    Gets the Hydrologic Soil Group details.
    :param musym: Map unit symbol.
    :return: Feature containing the HSG details.
    """
    # Filter returns a FeatureCollection of one element, first() gets that single feature element.
    return statsgo_soil_details.filter(ee.Filter.eq("musym", musym)).first()


def get_cn(latitude, longitude):
    """
    Finds the curve number for a given latitude/longitude coordinate.
    TODO: Change functions to accept geometry, define geometry prior to function to allow for HUC and custom defined geometries.
    :param latitude: Requested latitude coordinate.
    :param longitude: Requested longitude coordinate.
    :return: Curve Number value
    """
    def get_region_cn(soil):

        def calculate_region_cn(soil):
            type_keys = ee.Dictionary(type_count.get("landcover"))
            values = ee.Dictionary(type_keys).map(adjusted_cn)
            summed = ee.Number(values.values().reduce(ee.Reducer.sum()))
            cn_nw = summed.divide(ee.Number(count.get("landcover")))
            soil = soil.set({"CN": cn_nw})
            return ee.Feature(soil)
        def adjusted_cn(key, value):
            types = nlcd_legend.filter(ee.Filter.stringContains("lc_id", key))
            cn = types.first().get(hsg)
            a = ee.Dictionary(ee.Dictionary(type_count).get("landcover")).get(key)
            acn = ee.Number(a).multiply(ee.Number(cn))
            return acn
        def water_area(soil):
            soil = soil.set({"CN": 100})
            return ee.Feature(soil)
        type_count = nlcd_region.reduceRegion(reducer=ee.Reducer.frequencyHistogram(), geometry=point, scale=30)
        count = nlcd_region.reduceRegion(reducer=ee.Reducer.count(), geometry=point, scale=30)
        musym = soil.get("MUSYM")
        soil_group = get_hydrologic_group(musym)
        hsg = soil_group.get("hydgrpdcd")
        cn = ee.Algorithms.If(ee.Algorithms.IsEqual(musym, "s8369"), water_area(soil), calculate_region_cn(soil))
        # cn = calculate_region_cn(soil)
        return cn

    point = ee.Geometry.Point(ee.List([float(longitude), float(latitude)])).buffer(500)
    statsgo_region = get_statsgo_region(point)  # soil data
    nlcd_region = nlcd_landcover.clip(point)  # landcover data
    cns = statsgo_region.map(get_region_cn)
    cn_sum = cns.aggregate_sum("CN")
    cn_size = cns.size()
    wcn = ee.Number(cn_sum).divide(cn_size)
    return wcn.getInfo()


def get_runoff(startdate, enddate, latitude, longitude, cn):

    def create_timeseries(ele):
        data = ee.Dictionary(ee.Image(ele).reduceRegion(ee.Reducer.mean(), maxPixels=1000000000))
        runoff = ee.List(ee.Dictionary(data).values()).get(0)
        f = ee.Feature(ele.geometry())
        f = f.set("cn_runoff", runoff)
        f = f.set("date", ele.get('system:index'))
        return f

    def compute_runoff(i):
        min = ee.Number(runoff_a)
        q = i.expression('(float(P) <= float(MIN)*float(S) ? 0 : ((float(P) - float(MIN)*float(S)) ** 2) / (float(P) + (1-float(MIN)) * float(S)))',
                         {
                             'S': S,
                             'MIN': min,
                             'P': ee.Image(i).select('prcp')
                         })
        return ee.Image(q)

    def clip_to_geometry(i):
        return ee.Image(i).clip(ee.Geometry(point))

    point = ee.Geometry.Point(ee.List([float(longitude), float(latitude)])).buffer(500)
    S = ee.Number(25.4 * ((1000/float(cn)) - 10))
    result_metadata["S_value"] = S
    rain = ee.ImageCollection('NASA/ORNL/DAYMET_V3').select('prcp').map(clip_to_geometry)\
        .filterDate(ee.Date(startdate), ee.Date(enddate))
    ts = []
    runoff_a = 0.1
    result_metadata["runoff_coefficient"] = runoff_a
    Q = rain.map(compute_runoff)
    fCollection = Q.map(create_timeseries).getInfo()['features']

    for f in fCollection:
        date = f['properties']['date']
        data = f['properties']['cn_runoff']
        ts.append([date, data])

    return ts


def get_cn_runoff(startdate, enddate, latitude, longitude):
    result_metadata = {'startdate': startdate, 'enddate': enddate, 'latitude': latitude, 'longitude': longitude}
    weighted_cn = get_cn(latitude, longitude)
    result_runoff = get_runoff(startdate, enddate, latitude, longitude, weighted_cn)
    result = '{"source": "Weighted Curve Number", "dataset": "Surface Runoff", "metadata": ' + \
             json.dumps(result_metadata) + ', "data": ' + json.dumps(result_runoff) + '}'
    return result