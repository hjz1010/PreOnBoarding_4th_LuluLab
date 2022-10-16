# 프리온보딩 과제_4 룰루랩(LulaLab) - 병원 예약 시스템 구축
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=Poetry&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"/>&nbsp;

## 🏥 프로젝트 소개

원티드 프리온보딩 백엔드 코스 4차 과제 입니다.
  
Django와 MySQL를 이용하여 병원 예약 시스템을 구축했습니다.

▶️ [Project github Link](https://github.com/AhnSang0915/pre_onboarding_4th_lulu_lab)

- **개발 기간** : 2022.10.14(금) ~ 2022.10.16(일) (3Days)
  
- **개발 인원** : 백엔드 4명 (안상현, 음정민, 전은형, 홍현진)


## 🏥 데이터 모델링

▶️ [dbdiagram Link](https://dbdiagram.io/d/634921dff0018a1c5f030baa)
![image](https://user-images.githubusercontent.com/97498663/196033480-18bbc4aa-a7e3-40a9-abfe-c82236d8a9db.png)


## 🏥 프로젝트 실행 방법

- 사전에 Git, Poetry, MySQL이 설치되어있어야 합니다.
- 파이썬 버전 3.10이상이 필요합니다.

```shell
# 레포지토리 클론
$ git clone https://github.com/AhnSang0915/pre_onboarding_4th_lulu_lab.git

# 디렉토리 이동
$ cd pre_onboarding_4th_lulu_lab

# 패키지 설치
$ poetry install

# 데이터베이스 생성
mysql> create database 데이터베이스명 character set utf8mb4 collate utf8mb4_general_ci; 

# .env파일 만들기
SECRET_KEY = 'SECRET_KEY'
DB_USERNAME = 'DB유저이름'
DB_NAME = '데이터베이스명'
DB_PASSWORD = 'DB비밀번호'
DB_HOST = 'DB호스트주소'
DB_PORT = 'DB포트번호'

SMS_SERVICE_ID = '네이버 문자서비스 ID'
FROM_NUMBER = '문자 발신 번호'
ACCESS_KEY_ID = 'Access Key ID' (계정 엑세스 키)
NAVER_SECRET_KEY = 'Secret Key' (계정 시크릿 키)

# 데이터베이스 테이블 생성
$ poetry run python manage.py migrate

# 프로젝트 실행
$ poetry run python manage.py runserver

# server start : http://localhost:8000
```

## 🏥 적용 기술

- Back_End : Python, Django, Poetry, MySQL, Postman
- Colaboration: Slack, Zep
  

## 🏥 구현 기능 소개

- 예약 가능한 병원 목록 및 일시 확인하기(홍현진)
- 예약 등록하기(전은형)
- 이름/예약번호로 조회하기(안상현)
- 예약 변경하기(음정민)
- 예약내역 문자 발송(안상현)
  
### 안상현 (예약 목록 확인하기, 예약 정보 문자 발송하기)
---  
1. 예약 목록을 확인하는 API
    - GET 요청시 예약 정보를 안내합니다.
    - 예약자 이름 또는 예약 번호로 예약 정보를 조회할 수 있습니다.
    
2. 예약시 예약정보 문자 발송 API
    - NAVER CLOUD의 open API를 이용했습니다.
    - 예약 POST 요청시 예약정보가 저장되면 예약 정보를 문자로 안내하는 기능입니다.
    - 예약자, 예약일시, 예약번호를 안내해줍니다.
    
3. 고민했던 부분
    1. 모델링  
        예약 가능한 날짜와 시간을 조회하는 기능이 있어 날짜와 시간 테이블에 대해 고민했다. 처음 내 생각은 테이블에 미리 날짜와 시간을 만들어 놓고 boolean 값으로 기본값을 TRUE로 넣어놓고 예약시 Flase로 상태를 변경해 사용하려 생각했는데 팀원들과 회의 중 데이터가 너무 많고 쿼리를 불러오는 시간도 오래걸릴거 같아 시간 테이블만 생성했다.
    
    2. 예약 번호  
        처음 모델링할때 예약 번호를 Uuidfield를 사용해 자동으로 생성하려 했으나 실제 통신중 필요이상으로 길고 복잡했다. 진짜 예약 번호들을 찾아보고 간단하게 만드는게 좋다고 판단해 팀원들과 고민하여 예약번호를 직접 생성해 사용했다.
        
    3. SMS 예약 정보 전송  
        예약 번호로 예약 조회를 할 수 있는 기능이 있는데 실제 사용자들이 예약 번호를 기억하지 못할것 같았다. 응답 값으로 화면에 보여주긴 하지만 따로 저장하지 않고 문자로 예약정보를 전달하면 이후 예약조회를 할 일이 생기면 문자를 보고 간편하게 예약 조회를 할수 있을것 같아 문자메세지로 정보를 전달하게 구현했다.

### 음정민 (기능)

--- 

- 사용하신 개발언어
- 사용하신 프레임워크
- 사용하신 RDBMS
- 데이터 설계
- 그 밖에 고민하셨던 또는 설명하고 싶으신 부분 사전과제 제출은 메일 또는 github 등 소스저장소에 업로드하여 확인할 수 있는 경로를 공유해주시면 됩니다.

### 전은형 (예약 등록하기)

--- 
1. 예약 등록하는 API
    - POST 요청에 Body로 예약자명, 예약자 연락처, 환자명, 환자 생년월일, 병원, 날짜, 시간, 진료 타입을 받아온다.
    - 예약자명, 예약자 연락처, 환자명, 환자 생년월일, 날짜는 유효성 검사를 거친다.
    - 연락처 중복 여부 확인 후 중복이면 409 에러를 반환한다.
    - 병원, 시간, 진료 타입이 없는 값일 경우 404 에러를 반환한다.
    - 예약 날짜 확인 후 당일 예약은 불가하게끔 400 에러를 반환한다.
    - 예약자 + 환자 이름 + 환자 생년월일 + 병원 + 날짜 + 시간 전체 데이터가 일치하면 중복 예약으로 409 에러를 반환한다.
    - 위의 절차를 거쳐 예약에 성공하면 예약자의 이름과 예약번호를 결과값으로 반환한다.
    
2. 고민했던 부분
    1. 모델링    
        예약자의 이름과 연락처를 입력받아 Users 테이블에 저장한다. 이때 Users 테이블에는 블랙리스트 여부를 나타내는 컬럼이 있다. 예약자 데이터를 생성할 때 블랙리스트 컬럼의 값을 처음에는 False값이 들어가도록 하드코딩했었다. 팀원들과 상의 후 블랙리스트 컬럼에 기본값을 설정하기로 수정했고 해당 경험으로 앞으로는 기본값이나 null값까지 생각해서 모델링을 진행해야겠다고 느꼈다.
        
    2. get(), filter()  
        DB에 저장된 연락처와 입력받은 연락처가 동일할 경우 중복 에러를 일으키고 싶었다. 이름까지 동일한 경우에는 해당 예약자 객체로 예약을 생성해야하기 때문에 연락처만 중복여부를 확인해야했다. 해당 로직을 구현할 때 get()을 사용했었지만 해당 객체가 없는 경우 에러를 일으켜서 로직 작성이 불가했다. 그래서 결과값이 없는 경우 빈 값을 반환하는 filter()를 사용했고, 쿼리셋을 반환되기 때문에 리스트 컴프리헨션을 사용해 인덱싱으로 연락처 중복값을 처리했다.
    
    3. transaction  
        새로운 예약자일 경우 Users테이블에 저장한 뒤에 예약이 이뤄져야했다. 이를 한 큐에 처리하기 위해 transaction을 이용했고 두 작업을 하나로 묶을 수 있었다.

### 홍현진 (예약 가능한 병원 목록 반환하기, 예약 가능한 날짜와 시간 반환하기)

--- 
1. 예약 가능한 병원의 목록을 반환하는 API
    - GET 요청에 Query parameter로 필터링 조건을 받아온다.
    - 조건은 병원이 위치한 지역(province)와 병원의 진료과목(type) 두 가지로 설정.
    - 예약가능(is_available) 상태인 병원 중 조건에 해당하는 데이터를 DB에서 불러온다.
    - JSON 형태로 반환한다.
    
2. 예약 가능한 날짜와 시간을 반환하는 API
    - GET 요청에 Path parameter로 hosiptal_id를 받아온다.
    - 해당 병원의 예약 가능한 일시를 반환하기 위해
    - 예약이 오픈되는 날짜를 먼저 생성하고 (+1일~+7일로 설정)
    - 각 날짜의 모든 진료 시간에서 이미 예약이 되어있는 시간을 제외한다.
    
3. 고민했던 부분
    1. 모델링    
        예약가능 일시를 보여주는 방식에 대해 팀원들과 함께 고민하며 모델링 작업을 진행했다. 모든 날짜+시간을 DB에 먼저 생성하고 예약이 생기면 업데이트 하는 방식도 고려했으나, 불필요한 테이터들이 많이 생성된다고 판단되어 로직을 조금 복잡해지더라도 DB를 간결하게 하기로 결정했다.

    2. 리펙토링    
        오픈되어 있는 모든 일시 중 예약이 존재하는 일시를 제외한 예약가능 일시 목록을 생성하면서, 초반에 구현한 로직에는 반복문이 지나치게 사용되어 가독성과 효율성이 떨어진다고 생각했다. 하드코딩을 없애고, 반복문 대신 리스트에 중복되는 값을 제거하는 방법으로 최종 기능을 구현했다.
        
    3. datetime.now(), timezone.now(), timezone.localtime()    
        기존에 알고 있던 오늘 날짜를 반환하는 방법은 datetime.now()였다. 이번에 구현하는 프로젝트에서는 문제가 없지만, 확장성을 고려하여 timezone이 포함된 Aware 객체를 사용하는 코드로 수정하고 싶었다. 구글링을 하고 결과를 찍어보면서 timezone.now()와 localtime()을 거쳐 최종적으로는 시간값이 없는 timezone.localdate()을 사용하게 되었다.


## 🏥 API DOC
👉 [Postman API DOC](https://documenter.getpostman.com/view/22579998/2s8479zwn1)



## Reference

- 이 프로젝트는 원티드 프리온보딩에서 제공한 기업과제 입니다.
  
- 실무에 사용될 수 있는 프로젝트이기에 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
