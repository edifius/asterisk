#!/usr/bin/env bash
cd /
yum install wget gcc openssl-devel bzip2-devel curl git sox
# ========================================================================================================================
# install xz for unpacking tar files
# ========================================================================================================================
if [$(uname -a | grep i386)];
then
wget http://mirror.centos.org/centos/6/os/i386/Packages/xz-4.999.9-0.5.beta.20091007git.el6.i686.rpm
rpm -i xz-4.999.9-0.5.beta.20091007git.el6.i686.rpm
else
wget http://mirror.centos.org/centos/6/os/x86_64/Packages/xz-4.999.9-0.5.beta.20091007git.el6.x86_64.rpm
rpm -i xz-4.999.9-0.5.beta.20091007git.el6.x86_64.rpm
fi
# ========================================================================================================================

# ========================================================================================================================
# Install python 2.7.15
# ========================================================================================================================
cd /usr/src
wget https://www.python.org/ftp/python/2.7.15/Python-2.7.15.tgz
tar -xzf Python-2.7.15.tgz
cd Python-2.7.15
./configure --enable-optimizations
make
make altinstall
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python2.7 get-pip.py
# ========================================================================================================================

# ========================================================================================================================
# Install ffmpeg
# Refer to:
# https://www.johnvansickle.com/ffmpeg/
#
# if this fails
# ========================================================================================================================
cd /
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz
tar -xvf ffmpeg-release-64bit-static.tar.xz

# ========================================================================================================================
# 1. Create symlink to ffmpeg binary
# 2. Update $PATH to add ffmpeg in .bash_profile or .bashrc conditionally
# ========================================================================================================================
ln -s /ffmpeg-4.0.2-64bit-static/ffmpeg /usr/bin/ffmpeg
cd ~
if [$(ls -a | grep .bashrc)];
then
echo "$(cat .bashrc) $(echo $'\nexport PATH=/usr/bin/ffmpeg:$PATH')" > .bashrc
source .bashrc
else
echo "$(cat .bash_profile) $(echo $'\n#export PATH=/usr/bin/ffmpeg:$PATH')" > .bash_profile
source .bash_profile
fi
# ========================================================================================================================

# ========================================================================================================================
# Build libsndfile for scikits.audiolab
# ========================================================================================================================
wget http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.28.tar.gz
tar -xvf libsndfile-1.0.28.tar.gz
cd libsndfile-1.0.28
./configure
make
make install
# ========================================================================================================================

# ========================================================================================================================
# Install Asterisk-AGI-sdk
# ========================================================================================================================
cd /var/lib/asterisk/agi-bin
git clone https://github.com/Vernacular-ai/asterisk-agi-sdk.git
cp -R asterisk-agi-sdk/* .
rm -rf asterisk-agi-sdk
pip install -r requirements.txt
# ========================================================================================================================
#                                        *** FIN ***
