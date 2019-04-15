import time
import json
import sys,os
import googleapiclient.discovery
from google.oauth2 import service_account
from googleapiclient.errors import Error
from util import print_error,print_log,print_result,write_error
from errorutils import ErrorUtils

class tcp_load_balancer():

    def __init__(self,auth_security):
        """
        Login to google cloud through account json file from google cloud.
        """

        try:
            auth_security = auth_security
            SCOPES = ["https://www.googleapis.com/auth/compute"]
            credentials = service_account.Credentials.from_service_account_info(auth_security, scopes=SCOPES)
            print("credentials",credentials)
            self.service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

        except Exception as er:
            print_error("Getting Service Account Failed.")
            print("Error While Getting Service Account ",er)
            sys.exit(127)


    def _getting_instances(self,project,region,instance_list = []):
        """
        function used the get the list of targetpools in compute
        By using project name and region name.

        :param project:
        :param zone:
        :param instance:
        :return:
        """
        try:
            print("Getting Instances from the instance list using region and instance name")
            instances = []
            try:
                request = self.service.regions().get(project=project, region=region)
                response = request.execute()
            except Exception as er:
                print_error(er)
            print("response for Getting instance is :",response)
            if response:
                zones = response["zones"]
                count = 0
                for zone in zones:
                    count = count + 1
                    zone = zone.split('/')[-1]
                    for instance in instance_list:
                        instance = instance.strip()
                        try:
                            request = self.service.instances().get(project=project, zone=zone, instance=instance)
                            response = request.execute()
                        except:
                            continue
                        if response:
                            instance_name = response["selfLink"]
                            if not instance_list.__contains__(instance_name):
                                instances.append(instance_name)
                        else:
                            continue
                self.instance = instances
                print("source instances is :",self.instance)
            else:
                print("No instance are there to add ,Please create the new instance")

        except Error as e:
            print_error(ErrorUtils.validation_error("InvalidValue", e.message))
            write_error(e)
            sys.exit(127)
        except Exception as err:
                print_error("Given source {} not exist".format(instance_list))
                write_error(ErrorUtils.internal_error(err))
                sys.exit(127)

    def create_healthcheck(self,project,healthcheck):
        """
        Create health check using healthcheck name

        :param healthcheck:
        :return:
        """

        try:
            print("creating healthcheck...")
            health_check_body = {
                "name": healthcheck,
                "type": "HTTP",
                "httpHealthCheck": {
                    "port": 10256,
                    "portName": "http",
                    "requestPath": "/"
                }
            }

            request = self.service.httpHealthChecks().insert(project=project, body=health_check_body)
            response = request.execute()
            time.sleep(2)
            if response:
                self.target_link = response["targetLink"]
                print("Healthcheck created successfully.")

        except Error as e:
            print("error in Error ",e)
            print("Error while Geting creating backend service.", e)
            print_error(ErrorUtils.validation_error("InvalidValue", e.message, healthcheck))
            write_error(e)
            sys.exit(127)

        except Exception as err:
            print("Error while Geting creating creating healthcheck.",err)
            print_error(ErrorUtils.internal_error(err))
            write_error(err)
            sys.exit(127)

    def delete_healthcheck(self,project,health_check):
        """
        deleteing the healthcheck using existing healthcheck name
        :return:
        """
        try:
            print("Deleting Healthcheck...")
            request = self.service.httpHealthChecks().delete(project=project, healthCheck=health_check)
            response = request.execute()
            if response:
                print("Health check deleted successfully")

        except Error as e:
            print("error in Error ",e)
            print("Error while Geting creating backend service.", e)
            print_error(ErrorUtils.validation_error("InvalidValue", e.message, health_check))
            write_error(e)
            sys.exit(127)

        except Exception as err:
            print("Error while Deleting healthcheck.",err)
            print_error(ErrorUtils.internal_error(err))
            write_error(err)
            sys.exit(127)

    def _creating_backend(self,project, region,tcplbname,healthCheck):
        """
        Creating backend service with existing instance and healthcheck for tcp load balancing
        :param project:
        :param region:
        :param tcplbname:
        :param healthCheck:
        :return:
        """

        try:
            print(project, region,tcplbname,healthCheck)
            target_pool_body = {
                "name": tcplbname,
                "instances":self.instance,
                "healthChecks": [
                    "https://www.googleapis.com/compute/v1/projects/{0}/global/httpHealthChecks/{1}".format(project,healthCheck)
                ]
            }
            print("payload for target_pool_body is :",target_pool_body)
            request = self.service.targetPools().insert(project=project, region=region, body=target_pool_body)
            response = request.execute()
            if response:
                self.target_pool_name = response["name"]
                self.target_link = response["targetLink"]
            print("Response for TCP back end is :",response)
            print_log("Created backend service successfully.")
            return True
        except Error as e:
            print("error in Error ",e)
            print("Error while Geting creating backend service.", e)
            print_error(ErrorUtils.validation_error("InvalidValue", e.message, tcplbname))
            write_error(e)
            sys.exit(127)

        except Exception as err:
            print("Error while Geting creating backend service.",err)
            print_error(ErrorUtils.internal_error(err))
            write_error(err)
            sys.exit(127)

    def creating_frontend(self,project,region,lb_name):
        """
        creating backend configuration for tcp loadbalancing
        :param project:
        :param region:
        :return:
        """
        try:
            print("name",self.target_pool_name,"target",self.target_link,)
            forwarding_rule_body = {
                "name": self.target_pool_name,
                "target": self.target_link,
                "IPProtocol": "TCP"
            }
            request = self.service.forwardingRules().insert(project=project, region=region, body=forwarding_rule_body)
            response = request.execute()
            time.sleep(30)
            if response:
                print("Response for front end is :",response)
                operationId = response["targetLink"].split('/')[-1]
                print("Operation id is :",operationId)
                request = self.service.forwardingRules().get(project=project, region=region, forwardingRule=operationId)
                response = request.execute()
                if response:
                    print("response of operation id is :",response)
                    Ipaddress = response["IPAddress"]
                    print("ipaddress for the application access is : ",Ipaddress)
                # data_response = response.replace("\r","")
                # print_result(data_response)
            print_log("Created front end service successfully.")

            result = {"hostName":"TCPloadbalancer"}
            result['ipAddress'] = str(Ipaddress)
            print("Result is :",result)
            print_result(json.dumps(result))

        except Exception as err:
            print("Error while Geting creating front service.", err)
            print_error(ErrorUtils.internal_error(err))
            write_error(err)
            print_log("Start Rollbacking...")
            self.delete_backend(self,project, region,lb_name)
            sys.exit(127)

    def delete_frontend(self,project,region,lb_name):
        """
        Deleting the front end configuration using loadbalancer name
        :param project:
        :param region:
        :param lb_name:
        :return:
        """
        try:
            target_name = None
            print("Deleting the front end from TCP load balancer")
            request = self.service.forwardingRules().list(project=project, region=region)
            if request:
                print("Getting response from the Cloud centre")
                response = request.execute()
                for forwarding_rule in response['items']:
                    if lb_name in str(forwarding_rule["target"]):
                        target_name = forwarding_rule["name"]
                        break
                request = self.service.forwardingRules().delete(project=project, region=region, forwardingRule= target_name)
                response = request.execute()
                if response:
                    print("deleted TCP front end successfully!!!")
        except Exception as er:
            write_error(er)
            print_error(er)
            sys.exit(127)
            print(er)

    def delete_backend(self,project,region,lb_name):
        """
        Deleting backend configuration from the loadbalancer name
        :param project:
        :param region:
        :param lb_name:
        :return:
        """
        request = self.service.targetPools().delete(project=project, region=region, targetPool=lb_name)
        response = request.execute()
        if response:
            print("deleted TCP backend successfully!!!")

