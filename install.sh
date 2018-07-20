#!/usr/bin/env bash
yum install wget gcc
wget http://www.python.org/ftp/python/2.7.10/Python-2.7.10.tar.xz
if [$(uname -a | grep i386)];
then
wget http://mirror.centos.org/centos/6/os/i386/Packages/xz-4.999.9-0.5.beta.20091007git.el6.i686.rpm
rpm -i xz-4.999.9-0.5.beta.20091007git.el6.i686.rpm
else
wget http://mirror.centos.org/centos/6/os/x86_64/Packages/xz-4.999.9-0.5.beta.20091007git.el6.x86_64.rpm
rpm -i xz-4.999.9-0.5.beta.20091007git.el6.x86_64.rpm
fi
tar -xvf Python-2.7.10.tar.xz
cd Python-2.7.10
./configure
make
make altinstall
cd ..
wget https://repo.anaconda.com/archive/Anaconda2-5.2.0-Linux-x86_64.sh
sh Anaconda2-5.2.0-Linux-x86_64.sh
yum install git
conda update conda
wget http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.28.tar.gz
tar -xvf libsndfile-1.0.28.tar.gz
cd libsndfile-1.0.28
./configure
make
make install
cd ..
git pull origin https://github.com/Vernacular-ai/asterisk-agi-sdk.git