# FLASK_QED README
*Last updated 05/28/2018*

#### Description
flask_qed is a flask application for executing qed logic and model data. Models are initiated through REST API endpoints utilizing [flask](http://flask.pocoo.org/) and [flask_restful](https://flask-restful.readthedocs.io/en/latest/). The endpoints then pass off the tasks to celery for async execution, with a returned response containing a unique task_id. Task status and task data endpoints are provided where the only necessary argument is the unique task_id. Upon successful completion of a task, the data is dumped into a mongoDB database which is retrievable using the task_id, prior to data expiration currently set to 24 hours after task completion. The entire qed application, including flask-qed, is implemented using docker-compose where each application is contained in a separate docker container. The flask stack requires 4 docker containers, the flask container itself, [celery](http://www.celeryproject.org/), [redis](https://redis.io/) and [mongoDB](https://www.mongodb.com/). These containers are listed in qed's docker-compose.yml.

#### Multiple Flask Application
The flask application for flask_qed is executed from the flask_cgi.py file. Here a flask app is imported from both pram_flask and hms_flask where both are merged into a single flask app using werkzeug.wsgi DispatcherMiddleware. The different flask applications are routed by a url prefix. [Documentation on combining flask applications.](http://flask.pocoo.org/docs/0.12/patterns/appdispatch/#combining-applications)

#### Flask Docker HUB Image
The docker image for qed_flask is built on top of the [quanted/qed_py3](https://hub.docker.com/r/quanted/qed_py3/) image. The quanted/qed_py3 image provides GDAL, GeoS and Proj4 applications for use by the qed models. By default, quanted/qed_py3 will use the latest version from docker hub which is built from the master branch of [qed_py3](https://github.com/quanted/qed_py3). For running the other branch images, 'staging' and 'dev', the container can be built specifying the version with 'build --build-arg version=dev SERVICE' when running docker-compose.

### Adding New Flask Applications
Add your flask application that you wish to merge into flask_qed as a submodule to the flask_qed repo, in the same way that hms_flask and pram_flask. Except for importing celery from the parent directory, no changes are necessary inside of the flask application that is being added to flask_qed.
##### Updating Celery
Celery is configured and initialized from the parent flask directory, flask_qed, in [celery_cgi.py](https://github.com/quanted/flask_qed/blob/dev/celery_cgi.py). Here any additional tasks specific to each flask application need to be added to the celery_tasks list, where the string points to the location of where celery tasks are declared in the flask app.
##### Updating Flask
To integrate a new flask application into the flask_qed flask app, the new flask app needs to be imported into [flask_cgi.py](https://github.com/quanted/flask_qed/blob/dev/flask_cgi.py). Specifically, the flask 'app' itself needs to be imported and added to the DispatcherMiddleware function call, in the same way as hms and pram, 'import hms_flask.flask_hms as hms' and 'hms.app'. The routing to the new flask app is set by the key value in the form of a url prefix, i.e. '/hms'. To hit any endpoint in your new flask app after the merge, prepend the key value prefix set in flask_cgi.py to the url endpoint you are wanting to hit.

### Adding New Endpoint (using celery)
Examples are being taken from the hms_flask application.
##### flask_hms.py
In the python file that creates the flask application, the flask app is wrapped by flask restful and assigned to 'api' in the following example. Flask restful requires a class implementing Resource as the endpoint resource. Such as:
```code
api.add_resource(IMPORTED_MODULE.CLASS, '/new/endpoint/url')
```
##### New module
Inside your new module class, have the following imports
```code
from flask import Response
from flask_restful import Resource, reqparse
```
To parse the arguments from your request, use reqparse
```code
parser = reqparse.RequestParser()
parser.add_argument('ARGUMENT1')
parser.add_argument('ARGUMENT2')
```
Your class must accept the flask_restful Resource imported earlier
```code
class MyNewClass(Resource):
```
For each HTTP method you wish your new endpoint to accept, add the appropriate function inside the class.
These functions are the equivalent of C# web controllers.
```code
def post(self):
   """ Accept POST requests """
   """ POST request code goes here """

def get(self):
   """ Accept GET requests """
   """ GET request code goes here """

def put(self):
   """ Accept PUT requests """
   """ PUT request code goes here """

def delete(self):
   """ Accept DELETE requests """
   """ DELETE request code here """
```
##### Using Celery
In addition to the http method function, each class that executes a model should have another function where the model is actually excuted, instead of in the http method function. The reason for this is to separate the functions that utilize flask and celery, this helps keep the code clean and allows for much simplier code. Celery is imported from the parent flask application:
```
from celery_cgi import celery
```
##### Example Function
To run a function with celery, the function must use the 'apply_async' function and have the '@celery.task' decorator. The following provides a simple example of utilizing celery from a flask call, which also dumps data into a mongoDB database. These examples can be found [here](https://github.com/quanted/hms_flask/blob/dev/modules/hms_controller.py).
```
def get(self):
    test_id = self.run_test.apply_async(queue="qed")
    return Response(json.dumps({'job_id': test_id.id}))

@celery.task(name="hms_flask_test", bind=True)
def run_test(self):
    task_id = celery.current_task.request.id
    mongo_db = connect_to_mongoDB()
    posts = mongo_db.posts
    time_stamp = datetime.utcnow()
    data_value = {"request_time": str(time_stamp)}
    data = {'_id': task_id, 'date': time_stamp, 'data': json.dumps(data_value)}
    posts.insert_one(data)
```
The apply_async function is simply added to the end of the function call with an args parameter which is a tuple that contains the function arguments. This is also where the specific celery que is stated.

The decorator uses the previously imported celery, some examples have @app.task because they have assigned celery to 'app'. The decorator allows you to state the name of this celery task, as it will be seen in the celery logs, as well as any additions/changes to the celery settings to be used for this task.

The id assigned to this task by celery is returned to the apply_async function call and is retrievable inside the celery function with 'celery.current_task.request.id'.

The data that is generated from this celery task is dumped into our mongoDB database, with an assigned id and timestamp. These are used for data retrieval and expiring data entries in the database.

##### MongoDB
To maintain database integrity, each celery task must establish it's own connection to the mongoDB database. This can be seen in the function call connect_to_mongoDB() in the previous code example, which is defined below:
```
def connect_to_mongoDB():
    if IN_DOCKER == "False":
        # Dev env mongoDB
        logging.info("Connecting to mongoDB at: mongodb://localhost:27017/0")
        mongo = pymongo.MongoClient(host='mongodb://localhost:27017/0')
    else:
        # Production env mongoDB
        logging.info("Connecting to mongoDB at: mongodb://mongodb:27017/0")
        mongo = pymongo.MongoClient(host='mongodb://mongodb:27017/0')
    mongo_db = mongo['flask_hms']
    mongo.flask_hms.Collection.create_index([("date", pymongo.DESCENDING)], expireAfterSeconds=86400)
    # ALL entries into mongo.flask_hms must have datetime.utcnow() timestamp, which is used to delete the record after 86400
    # seconds, 24 hours.
    return mongo_db
```

##### Status/Data Retrieval
Data retrieval and status updates can be handled with the same function, or with different functions/endpoints if that is required. Celery allows for a specific task status to be queried, where Redis checks the current state of the specified task and returns the celery state data. The following is a simple example of a combined get status/data function:
```
class HMSTaskData(Resource):
    """
    Controller class to retrieve data from the mongoDB database and/or checking status of a task
    """
    parser = parser_base.copy()
    parser.add_argument('job_id')

    def get(self):
        args = self.parser.parse_args()
        task_id = args.job_id
        if task_id is not None:
            task = celery.AsyncResult(task_id)
            if task.status == "SUCCESS":
                mongo_db = connect_to_mongoDB()
                posts = mongo_db.posts
                data = json.loads(posts.find_one({'_id': task_id})['data'])
                return Response(json.dumps({'id': task.id, 'status': task.status, 'data': data}))
            else:
                return Response(json.dumps({'id': task.id, 'status': task.status}))
        else:
            return Response(json.dumps({'error': 'id provided is invalid.'}))
```
To get the current state of a celery task, call the celery.AsyncResult() function with the task_id originally provided when the task was initated.

#### Overview
The examples provided above can be found [here](https://github.com/quanted/qed_flask). The following is completely functional as mentioned here on the dev and staging branches. Local development and testing can be done using either Docker locally or executing each of the applications used in the stack locally.