class udp_load_balancer():
    def __init__(self,auth_security):
        """
        Login to google cloud through account json file from google cloud.
        """
        try:
            auth_sercurity  = auth_security
            SCOPES = ["https://www.googleapis.com/auth/compute"]
            credentials = service_account.Credentials.from_service_account_info(auth_sercurity, scopes=SCOPES)
            self.service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
        except Exception as err:
            print(err)
            sys.exit(127)

    def _getting_instances(self,project,region,instance_list):
        """
        function used the get the list of targetpools in compute
        By using project name and region name.

        :param project:
        :param zone:
        :param instance:
        :return:
        """
        try:
            instances = []
            print("Getting instance for creating UDP loadbalancer")
            request = self.service.regions().get(project=project, region=region)
            response = request.execute()
            if response:
                zones = response["zones"]
                count = 0
                for zone in zones:
                    count = count + 1
                    zone = zone.split('/')[-1]
                    print(zone)
                    print(project, zone, instance_list)
                    for instance in instance_list:
                        try:
                            request = self.service.instances().get(project=project, zone=zone, instance=instance)
                            response = request.execute()

                        except:
                            continue
                        if response:
                            instance_name = response["selfLink"]
                            if not instance_list.__contains__(instance_name):
                                instances.append(instance_name)
                        else:
                            continue
                self.instance = instances
                print("source instances is :", self.instance)
            else:
                print("No instance are there .")
                print("Please create the new instance")
        except Exception as er:
            print("Error, there is no istance are there. Please create new instance")
            print_error(er)
            sys.exit(127)

    def create_healthcheck(self,project,healthcheck):
        """
        Create health check using healthcheck name

        :param healthcheck:
        :return:
        """

        try:
            print("creating healthcheck...")
            health_check_body = {
                "name": healthcheck,
                "type": "HTTP",
                "httpHealthCheck": {
                    "port": 10256,
                    "portName": "http",
                    "requestPath": "/"
                }
            }

            request = self.service.httpHealthChecks().insert(project=project, body=health_check_body)
            response = request.execute()
            time.sleep(2)
            if response:
                self.target_link = response["targetLink"]
                print("Healthcheck created successfully.")

        except Error as e:
            print("error in Error ",e)
            print("Error while Geting creating backend service.", e)
            print_error(ErrorUtils.validation_error("InvalidValue", e.message, healthcheck))
            write_error(e)
            sys.exit(127)

        except Exception as err:
            print("Error while Geting creating creating healthcheck.",err)
            print_error(ErrorUtils.internal_error(err))
            write_error(err)
            sys.exit(127)

    def delete_healthcheck(self,project,health_check):
        """
        deleteing the healthcheck using existing healthcheck name
        :return:
        """
        try:
            print("Deleting Healthcheck...")
            request = self.service.httpHealthChecks().delete(project=project, healthCheck=health_check)
            response = request.execute()
            if response:
                print("Health check deleted successfully")

        except Error as e:
            print("error in Error ",e)
            print("Error while Geting creating backend service.", e)
            print_error(ErrorUtils.validation_error("InvalidValue", e.message, health_check))
            write_error(e)
            sys.exit(127)

        except Exception as err:
            print("Error while Deleting healthcheck.",err)
            print_error(ErrorUtils.internal_error(err))
            write_error(err)
            sys.exit(127)
    def _creating_backend(self,project, region,udplbname,healthCheck):
        """

        Creating backend service with existing instance and healthcheck for tcp load balancing
        :param project:
        :param region:
        :return:
        """
        try:
            target_pool_body = {
                "name": udplbname,
                "instances": self.instance,
                "healthChecks": [
                    "https://www.googleapis.com/compute/v1/projects/{0}/global/httpHealthChecks/{1}".format(project,
                                                                                                            healthCheck)
                ]
            }
            request = self.service.targetPools().insert(project=project, region=region, body=target_pool_body)
            response = request.execute()
            if response:
                self.target_pool_name = response["name"]
                self.target_link = response["targetLink"]
            print_log("Created backend service successfully.")

        except Error as e:
            print("Error while Geting creating backend service.", e)
            print_error(ErrorUtils.validation_error("InvalidValue", e.message, udplbname))
            write_error(e)
            sys.exit(127)

        except Exception as err:
            print(err)
            print_error(err)
            sys.exit(127)

    def creating_frontend(self,project,region,udplbname):
        """
        creating backend configuration for tcp loadbalancing
        :param project:
        :param region:
        :return:
        """
        try:
            print("name",self.target_pool_name,"target",self.target_link,)
            forwarding_rule_body = {
                "name": self.target_pool_name,
                "target": self.target_link,
                "IPProtocol": "UDP"
            }
            request = self.service.forwardingRules().insert(project=project, region=region, body=forwarding_rule_body)
            response = request.execute()
            time.sleep(30)
            if response:
                operationId = response["targetLink"].split('/')[-1]
                print("Operation id is :", operationId)
                request = self.service.forwardingRules().get(project=project, region=region, forwardingRule=operationId)
                response = request.execute()
                if response:
                    Ipaddress = response["IPAddress"]
                    print("ipaddress for the application access is : ", Ipaddress)

            print_log("Created frontend service successfully.")

            result = {"hostName": "UDPLoadbalancer"}
            result['ipAddress'] = str(Ipaddress)
            print("Result is :", result)
            print_result(json.dumps(result))
        except Exception as err:
            print(err)
            print_error(err)
            print_log("Start Rollbacking...")
            self.delete_backend(self, project, region,udplbname)
            sys.exit(127)

    def delete_frontend(self,project,region,lb_name):
        """
        Deleting the front end configuration using loadbalancer name
        :param project:
        :param region:
        :param lb_name:
        :return:
        """
        print("Deleting front end")
        target_name = None
        request = self.service.forwardingRules().list(project=project, region=region)
        if request:
            response = request.execute()
            for forwarding_rule in response['items']:
                if lb_name in str(forwarding_rule["target"]):
                    target_name = forwarding_rule["name"]
                    break
            request = self.service.forwardingRules().delete(project=project, region=region, forwardingRule= target_name)
            response = request.execute()
            if response:
                print("deleted UDP front end successfully!!!")

    def delete_backend(self,project,region,lb_name):
        """
        Deleting backend configuration from the loadbalancer name
        :param project:
        :param region:
        :param lb_name:
        :return:
        """
        print("Deleting backend service")
        request = self.service.targetPools().delete(project=project, region=region, targetPool=lb_name)
        response = request.execute()
        if response:
            print("deleted UDP backend successfully!!!")

