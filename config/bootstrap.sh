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
apt-get upgrade

install git
install python3
install python3-dev
install python3-pip
install sqlite3

sudo pip3 install -r /vagrant/config/requirements.txt


exit 0
