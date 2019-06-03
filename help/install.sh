#!/usr/bin/env bash
clear;
echo "--------------------------------------------------------------"
echo "############## CRC Portal Installation Script  ############## "
echo "--------------------------------------------------------------"
sleep 2
apt-get udpate # to get the latest package list
apt-get autoremove # to remove any redundancy package
apt-get -y upgrade
echo ""
echo "--------------------------------------------------------------"
echo "############## 1 # Install common library       ##############"
echo "--------------------------------------------------------------"
sleep 2
apt-get install libssl-dev openssl
apt-get install software-properties-common
echo ""
echo "--------------------------------------------------------------"
echo "############## 2 # Install mysql server         ##############"
echo "--------------------------------------------------------------"
sleep 2
read -p "Install MySQL (Y/N): " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    wget https://dev.mysql.com/get/mysql-apt-config_0.8.9-1_all.deb
    dpkg -i mysql-apt-config_0.8.9-1_all.deb
    apt-get update
    apt-get install -y mysql-server
    apt-get install -y libsqlite3-dev
    apt-get install -y libmysqlclient-dev
fi
echo ""
echo "--------------------------------------------------------------"
echo "############## 3 # install mail Postfix service ##############"
echo "--------------------------------------------------------------"
sleep 2
apt-get install -y mailutils
apt-get install -y postfix
echo ""
echo "--------------------------------------------------------------"
echo "############## 4 # install python 3.5           ##############"
echo "--------------------------------------------------------------"
wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz
tar xzvf Python-3.5.0.tgz
(cd Python-3.5.0 && ./configure)
(cd Python-3.5.0 && make)
(cd Python-3.5.0 && make install)
echo ""
echo "--------------------------------------------------------------"
echo "############## 5 # install python libs...       ##############"
echo "--------------------------------------------------------------"
sleep 2
apt-get install -y build-essential libpq-dev libssl-dev openssl libffi-dev zlib1g-dev
apt-get install -y python3-pip python3-dev
apt-get install -y python-django gunicorn python-gevent
apt-get install -y python-mysqldb
pip install --upgrade setuptools
python3 -m pip install --upgrade pip setuptools
echo ""
echo "--------------------------------------------------------------"
echo "############## 6 # install Django ...           ##############"
echo "--------------------------------------------------------------"
sleep 2
#pip3 install --upgrade django
pip3 install Django==2.1.1
echo ""
echo "--------------------------------------------------------------"
echo "############## 7 # install Django Modules...    ##############"
echo "--------------------------------------------------------------"
sleep 2
pip3 install mysqlclient
#pip3 install django-mptt
#pip3 install django-mptt --upgrade
pip3 install django-polymorphic==2.0
#pip3 install djangorestframework
##pip3 install django-filer     # Filtering support
pip3 install markdown     # Markdown support for the browsable API.
pip3 install mysql-connector-python
pip3 install applicationinsights
pip3 install pyparsing==2.2.1
pip3 install python-dateutil==2.7.3
pip3 install pycrypto
echo ""
echo "--------------------------------------------------------------"
echo "############## 8 # install Django RestFramework ##############"
echo "--------------------------------------------------------------"
sleep 2
pip3 install djangorestframework
pip3 install django-filter
echo ""
echo "--------------------------------------------------------------"
echo "############## 9 # install shell web services   ##############"
echo "--------------------------------------------------------------"
sleep 2
apt-get install -y openssl shellinabox
echo ""
echo "--------------------------------------------------------------"
echo "############## 10 # install back end services... ##############"
echo "--------------------------------------------------------------"
sleep 2
pip3 install Flask
pip3 install flask-mysql
pip3 install flask-crossdomain
pip3 install decorators
pip3 install schedule
echo ""
echo "--------------------------------------------------------------"
echo "############## Finish installing all requirements ############"
echo "--------------------------------------------------------------"
echo ""
echo "* Do the following:"
echo "1. install DB see baseDB file"
echo "2. grap the source: git clone https://github.com/qursaan/crc-portal.git"
echo "3. build using rebuild.sh"
echo "4. solve any error appear"
echo "5. run: python manage.py runserver 0:8888"