class http_load_balancer():

    def __init__(self,auth_security):
        """
        Login to google cloud through account json file from google cloud.
        """
        auth_security = auth_security
        SCOPES = ["https://www.googleapis.com/auth/compute"]
        credentials = service_account.Credentials.from_service_account_info(
            auth_security, scopes=SCOPES)
        self.service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    def _getting_instances(self,project, region, instance_list=[]):
        """
        function used the get the list of targetpools in compute
        By using project name and region name.

        :param project:
        :param zone:
        :param instance:
        :return:
        """
        try:
            print("Getting Instances from the instance list using region and instance name")
            print(project, region, instance_list)
            instances = []
            try:
                request = self.service.regions().get(project=project, region=region)
                response = request.execute()
            except Exception as er:
                print(er)
            print("response", response)
            if response:
                zones = response["zones"]
                print("Zones is :", zones)
                count = 0
                instance_groupname = "sresat1"
                for zone in zones:
                    count = count + 1
                    zone = zone.split('/')[-1]
                    for instance in instance_list:
                        instance = instance.strip()
                        try:
                            request = self.service.instances().get(project=project, zone=zone, instance=instance)
                            response = request.execute()
                            print("instance response is ", response)
                        except:
                            continue
                        if response:
                            print("Response is :", response)
                            network_name = response["networkInterfaces"][0]["network"]
                            print("network is :", network_name)
                            instance_name = response["selfLink"]
                            print("Instance name is :", instance_name)
                            if not instance_list.__contains__(instance_name):
                                instances.append(instance_name)
                        else:
                            continue
                        print("checking wether resource group exisit or not if its not creating resource group")
                        try:
                            request = self.service.instanceGroups().get(project=project, zone=zone, instanceGroup=instance_groupname)
                            response = request.execute()
                            if response:
                                print("Given Resourcegroup is exisit ")
                        except:
                            print("Given Resource group is not exisit so creating new resource group.")
                            instance_group_body = {
                                "name": instance_groupname,
                                "network": network_name
                            }
                            request = self.service.instanceGroups().insert(project=project, zone=zone,
                                                                      body=instance_group_body)
                            response = request.execute()
                            if response:
                                print("Resource group creation is successfully created.")

                        instance_groups_add_instances_request_body = {
                            "instances": [
                                {
                                    "instance": instance_name
                                }
                            ]
                        }
                        request = self.service.instanceGroups().addInstances(project=project, zone=zone,
                                                                        instanceGroup=instance_groupname,
                                                                        body=instance_groups_add_instances_request_body)
                        response = request.execute()
                        print("response is ", response)
                        if response:
                            self.target_instancegroup = response["targetLink"]
                print("source instances is :", response)
            else:
                print("No instance are there .")
                print("Please create the new instance")
        except Exception as er:
            print("Error, there is no istance are there. Please create new instance", er)
            print_error(er)
            sys.exit(127)
    def create_healthcheck(self,project,healthcheck):
        """
        Create health check using healthcheck name

        :param healthcheck:
        :return:
        """

        try:
            print("creating healthcheck...")
            health_check_body = {
                  "name": healthcheck,
                  "type": "HTTP",
                  "httpHealthCheck": {
                    "port": 10256,
                    "portName": "http",
                    "requestPath": "/"
                  }
            }

            request = self.service.httpHealthChecks().insert(project=project, body=health_check_body)
            response = request.execute()
            time.sleep(2)
            if response:
                self.target_link = response["targetLink"]
                print("Healthcheck created successfully.")

        except Error as e:
            print("error in Error ",e)
            print("Error while Geting creating backend service.", e)
            print_error(ErrorUtils.validation_error("InvalidValue", e.message, healthcheck))
            write_error(e)
            sys.exit(127)

        except Exception as err:
            print("Error while Geting creating creating healthcheck.",err)
            print_error(ErrorUtils.internal_error(err))
            write_error(err)
            sys.exit(127)

    def delete_healthcheck(self,project,health_check):
        """
        deleteing the healthcheck using existing healthcheck name
        :return:
        """
        try:
            print("Deleting Healthcheck...")
            request = self.service.httpHealthChecks().delete(project=project, healthCheck=health_check)
            response = request.execute()
            if response:
                print("Health check deleted successfully")

        except Error as e:
            print("error in Error ",e)
            print("Error while Geting creating backend service.", e)
            print_error(ErrorUtils.validation_error("InvalidValue", e.message, health_check))
            write_error(e)
            sys.exit(127)

        except Exception as err:
            print("Error while Deleting healthcheck.",err)
            print_error(ErrorUtils.internal_error(err))
            write_error(err)
            sys.exit(127)

    def creating_healthyevet(self,project,healthCheck):
        """
        creating healthy event
        :param project:
        :param healthCheck:
        :return:
        """
        try:
            if healthCheck:
                data = {
                      "name": "sampletest",
                      "healthChecks": [
                        "https://www.googleapis.com/compute/v1/projects/{0}/global/httpHealthChecks/{1}".format(project,healthCheck)
                      ]
                    }
            data = json.dumps(data)
            url = "https://www.googleapis.com/compute/v1/projects/{}/global/backendServices".format(project)
            self.session.post(url, params=self.params, headers=self.headers, data=data)
        except Exception as err:
            print(err)

    def createBackendService(self, project, healthCheck,backendservicename):
        """
        creating backend service for HTTP load balancer with below params
        :param project:
        :param healthCheck:
        :return:
        """
        try:
            backendservicename = backendservicename+"bcservice"
            backend_service_body = {
                    "name": backendservicename,
                    "backends": [
                        {
                            "group": self.target_instancegroup
                        }
                    ],
                    "healthChecks": [
                        "https://www.googleapis.com/compute/v1/projects/{0}/global/httpHealthChecks/{1}".format(project,healthCheck)
                      ]
                }
            request = self.service.backendServices().insert(project=project, body=backend_service_body)
            response = request.execute()
            print("creating backend service name  status code",response)

            if response:
                self.targetlink_backendservice= response["targetLink"]
            print("Created backend service successfully...")
            print_log("Created backend service successfully")
        except Exception as err:
            print(err)
            print_error(err)
            sys.exit(127)

    def createUrlMap(self,project,httplbname):
        """
        creating urlmap configuration for HTTP load balancer using below params
        :param project:
        :param httplbname:
        :return:
        """
        try:
            url_map_body = {
                  "name": httplbname,
                  "defaultService": self.targetlink_backendservice
                }
            request = self.service.urlMaps().insert(project=project, body=url_map_body)
            response = request.execute()

            if response:
                self.targetlink_urlmap = response["targetLink"]
            print("created rule map added successfully ")
            print_log("created rule map added successfully")
        except Error as e:
            print("Error while Geting creating backend service.", e)
            print_error(ErrorUtils.validation_error("InvalidValue", e.message, httplbname))
            write_error(e)
            sys.exit(127)

        except Exception as error:
            print_log("Error while creating URL map so deleting Backend service")
            self.delete_backend_service(project,httplbname)
            print(error)
            print_error(error)
            sys.exit(127)

    def createHttpproxy(self,project,httpproxyname):

        """
        Creating httpProxy for the HTTP load balancer using below params
        :param project:
        :param httpproxyname:
        :return:
        """
        try:
            target_http_proxy_body = {
                  "name": httpproxyname+"httpproxy",
                  "urlMap": self.targetlink_urlmap
                }
            request = self.service.targetHttpProxies().insert(project=project, body=target_http_proxy_body)
            response = request.execute()
            if response:
                self.targetlink_httpproxy = response["targetLink"]
            print("created http proxy added successfully")
        except Exception as er:
            print_log("Error while creating httpporxy ,so reverting configuration")
            self.delete_backend_service(project, httpproxyname)
            self.delete_url_map(project,httpproxyname)
            print(er)
            print_error(er)
            sys.exit(127)

    def createForwardingrules(self,project,globalforwadingruleName,IPProtocol,portrange):
        """

        creating forwardingrule for HTTP load balancer using below params
        :param project:
        :param globalforwadingruleName:
        :param IPProtocol:
        :param portrange:
        :return:
        """
        try:
            farwording_rule = globalforwadingruleName
            forwarding_rule_body = {
                  "name": globalforwadingruleName+"frwdrules",
                  "target": self.targetlink_httpproxy,
                  "IPProtocol": IPProtocol,
                  "portRange": portrange ##"80-8080"
                }
            request = self.service.globalForwardingRules().insert(project=project, body=forwarding_rule_body)
            response = request.execute()
            time.sleep(30)
            if response:
                print("response for globalforwarding rule :",response)
                operationId = response["targetLink"].split('/')[-1]
                print("Operatio id is :",operationId)
                request = self.service.globalForwardingRules().get(project=project, forwardingRule=operationId)
                response = request.execute()

                if response:
                    Ipaddress = response["IPAddress"]
                    print("ipaddress for the application access is : ", Ipaddress)

                print("Global forwarding rule added successfully")
                print_log('forwarding rule added Successfully.')

            result = {"hostName": "HTTPloadbalancer"}
            result['ipAddress'] = str(Ipaddress)
            print("Result is :", result)
            print_result(json.dumps(result))


        except Exception as err:
            print_log("Error while creating forwarding rule.so reverting all configuration.")
            self.delete_backend_service(project, farwording_rule)
            self.delete_url_map(project, farwording_rule)
            self.delete_http_proxy(project, farwording_rule)
            print(err)
            print_error(err)
            sys.exit(127)

    def delete_global_forwarding_rule(self,project,globalForwadingRule):
        """
        Deleting http globalforwardrule using following params
        :param project:
        :param globalForwadingRule:
        :return:
        """
        globalForwadingRule= globalForwadingRule+"frwdrules"
        request = self.service.globalForwardingRules().delete(project=project, forwardingRule=globalForwadingRule)
        response = request.execute()
        if response:
            print("Global forwaring Rule deleted successfully")

    def delete_http_proxy(self,project,target_http_proxy):
        """
        Deleting httpproxy config from the below params
        :param project:
        :param target_http_proxy:
        :return:
        """
        target_http_proxy = target_http_proxy+"httpproxy"
        request = self.service.targetHttpProxies().delete(project=project, targetHttpProxy=target_http_proxy)
        response = request.execute()
        if response:
            print("Http proxy deletion completed successfully")

    def delete_url_map(self,project,url_map):
        """
        Deleting url map for http load balancer using below params
        :param project:
        :param url_map:
        :return:
        """
        url_map = url_map
        request = self.service.urlMaps().delete(project=project, urlMap=url_map)
        response = request.execute()
        if response:
            print("Urlmap deletion completed successfully")

    def delete_backend_service(self,project,backEndServiceName):
        """
        Deleting back end service for http loadbalancer using below params.
        :param project:
        :param backEndServiceName:
        :return:
        """

        backEndServiceName=backEndServiceName+"bcservice"
        request = self.service.backendServices().delete(project=project, backendService=backEndServiceName)
        response = request.execute()
        if response:
            print("Backend service is deletion completed sucessfully.")


