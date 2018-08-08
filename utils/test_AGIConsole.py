from unittest import TestCase
from agi_logger import AGIConsole


logging_meta_data = {
    'host_url'          : 'url',
    'session_id'        : '1234',
    'client_id'         : '1234',
    'access_token'      : 'b4d455',
    'virtual_number'    : 'test',
    'caller_id'         : 'test',
    'dtmf'              : 'NA',
    'env'               : 'NA'
}



class TestAGIConsole(TestCase):
    def test_console_log(self):
        __console = AGIConsole(debug_mode=True, meta_data=logging_meta_data)
        __console.log('message', **{
            'url': 'http://url.com',
            'headers': '{content-type: "application/json"}',
            'response_text': '{}',
            'response_status_code': '200'
        })
        self.fail()
