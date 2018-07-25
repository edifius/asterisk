#!/usr/bin/env bash
cd /
cat art/art.txt
# ========================================================================================================================
# Install if python path is provided
# Usage:
#   -i flag installs python 2.7.15
#   -p requires /path/to/python2.7
# ========================================================================================================================
install_flag=""
python_bin_path=""


while getopts 'ip:' flag;
do
  case "${flag}" in
    i) install_flag='true' ;;
    p) python_bin_path="${OPTARG}" ;;
    *)  echo "==================================================="
        echo "Python2.7 is necessary for running this script!"
        echo "Use the script like:"
        echo "sh install.sh -p /path/to/python2.7.*"
        echo "..."
        echo "or (this may not work for all devices)"
        echo "sh install.sh -p $(which python2.7)"
        echo "----------------------------------------------------"
        echo "If you want python 2.7 installed with this script"
        echo "run it like:"
        echo "sh install.sh -i"
        echo "===================================================="
    exit 1 ;;
  esac
done

if [ -z $install_flag ];
then
    if [ -z $python_bin_path ];
    then
        echo "==================================================="
        echo "Python2.7 is necessary for running this script!"
        echo "Use the script like:"
        echo "sh install.sh -p /path/to/python2.7.*"
        echo "..."
        echo "or (this may not work for all devices)"
        echo "sh install.sh -p $(which python2.7)"
        echo "----------------------------------------------------"
        echo "If you want python 2.7 installed with this script"
        echo "run it like:"
        echo "sh install.sh -i"
        echo "===================================================="
        exit 0
    fi
fi
# ========================================================================================================================

yum install wget gcc openssl-devel bzip2-devel curl git sox
# ========================================================================================================================
# install xz for unpacking tar files
# ========================================================================================================================
if [ -z "$(xz -V)" ];
then
    if [ $(uname -a | grep i386) ];
    then
        wget http://mirror.centos.org/centos/6/os/i386/Packages/xz-4.999.9-0.5.beta.20091007git.el6.i686.rpm
        rpm -i xz-4.999.9-0.5.beta.20091007git.el6.i686.rpm
    else
        wget http://mirror.centos.org/centos/6/os/x86_64/Packages/xz-4.999.9-0.5.beta.20091007git.el6.x86_64.rpm
        rpm -i xz-4.999.9-0.5.beta.20091007git.el6.x86_64.rpm
    fi
fi
# ========================================================================================================================

# ========================================================================================================================
# Install python 2.7.15
# ========================================================================================================================
if [ "$install_flag" == "true" ];
then
    cd /usr/src
    wget https://www.python.org/ftp/python/2.7.15/Python-2.7.15.tgz
    tar -xzf Python-2.7.15.tgz
    cd Python-2.7.15
    ./configure --enable-optimizations
    make
    make altinstall
    curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
    python2.7 get-pip.py
    python_bin_path="$(which python2.7)"
    cd /
fi
# ========================================================================================================================

# ========================================================================================================================
# Remove pre-existing and create create custom symlink
# and add to $PATH
# ========================================================================================================================
rm -f /usr/bin/vai-agi-python-path
ln -s "$python_bin_path" /usr/bin/vai-agi-python-path
if [ -f ~/.bashrc ];
then
    echo "$(cat ~/.bashrc) $(echo $'\nexport PATH=/usr/bin/vai-agi-python-path:$PATH')" > ~/.bashrc
    source .bashrc
else
    echo "$(cat ~/.bash_profile) $(echo $'\nexport PATH=/usr/bin/vai-agi-python-path:$PATH')" > ~/.bash_profile
    source .bash_profile
fi
# ========================================================================================================================

# ========================================================================================================================
# Install ffmpeg
# Refer to:
# https://www.johnvansickle.com/ffmpeg/
# if this section fails
# ========================================================================================================================
cd /
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz
tar -xvf ffmpeg-release-64bit-static.tar.xz

# ========================================================================================================================
# 1. Create symlink to ffmpeg binary
# 2. Update $PATH to add ffmpeg in .bash_profile or .bashrc conditionally
# ========================================================================================================================
ln -s /ffmpeg-4.0.2-64bit-static/ffmpeg /usr/bin/ffmpeg
if [ -f ~/.bashrc ];
then
    echo "$(cat ~/.bashrc) $(echo $'\nexport PATH=/usr/bin/ffmpeg:$PATH')" > ~/.bashrc
    source .bashrc
else
    echo "$(cat ~/.bash_profile) $(echo $'\nexport PATH=/usr/bin/ffmpeg:$PATH')" > ~/.bash_profile
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
cat art/fin.txt
#                                        *** FIN ***
