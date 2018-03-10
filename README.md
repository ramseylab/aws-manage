# aws-manage
Manage Ramsey Lab EC2 instances

## Installation instructions (for Ubuntu 16.04):

- Install `nginx` using `apt-get` 
- Configure `nginx` site (see attached config file `nginx-sites-advailable-default` which should be installed and renamed as `/etc/nginx/sites-enabled/default`) 
- Install `apache2-utils` using apt-get, to get the command `htpasswd`.
- Install uwsgi compiled for CGI mode (see shell script `build-uwsgi-cgi.sh`)
- configure uwsgi by installing `uwsgi-cgi-py.ini` into `/etc/uwsgi`)
- Set up systemd to run `uwsgi` by copying the config file `uwsgi.service` to `/etc/systemd/system`.
- Install python3 and pip3
- Make a home directory `/home/www-data` for user `www-data` and set it to ownership `www-data.www-data`
- Using pip3, install `boto3` python package under local user `www-data`
- Using pip3, install `awscli` python package under local user `www-data`
- Make sure that user `www-data` has `~/.local/bin` in the path (example `.bash_profile` provided as `www-data.bash_profile`)
- IMPORTANT: set up password protection for directory `/var/www/html` using `htpasswd -c /var/www/html/.htpasswd ramseylab`
- install the CGI script `manage-instances-cgi.py` into `/var/www/html/cgi-bin`
- configure `aws` using `aws configure`
