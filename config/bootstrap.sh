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
install python
install python-pip
install python-dev
install python-software-properties

sudo pip install -r /vagrant/config/requirements.txt


exit 0
