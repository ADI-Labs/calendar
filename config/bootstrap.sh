#!/usr/bin/env bash

# installs the package passed in if it's not installed
install () {
    package=$1
    dpkg-query -l $package &> /dev/null
    if [ $? -ne 0 ]; then
        apt-get -y install $package
    fi
}

apt-get update

install sqlite3

# install python
install python3
install python3-dev
install python3-software-properties
install git

wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
sudo python3 get-pip.py
rm get-pip.py

sudo pip3 install -r /vagrant/config/requirements.txt


exit 0
