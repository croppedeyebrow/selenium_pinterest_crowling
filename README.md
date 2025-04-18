# 사이드 프로젝트 데이터 수집용 크롤링 파이썬 레포

## 사용 기술

- Selenium
- schedule
- pandas_csv

### 주의사항

> **핀터레스트 로그인 정보는 본인의 정보로 입력해야 합니다.**  
> **크롤링 대상 키워드는 본인이 원하는 키워드로 입력해야 합니다. (영어 검색어)**

> **핀터레스트는 본질적으로 크롤링을 방지하는 기능을 가지고 있습니다.**  
> 따라서, 너무 짧은 주기는 피하고, 한번에 많이 불러온 후 주기를 넓히거나 다양한 아이디를 활용하시길 권장합니다.

---

### 파일 수집 내용

- `img_url`
- `img_filename`
- `search_term`
- `crawled_at`  
  (img_filename은 폴더에 따로 저장됩니다.)

### 파일 수집 목적{main.py}

- 패션 코디 이미지를 추출하여, 추후 전처리용 raw data로 활용합니다.

### 파일 수집 후 전처리{lookdata.py}

- 검색어에서 키워드를 추출하여, 키워드에 맞는 컬럼으로 재배치합니다.

## 프로젝트 진행 상황 및 오류 수정 정리

### 1. 초기 프로젝트 설정

- Selenium, Pandas, schedule을 사용한 Pinterest 이미지 크롤링 프로젝트 구축
- 크롤링된 이미지를 CSV 파일에 저장하는 기능 구현
- 이미지 파일을 로컬 폴더에 저장하는 기능 구현

### 2. 주요 오류 및 수정 사항

#### 2.1. URL 관련 오류

- **문제**: `"https" is not defined` 오류 발생
- **원인**: URL 문자열이 따옴표 없이 사용됨
- **해결**: URL을 문자열로 처리하도록 수정

#### 2.2. 변수 정의 오류

- **문제**: `"pinterestcrowling" is not defined` 오류 발생
- **원인**: 변수명이 문자열로 처리되지 않음
- **해결**: 변수명을 문자열로 처리하도록 수정

#### 2.3. 중복 이미지 처리

- **문제**: 동일한 이미지가 여러 번 저장되는 문제
- **해결**: `remove_duplicates` 함수를 `crawl_images` 함수 내에 추가하여 중복 제거

#### 2.4. 크롤링 결과 없음 문제

- **문제**: 로그인 후 검색 결과가 나타나지 않음
- **해결**:
  - 로그인 후 대기 시간 추가
  - 스크롤 다운 기능 구현하여 더 많은 이미지 로드

#### 2.5. 모듈 import 오류

- **문제**: `"requests" is not defined` 오류 발생
- **해결**: 파일 상단에 `requests` 모듈 import 추가

#### 2.6. 코드 구조 오류

- **문제**: `"driver" is not defined` 오류 발생
- **원인**: `finally` 블록의 들여쓰기 오류
- **해결**: `finally` 블록의 들여쓰기 수정

#### 2.7. 이미지 저장 방식 변경

- **문제**: 이미지를 Base64로 인코딩하여 CSV에 저장하는 방식의 비효율성
- **해결**:
  - `crowlingimg` 폴더 생성
  - 이미지를 파일로 저장하고 CSV에는 파일 경로만 저장

#### 2.8. URL 그룹화 및 스케줄링

- **문제**: 모든 URL을 한 번에 크롤링하는 방식의 비효율성
- **해결**:
  - URL을 5개씩 그룹화
  - 30분 간격으로 그룹 크롤링 실행
  - 특정 URL부터 시작할 수 있는 기능 추가

#### 2.9. CSV 파일 저장 방식 개선

- **문제**: 기존 CSV 파일과 새 데이터를 병합하는 방식의 비효율성
- **해결**:
  - `to_csv()` 함수에 `mode='a'` 옵션 사용
  - 기존 파일이 없을 경우에만 헤더 추가

#### 2.10. 카테고리 분류 오류

- **문제**: 모든 이미지가 'lovely' 카테고리로 분류됨
- **원인**: `if 'cute' or 'lovely' in search_term:` 구문의 논리 오류
- **해결**:
  - 조건문을 `if 'cute' in search_term or 'lovely' in search_term:` 형태로 수정
  - 각 스타일 카테고리에 대한 조건 검사 로직 개선

### 3. 현재 구현된 기능

- Pinterest 로그인 및 이미지 크롤링
- 이미지 파일 로컬 저장
- CSV 파일에 메타데이터 저장
- URL 그룹화 및 스케줄링
- 카테고리 분류 (TPO, 날씨, 선호도, 연령대)
- 중복 이미지 제거

### 4. 향후 개선 사항

- 크롤링 속도 및 안정성 향상
- 카테고리 분류 정확도 개선
- 에러 처리 및 로깅 강화
- 사용자 인터페이스 개선
