#!/usr/bin/env python

import boto3
import os
import sys
import json
from util import print_error, print_log, print_result, write_error
import zipfile
import fileinput
import shutil
import time
from botocore.exceptions import ClientError


platform_list = {
    'G0' : 'Go 1 running on 64bit Amazon Linux/2.11.4',
    '.NET' : 'IIS 10.0 running on 64bit Windows Server 2016/2.1.0',
    'Java' : 'Java 8 running on 64bit Amazon Linux/2.8.6',
    'Node Js' : 'Node.js running on 64bit Amazon Linux/4.9.2',
    'Ruby' : 'Puma with Ruby 2.6 running on 64bit Amazon Linux/2.9.6',
    'PHP' : 'PHP 7.2 running on 64bit Amazon Linux/2.8.12',
    'Python' : 'Python 3.6 running on 64bit Amazon Linux/2.8.6',
    'Tomcat' : 'Tomcat 8.5 with Java 8 running on 64bit Amazon Linux/3.1.6',

}


def aws_conncetion(env_data):
    try:
        # boto3 client configuration
        ebclient = boto3.client('elasticbeanstalk', aws_access_key_id=env_data["ACCESS_KEY"],
                              aws_secret_access_key=env_data["SECRET_KEY"], region_name=env_data["region"])
        s3resource = boto3.resource('s3', aws_access_key_id=env_data["ACCESS_KEY"],
                              aws_secret_access_key=env_data["SECRET_KEY"], region_name=env_data["region"])

        s3client = boto3.client('s3', aws_access_key_id=env_data["ACCESS_KEY"],
                                  aws_secret_access_key=env_data["SECRET_KEY"], region_name=env_data["region"])

        ec2client = boto3.client('ec2', aws_access_key_id=env_data["ACCESS_KEY"],
                              aws_secret_access_key=env_data["SECRET_KEY"], region_name=env_data["region"])
        conn = {
            'ebclient': ebclient,
            's3resource': s3resource,
            's3client': s3client,
            'ec2client': ec2client,
        }
        return conn

    except Exception as err:
        # write_error(err)
        print_error(err)
        sys.exit(127)

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def get_package_base_name(app_package):
    name_list = app_package.split('PACKAGE_DIR%')
    package_zip = name_list[len(name_list) - 1].split('.')
    return package_zip[0]

def upload_s3_file(s3client, data):
    try:
        print_log("Creating bucket")
        response = s3client.create_bucket(
            ACL= 'public-read',
            Bucket=data['bucketName'],
            CreateBucketConfiguration={
                'LocationConstraint': data['region']
            }
        )
        if response:
            local_file=data['appPackage']
            key_name=data['bucketKey']
            print_log(local_file)
            print_log(key_name)
            print_log("Uploading application package into s3 bucket")
            s3client.upload_file(local_file, data['bucketName'], key_name)
            return True
        else:
            print_log('Failed to create the bucket in S3!')
            return False
    except ClientError as e:
        print_error(e.response['Error']['Message'])
        return False
    except Exception as e:
        print_error(e)
        return False

def create_application(conn, data):
    try:
        print_log("Creating application")
        ebclient = conn['ebclient']
        response = ebclient.create_application(
            ApplicationName=data['appName'],
            Description=data['appNameDesc']
        )
        return True if len(response) > 0 else False
    except ClientError as e:
        print_error(e.response['Error']['Message'])
        delete_bucket(conn, data['bucketName'])
        print_error(e.response['Error']['Message'])
        return False
    except Exception as e:
        print_error(e)
        delete_bucket(conn, data['bucketName'])
        return False

def create_application_version(conn, data):
    print_log('Creating application version')
    try:
        ebclient = conn['ebclient']
        response = ebclient.create_application_version(
            ApplicationName=data['appName'],
            VersionLabel=data['versionLabel'],
            SourceBundle={
                'S3Bucket': data['bucketName'],
                'S3Key': data['bucketKey']
            },
            AutoCreateApplication=True,
            Process=True,
        )
        return True if len(response) > 0 else False
    except ClientError as e:
        print_error(e.response['Error']['Message'])
        delete_application(ebclient, data['appName'])
        delete_bucket(conn, data['bucketName'])
        return False
    except Exception as e:
        print_error(e)
        delete_application(ebclient, data['appName'])
        delete_bucket(conn, data['bucketName'])
        return False

def create_environment(conn, data):

    print_log('Creating Environment')
    try:
        ebclient = conn['ebclient']
        platform = 'arn:aws:elasticbeanstalk:' + data['region'] + '::platform/' + platform_list[data['platform']]
        response = ebclient.create_environment(
            ApplicationName=data['appName'],
            CNAMEPrefix=data['domainNamePrefix'] 
            EnvironmentName=data['environmentName'],
            SolutionStackName=platform,
            VersionLabel=data['versionLabel']
        )
        return response['EnvironmentId'] if len(response) > 0 else False
    except ClientError as e:
        print_error(e.response['Error']['Message'])
        delete_application(ebclient, data['appName'])
        delete_bucket(conn, data['bucketName'])
        return False
    except Exception as e:
        print_error(e)
        delete_application(ebclient, data['appName'])
        delete_bucket(conn, data['bucketName'])
        return False

