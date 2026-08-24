# 우리술 성분 정보 수집기

공공데이터포털의 **농촌진흥청 국립식량과학원 농식품 우리술 성분 정보 API**를 호출하고, 응답을 JSON으로 백업한 뒤 MariaDB에 저장하는 Python 프로그램입니다.

## 동작 흐름

`main.py`를 실행하면 다음 순서로 동작합니다.
1. MariaDB에 연결합니다. 설정한 데이터베이스가 없으면 자동으로 생성합니다.
2. `ITEM`, `CMPR_ITEM_LIST`, `CMPR_DTL_LIST` 테이블을 생성합니다.
3. 2014년의 주종 코드 `435001`부터 `435004`까지 API를 호출합니다.
4. API의 XML 응답을 Python 객체로 변환하고 `response0.json`, `response1.json`과 같은 파일로 저장합니다.
5. 다음 데이터를 데이터베이스에 삽입합니다.
	- `ITEM`: 주종 기본 정보
	- `CMPR_ITEM_LIST`: 비교 항목 정보
	- `CMPR_DTL_LIST`: 비교 항목의 상세 성분 정보
6. API 연결에 실패한 코드는 출력 후 다음 코드로 넘어갑니다.

## 프로젝트 구조

```text
ConnectDB/
├── main.py                    # 프로그램 시작점
├── error.py                   # API, 파싱, DB 예외 클래스
├── requirements.txt           # Python 의존성
├── readme.md
├── response0.json ...         # API 응답 백업 파일
├── api/
│   ├── Connect_Api.py         # API 호출 및 응답 검증
│   ├── Constant.py            # 환경 변수 로드
│   └── File_Writer.py         # JSON 파일 저장
├── db/
│   ├── Connect_Db.py          # MariaDB 연결 및 DB 생성
│   ├── Create_Table.py        # 테이블 생성
│   └── Insert_Data.py         # 데이터 삽입
└── parser/
	├── Make_Class.py          # 데이터 모델 클래스
	└── Parsing_Data.py        # JSON 파싱
```

## 실행 환경

- Python 3
- MariaDB 또는 MySQL
- API 서비스 키
- 데이터베이스 계정에 데이터베이스 생성 권한

## 설치

Windows PowerShell 기준입니다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 환경 변수 설정

프로젝트 루트에 `.env` 파일을 만들고 다음 값을 설정합니다.

```dotenv
KOREAN_ALCOHOL_API_URL=https://example.com/api-url
KOREAN_ALCOHOL_API_KEY=발급받은_API_서비스키

DB_HOST=localhost
DB_USER=사용자명
DB_PASSWORD=비밀번호
DB_NAME=데이터베이스명
DB_CHARSET=utf8mb4
```

현재 `db/Connect_Db.py`는 `DB_PORT`를 읽지 않으므로 별도 포트를 사용하려면 해당 코드의 연결 설정을 수정해야 합니다. `.env` 파일과 실제 API 키는 저장소에 커밋하지 마세요.

## 실행

```powershell
python main.py
```

실행 중 생성된 API 응답은 현재 작업 디렉터리에 `response0.json`부터 순서대로 저장됩니다. `parser/Parsing_Data.py`도 이 위치의 파일을 읽으므로, 다른 디렉터리에서 실행하지 않는 것이 안전합니다.

## 데이터베이스 스키마

### `ITEM`

- 기본키: `(measure_Year, achl_Kind_Code)`
- 주종명, 표본 수, 표본 비고를 저장합니다.

### `CMPR_ITEM_LIST`

- 기본키: `(cmpr_Item_Code, measure_Year, achl_Kind_Code)`
- `ITEM`의 `(measure_Year, achl_Kind_Code)`를 외래키로 참조합니다.


### `CMPR_DTL_LIST`

- 기본키: `(cmpr_Dtl_Code, cmpr_Item_Code, measure_Year, achl_Kind_Code)`
- 비교 항목의 상세 성분과 측정값을 저장합니다.

테이블 생성은 `CREATE TABLE IF NOT EXISTS`로 수행되므로, 이미 존재하는 테이블의 제약조건은 코드가 바뀌어도 자동으로 변경되지 않습니다. 실제 DB 구조는 다음 명령으로 확인할 수 있습니다.

```sql
SHOW CREATE TABLE CMPR_ITEM_LIST;
SHOW CREATE TABLE CMPR_DTL_LIST;
```

## 중복 저장 및 삽입 주의사항

삽입 함수는 모두 `INSERT IGNORE`를 사용합니다. 기본키, UNIQUE 제약, 외래키 등의 충돌이 발생하면 오류를 표시하지 않고 해당 행을 건너뜁니다. 이때 반환되는 `rowcount`가 `0`이면 새 행이 삽입되지 않은 것입니다.

따라서 데이터가 누락된 것처럼 보이면 다음을 확인하세요.

1. `CMPR_ITEM_LIST`의 `UNIQUE (cmpr_Item_Code, measure_Year)` 제약
2. 이미 실행된 이전 데이터와 동일한 기본키
3. `ITEM`이 먼저 삽입되었는지 여부
4. 실제 DB 테이블이 최신 코드의 스키마인지 여부

## 응답 파싱 형식

파서는 다음 구조의 API 응답을 기대합니다.

```text
response.body.items.item
└── cmpr_Item_List.item
	└── cmpr_Dtl_List.item
```

현재 파서는 비교 항목과 상세 항목이 목록 형태로 제공되는 응답을 기준으로 작성되어 있습니다. API가 목록 대신 단일 객체를 반환하는 경우 파싱 오류가 발생할 수 있습니다.

## 의존성

주요 패키지는 다음과 같습니다.

- `requests`: API HTTP 요청
- `xmltodict`: XML 응답 변환
- `PyMySQL`: MariaDB/MySQL 연결
- `python-dotenv`: `.env` 환경 변수 로드

전체 고정 버전은 `requirements.txt`에서 확인할 수 있습니다.

## 현재 구현상의 참고사항

- API 요청에 timeout이 설정되어 있지 않아 네트워크 응답이 지연되면 프로그램이 오래 대기할 수 있습니다.
- API 응답은 API 내부 오류 검증 전에 JSON 파일로 저장될 수 있습니다.
- DB 삽입이나 파싱 오류는 현재 전체 실행을 중단시킬 수 있습니다.
