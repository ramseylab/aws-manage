# aws-manage
Manage Ramsey Lab EC2 instances

## What is it?

This is a simple python/CGI-based manager for AWS EC2 instances. It currently
works only in a single AWS zone. It is designed to run in Ubuntu 18.04 on an EC2
instance (no other method of deployment or host OS is tested or supported).

## EC2 instance details:

These are the minimum specifications of the EC2 instance for running the `aws-manage`
software.

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
            

## Screen capture of the AWS instance manager in the browser:

![screen capture of aws-manage](https://raw.githubusercontent.com/ramseylab/aws-manage/master/aws-manage-screen-capture.png)
