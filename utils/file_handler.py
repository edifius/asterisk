import os
import requests
import sox
from utils.log import __console
from constants.constants import MP3, GSM

__base_path = '/var/lib/asterisk/sounds'
__base_url  = 'https://s3.ap-south-1.amazonaws.com/hermes-responses/'

'icici_demo/common/dtmf_call_language.mp3'


def download_if_absent(url, path):
    file_data = requests.get(url)
    file_name, ext = path.split('.')

    if os.path.exists(__base_path + '/' + path):
        return file_name

    with open(__base_path + '/' + path, 'wb+') as f:
        f.write(file_data.content)
        transform_sound_file(__base_path + '/'+ file_name, MP3, GSM)
    return file_name


def transform_sound_file(file_name, from_format, to_format):
    __console.log('start conversion --> gsm')
    tfm = sox.Transformer()
    tfm.build(file_name + from_format, file_name + to_format)
    __console.log('conversion ends')


def strip_base_url(url):
    return url.replace(__base_url, '')


def make_nested_directories(directories):
    dir_path = __base_path
    for directory in directories:
        dir_path += '/' + directory
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)


def download(url):
    file_path           = strip_base_url(url)
    directory_structure = file_path.split('/')
    directories         = directory_structure[:-1]
    make_nested_directories(directories)
    return download_if_absent(url, file_path)

__console.log('loaded ', __name__)