def describe_environment_resources(conn, data):

    try:
        ebclient = conn['ebclient']
        response = ebclient.describe_environment_resources(
            EnvironmentId=data['env_id']
        )
        return response['EnvironmentResources']['Instances'][0]['Id'] if len(response) > 0 else False
    except ClientError as e:
        print_error(e.response['Error']['Message'])
        delete_application(ebclient, data['appName'])
        delete_bucket(conn, data['bucketName'])
        return False
    except Exception as e:
        print_error(e)
        return False

def describe_environments(conn, data):

    try:
        ebclient = conn['ebclient']
        response = ebclient.describe_environments(
            ApplicationName=data['appName'],
            VersionLabel=data['versionLabel'],
            EnvironmentIds=[
                data['env_id'],
            ],

        )
        return response['Environments'][0]['Status'] if len(response) > 0 else False
    except ClientError as e:
        print_error(e.response['Error']['Message'])
        delete_application(ebclient, data['appName'])
        delete_bucket(conn, data['bucketName'])
        return False
    except Exception as e:
        print_error(e)
        return False

def describe_application_versions(conn, data):
    print_log('Checking application version status')
    try:
        ebclient = conn['ebclient']
        response = ebclient.describe_application_versions(
            ApplicationName=data['appName'],
            VersionLabels=[data['versionLabel']]
        )

        return response['ApplicationVersions'][0]['Status'] if len(response) > 0 else False
    except ClientError as e:
        print_error(e.response['Error']['Message'])
        delete_application(ebclient, data['appName'])
        delete_bucket(conn, data['bucketName'])
        return False
    except Exception as e:
        print_error(e)
        return False


### Get instance for VPC ID ####
def describe_instances(conn, data):
    try:
        ec2client = conn['ec2client']
        response = ec2client.describe_instances(
            Filters=[
            ],
            InstanceIds=[
                data['instance_id']
            ]
        )
        if len(response) > 0:
            return {
                'Cloud_Setting_vpcId' : response['Reservations'][0]['Instances'][0]['VpcId'] ,
                'Cloud_Setting_subnetId' : response['Reservations'][0]['Instances'][0]['SubnetId']
            }
        else:
            return False
    except ClientError as e:
        print_error(e.response['Error']['Message'])
        delete_application(conn['ebclient'], data['appName'])
        delete_bucket(conn, data['bucketName'])
        return False
    except Exception as e:
        print_error(e)
        return False

def describe_applications(ebclient, appName):
    try:
        response = ebclient.describe_applications(
            ApplicationNames=[
                appName,
            ]
        )
        return True if len(response) > 0 else False
    except Exception as e:
        print_error(e)
        return False

### Get a list of keys in an S3 bucket  ###
def delete_s3_objects(conn, bucket):
    print_log('Deleting S3 objects')
    try:
        s3client = conn['s3client']
        s3 = conn['s3resource']
        resp = s3client.list_objects_v2(Bucket=bucket)
        for obj in resp['Contents']:
            del_obj = s3.Object(bucket, obj['Key'])
            del_obj.delete()

        return True
    except ClientError as e:
        print_error(e.response['Error']['Message'])
        return False
    except Exception as e:
        print_error(e)
        return False

def delete_bucket(conn, bucketName):
    try:
        s3client = conn['s3client']
        if bool(delete_s3_objects(conn, bucketName)) == True:
            print_log('Deleting bucket')
            response = s3client.delete_bucket(
                Bucket=bucketName
            )
            if response:
                print_log('Bucket deleted!')
                return True
        else:
            print_error("Failed to delete the s3 bucket")
            return False
    except ClientError as e:
        print_error(e.response['Error']['Message'])
        return False
    except Exception as err:
        print_error(err)
        sys.exit(127)

def delete_application(ebclient, appName):
    print_log('Deleting application')
    try:
        response = ebclient.delete_application(
            ApplicationName=appName,
            TerminateEnvByForce=True
        )
        if response:
            time.sleep(100)
            print("Application deleted!")
            return True
    except ClientError as e:
        print_error(e.response['Error']['Message'])
        return False
    except Exception as err:
        print_error(err)
        sys.exit(127)

