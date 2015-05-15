import os, sys, sqlite3

file_path = os.path.abspath(os.path.dirname(__file__))
db = os.path.join(file_path, 'sqliteDB', 'ore.s3db')
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
    c.execute('SELECT DISTINCT Crop FROM CCA')

    return c.fetchall()

# , GrpName, SubGrpNo, SubGrpName
def oreDbQuery():
    c.execute('SELECT DISTINCT Crop, GrpNo, GrpName, SubGrpNo, SubGrpName, Category FROM CCA')

    return c.fetchall()

def generateSQLFilter(filter):
    # e.g. "Category=? AND AppEquip IN (?, ?, ?, ?)"
    query_string = "Category=? AND "

    i = 0
    while i < len(filter):
        print filter[i]
        if i > 0:
            query_string += ", ?"
        else:  # i == 0 (first loop pass)
            query_string += "AppEquip IN (?"

        i += 1

    query_string += ")"

    return query_string


def oreWorkerActivities(category, filter=None):
    """
    Get
    """

    if filter:
        print 'Filter exists!'

        generateSQLFilter(filter)
        print generateSQLFilter(filter)

        crop_category = (category, filter)
        c.execute( 'SELECT DISTINCT Activity, AppType, AppEquip, Formulation '
                   'FROM CCA WHERE Category=? AND AppEquip=?',
                   crop_category )
    else:
        crop_category = (category, )  # Must be a tuple
        c.execute( 'SELECT DISTINCT Activity, AppType, AppEquip, Formulation '
                   'FROM CCA WHERE Category=?',
                   crop_category )

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