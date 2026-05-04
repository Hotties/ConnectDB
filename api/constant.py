import os
from dotenv import load_dotenv

# .env 파일이 없어도 에러는 안 나지만, False를 반환함
if not load_dotenv():
    # 파일이 없으면 경고를 띄우거나 바로 종료할 수도 있음
    print("Warning: .env file not found. Using system environment variables.")

# print(f"파일 존재 여부: {os.path.exists('.env')}")
# print(f"로딩 성공: {load_dotenv()}")
# print(f"가져온 URL: {os.getenv('KOREAN_ALCOHOL_API_URL')}")
# print(f"가져온 API 키: {os.getenv('KOREAN_ALCOHOL_API_KEY')}")

class _constant:
    def __setattr__(self, name, value):
        # 값이 None이면 할당 자체를 막거나 에러 발생
        if value is None:
            raise ValueError(f"환경 변수 '{name}'를 찾을 수 없습니다. .env 파일을 확인하세요.")
        if name in self.__dict__:
            raise Exception('Cannot allocate values in variable.')
        self.__dict__[name] = value

_constants = _constant()


_constants.url = os.getenv("KOREAN_ALCOHOL_API_URL")
_constants.serviceKey = os.getenv("KOREAN_ALCOHOL_API_KEY")