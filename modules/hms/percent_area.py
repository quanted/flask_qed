from flask import Response, Flask, request, jsonify
from flask_restful import Resource, reqparse, abort
from werkzeug.datastructures import FileStorage
from osgeo import ogr, osr
import urllib.request
from zipfile import *
import shapefile
import datetime
import requests
import shutil
import json
import time
import io
import re

parser = reqparse.RequestParser()
parser.add_argument('huc_8_num')
parser.add_argument('huc_12_num')
parser.add_argument('com_id_num')
parser.add_argument('lat_long_x')
parser.add_argument('lat_long_y')
parser.add_argument('filename', location='files', type=FileStorage)

class getPercentArea(Resource):
	'''
	User sends Catchment ID (CommID) and HUC8 number to get % area of each NLDAS/GLDAS cell covered by the catchment
	Sample usage: 
	1) http://127.0.0.1:5000/gis/rest/hms/percentage/?huc_12_num=020100050107
	2) http://127.0.0.1:5000/gis/rest/hms/percentage/?huc_8_num=01060002
	3) http://127.0.0.1:5000/gis/rest/hms/percentage/?huc_8_num=01060002&com_id_num=9311911
	6/7) http://127.0.0.1:5000/gis/rest/hms/percentage/?lat_long_x=-83.5&lat_long_y=33.5
	'''
	def get(self):
		args = parser.parse_args()
		huc_8_num = args.huc_8_num
		huc_12_num = args.huc_12_num
		com_id_num = args.com_id_num
		latlongx = args.lat_long_x
		latlongy = args.lat_long_y
		if(huc_8_num):
			tab = process_huc_8(huc_8_num, com_id_num)
		elif(huc_12_num):
			tab = process_huc_12(huc_12_num[0:8])	#Huc12s are catalogued on ftp server by huc8 numbers
		elif(latlongx and latlongy):
			coord = '(' + latlongx + '+' + latlongy + ')'
			tab = process_lat_long(coord)
		return jsonify(tab)

	'''
	User uploads geojson of a catchment or NHDPlus
	Sample usage:
	4/5) curl -X POST -F 'filename=@file.geojson' http://127.0.0.1:5000/gis/rest/hms/percentage/
	'''
	def post(self):
		args = parser.parse_args()
		if(args.filename is not None):		#Using curl
			tab = process_geojson(args.filename.read())
		else:
			return Response("{'posting error': 'POST operation failed'}")
		return jsonify(tab)

class GeometryTable():
	def __init__(self):
    		self.geometry = {}   # Dictionary of catchments, where the key is the catchment ID
    		self.metadata = {}	 # and the value is a Catchment

class Catchment():
	def __init__(self):
    		self.points = []     # An array of CatchmentPoint objects


class CatchmentPoint():
	def __init__(self, cellArea, containedArea,	latitude, longitude, percentArea):
		self.cellArea = cellArea
		self.containedArea = containedArea
		self.latitude = latitude
		self.longitude = longitude
		self.percentArea = percentArea

def process_huc_8(huc_8_num, com_id_num):
	url = 'ftp://newftp.epa.gov/exposure/BasinsData/NHDPlus21/NHDPlus' + str(huc_8_num) + '.zip'
	req = urllib.request.urlopen(url)
	shzip = ZipFile(io.BytesIO(req.read()))
	mshp = shzip.open('NHDPlus' + str(huc_8_num) + '/Drainage/Catchment.shp')
	mdbf = shzip.open('NHDPlus' + str(huc_8_num) + '/Drainage/Catchment.dbf')
	sfile = shp_to_geojson(mshp, mdbf)
	result_table = readGeometry(sfile, url, com_id_num)
	return result_table

def process_huc_12(huc_12_num):
	url = 'ftp://newftp.epa.gov/exposure/NHDV1/HUC12_Boundries/' + str(huc_12_num) + '.zip'
	req = urllib.request.urlopen(url)
	shzip = ZipFile(io.BytesIO(req.read()))
	mshp = shzip.open(str(huc_12_num) + '/huc12.shp')
	mdbf = shzip.open(str(huc_12_num) + '/huc12.dbf')
	sfile = shp_to_geojson(mshp, mdbf)
	result_table = readGeometry(sfile, url, None)
	return result_table

def process_lat_long(coordinate):
	url = 'https://ofmpub.epa.gov/waters10/SpatialAssignment.Service?pGeometry=POINT' + coordinate + '&pLayer=NHDPLUS_CATCHMENT&pSpatialSnap=TRUE&pReturnGeometry=TRUE'
	req = urllib.request.urlopen(url)
	sfile = req.read()
	com = re.search(r'("[0-9]{2,}")', str(sfile))
	geojson = re.search(r'(?={"type").*(]})', str(sfile))
	result_table = readGeometry(geojson.group(0), url, com.group(0).replace('"', ''))
	return result_table

def process_geojson(file):
	result_table = readGeometry(file, None, None)
	return result_table

def shp_to_geojson(mshp, mdbf):
	# read the shapefile
	reader = shapefile.Reader(shp=mshp, dbf=mdbf)
	fields = reader.fields[1:]
	field_names = [field[0] for field in fields]
	buffer = []
	for sr in reader.shapeRecords():
		atr = dict(zip(field_names, sr.record))
		geom = sr.shape.__geo_interface__
		buffer.append(dict(type="Feature", geometry=geom, properties=atr))
	# write the GeoJSON file
	geojson = json.dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n"
	return geojson

