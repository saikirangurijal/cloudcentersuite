from google.oauth2 import service_account
import googleapiclient.discovery
import json, sys, time, os
import base64
from google.cloud import storage
from util import print_error, print_log, print_result
def create_bucket(credentials,project_name,bucket_name):
    try:
        """Creates a new bucket."""
        storage_client = storage.Client(credentials=credentials, project=project_name)
        bucket = storage_client.create_bucket(bucket_name)
        print('Bucket {} created'.format(bucket.name))
        print_log("Bucket created")
        return bucket.name
    except:
	pass

def upload_blob(credentials, bucket_name, source_file_name, destination_blob_name, project_name):
    try:
        """Uploads a file to the bucket."""
        storage_client = storage.Client(credentials=credentials, project=project_name)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))
        print("Application File uploaded to bucket")
        return destination_blob_name
    except Exception as e:
        print(e)
        print_error(e)
        sys.exit(127)

def get_package_base_name(appPackage):
    name_list = appPackage.split('/')
    package_zip = name_list[len(name_list) - 1].split('.')
    return package_zip[0]
# Creating google cloud function
def createcloudfunction(service, req_body, project_name, bucket_name, credentials):
    destination_blob_name = "storage"
    try:
        storage_path = upload_blob(credentials, bucket_name, source_file_name, destination_blob_name, project_name)
        req_body["sourceArchiveUrl"] = "gs://" + bucket_name + "/" + storage_path
        print_log("File uploaded")
    except Exception as e:
        print(e)
        print_error(e)
        sys.exit(127)
    try:
        print(req_body)
        operation = service.projects().locations().functions().create(
            location='projects/' + project_name + '/locations/'+os.environ['Region'], body=req_body)
        response = operation.execute()
        print(response)
        print_result(json.dumps(response))
        print("Function created successfully")
    except Exception as e:
        print(e)
        print_error(e)
        sys.exit(127)

def delete_blob(credentials,project_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client(credentials=credentials, project=project_name)
    bucket_name="serverlessfunction"
    blob_name="storage"
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
    print('Blob {} deleted.'.format(blob_name))

# Deleting cloud function
def deletecloudfunction(credentials,service, function_name, project_name):
    try:
        operation = service.projects().locations().functions().delete(
            name="projects/" + project_name + '/locations/'+os.environ['Region']+'/functions/' + function_name)
        response = operation.execute()
        print_result(json.dumps(response))
        if 'type' in response:
            items = response['type']
            print(items)
        storage_client = storage.Client(credentials=credentials, project=project_name)
        delete_blob(credentials,project_name)
        bucket = storage_client.get_bucket("serverlessfunction")
        bucket.delete()
    except Exception as err:
        print(err)
        print_error(err)
        sys.exit(127)
command = sys.argv[1]
if __name__ == "__main__":
    app_package = os.environ["AppPackage"]
    print(app_package)
    app_package_base_name = get_package_base_name(app_package)
    source_file_name = "/opt/remoteFiles/cliqr_local_file/" + app_package_base_name + ".zip"
#    source_file_name="quiz.zip"
#SERVICE_ACCOUNT_FILE = r'serviceaccount.json'
    auth_security = os.environ['CliqrCloud_JsonServiceAccount']
    auth_security = auth_security.replace('\n', '')
    auth_security = json.loads(auth_security)
    project_name = auth_security['project_id']
    print(project_name)
    project_name = str(project_name)
    function_name = os.environ["FunctionName"]
    dependents = os.environ['CliqrDependencies']
    print(os.environ)
    try:
    	InstanceName =os.environ['CliqrTier_' + dependents + '_instanceName']
    	MysqlUser =os.environ['CliqrTier_' + dependents + '_Database_Username']
    	Mysqlpassword =os.environ['CliqrTier_' + dependents + '_param1']
        Mysqlpassword= base64.b64decode(Mysqlpassword).decode()
    	Mysqldatabase = os.environ['CliqrTier_' + dependents + '_Database_Name']
    except Exception as err:
    	print("Error getting paraameters from mysql")
    	sys.exit(127)
    req_body = {
    "name": "projects/" + project_name + "/locations/"+os.environ['Region']+"/functions/" + function_name,
    "description": "",
    "entryPoint": os.environ['EntryPoint'],
    "timeout": "60s",
    "availableMemoryMb": 256,
    "labels": {
        "deployment-tool": "console-cloud"
    },
    "runtime": os.environ['Runtime'],
    "environmentVariables": {},
    "httpsTrigger": {},
    "maxInstances": 0,
    "vpcConnector": "",
    "serviceAccountEmail": project_name + "@appspot.gserviceaccount.com",
    "sourceArchiveUrl": "",
    "environmentVariables": {"INSTANCE_CONNECTION_NAME": project_name +":" +os.environ["CliqrCloud_Region"]+":"+InstanceName,
                             "MYSQL_USER": MysqlUser,
                             "MYSQL_PASSWORD": Mysqlpassword,
                             "MYSQL_DATABASE": Mysqldatabase}
}
    bucket_name = "serverlessfunction"
# Authenticating Google account
    print(req_body)
    try:
        SCOPES = [
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/devstorage.read_write',
        'https://www.googleapis.com/auth/devstorage.full_control']
        credentials = service_account.Credentials.from_service_account_info(auth_security, scopes=SCOPES)
        service = googleapiclient.discovery.build('cloudfunctions', 'v1', credentials=credentials)
        storage_client = storage.Client(credentials=credentials, project=project_name)
        print_log("Google authentication succesfull")
    except Exception as e:
        print(e)
        print_error(e)
        sys.exit(127)
    if command == "start":
        print_log("Intiating to create cloud functions")
        create_bucket(credentials,project_name,bucket_name)
        createcloudfunction(service, req_body, project_name, bucket_name, credentials)
    elif command == "stop":
        deletecloudfunction(credentials,service, function_name, project_name)
    else:
        print("Command error")
        print_error("Getting Service Account Failed.")
