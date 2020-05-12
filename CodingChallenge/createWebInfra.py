# Title: Web infrastructure App - createWebInfra.py
# Description: Python application to create web infrastructure
# Airtek Coding Exercise
# Version: 2.0
# Author: Ayo Salawu
# Date: May 12 2020


#Importing required Modules
import botocore
import boto3
import botocore.exceptions
import os
import threading
import argparse


# Add some color
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
NORMAL = "\033[0;0m"
BOLD = "\033[1m"

#Declare Global Variables
subnet1a=''
HW1aCidrBlock='192.16.1.0/24'
subnet1b=''
HW1bCidrBlock='192.16.2.0/24'
LBGroup='hello-world-access'
EC2Group='hello-world-ec2'
HWAvailabilityZone1='us-east-1a'
HWAvailabilityZone2='us-east-1b'
InstanceId=''

ec2 = boto3.resource('ec2')
client = boto3.client('elb')

def make_vpc_igw(ec2, ig_tag):
    # Create VPC
    vpc = ec2.create_vpc(CidrBlock='192.16.0.0/16')
    print(GREEN + "The VPC is now created as " + "hello-world-service")
    vpc.create_tags(Tags=[{"Key": "Name", "Value": "hello-world-service"}])
    vpc.wait_until_available()

    # Enable public dns hostname for ease of access via SSH
    ec2Client = boto3.client('ec2')
    ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsSupport = { 'Value': True } )
    ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsHostnames = { 'Value': True } )
    #Create Internet Gateway and attach it to the VPC
    internet_gateway = ec2.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=internet_gateway.id)
    ig_tag =internet_gateway.create_tags(Tags=[{"Key": "Name", "Value": "hello-world-service"}])

def make_snet_rtable(vpc, route, rt_tag, ec2, subnet1a_tag, subnet1b_tag):
    # Create a RouteTable and a Public Route
try:    
    routetable = vpc.create_route_table()
    route = routetable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internet_gateway.id)
    rt_tag = routetable.create_tags(Tags=[{"Key": "Name", "Value": "hello-world-service"}])
    # Create Subnet and associate it with RouteTable
    subnet1a = ec2.create_subnet(CidrBlock=HW1aCidrBlock, AvailabilityZone=HWAvailabilityZone1, VpcId=vpc.id)
    subnet1b = ec2.create_subnet(CidrBlock=HW1bCidrBlock, AvailabilityZone=HWAvailabilityZone2, VpcId=vpc.id)
    routetable.associate_with_subnet(SubnetId=subnet1a.id)
    routetable.associate_with_subnet(SubnetId=subnet1b.id)
    subnet1a_tag = subnet1a.create_tags(Tags=[{"Key": "Name", "Value": "hello-world-service"}])
    subnet1b_tag = subnet1b.create_tags(Tags=[{"Key": "Name", "Value": "hello-world-service"}])
    print(GREEN + "The Internet Gateway, Routetables and Subnets are now created")
except: client.meta.client.exceptions.

# Create security groups for loadbalancer and instance
def make_sg(ec2, lbtag, ec2tag):
    #Loadbalancer Security Group
    lbsecuritygroup = ec2.create_security_group(GroupName=LBGroup, Description='Access to LB', VpcId=vpc.id)
    lbsecuritygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=80, ToPort=80)
    lbtag = lbsecuritygroup.create_tags(Tags=[{"Key": "Name", "Value": "lb-hello-world-service"}])

    #Instance Security Group
    ec2securitygroup = ec2.create_security_group(GroupName=EC2Group, Description='Access to EC2', VpcId=vpc.id)
    #ec2securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
    ec2securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=80, ToPort=80)
    ec2tag = ec2securitygroup.create_tags(Tags=[{"Key": "Name", "Value": "ec2-hello-world-service"}])
    print(BLUE + "The Loadbalancer and EC2 Security Groups are now created")

# Create a key pair and store it in a file
def make_key(ec2):
try: 
    outfile = open('hello-world.pem', 'w') 
    key_pair = ec2.create_key_pair(KeyName='hello-world')
    KeyPairOut = str(key_pair.key_material)
    outfile.write(KeyPairOut)
except: client.meta.client.exceptions.KeyPairAlreadyExists as err:
    print("KeyPair {} already exists!".format(err.response['Error']['KeyName']


#Define Userdata from AMi and Create Linux ec2 Instance 
def make_ec2(ec2, subnet1a,ec2securitygroup, instances):
    user_data = '''#!/bin/bash
    sudo -i
    service httpd restart
    echo test > /robot.txt'''

    instances = ec2.create_instances(
    ImageId='ami-0cecbfa32f2a06c30', UserData=user_data,
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    NetworkInterfaces=[{
    'SubnetId': subnet1a.id,
    'DeviceIndex': 0,
    'AssociatePublicIpAddress': True,
    'Groups': [ec2securitygroup.id]
    }],
    KeyName='hello-world')
    print(GREEN + "Now spinning up ec2 instance with some metadata based off of the Golden image")

#Create Loadbalancer
def make_lb(subnet1a,subnet1b,lbsecuritygroup, lb_response):
    lb_response = client.create_load_balancer(
        LoadBalancerName='hello-world-lb',
        Listeners=[
            {
                'Protocol': 'HTTP',
                'LoadBalancerPort': 80,
                'InstanceProtocol': 'HTTP',
                'InstancePort': 80
                
            },
        ],
        
        Subnets=[
            subnet1a.id, subnet1b.id
        ],
        SecurityGroups=[
            lbsecuritygroup.id,
        ],
        Scheme='',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'lb-hello-world-service'
            },
        ]
    )

#Register ec2 behind Loadbalancer
def reg_ec2(ec2,InstanceId,reg_response,loadb_response):
    for instance in ec2.instances.all():
        print(
            "Id: {0}\nPlatform: {1}\nType: {2}\nPublic IPv4: {3}\nAMI: {4}\nState: {5}\n".format(
            instance.id, instance.platform, instance.instance_type, instance.public_ip_address, instance.image.id, instance.state
            )
        )

    print("Confirming the ec2 instance " + (instance.id) + " is running")
    print(YELLOW + "Now registering the instance " + (instance.id))

    reg_response = client.register_instances_with_load_balancer(
        LoadBalancerName='hello-world-lb',
        Instances=[
            {
                'InstanceId': instance.id
            },
        ]
    )
    #Details of Loadbalancer 
    loadb_response = client.describe_load_balancers(
        LoadBalancerNames=[
            'hello-world-lb',
        ],
    )

def outp(loadb_response):
    #print(loadb_response['LoadBalancerDescriptions'][0]['DNSName'])
    print(GREEN + "The Infrastructure is now created") 
    print (YELLOW + "Please wait a few moments for the App to be reachable at " + loadb_response['LoadBalancerDescriptions'][0]['DNSName'])


