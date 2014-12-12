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