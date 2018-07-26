#!/usr/bin/env bash
cd /
base64 -d <<<"H4sIAOvjWFsAA81VSY4DIQy89yusXHwYljt8BYk8hMePyzY06cksh0iTVisKuCiXyyY56C2e478F2P
N6GSHG8Et8B9jy2FbpNSISjx8ATJSYmqPvgNOYMnLvKT+c7h2c6WkF3yoIwihvuYZOskxUVY0yI2PBe5gPFdFNRmB5M0
FZiB9CkIl+qhEnOuBKytfQItOwPc0kgJbpEB96xt7QPN4c1jXsMpfZ8FjE3SL9qltug5KOGU8XMuRFMDfT4W5IU7BRsa
ew7EKHQYK2GflvCOetkAU9bYAWnvVs4EVGroSpJpq2MfIf5MJamXngPyvcOzHsy7DakpXuUJ71D8hYprhFBl5k5Ipqtl
LamFuHjUwDV1KLWQ4MjXknLAc+Wu8tF023oORQh2jKgZE8wYuMLAwm85GtKVVvivtBugtReVSyPm8yMlqjRVZnrVQkX7
H6fcgtJe7sCV5k0w05zDHyZMeIzl7fhcbLNzeCKnIZeijrG9LpFNv0ipK7IqhVvwp1AxtZh0WPl4V4jagui42SDy72o9
GaDJs2z5B4dlWhpSAJ2Y3R3x6s8gMYZMKRfFrDutBaKDD+8yUexdtqzxxyD/ipMfMh3QYVI+SdsIgVX8CGlf7ANH7Cfv
lP2fi+Pp6P/wC9gm3j9i36Xf5hj09Uwo62cggAAA==" | gunzip
# ========================================================================================================================
# Install if python path is provided
# Usage:
#   -i flag installs python 2.7.15
#   -p requires /path/to/python2.7
# ========================================================================================================================
install_python_flag=""
skip_install_ffmpeg_flag="false"
skip_install_libsndfile_flag="false"
python_bin_path=""


while getopts 'ibcp:' flag;
do
  case "${flag}" in
    i) install_python_flag='true' ;;
    b) skip_install_ffmpeg_flag='true' ;;
    c) skip_install_libsndfile_flag='true' ;;
    p) python_bin_path="${OPTARG}" ;;
    *)  base64 -d <<<"H4sIALDoWFsAA72TwQrCMAyG732KCB4UnAcvguADePPiA3RdaoM1K23n2Ns7dGOT6kFFc2
    qakP/jJ9lu3w6xb6IpebVcAwVgVBiC9A3o0oOvmImPEE1bCsqTixNxCNh+YJeDpRNuhAgGiEOU1i7bZ+ZgOqsNKQ
    OuHz8XIvsgxE5DU1ZQS47dMLjB3tWwgJqiGSMmMPSVsLQeZdGAkRccqXYokgvQ+uzwmMjmT034LYqlPHChyWKCo/
    6Ls+htecQa+lK/fkx454GXPHkVh02LZV/pWNKtUk68f27twV0BIcOWF6UDAAA=" | gunzip
    exit 1 ;;
  esac
done

if [ -z $install_python_flag ];
then
    if [ -z $python_bin_path ];
    then
        base64 -d <<<"H4sIALDoWFsAA72TwQrCMAyG732KCB4UnAcvguADePPiA3RdaoM1K23n2Ns7dGOT6kFFc2
        qakP/jJ9lu3w6xb6IpebVcAwVgVBiC9A3o0oOvmImPEE1bCsqTixNxCNh+YJeDpRNuhAgGiEOU1i7bZ+ZgOq
        sNKQOuHz8XIvsgxE5DU1ZQS47dMLjB3tWwgJqiGSMmMPSVsLQeZdGAkRccqXYokgvQ+uzwmMjmT034LYqlPH
        ChyWKCo/6Ls+htecQa+lK/fkx454GXPHkVh02LZV/pWNKtUk68f27twV0BIcOWF6UDAAA=" | gunzip
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
if [ "$install_python_flag" == "true" ];
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
    source ~/.bashrc
else
    echo "$(cat ~/.bash_profile) $(echo $'\nexport PATH=/usr/bin/vai-agi-python-path:$PATH')" > ~/.bash_profile
    source ~/.bash_profile
fi
# ========================================================================================================================

# ========================================================================================================================
# Install ffmpeg
# Refer to:
# https://www.johnvansickle.com/ffmpeg/
# if this section fails
#
# 1. Create symlink to ffmpeg binary
# 2. Update $PATH to add ffmpeg in .bash_profile or .bashrc conditionally
# ========================================================================================================================
cd /
if [ "$skip_install_ffmpeg_flag" == "false" ];
then
    wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz
    tar -xvf ffmpeg-release-64bit-static.tar.xz
    ln -s /ffmpeg-4.0.2-64bit-static/ffmpeg /usr/bin/ffmpeg
    if [ -f ~/.bashrc ];
    then
        echo "$(cat ~/.bashrc) $(echo $'\nexport PATH=/usr/bin/ffmpeg:$PATH')" > ~/.bashrc
        source ~/.bashrc
    else
        echo "$(cat ~/.bash_profile) $(echo $'\nexport PATH=/usr/bin/ffmpeg:$PATH')" > ~/.bash_profile
        source ~/.bash_profile
    fi
fi

# ========================================================================================================================

# ========================================================================================================================
# Build libsndfile for scikits.audiolab
# ========================================================================================================================
if [ "$skip_install_libsndfile_flag" == "false" ];
then
    wget http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.28.tar.gz
    tar -xvf libsndfile-1.0.28.tar.gz
    cd libsndfile-1.0.28
    ./configure
    make
    make install
fi
# ========================================================================================================================

# ========================================================================================================================
# Install Asterisk-AGI-sdk
# ========================================================================================================================
cd /var/lib/asterisk/agi-bin
git clone https://github.com/Vernacular-ai/asterisk-agi-sdk.git
cp -R -f asterisk-agi-sdk/* .
rm -rf asterisk-agi-sdk
pip2.7 install -r requirements.txt
# ========================================================================================================================
base64 -d <<<"H4sIAIvjWFsAA61Uy47DIAy88xXWXnzhcYdfQQof4o9fP2hws+yuVOGSahK145nBIcDxiimlCBBO0
46UMgIpc2bM6wwzU0LVFaCALAA8wo12NWYmbVBGNn6rqEl9UmSXpNEMpTQWL15Q6F8Sl+KCorl6ze1av7aedWqfG/AT
3Sm+wakZJecOsgA4jymWSZV+5tO36E6xePjSbLPBc2IqujYjeZz5YyRlinpHQM6rt93svinzdU3dpDGgpUGQzWCBHSL
v1UGRidk0S0h8L3qqBdykJ6mxBpUbPxHoBi+vD5jzEM2oPW63Vf8hBB3VGGakJ1LNTpGDPALRpsFyxqTPmTa+ZiSX+T
rx1waRU+TF6bASx/I4N7iJGsN7FLru1w45RQ4ygjQiR/bnibS67NAvJS3G1/mzblWA8A05NuBoowUAAA==" | gunzip
#                                        *** FIN ***
