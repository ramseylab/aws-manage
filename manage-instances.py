import sys
import boto3
import argparse
import json

parser = argparse.ArgumentParser(description="Lists, stops, and starts EC2 instances for the Ramsey Lab",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('command', metavar='command', type=str, help='the command to be run', choices=["list","stop","start"])
parser.add_argument('--instance-id', action='store', metavar='instance_id', type=str, help='the AWS instance ID of the instance to stop or start', default=None)

args = parser.parse_args()
command = args.command
req_instance_id = args.instance_id

result = dict()
ec2 = boto3.client("ec2")

if command == "list":
    response = ec2.describe_instances()
    result['list_data'] = []
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
                        keep_instance = True
            if keep_instance:
                result['list_data'].append({'instance-id': instance['InstanceId'],
                                            'instance-state': instance['State']['Name'],
                                            'instance-name': instance_name})
    result['status'] = 'success'
    result['status_message'] = ''
else:
    if command == "start":
        try:
            ec2.start_instances(InstanceIds=[req_instance_id])
            result['status'] = 'OK'
            result['status-message'] = ''
        except:
            result['status'] = 'error'
            result['status-message'] = str(sys.exc_info()[0])
    else:
        if command == "stop":
            try:
                ec2.stop_instances(InstanceIds=[req_instance_id])
                result['status'] = 'OK'
                result['status-message'] = ''
            except:
                result['status'] = 'error'
                result['status-message'] = str(sys.exc_info()[0])
        else:
            result['status'] = 'error'
            result['status-message'] = 'invalid command: ' + command
print(json.dumps(result))

