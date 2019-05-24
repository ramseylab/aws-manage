# aws-manage
Manage Ramsey Lab EC2 instances

## EC2 instance details:

- Instance type: `t2.micro`
- AMI: Ubuntu 18.04
- security group:  allow inbound traffic to TCP ports 22 and 80

## Installation instructions (for Ubuntu 16.04):

Log into your `t2.micro` instance as user `ubuntu` and perform these steps:

    ./aws-manage/run-setup.sh

## Running and maintaining the system:

- Cold start:

        sudo service nginx start
        sudo service uwsgi start

- URL for accessing the system:

        http://YOUR_INSTANCE_IP/cgi-bin/manage-instances-cgi.py
        
- Troubleshooting:

    - 503 Bad Gateway error:
    
            sudo service uwsgi start
            
