# API 관련 에러
class ApiError(Exception):
    """Base class for API-related errors."""
    pass

class ServiceKeyError(ApiError):
    """Raised when the API service key is invalid or missing."""
    pass

class ApiConnectError(ApiError):
    """Raised when HTTP response code is not 200."""
    def __init__(self, status_code):
        super().__init__(f"API 연결 실패: HTTP 상태 코드 {status_code}")

class ApiResponseError(ApiError):
    """Raised when API response contains logical errors (e.g. no data, result_Code != '00')."""
    def __init__(self, code, msg):
        super().__init__(f"API 응답 오류: 코드 {code}, 메시지 '{msg}'")

# 데이터 파싱 관련 에러
class DataParsingError(Exception):
    """Raised when data parsing fails due to unexpected structure or missing fields."""
    pass

# DB 관련 에러
class DatabaseError(Exception):
    """Base class for database-related errors."""
    pass

class InsertError(DatabaseError):
    """Raised when insertion into the database fails due to data integrity or other issues."""
    def __init__(self, msg="데이터 삽입 오류"):
        super().__init__(msg)
