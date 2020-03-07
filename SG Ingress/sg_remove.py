import boto3, datetime, twilio, json, threading

from datetime import date, datetime, timedelta, timezone

# Add some color
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
NORMAL = "\033[0;0m"
BOLD = "\033[1m"

date1 = date.today()
s3 = boto3.resource('s3')
obj = s3.Object('temitopic1979','params.json')
body = obj.get()['Body'].read().decode('utf-8')
json_content = json.loads(body)
for i in obj:
    print(body)

Desc = json_content['Description']
date_expiry = json_content['date_expiry']

#f'params{desc["Description"]}.json'

# future expiry dates
if str(date1) < str(date_expiry):

    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2')
    security_group = ec2.SecurityGroup('id')
    response = security_group.revoke_ingress(
        GroupName='test-sg',
        IpPermissions=[
            {

                'IpProtocol': 'TCP',
                'IpRanges': [
                    {
                        'CidrIp': '142.122.124.112/32',
                        'Description': 'DOSD-564-1'
                    },
                ],

                'ToPort': 8900,
                'FromPort': 8900

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
        # sys.stdout.write(GREEN + '\rDone. ' + NORMAL)


    t = threading.Thread(target=animate)

    # Output what is going to happen
    print(BLUE + "The Ingress Rule has been removed as scheduled on " + str(date1) + NORMAL + BOLD + NORMAL)



     #insert removal code!!

    from twilio.rest import Client

# the following line needs your Twilio Account SID and Auth Token
client = Client("ACxxxxxx", "cXXXXX")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
client.messages.create(to="+14377741007",
                       from_="+1205740-2281",
                       body="Hello from Python! Ingress rule for " + str(Desc) + "Ayos code is Slick!!")
