import os
import boto3
import sys
import time
import json
from util import print_error


def loadEnvData():
    try:
        dataDic = {'regionName': os.getenv('region'),
                   'awsAccessKeyId': os.getenv('CliqrCloudAccountPwd'),
                   'awsSecretAccessKey': os.getenv('CliqrCloud_AccessSecretKey'),
                   'keyName': os.getenv('AwsEc2KeyName'),
                   'clusterName': os.getenv('EMRClusterName'),
                   'clusterLogPath': os.getenv('S3ClusterLogPath'),
                   'numNodes': os.getenv('NumberOfNodes'),
                   'installApplication': os.getenv('InstallApplications'),
                   'stepType': os.getenv('StepType'),
                   'streamingTypeinputs': os.getenv('StreamingTypeInputs'),
                   'hiveTypeinputs': os.getenv('HiveTypeInputs'),
                   'pigTypeInputs': os.getenv('PigTypeInputs'),
                   'sparkDeploymode': os.getenv('SparkDeployMode'),
                   'sparkSubmitOptions': os.getenv('SparkSubmitOptions'),
                   'sparkApplicationLocation': os.getenv('SparkApplicationLocation'),
                   'customJarTypeJarlocation': os.getenv('CustomJarTypeJarlocation'),
                   'customjarTypeArguments': os.getenv('CustomJarTypeArguments')}

        return dataDic
    except Exception as e:
        print_error(e)
        sys.exit(127)


data = loadEnvData()
steps = []


def connectAwsEmr():
    try:
        connection = boto3.client('emr', region_name=data['regionName'], aws_access_key_id=data['awsAccessKeyId'],
                                  aws_secret_access_key=data['awsSecretAccessKey'])
        return connection
    except Exception as e:
        print_error(e)
        sys.exit(127)


def describeKeyPair():
    try:
        ec2 = boto3.client('ec2', region_name=data['regionName'], aws_access_key_id=data['awsAccessKeyId'],
                           aws_secret_access_key=data['awsSecretAccessKey'])
        response = ec2.describe_key_pairs()

        for keypairs in response['KeyPairs']:
            if keypairs['KeyName'] == data['keyName']:
                keyname = keypairs['KeyName']
                return keyname

        print_error("'" + data['keyName'] + "' KeyPair Not Found In The Region '" + data['regionName'] + "'")
        sys.exit(127)
    except Exception as e:
        print("'" + data['keyName'] + "' KeyPair Not Found In The Region '" + data['regionName'] + "'\n")
        print_error(e)
        sys.exit(127)


def installApplications():
    applications = [
        {
            'Name': 'Hadoop'
        },
    ]
    if data['installApplication'] == "":
        return applications
    else:
        appsList = data['installApplication'].split(',')
        for app in appsList:
            applications.append({'Name':app.strip()})
        return applications


def getSteptype():
    steplis = data['stepType'].split(',')
    for step in steplis:
        if step == 'Streaming Program':
            streamingStepCreation()
        elif step == 'Hive Program':
            hiveStepCreation()
        elif step == 'Pig Program':
            pigStepCreation()
        elif step == 'Spark Application':
            sparkStepCreation()
        elif step == 'Custom JAR':
            customStepcreation()


def streamingStepCreation():
    global steps

    streamingInputs = data['streamingTypeinputs'].split(',')

    if len(streamingInputs) < 4 or "" in streamingInputs:
        print_error("Streaming Program Step Inputs are Not Configured Properly")
        sys.exit(127)

    mapLocation, reduceLocation, inputLocation, outputLocation = streamingInputs[0], streamingInputs[1], \
                                                                 streamingInputs[2], streamingInputs[3]

    files = "s3://" + mapLocation + "," + "s3://" + reduceLocation
    mapperPath = mapLocation.split('/')
    mapperName = mapperPath[-1]
    reducerPath = reduceLocation.split('/')
    reducerName = reducerPath[-1]
    inputLocName = "s3://" + inputLocation
    outputLocName = "s3://" + outputLocation

    step = {'Name': 'Streaming Program',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': [
                    'hadoop-streaming',
                    '-files', files,
                    '-mapper', mapperName,
                    '-reducer', reducerName,
                    '-input', inputLocName,
                    '-output', outputLocName
                ]}
            }
    steps.append(step)


