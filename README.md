# 프리온보딩 과제_4 룰루랩(LulaLab) - 병원 예약 시스템 구축
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=Poetry&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"/>&nbsp;

## 🏥 프로젝트 소개

원티드 프리온보딩 백엔드 코스 4차 과제 입니다.
  
Django와 MySQL를 이용하여 병원 예약 시스템을 구축했습니다.
모델링 및 개발 초기 세팅부터 구현했으며, 백엔드 부분 데이터 통신 구현하였습니다.

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

- 공통인거 있으면
- 여기다가
- 적으면될듯?
- 근데 이미 위에 다 있는거같음
- 왜 파이썬장고마이에스큐ㅔㄹ썼는지 적어야하나?
  
### 안상현 (기능)
---  

- 사용하신 개발언어
- 사용하신 프레임워크
- 사용하신 RDBMS
- 데이터 설계
- 그 밖에 고민하셨던 또는 설명하고 싶으신 부분 사전과제 제출은 메일 또는 github 등 소스저장소에 업로드하여 확인할 수 있는 경로를 공유해주시면 됩니다.

### 음정민 (기능)

--- 

- 사용하신 개발언어
- 사용하신 프레임워크
- 사용하신 RDBMS
- 데이터 설계
- 그 밖에 고민하셨던 또는 설명하고 싶으신 부분 사전과제 제출은 메일 또는 github 등 소스저장소에 업로드하여 확인할 수 있는 경로를 공유해주시면 됩니다.

### 전은형 (기능)

--- 
- 사용하신 개발언어
- 사용하신 프레임워크
- 사용하신 RDBMS
- 데이터 설계
- 그 밖에 고민하셨던 또는 설명하고 싶으신 부분 사전과제 제출은 메일 또는 github 등 소스저장소에 업로드하여 확인할 수 있는 경로를 공유해주시면 됩니다.

### 홍현진 (기능)

--- 
- 사용하신 개발언어
- 사용하신 프레임워크
- 사용하신 RDBMS
- 데이터 설계
- 그 밖에 고민하셨던 또는 설명하고 싶으신 부분 사전과제 제출은 메일 또는 github 등 소스저장소에 업로드하여 확인할 수 있는 경로를 공유해주시면 됩니다.


## 🏥 API DOC
👉 [Postman API DOC](https://documenter.getpostman.com/view/22579998/2s8479zwn1)



## Reference

- 이 프로젝트는 원티드 프리온보딩에서 제공한 기업과제 입니다.
  
- 실무에 사용될 수 있는 프로젝트이기에 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