### Start Functionality #####
def start(env_data, conn):

    status = False
    try:
        if bool(upload_s3_file(conn['s3client'], env_data)) == False:
            print_log('Unable to upload the file into s3')
            return False
        else:
            status = "file_uploaded"

        if bool(create_application(conn, env_data)) == False:
            print_log('Unable to create application')
            return False
        else:
            status = 'app_created'

        if bool(create_application_version(conn, env_data)) == False:
            print_log('Unable to create application version')
            return False

        flag = 1
        while flag == 1:
            version_status = describe_application_versions(conn, env_data)
            print(version_status)
            if version_status == 'PROCESSED':
                print("Status Processed")
                flag = 0
            elif version_status == 'FAILED' or version_status == 'UNPROCESSED':
                print("Revoking process due to application version" + version_status)
                delete_application(conn['ebclient'], env_data['appName'])
                return False
            else:
                print("Continue to check the application version status until it's processed")
                time.sleep(100)
                continue


        env_id = create_environment(conn, env_data)
        if bool(env_id) == False:
            print_log('Unable to create environment')
            return False
        elif env_id:
            env_flag = 1
            while env_flag == 1:
                env_data['env_id'] = env_id
                health_status = describe_environments(conn, env_data)
                print(health_status)
                if health_status == 'Ready':
                    print("Status Processed")
                    env_flag = 0
                elif health_status == 'Terminating' or health_status == 'Terminated':
                    print("Revoking process due to environment status " + health_status)
                    delete_application(conn['ebclient'], env_data['appName'])
                    return False
                else:
                    print("Continue to check the environment status until it's ready")
                    time.sleep(100)
                    continue

            instance_id = describe_environment_resources(conn, env_data)
            if bool(instance_id) == False:
                print_log('Unable to get the instance information')
                return False
            elif instance_id:
                env_data['instance_id'] = instance_id
                vpc_info = describe_instances(conn, env_data)
                if bool(vpc_info) == False:
                    print_log('Unable to get the instance information')
                    return False
                else:
                    return vpc_info

    except Exception as err:
        print_error(err)
        if status == "app_created":
            delete_application(conn['ebclient'], env_data['appName'])
            delete_bucket(conn, env_data['bucketName'])
        elif status == "file_uploaded":
            delete_bucket(conn, env_data['bucketName'])
        sys.exit(127)



def main():
    """
        This is the function to create or delete the service action based on life cycle action command
        :param cmd:
        :return:
        """
    arguments = sys.argv[1]
    
    print(arguments)
    try:
        # get environmantal data and stored in dict
        print_log("Getting environment variables")
        env_data = {}
        
        env_data["ACCESS_KEY"] = os.environ["CliqrCloudAccountPwd"]
        env_data["SECRET_KEY"] = os.environ["CliqrCloud_AccessSecretKey"]
        env_data["region"] = os.environ["region"]
        env_data["appName"] =  os.environ["appName"]
        env_data["appNameDesc"] = os.environ["appNameDesc"]
        env_data["bucketName"] = os.environ["bucketName"]
        env_data["domainNamePrefix"] = os.environ["domainNamePrefix"]
        env_data["versionLabel"] = os.environ["versionLabel"]
        env_data["environmentName"] = os.environ["environmentName"] 
        env_data["platform"] = os.environ["platform"]

        app_package_base_name = get_package_base_name(os.environ["appPackage"])
        if os.getenv('appFilePackage') != None:
       	    appFilePackage = os.environ["appFilePackage"]
            app_package_base_name =  get_package_base_name(appFilePackage)
        print_log(app_package_base_name)
        source_file_name = "/opt/remoteFiles/cliqr_local_file/" + app_package_base_name + ".zip"
        env_data["appPackage"] = source_file_name
        env_data["bucketKey"] = app_package_base_name + ".zip"

        print_log("Start AWS Connection")
        aws_conn = aws_conncetion(env_data)
        ebclient = aws_conn['ebclient']
        print_log("AWS Connected")
        dependencies = os.environ.get('CliqrDependencies', "")
        if len(dependencies) > 0:
            configFileName =  os.environ["appPackageConfigFile"]
            db_host = os.environ['CliqrTier_' + dependencies + '_PUBLIC_IP']
            if db_host:
                with zipfile.ZipFile(source_file_name, 'r') as zip:
                    zip.extractall("/opt/remoteFiles/cliqr_local_file/")

                folder = "/opt/remoteFiles/cliqr_local_file/" + app_package_base_name
                
                filename= folder+configFileName
                with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
                    for line in file:
                        print(line.replace("%DB_TIER_IP%", db_host))

                shutil.make_archive(folder, 'zip', folder)
        link = env_data['domainNamePrefix'] + "." + env_data['region'] + ".elasticbeanstalk.com"
	
        if arguments in "start":
            response = start(env_data, aws_conn)
            if response:
                print_log("Application created and configured successfully.\n Access link: "+ link)
                json_result = {
                    "hostName": '',
                    "ipAddress": "",
                    "environment": response
                }
                print_result(json.dumps(json_result))
        elif arguments in "stop":
            print_log("Deleting applictaion...")
            delete_application(ebclient, env_data['appName'])
            delete_bucket(aws_conn, env_data['bucketName'])


    except Exception as er:
        print_error(er.message)
        f = open('FAILURE', 'w')
        f.write(str(er))
        f.close()
        print_error("Unable to get environmental variables")
        sys.exit(127)



main()