def hiveStepCreation():
    global steps
    step = ''
    hiveInputs = data['hiveTypeinputs'].split(',')

    if (2 == len(hiveInputs) and "" in hiveInputs) or 2 > len(hiveInputs):
        print_error("Hive Program Step Inputs are Not Configured Properly")
        sys.exit(127)

    if len(hiveInputs) == 3 and hiveInputs[1] == "" and hiveInputs[2] != "":
        print_error("Hive Program Step Inputs are Not Configured Properly")
        sys.exit(127)

    if len(hiveInputs) >= 3 and hiveInputs[2] != "":
        step = {'Name': 'Hive Program',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': [
                        'hive-script',
                        '--run-hive-script',
                        '--args',
                        '-f','s3://' + hiveInputs[0],
                        '-d','INPUT=s3://' + hiveInputs[1],
                        '-d','OUTPUT=s3://' + hiveInputs[2]
                    ]}
                }

    elif len(hiveInputs) == 2 or len(hiveInputs) >= 3 and hiveInputs[2] == "":
        step = {'Name': 'Hive Program',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': [
                        'hive-script',
                        '--run-hive-script',
                        '--args',
                        '-f', 's3://' + hiveInputs[0],
                        '-d', 'INPUT=s3://' + hiveInputs[1]
                    ]}
                }


    steps.append(step)


def pigStepCreation():
    global steps
    step = ''
    pigInputs = data['pigTypeInputs'].split(',')

    if (2 == len(pigInputs) and "" in pigInputs) or 2 > len(pigInputs):
        print_error("Pig Program Step Inputs are Not Configured Properly")
        sys.exit(127)

    if len(pigInputs) == 3 and pigInputs[1] == "" and pigInputs[2] != "":
        print_error("Pig Program Step Inputs are Not Configured Properly")
        sys.exit(127)

    if len(pigInputs) >= 3 and pigInputs[2] != "":
        step = {'Name': 'Pig Program',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': [
                        'pig-script',
                        '--run-pig-script',
                        '--args',
                        '-f', 's3://' + pigInputs[0],
                        '-p', 'INPUT=s3://' + pigInputs[1],
                        '-p', 'OUTPUT=s3://' + pigInputs[2]
                    ]}
                }


    elif len(pigInputs) == 2 or len(pigInputs) >= 3 and pigInputs[2] == "":
        step = {'Name': 'Pig Program',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': [
                        'pig-script',
                        '--run-pig-script',
                        '--args',
                        '-f', 's3://' + pigInputs[0],
                        '-p', 'INPUT=s3://' + pigInputs[1]
                    ]}
                }

    steps.append(step)


def sparkStepCreation():
    global steps

    if "" == data['sparkApplicationLocation']:
        print_error("S3 Location OF SparkApplication Is Not Defined")
        sys.exit(127)
    step = {'Name': 'Spark Application',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': [
                    'spark-submit',
                    '--deploy-mode', data['sparkDeploymode'].lower(),
                ]}
            }
    if data['sparkDeploymode'] == 'Cluster':
        sparkApplicationLocation = 's3://' + data['sparkApplicationLocation']
    else:
        sparkApplicationLocation = data['sparkApplicationLocation']

    if data['sparkSubmitOptions'] != '':
        step['HadoopJarStep']['Args'].append(data['sparkSubmitOptions'] )
        step['HadoopJarStep']['Args'].append(sparkApplicationLocation)
    else:
        step['HadoopJarStep']['Args'].append(sparkApplicationLocation)
    steps.append(step)


def customStepcreation():
    global steps

    if "" == data['customJarTypeJarlocation']:
        print_error("S3 Location OF CustomJarType Is Not Defined")
        sys.exit(127)

    step = {'Name': 'Custom JAR',
            'HadoopJarStep': {
                'Jar': data['customJarTypeJarlocation'],
                'Args': []
            }
            }
    if data['customjarTypeArguments'] != "":
        step['HadoopJarStep']['Args'].append(data['customjarTypeArguments'])

    steps.append(step)


