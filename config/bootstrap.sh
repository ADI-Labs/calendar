#!/usr/bin/env bash

apt-get update
apt-get upgrade

apt-get install --yes git \
    postgresql-9.3 \
    vim

sudo -u postgres psql -c "CREATE USER adi_calendar WITH PASSWORD 'bzYcqT4k';"
sudo -u postgres psql -c "CREATE DATABASE calendar;"
sudo -u postgres psql -c "GRANT CONNECT ON DATABASE calendar TO adi_calendar;"
sudo -u postgres psql -c "GRANT ALL ON DATABASE calendar TO adi_calendar;"


if [ ! -d "/opt/conda" ]; then
    wget --quiet --no-clobber http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh -b -p "/opt/conda"
    echo 'export PATH="/opt/conda/bin:$PATH"' >> /home/vagrant/.bashrc
    sudo chown -R vagrant:vagrant /opt/conda
fi

export PATH="/opt/conda/bin:$PATH"

conda update --yes --quiet conda
sudo chown -R vagrant:vagrant /opt/conda

conda env update --name root --file /vagrant/config/environment.yml
