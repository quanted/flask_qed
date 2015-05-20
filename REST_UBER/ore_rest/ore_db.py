import logging
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

def generateSQLFilter(filter, es_type, category):
    # e.g. "Category=? AND AppEquip IN (?, ?, ?, ?)"
    query_string = "Category=?"
    insertion_list = [category]

    i = 0
    while i < len(filter):
        print filter[i]
        # if i > 0:
        #     query_string += ", ?"
        # else:  # i == 0 (first loop pass)
        #     query_string += es_type + " IS NOT (?"
        insertion_list.append(filter[i])
        query_string += " AND " + es_type + " IS NOT ?"
        i += 1

    # query_string += ")"

    return query_string, insertion_list


def oreWorkerActivities(query):
    """
    Get
    """
    print query
    category = query['crop_category']

    try:
        filter = query['es_type_filter']
        es_type = query['es_type']
        print 'Filter exists!'

        query_string = generateSQLFilter(filter, es_type, category)
        print query_string

        crop_category = tuple(query_string[1])
        c.execute( 'SELECT DISTINCT Activity, AppType, AppEquip, Formulation '
                   'FROM CCA WHERE ' + query_string[0],
                   crop_category )

    except KeyError, e:
        logging.exception(e)
        crop_category = (category, )  # Must be a tuple
        c.execute( 'SELECT DISTINCT Activity, AppType, AppEquip, Formulation '
                   'FROM CCA WHERE Category=?',
                   crop_category )

    query = c.fetchall()

    formulation = []
    appequip = []
    apptype = []
    activity = []

    # print query

    for result in query:

        if result[0] not in activity:
            activity.append(result[0])
        if result[1] not in apptype:
            apptype.append(result[1])
        if result[2] not in appequip:
            appequip.append(result[2])
        if result[3] not in formulation:
            formulation.append(result[3])

    # print activity
    # print apptype
    # print appequip
    # print formulation

    return { 'Activity': activity,
             'AppType': apptype,
             'AppEquip': appequip,
             'Formulation': formulation }