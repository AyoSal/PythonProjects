import boto3, datetime, threading

# Title: sg_ingress.py
# Description: Create Ingress Rule with Python
# Version: 1.0
# Author: Ayo Salawu
# Date: February 27, 2020
## Testing for codeql scanning
# ===============================================================================

# Import required modules

import argparse, json, datetime, threading

# Date and Header
date = datetime.datetime.now()

# Add some color
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
NORMAL = "\033[0;0m"
BOLD = "\033[1m"

from datetime import date, datetime, timedelta, timezone
date1 = date.today()

# future expiry dates
expiry_date = date1 + timedelta(days=14)

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
security_group = ec2.SecurityGroup('id')
def create_dictionary(file_name):
    with open(file_name, 'r') as t:
        param_dict = json.load(t)
    return param_dict
param_dict = create_dictionary('/Users/AyoSal/Documents/python/params.json')
param_dict['date_expiry'] = str(expiry_date)
#for x in param_dict:
ingress_add = security_group.authorize_ingress(
    GroupName=param_dict['GroupName'],
    IpPermissions=[
        {

            'IpProtocol': param_dict['IpProtocol'],
            'IpRanges': [
                {
                    'CidrIp':  param_dict['CidrIP'],
                    'Description':  param_dict['Description']
                },
            ],

            'ToPort': param_dict['ToPort'],
           'FromPort': param_dict['FromPort']

        }
    ]

)

# Fancy animation (tweaked from Stack..)
done = False
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write(YELLOW + '\rParsing ' + c + NORMAL)
        sys.stdout.flush()
        time.sleep(0.1)

t = threading.Thread(target=animate)

with open('/Users/AyoSal/Documents/python/param_dict', 'a') as json_file:
  json.dump(param_dict, json_file, indent = 4, sort_keys=True)
  #json.dump(IpPermissions, json_file, indent=4, sort_keys=True)

#Upload generated file to S3 bucket
s3 = boto3.client('s3')
s3.upload_file('/Users/AyoSal/Documents/python/param_dict','temitopic1979',f'params{param_dict["Description"]}.json')

s3.upload_file('/Users/AyoSal/Documents/python/param_dict','temitopic1979','params.json')

# Output what is going to happen
print(BLUE + "The Ingress rule has been added to sg on " + str(date1) + NORMAL + BOLD + NORMAL)

print(GREEN + "The Ingress rule will be removed on " + str(expiry_date) + NORMAL + BOLD + NORMAL)