def readGeometry(sfile, url, com):
	metadataList = []
	metadataList.append(time.time())
	shapeFiles = []
	nldasFiles = []
	colNames = []
	nldasurl = 'https://ldas.gsfc.nasa.gov/nldas/gis/NLDAS_Grid_Reference.zip'
	metadataList.append(url)
	metadataList.append(nldasurl)
	resp = urllib.request.urlopen(nldasurl)
	gridzip = ZipFile(io.BytesIO(resp.read()))
	gshp = gridzip.open('NLDAS_Grid_Reference.shp')
	gdbf = gridzip.open('NLDAS_Grid_Reference.dbf')
	gfile = shp_to_geojson(gshp, gdbf)
	#print("FINISHED CONVERTING: ", time.time() - metadataList[0])
	shape = ogr.Open(sfile)
	nldas = ogr.Open(gfile)
	shapeLayer = shape.GetLayer()
	nldasLayer = nldas.GetLayer()
	# Getting data for reprojection
	shapeProj = shapeLayer.GetSpatialRef()
	nldasProj = nldasLayer.GetSpatialRef()
	coordTrans = osr.CoordinateTransformation(shapeProj, nldasProj)
	# Getting features from shapefile
	colLayer = shape.GetLayer(0).GetLayerDefn()
	for i in range(colLayer.GetFieldCount()):
		colNames.append(colLayer.GetFieldDefn(i).GetName())
	coms, huc8s, huc12s = [], [], []
	overlap, polygons = [], []
	if ('COMID' in colNames):
		huc12s = [None] * len(shapeLayer)  # No huc 12s
		for feature in shapeLayer:
			if (com):
				if (feature.GetField('COMID') == int(com)):  # Only focusing on the given catchment argument
					polygons.append(feature)
					coms.append(feature.GetField('COMID'))
					huc8s.append(feature.GetField('HUC8'))
			# break #Since only one catchment is needed
			else:
				polygons.append(feature)
				coms.append(feature.GetField('COMID'))
				huc8s.append(feature.GetField('HUC8'))
	elif ('HUC_8' in colNames):
		coms = [None] * len(shapeLayer)  # No catchments
		for feature in shapeLayer:
			polygons.append(feature)
			huc8s.append(feature.GetField('HUC_8'))
			huc12s.append(feature.GetField('HUC_12'))
	else:
		coms = [None] * len(shapeLayer)
		if(com):
			coms[0] = com
		huc8s = [None] * len(shapeLayer)
		huc12s = [None] * len(shapeLayer)
		for feature in shapeLayer:
			polygons.append(feature)
	# Reproject geometries from shapefile
	totalPoly = ogr.Geometry(ogr.wkbMultiPolygon)
	# Treat all polygons as one larger one since we are just finding overlapping cells
	for polygon in polygons:
		poly = polygon.GetGeometryRef()
		poly.Transform(coordTrans)
		totalPoly.AddGeometry(poly)
	totalPoly = totalPoly.UnionCascaded()
	if (totalPoly == None):
		totalPoly = polygons[0].GetGeometryRef()  # latLong
	# Calculate cells that contain polygons ahead of time to make intersections faster
	# This block of code should be parallelized if possible
	for feature in nldasLayer:
		cell = feature.GetGeometryRef()
		if (totalPoly.Intersects(cell) and feature not in overlap):
			overlap.append(feature)
	return calculations(overlap, polygons, coms, huc8s, huc12s, metadataList)

def calculations(overlap, polygons, coms, huc8s, huc12s, metadataList):
	# Iterate through smaller list of overlapping cells to calculate data
	#table.geometry = {"HUC 8 ID": huc8s[0]}
	#huc8table = [{"HUC 8 ID": huc8s[0]}]
	table = GeometryTable()
	i = 0;
	num_points = 0
	for polygon in polygons:
		poly = polygon.GetGeometryRef()
		huc12table = Catchment()
		#huc12table.points.append({"HUC 12 ID": huc12s[i]})
		#huc12table.points.append({"Catchment ID": coms[i]})
		for feature in overlap:
			cell = feature.GetGeometryRef()
			interArea = 0
			squareArea = cell.Area()
			if (poly.Intersects(cell)):
				inter = poly.Intersection(cell)
				interArea += inter.Area()
				percentArea = (interArea / squareArea) * 100
				catchtable = CatchmentPoint(squareArea, interArea, cell.Centroid().GetY(), cell.Centroid().GetX(), percentArea)
				huc12table.points.append(catchtable.__dict__)
				num_points += 1
		table.geometry[coms[i]] = huc12table.__dict__
		#huc8table.append(huc12table)
		i += 1
	#table.geometry.append(huc8table)
	table.metadata['request date'] = datetime.datetime.now()
	table.metadata['number of points'] = num_points
	table.metadata['shapefile source'] = metadataList[2]
	table.metadata['nldas source'] = metadataList[1]
	table.metadata['execution time'] = time.time() - metadataList[0]
	# De-reference shapefiles
	shape = None
	nldas = None
	return table.__dict__