def main(cmd):
    """
    main method is used to invoke all required function based on give input like TCP,UDP,HTTP

    :param cmd:
    :return:
    """


    arguments = cmd
    time_to_live = 10
    try:

        loadBalancerType = os.environ['gelbLoadBalancerType']
        region_name = os.environ['region']
        #loadBalancerName = os.environ["parentJobName"]
        loadBalancerName = os.environ["gelbLoadBalancerName"]
        dependents = os.environ.get('CliqrDependencies', "")
        health_check = os.environ['gelbHealthCheck']
        account_access_info = os.environ['CliqrCloud_JsonServiceAccount']

        auth_security = account_access_info.replace('\n', '')
        auth_security = json.loads(auth_security)

        #project_name = os.environ['Cloud_Setting_projectName']
        project_name = auth_security['project_id']


        print("project_name is :", project_name)
        print("region_name is:", region_name)
        print("loadBalancerType is :", loadBalancerType)
        try:
            string = loadBalancerName
            loadBalancerName = ''.join(e for e in string if e.isalnum())
        except:
            pass

        if loadBalancerType in "TCP":
             tcpLbname = loadBalancerName
             print("tcpLbname is:", tcpLbname)
        elif loadBalancerType in "HTTP":
            httplbname = loadBalancerName
            print("httplbname is:", httplbname)
        elif loadBalancerType in "UDP":
            udplbname = loadBalancerName
            print("udplbname is :", udplbname)
        else:
             print("Invalid load balancer type from the user. Please give Load balancer type like [ HTTP,TCP,UDP]")

        if len(dependents) > 0:
            istances = str(os.environ['CliqrTier_' + dependents + '_HOSTNAME']).split(',')
            print("my instances is ===================>{}".format(istances))

        # if len(dependents) == 0:
        #      istances = None
        #      print("my instances is ===================>{}".format(istances))

        instance_name = istances
        print("instance_name is :",instance_name)
        print("health_check is :",health_check)

    except Exception as er:
        print_error(er.message)
        write_error(er)
        print_error("Unable to get environmental variables")
        sys.exit(127)

    # b64param = _to_bytes(sshKey, "ISO-8859-1")



    def __create_tcp_loadbalancer(tcpLbname,instance_name,region_name,health_check):

        """
        creating tcp load balancer using below parameters
        :param tcpLbname:
        :param instance_name:
        :param region_name:
        :param health_check:
        :return:
        """

        try:
            _object = tcp_load_balancer(auth_security)
            _object._getting_instances(project_name, region_name, instance_name)
            print_log("Creating backend service ...")
            time.sleep(time_to_live)
            _object.create_healthcheck(project_name,health_check)
            _object._creating_backend(project_name, region_name, tcpLbname, health_check)
            time.sleep(time_to_live)
            print_log("Creating frontend service ...")
            _object.creating_frontend(project_name,region_name,tcpLbname)
            return True
        except Exception as err:
            print("Error while creating tcp loadbalancer {}".format(err))
            write_error(err)

    def delete_tcp_loadbalancer(tcpLbname,region_name):

        """
        Deleting tcp load balancer using below parameter
        :param tcpLbname:
        :param region_name:
        :return:
        """

        try:
            _object = tcp_load_balancer(auth_security)
            _object.delete_frontend(project_name,region_name,tcpLbname)
            time.sleep(time_to_live)
            _object.delete_backend(project_name,region_name,tcpLbname)
            _object.delete_healthcheck(project_name,health_check)
            return True
        except Exception as err:
            print("Error while creating tcp load balancer {}".format(err))

    def create_http_loadbalancer(httplbname,health_check):
        """
        creating HTTP load balancer using below parameter.
        :param httplbname: 
        :param health_check: 
        :return: 
        """
        try:
            obj = http_load_balancer(auth_security)
            obj._getting_instances(project_name,region_name,instance_name)
            time.sleep(time_to_live)
            print_log("Creating backend service ...")
            obj.create_healthcheck(project_name,health_check)
            time.sleep(time_to_live)
            obj.createBackendService(project_name,health_check, httplbname)
            time.sleep(time_to_live)
            print_log("Creating url map...")
            obj.createUrlMap(project_name, httplbname)
            time.sleep(time_to_live)
            obj.createHttpproxy(project_name, httplbname)
            time.sleep(time_to_live)
            print_log("Creating forwarding rule...")
            obj.createForwardingrules(project_name, httplbname, "TCP", "8080-8080")
            return True
        except Exception as err:
            print("Error while creating HTTP load balancer {}".format(err))

    def delete_httpLb(httplbname):
        """
        Deleting HTTP load balancer using below parameter.
        :param httplbname:
        :return:
        """
        try:
            dl_lb = http_load_balancer(auth_security)
            dl_lb.delete_global_forwarding_rule(project_name,httplbname)
            time.sleep(time_to_live)
            dl_lb.delete_http_proxy(project_name,httplbname)
            time.sleep(time_to_live)
            dl_lb.delete_url_map(project_name,httplbname)
            time.sleep(time_to_live)
            dl_lb.delete_backend_service(project_name,httplbname)
            # dl_lb.delete_healthcheck(project_name,health_check)
            return True
        except Exception as err:
            print("Error while Deleting HTTP load balancer {}".format(err))

    def create_udp_loadbalancer(udplbname):
        """
        Creating UDP load balancer using below parameter
        :param udplbname:
        :return:
        """
        try:
            _object = udp_load_balancer(auth_security)
            _object._getting_instances(project_name, region_name, instance_name)
            print_log("Creating Backend service ...")

            _object.create_healthcheck(project_name,health_check)
            time.sleep(time_to_live)
            _object._creating_backend(project_name, region_name, udplbname, health_check)
            time.sleep(time_to_live)
            print("Creating frontend service...")
            _object.creating_frontend(project_name, region_name,udplbname)
            return True
        except Exception as err:
            print("Error while creating UDP load balancer {}",err)

    def delete_udp_loadbalancer(udplbname,region_name):
        """
        Deleting UDP load balancer using below parameter.
        :param udplbname:
        :param region_name:
        :return:
        """
        try:
            _object = udp_load_balancer(auth_security)
            _object.delete_frontend(project_name,region_name,udplbname)
            time.sleep(time_to_live)
            _object.delete_backend(project_name,region_name,udplbname)
            _object.delete_healthcheck(project_name,health_check)
            return True
        except Exception as err:
            print("Error while deleting UDP load balancer {}".format(err))

    if arguments in "start":
        print_log("Creating Load balancer...")
        if loadBalancerType in "TCP":
            try:
                if __create_tcp_loadbalancer(tcpLbname,instance_name,region_name,health_check):
                    print_log("Created Loadbalancer Successfully")
            except:
                print("Error while taking arguments from the user for TCP load balancer")
        elif loadBalancerType in "HTTP":
            try:
                if create_http_loadbalancer(httplbname, health_check):
                    print_log("Created Loadbalancer Successfully ")
            except Exception as er:
                print(er)
                print("Error while taking arguments from the user for HTTP load balancer")
        elif loadBalancerType in "UDP":
            try:
                if create_udp_loadbalancer(udplbname):
                    print_log("Created Loadbalancer Successfully")
            except:
                print("Error while taking arguments from the user for UDP Loadbalancer")


    elif arguments in "stop":
        print_log("deleting Load balancer...")
        if loadBalancerType in "TCP":
            try:
                print("Stoping the TCP loadbalancer")
                delete_tcp_loadbalancer(tcpLbname,region_name)
            except:
                print("Error while taking arguments from the user")

        elif loadBalancerType in "HTTP":
            try:
                print("Deleting HTTP Load balancer.")
                delete_httpLb(httplbname)
            except:
                print("Error while taking arguments from the user")

        elif loadBalancerType in "UDP":
            try:
                print("Deleting UDP loadbalancer.")
                delete_udp_loadbalancer(udplbname,region_name)
            except:
                print("Error while taking arguments from the user")
        else:
            print("Error, Please give correct loadbalancer type.")