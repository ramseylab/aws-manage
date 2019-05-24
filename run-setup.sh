#!/bin/bash
# This script should be run as user `ubuntu` on a clean Ubuntu 18.04 AMI OS in AWS.
# Not tested with any other setup conditions, YMMV.

# Update `apt-get`
sudo apt-get update -y

# Install the `nginx` webserver, `make`, and `apache2-utils` (the latter is needed to get the command `htpasswd`)
sudo apt-get install -y nginx make python python3-pip gcc apache2-utils

# `cd` to the home directory:
cd ~

# Download the `aws-manage` software from the ramseylab GitHub site:
git clone https://github.com/ramseylab/aws-manage.git

# Configure `nginx` site (see attached config file `nginx-sites-advailable-default` which should be installed and renamed as `/etc/nginx/sites-enabled/default`)
sudo cp aws-manage/nginx-sites-available-default /etc/nginx/sites-enabled/default

# Install uwsgi compiled for CGI mode (see shell script `build-uwsgi-cgi.sh`) into /usr/local/bin:
sudo bash aws-manage/build-uwsgi-cgi.sh
sudo mv /tmp/uwsgi-cgi /usr/local/bin

# Configure uwsgi by installing `uwsgi-cgi-py.ini` into `/etc/uwsgi`):
sudo mkdir /etc/uwsgi
sudo cp /home/ubuntu/aws-manage/uwsgi-cgi-py.ini /etc/uwsgi

# Set up systemd to run `uwsgi` by copying the config file `uwsgi.service` to `/etc/systemd/system`:
sudo cp aws-manage/uwsgi.service  /etc/systemd/system

# Make a home directory `/home/www-data` for user `www-data` and set it to ownership `www-data.www-data`
sudo mkdir /home/www-data
sudo chown www-data.www-data /home/www-data

# Make the www-data user have home directory '/home/www-data' and shell '/bin/bash'
sudo usermod -d /home/www-data www-data
sudo usermod -s /bin/bash www-data

# Using pip3, install python3 packages boto and awscli locally under the "www-data" user:
sudo su - www-data -c "pip3 install --user boto3 awscli"

# Make sure that user `www-data` has `~/.local/bin` in the path (example `.bash_profile` provided as `www-data.bash_profile`)
sudo cp aws-manage/www-data.bash_profile /home/www-data/.bash_profile

# Set up password protection for directory `/var/www/html` using `htpasswd -c /var/www/html/.htpasswd ramseylab`
# (this command requires you to manually enter the password, so the setup script is not fully automated)
sudo htpasswd -c /var/www/html/.htpasswd ramseylab

# Install the CGI script `manage-instances-cgi.py` into `/var/www/html/cgi-bin`
sudo mkdir /var/www/html/cgi-bin
sudo cp aws-manage/manage-instances-cgi.py  /var/www/html/cgi-bin

# Create a log file directory `/var/log/uwsgi` that user `www-data` can write into
sudo mkdir /var/log/uwsgi
sudo chown www-data.www-data /var/log/uwsgi

# Configure AWS using `aws configure`:
# Note: this step also requires manual data entry at the prompt; copy and paste from the CSV file of your AWS login credentials
# (when prompted, specify the same AWS zone that your instances are normally in; leave the "Default output format" as [None]):
sudo su - www-data -c "aws configure"




