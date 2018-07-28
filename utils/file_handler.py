#!/usr/bin/vai-agi-python-path
import os
import requests
import subprocess
from utils.log import __console
from constants.constants import MP3, GSM

__base_path = '/var/lib/asterisk/sounds'
__base_url  = 'https://s3.ap-south-1.amazonaws.com/hermes-responses/'

'icici_demo/common/dtmf_call_language.mp3'


def split_file_extension(path):
    """
    default second element of the tuple is .mp3
    :param path: str
    :return: (str, str)
    """
    return (path[:-4], path[-4:]) if '.' == path[-4] else (path, '.mp3')


def download_if_absent(url, path):
    file_data = requests.get(url)
    # Assume the file to be of type .mp3 if there is no extension
    # provided.
    file_name, ext = split_file_extension(path)
    save_path = file_name + ext
    if os.path.exists(__base_path + '/' + save_path):
        return file_name
    with open(__base_path + '/' + save_path, 'wb+') as f:
        f.write(file_data.content)
    transform_sound_file(__base_path + '/'+ file_name, MP3, GSM)
    return file_name


def transform_sound_file(file_name, from_format, to_format):
    intermediate_format = '.flac'
    __console.log('start conversion', file_name, from_format, '-->', intermediate_format)
    # PATCH: convert to .flac as intermediate
    # as sox has support for .flac -> .gsm
    subprocess.call(['ffmpeg', '-i', file_name + from_format, file_name + intermediate_format])

    __console.log('start conversion', file_name, intermediate_format,' --> .gsm')
    subprocess.call([
        'sox', file_name + intermediate_format, '-r', '8000', '-c1', file_name + to_format
    ])
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
