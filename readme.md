# 우리술 성분 정보 수집기 (Public Data Collector)

이 프로젝트는 **공공데이터포털**에서 제공하는  
**농촌진흥청 국립식량과학원 - 농식품 우리술 성분 정보 API**를 활용하여  
API 데이터를 수집하고, **MariaDB**에 저장하는 Python 기반 프로그램입니다.

---

## 📁 프로젝트 구조

connectapi/
├── maria.py                  # 메인 실행 파일
├── error.py
├── requirements.txt
├── .env                      # 환경 변수 파일 (API 키 등)
├── response{0-5}.json        # 샘플 응답 데이터
├── api/
│   ├── connect_api.py
│   ├── constant.py
│   └── file_writer.py
├── db/
│   ├── Connect_Db.py
│   ├── Create_Table.py
│   └── Insert_Data.py
├── parser/
│   ├── make_class.py
│   └── parsing_Data.py

---

## 🚀 실행 방법

1. **프로젝트 클론 또는 다운로드**


git clone https://github.com/your-repo/connectapi.git
cd connectapi

2. **가상환경 설정(Optional)**

python -m venv venv
source venv/bin/activate  # 윈도우는 venv\Scripts\activate

3. 필수 패키지 설치
pip install -r requirements.txt

4. .env 파일 설정
### Database info
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
DB_CHARSET=utf8

### API info
KOREAN_ALCOHOL_API_URL
KOREAN_ALCOHOL_API_KEY

5. 실행
python maria.py

## 주요 기능
* 공공데이터 API 요청 및 응답 수신

* JSON 파일로 백업 (response*.json)

* 응답 파싱 및 Python 객체로 변환

* MariaDB에 테이블 생성 및 데이터 삽입

## 사용 기술

* 언어: Python 3

* DB: MariaDB

* 라이브러리: requests, python-dotenv, pymysql 등