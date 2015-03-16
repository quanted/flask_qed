import os, sys, sqlite3

file_path = os.path.abspath(os.path.dirname(__file__))
db = os.path.join(file_path, 'sqliteDB', 'mergedDB.s3db')
# Connecting to the database file
conn = sqlite3.connect(db)
# conn.row_factory = sqlite3.Row
c = conn.cursor()


def loadChoices(query):
	
	choices = []

	if query == 'crop':
		choices = cropQuery()
	elif query == 'oreDb':
		choices = oreDbQuery()
	# print choices

	# choices = c.fetchone()
	# print choices.keys()

	# print choices['Crop']
	return choices

def cropQuery():
	c.execute('SELECT DISTINCT Crop FROM merged')

	return c.fetchall()

# , GrpName, SubGrpNo, SubGrpName
def oreDbQuery():
	c.execute('SELECT DISTINCT Crop, GrpNo, GrpName, SubGrpNo, SubGrpName, Category FROM merged')

	return c.fetchall()



def oreWorkerActivities(category):
	"""
	Get 
	"""

	crop_category = (category,)  # Must be a tuple

	cursor = c.execute('SELECT DISTINCT Activity, AppType, AppEquip, Formulation FROM merged WHERE Category=?', crop_category)
	
	query = c.fetchall()
	

	formulation = []
	appequip = []
	apptype = []
	activity = []

	print query

	
	for result in query:

		print result

		if result[0] not in activity:
			activity.append(result[0])
		if result[1] not in apptype:
			apptype.append(result[1])
		if result[2] not in appequip:
			appequip.append(result[2])
		if result[3] not in formulation:
			formulation.append(result[3])

	print activity
	print apptype
	print appequip
	print formulation

	return activity, apptype, appequip, formulation