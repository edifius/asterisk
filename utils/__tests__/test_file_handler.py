#!/usr/bin/vai-agi-python-path
from unittest import TestCase
from utils import file_handler


path_with_extension     = 'demo/common/file_name.mp3'
path_without_extension  = 'demo/common/file_name.mp3'
expected_result = ('demo/common/file_name', '.mp3')

class TestFileHandler(TestCase):
    def test_split_file_with_extension(self):
        test_result = file_handler.split_file_extension(path_with_extension)
        self.assertTupleEqual(test_result, expected_result)
