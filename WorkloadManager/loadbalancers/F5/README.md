# Integrating with F5 BIG-IP

## Introduction

The CloudCenter platform supports integration to various Load Balancers. This document provides information on integration with F5 by creating an external service in CloudCenter.

F5 BIG-IP provides a wide range of application delivery services, such as server load balancing (SLB), L4-L7 firewall and SSL VPN. With the use of iApps and rich foundation of F5 API, Cisco Cloud Center can deploy F5 virtual servers to provide SLB, FW and SSL VPN services to the applications.

Cisco Cloud Center will maintain the application services catalog, provide consistent and agile L4-L7 services to application deployment in both private and public cloud environments.

## Introduction

### CloudCenter
- CloudCenter 4.8 and above
- Knowledge on how to use CloudCenter

### F5 BIG-IP
- Release 12.1.x
- Download App Services iApps 2.0 from GitHub and import into BIG-IP
- BIG-IP management interface must be configured and reachable by Cloud Center
- BIG-IP must be licensed

## Service Package Bundle


The Packer Service bundle consists of the following files:

- service: The main script that has the logic for the integration
- serviceDictionary.csv: The dictionary CSV file that has the list of all the parameters and their defaults. If you want to get addition input from the user, they need to be added to this file and also in the UI. The format of this file is as follows:
```
DisplayName,paramName,paramType,defaultValue
e.g. Root Volume Size,root_volume_size,10
      The parameter name is key here and should match the parameter name in the UI
```
- bigip_rest.py: script that calls the F5 APIs. This python script is called from the main service script
- cliqr.template: F5 template file use by bigip_rest.py
