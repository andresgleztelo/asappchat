set -e -x

yum -y install nginx gcc gcc-c++ git mysql mysql-devel telnet libffi-devel patch

pip install uwsgi
pip install mysql
pip install mysqlclient
pip install redis
pip install django-websocket-redis
