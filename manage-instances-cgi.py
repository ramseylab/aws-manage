import sys
import boto3
import cgi
import cgitb
cgitb.enable()
#import argparse
#import json

# parser = argparse.ArgumentParser(description="Lists, stops, and starts EC2 instances for the Ramsey Lab",
#                                  formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# parser.add_argument('command', metavar='command', type=str, help='the command to be run', choices=["list","stop","start"])
# parser.add_argument('--instance-id', action='store', metavar='instance_id', type=str, help='the AWS instance ID of the instance to stop or start', default=None)

# args = parser.parse_args()
# command = args.command
# req_instance_id = args.instance_id

result = dict()
ec2 = boto3.client("ec2")

print("Content-type: text/html\n\n")

print("<!DOCTYPE html>")
print("<html>")
print("<head>")
print("<title>Ramsey Lab EC2 Instance Manager</title>")
print("</head>")
print("<body>")
print("<h1>Ramsey Lab EC2 Instance Manager</h1>")

form = cgi.FieldStorage()
if "command" in form:
    command = form["command"].value
    if "target_instance_id" not in form:
        print("<h1>Error</h1>")
        print("<p>need to specify the field target_instance_id</p>")
    else:
        if "manager_passcode" not in form:
            print("<h1>Error</h1>")
            print("<p>need to specify the manager passcode</p>")
        else:
            target_instance_id = form["target_instance_id"]
            manager_passcode = form["manager_passcode"]
            instance_info = ec2.describe_instance(InstanceIds=[target_instance_id])["Reservations"][0]["Instances"][0]
            instance_state = instance_info["State"]["Name"]
            instance_tags = instance_info["Tags"]
            for tag in instance_tags:
                if tag["Key"] == "ManagerPasscode":
                    if tag["Value"] != manager_passcode:
                        print("<h1>Passcode not correct</h1>")
                    else:
                        if command == "start":
                            if instance_state != "stopped":
                                print("<h1>Error</h1>")
                                print("<p>Instance is not stopped, so you cannot start it</p>")
                            else:
                                ec2.start_instances(InstanceIds=[target_instance_id])
                        else:
                            if command == "stop":
                                if instance_state != "running":
                                    print("<h1>Error</h1>")
                                    print("<p>Instance is not running, so you cannot stop it</p>")
                                else:
                                    ec2.start_instances(InstanceIds=[target_instance_id])
           
print("<table>")
response = ec2.describe_instances()
result['list_data'] = []
manager_passcode = ''
manager_passcodes = dict()
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_tags = instance['Tags']
        keep_instance = False
        for tag in instance_tags:
            if tag['Key'] == 'Customer' and tag['Value'] == 'ramseyst':
                keep_instance = True
            else:
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']
                else:
                    if tag['Key'] == 'ManagerPasscode':
                        manager_passcode = tag['Value']
        if keep_instance:
            instance_id = instance["InstanceId"]
            manager_passcodes[instance_id] = manager_passcode
            print("<tr><td>" + instance_name + "</td><td>" + instance["State"]["Name"] + "</td><td>" + instance_id + "</td></tr>")
            
#            result['list_data'].append({'instance-id': instance['InstanceId'],
#                                        'instance-state': instance['State']['Name'],
#                                        'instance-name': instance_name})
print("</table>")

        
print("</body>")
print("</html>")
            
# if command == "list":
#     response = ec2.describe_instances()
#     result['list_data'] = []
#     for reservation in response['Reservations']:
#         for instance in reservation['Instances']:
#             instance_tags = instance['Tags']
#             keep_instance = False
#             for tag in instance_tags:
#                 if tag['Key'] == 'Customer' and tag['Value'] == 'ramseyst':
#                     keep_instance = True
#                 else:
#                     if tag['Key'] == 'Name':
#                        instance_name = tag['Value']
#             if keep_instance:
#                 result['list_data'].append({'instance-id': instance['InstanceId'],
#                                             'instance-state': instance['State']['Name'],
#                                             'instance-name': instance_name})
#     result['status'] = 'success'
#     result['status_message'] = ''
# else:
#     if command == "start":
#         try:
#             ec2.start_instances(InstanceIds=[req_instance_id])
#             result['status'] = 'OK'
#             result['status-message'] = ''
#         except:
#             result['status'] = 'error'
#             result['status-message'] = str(sys.exc_info()[0])
#     else:
#         if command == "stop":
#             try:
#                 ec2.stop_instances(InstanceIds=[req_instance_id])
#                 result['status'] = 'OK'
#                 result['status-message'] = ''
#             except:
#                 result['status'] = 'error'
#                 result['status-message'] = str(sys.exc_info()[0])
#         else:
#             result['status'] = 'error'
#             result['status-message'] = 'invalid command: ' + command
# print(json.dumps(result))