def createDefaultRoles():
    try:

        client = boto3.client('iam', region_name=data['regionName'], aws_access_key_id=data['awsAccessKeyId'],
                              aws_secret_access_key=data['awsSecretAccessKey'])

        createEmrEc2Default(client)
        createEmrdefault(client)

    except Exception as e:
        print_error(e)
        sys.exit(127)


def createEmrEc2Default(client):
    try:
        client.get_role(
            RoleName='EMR_EC2_DefaultRole'
        )

    except Exception:
        path = '/'

        trust_policy = {
            "Version": "2012-10-17",
            "Statement": {
                "Effect": "Allow",
                "Principal": {"Service": "ec2.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        }

        client.create_role(
            Path=path,
            RoleName='EMR_EC2_DefaultRole',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            MaxSessionDuration=3600,
        )

        client.attach_role_policy(
            RoleName='EMR_EC2_DefaultRole',
            PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role'
        )

        client.create_instance_profile(
            InstanceProfileName='EMR_EC2_DefaultRole',
            Path='/'
        )

        client.add_role_to_instance_profile(

            RoleName='EMR_EC2_DefaultRole',
            InstanceProfileName='EMR_EC2_DefaultRole'
        )


def createEmrdefault(client):
    try:
        client.get_role(
            RoleName='EMR_DefaultRole'
        )

    except Exception:
        path = '/'

        trust_policy = {
            "Version": "2012-10-17",
            "Statement": {
                "Effect": "Allow",
                "Principal": {"Service": "elasticmapreduce.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        }

        client.create_role(
            Path=path,
            RoleName='EMR_DefaultRole',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            MaxSessionDuration=3600,
        )

        client.attach_role_policy(
            RoleName='EMR_DefaultRole',
            PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole'
        )


def getClusterState(cluster_id):
    try:
        response = connectAwsEmr().describe_cluster(
            ClusterId=cluster_id['JobFlowId']
        )
        if response['Cluster']['Status']['State'] == 'WAITING':
            with open("jobid.json", "w") as f:
                json.dump({'JobFlowId': cluster_id['JobFlowId']}, f)

        elif response['Cluster']['Status']['State'] == 'TERMINATED_WITH_ERRORS':
            print_error(response['Cluster']['Status']['StateChangeReason']['Message'])
            sys.exit(127)
        else:
            time.sleep(100)
            getClusterState(cluster_id)

    except Exception as e:
        print_error(e)
        sys.exit(127)


def runCluster():
    try:
        createDefaultRoles()
        getSteptype()
        cluster_id = connectAwsEmr().run_job_flow(Name=data['clusterName'], LogUri="s3://" + data['clusterLogPath'],
                                                  ReleaseLabel='emr-5.25.0',
                                                  Applications=installApplications(),
                                                  Instances={
                                                      'Ec2KeyName': describeKeyPair(),
                                                      'KeepJobFlowAliveWhenNoSteps': True,
                                                      'InstanceGroups': [
                                                          {'Name': 'master',
                                                           'InstanceRole': 'MASTER',
                                                           'InstanceType': 'm4.large',
                                                           'InstanceCount': 1,
                                                           'Configurations': [
                                                               {'Classification': 'yarn-site',
                                                                'Properties': {
                                                                    'yarn.nodemanager.vmem-check-enabled': 'false'}}]},
                                                          {'Name': 'core',
                                                           'InstanceRole': 'CORE',
                                                           'InstanceType': 'm4.large',
                                                           'InstanceCount': int(data['numNodes']) - 1,
                                                           'Configurations': [
                                                               {'Classification': 'yarn-site',
                                                                'Properties': {
                                                                    'yarn.nodemanager.vmem-check-enabled': 'false'}}]},
                                                      ]},
                                                  Steps=steps,
                                                  VisibleToAllUsers=True,
                                                  JobFlowRole='EMR_EC2_DefaultRole',
                                                  ServiceRole='EMR_DefaultRole',
                                                  Tags=[
                                                      {
                                                          'Key': 'mykey',
                                                          'Value': 'myvalue',
                                                      },

                                                  ],
                                                  )

        getClusterState(cluster_id)

    except Exception as e:
        print("Failed To Create The Cluster \n")
        print_error(e)
        sys.exit(127)


runCluster()
