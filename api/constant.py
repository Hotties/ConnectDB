import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로딩

class _constant:
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise Exception('Cannot allocate values in variable.')
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise Exception('Cannot delete variable')

_constants = _constant()
_constants.url = os.getenv("KOREAN_ALCOHOL_API_URL")
_constants.serviceKey = os.getenv("KOREAN_ALCOHOL_API_KEY")


import sys
sys.modules[__name__] = _constants
