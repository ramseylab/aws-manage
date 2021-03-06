import sys
import boto3
import cgi
import cgitb
cgitb.enable()

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
print("<form method=\"get\" action=\"/cgi-bin/manage-instances-cgi.py\">")
if "command" in form:
    command = form["command"].value
    if "target_instance_id" not in form:
        print("<h2>Error: need to specify the field target_instance_id</h2>")
    else:
        if "manager_passcode" not in form:
            print("<h2>Error: need to specify the manager passcode</h2>")
        else:
            target_instance_id = form["target_instance_id"].value
            target_manager_passcode = form["manager_passcode"].value
            instance_info = ec2.describe_instances(InstanceIds=[target_instance_id])["Reservations"][0]["Instances"][0]
            instance_state = instance_info["State"]["Name"]
            instance_tags = instance_info.get("Tags", None)
            if instance_tags is not None:
                manager_passcode = ""
                for tag in instance_tags:
                    if tag["Key"] == "ManagerPasscode":
                        manager_passcode = tag["Value"]
                if manager_passcode == "":
                    print("<h2>Warning: instance has no manager passcode set</h2>")
                if manager_passcode != target_manager_passcode:
                    print("<h2>Sorry:  Passcode not correct</h2>")
                else:
                    if command == "start":
                        if instance_state != "stopped":
                            print("<h2>Error: Instance is not currently stopped, so I can not start it.</h2>")
                        else:
                            try:
                                ec2.start_instances(InstanceIds=[target_instance_id])
                            except:
                                print("<h2>Error starting instance: " + str(sys.exec_info()[0]))
                    else:
                        if command == "stop":
                            if instance_state != "running":
                                print("<h2>Error: Instance is not currently running, so I can not stop it.</h2>")
                            else:
                                try:
                                    ec2.stop_instances(InstanceIds=[target_instance_id])
                                except:
                                    print("<h2>Error stopping instance: " + str(sys.exec_info()[0]))
            else:
                print("<h2>Error: target instance does not have any tags associated with it</h2>")             
print("<table border=\"1\">")
response = ec2.describe_instances()
result['list_data'] = []
manager_passcode = ''
manager_passcodes = dict()
print("<tr><td><em>Instance Name</em></td><td><em>Instance State</em></td><td><em>Instance ID</em></td><td>Instance Type</td><td>Public IP</td></tr>")
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_tags = instance.get('Tags', None)
        if instance_tags is not None:
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
                            keep_instance = True
            if keep_instance:
                instance_id = instance["InstanceId"]
                manager_passcodes[instance_id] = manager_passcode
                instance_state = instance["State"]["Name"]
                instance_type = instance["InstanceType"]
                public_ip = instance.get('PublicIpAddress', 'None')
                if instance_state != "pending" and instance_state != "stopping" and instance_state != "terminated":
                    print("<tr><td><input type=\"radio\" name=\"target_instance_id\" value=\"" + instance_id + "\" />" +
                          instance_name + "</td><td>" + instance_state + "</td><td>" + instance_id + "</td><td>" + instance_type + "</td></tr>")
                else:
                    print("<tr><td>" + instance_name + "</td><td>" + instance_state + "</td><td>" + instance_id +
                          "</td><td>" + instance_type + "</td><td>" + public_ip + "</td></tr>")

print("</table>")

print("<p><input type=\"radio\" name=\"command\" value=\"start\" />Start instance</p>")
print("<p><input type=\"radio\" name=\"command\" value=\"stop\" />Stop instance</p>")
print("<p>Enter Management Passcode for your instance here: <input type=\"text\" name=\"manager_passcode\" /></p>")

print("<p><input type=\"submit\" value=\"submit (this changes instance state!)\" /></p>")
print("<p><input type=\"reset\" value=\"clear form (no refresh)\" /></p>")
print("<a href=\"/cgi-bin/manage-instances-cgi.py\">reresh page</a></p>")
print("</form>")
print("</body>")
print("</html>")
