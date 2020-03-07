# PythonProjects
Listing of Python Projects by folder

SG Ingress Scripts -
Set of python scripts to automate addition of ingress-rules to security groups.

sg_ingress.py - for creating the ingress rule using a json file with the parameteres - params.json
script creates the rule and generates another json file. both json files updated into an S3 bucket
dates.py / revoke.py - for removal of ingress rule from security group in AWS
modules used - datetime boto3 json



Weather App - 
Small python script to give daily weather updates in desired city and send to user by sms. Goal is to setup as cron to run daily and inform user of weather for the day.

Makes use of following modules -

datetime pytemperature openweatherapi twilio requests json
