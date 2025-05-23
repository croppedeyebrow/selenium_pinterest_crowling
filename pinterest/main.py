from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import schedule
import time
import os
import random
import requests  # 추가
from datetime import datetime
from urllib.parse import urlparse, parse_qs  # URL 파싱을 위한 모듈 추가

def setup_driver():
    """웹 드라이버를 설정하고 반환하는 함수"""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')  # 샌드박스 모드 비활성화
        options.add_argument('--disable-dev-shm-usage')  # 공유 메모리 사용 비활성화
        options.add_argument('--disable-blink-features=AutomationControlled')  # 자동화 감지 비활성화
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 자동화 스위치 제외
        options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 비활성화
        
        service = Service(ChromeDriverManager().install())  # 드라이버 서비스 설정
        driver = webdriver.Chrome(service=service, options=options)  # 드라이버 인스턴스 생성
        
        return driver  # 드라이버 반환
    
    except Exception as e:
        print(f"드라이버 설정 중 오류 발생: {e}")  # 오류 발생 시 메시지 출력
        return None  # 드라이버가 설정되지 않으면 None 반환

def login(driver, username, password):
    """Pinterest에 로그인하는 함수"""
    driver.get("https://www.pinterest.com/login/")  # 로그인 페이지로 이동
    
    # 로그인 폼이 로드될 때까지 대기
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "id"))  # 사용자 이름 입력 필드 대기
    )
    
    # 사용자 이름과 비밀번호 입력
    driver.find_element(By.NAME, "id").send_keys(username)  # 사용자 이름 입력
    driver.find_element(By.NAME, "password").send_keys(password)  # 비밀번호 입력
    
    # 로그인 버튼 클릭
    driver.find_element(By.XPATH, "//button[@type='submit']").click()  # 로그인 버튼 클릭
    
    # 로그인 후 대기
    WebDriverWait(driver, 10).until(
        EC.url_changes("https://www.pinterest.com/login/")  # 로그인 후 URL 변경 대기
    )

def crawl_images(url, username, password):
    """지정된 URL에서 이미지 크롤링"""
    # 이미지 저장 폴더 생성
    img_folder = 'crowlingimg'
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
        
    driver = setup_driver()
    try:
        # 로그인 수행
        login(driver, username, password)  # 로그인 함수 호출
        
        # 로그인 후 잠시 대기
        time.sleep(8)  # 페이지 완전 로드를 위한 대기
        
        # 웹페이지 로드
        driver.get(url)  # 지정된 URL로 이동
        
        # URL에서 검색어 추출
        parsed_url = urlparse(url)  # URL 파싱
        query_params = parse_qs(parsed_url.query)  # 쿼리 매개변수 파싱
        
         # 'q' 매개변수에서 검색어 추출 (키가 'q'인지 확인)
        search_term = query_params.get('q', [''])[0] if 'q' in query_params else ''  # 'q' 매개변수에서 검색어 추출
        
        # 디버깅을 위한 출력
        print(f"추출된 검색어: {search_term}")  # 검색어 출력
        
        # 스크롤 다운을 통해 더 많은 이미지 로드
        for _ in range(15):  # 10번 스크롤
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 페이지 맨 아래로 스크롤
            time.sleep(5)  # 스크롤 후 로딩 대기
        
        # Pinterest의 실제 이미지 요소 선택자로 변경
        images = driver.find_elements(By.CSS_SELECTOR, "img[srcset]")  # 이미지 요소 선택
        image_data = []  # 이미지 데이터를 저장할 리스트
        
        # 각 이미지의 정보 추출
        for img in images:
            try:
                src = img.get_attribute('src')
                if src and not src.endswith('gif'):
                    # 이미지 파일명 생성 (검색어와 타임스탬프 포함)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    img_filename = f"{search_term}_{timestamp}_{len(image_data)}.jpg"
                    img_path = os.path.join(img_folder, img_filename)
                    
                    # 이미지 다운로드 및 저장
                    try:
                        response = requests.get(src)
                        if response.status_code == 200:
                            with open(img_path, 'wb') as f:
                                f.write(response.content)
                            
                            image_data.append({
                                'coordinate_img': src,
                                'image_filename': img_filename,
                                'crawled_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'search_term': search_term
                            })
                    except Exception as e:
                        print(f"이미지 다운로드 중 오류: {e}")
            except Exception as e:
                print(f"이미지 처리 중 오류 발생: {e}")
        
        return image_data
                
    finally:
        # 브라우저 자원 해제
        driver.quit()  # 드라이버 종료

def download_image(url, filename):
    """이미지를 다운로드하여 저장하는 함수"""
    try:
        response = requests.get(url)  # 이미지 URL에서 데이터 요청
        if response.status_code == 200:  # 요청이 성공적일 경우
            with open(filename, 'wb') as f:  # 파일 열기
                f.write(response.content)  # 이미지 데이터 저장
            print(f"이미지 저장 완료: {filename}")  # 저장 완료 메시지 출력
        else:
            print(f"이미지 다운로드 실패: {url}")  # 실패 메시지 출력
    except Exception as e:
        print(f"이미지 다운로드 중 오류 발생: {e}")  # 오류 발생 시 메시지 출력    
        

def save_to_csv(data, filename='pinterestcrowling.csv'):
    """크롤링한 데이터를 CSV 파일로 저장"""
    # 데이터프레임 생성
    df = pd.DataFrame(data)  # 데이터프레임으로 변환
    
    # CSV 파일 존재 여부 확인 및 처리
    try:
        if os.path.exists(filename):  # 문자열로 파일명 지정

            df.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8-sig')  # CSV 파일로 저장
            print(f"데이터가 {filename}에 추가되었습니다.")  # 추가 완료 메시지 출력
        
        else:
            # 파일이 없으면 새로 생성 (헤더 포함)
            df.to_csv(filename, index=False, encoding='utf-8-sig')  # CSV 파일로 저장
            print(f"새 파일 {filename}이 생성되었습니다.")  # 생성 완료 메시지 출력
    except Exception as e:
        print(f"CSV 파일 저장 중 오류 발생: {e}")  # 오류 발생 시 메시지 출력

def job(start_index=0):
    """크롤링 작업 실행"""
    # 크롤링할 URL 목록 설정
    urls = [
    #  미니멀
     
    #20대 -따뜻함 
    "https://kr.pinterest.com/search/pins/?q=minimal%20clothing%20for%20women%20in%20their%20early%2020s%20in%20the%20spring&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=minimal%20clothing%20for%20women%20in%20their%20mid%2020s%20in%20the%20spring&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=minimal%20clothing%20for%20women%20in%20their%20late%2020s%20in%20the%20spring&rs=typed",
    
     # 20대-더움움
    "https://kr.pinterest.com/search/pins/?q=minimal%20clothing%20for%20women%20in%20their%20early%2020s%20in%20the%20summer&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=minimal%20outfit%20for%20women%20in%20their%20mid%2020s%20in%20the%20summer&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=minimal%20outfit%20for%20women%20in%20their%20late%2020s%20in%20the%20summer&rs=typed",
    
    # 20대 - 시원함
    "https://kr.pinterest.com/search/pins/?q=minimal%20clothing%20for%20women%20in%20their%20early%2020s%20in%20the%20autumn&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=minimal%20clothing%20for%20women%20in%20their%20mid%2020s%20in%20the%20autumn&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=minimal%20clothing%20for%20women%20in%20their%20late%2020s%20in%20the%20autumn&rs=typed"
    
    #20대- 추움
    "https://kr.pinterest.com/search/pins/?q=minimal%20clothing%20for%20women%20in%20their%20early%2020s%20in%20the%20winter&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=minimal%20outfit%20for%20women%20in%20their%20mid%2020s%20in%20the%20winter&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=minimal%20outfit%20for%20women%20in%20their%20late%2020s%20in%20the%20winter&rs=typed"
    
    #20대 - 눈
    "https://kr.pinterest.com/search/pins/?q=Minimal%20outfits%20for%20women%20in%20their%20early%2020s%20on%20a%20snowy%20day&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=Minimal%20outfits%20for%20women%20in%20their%20mid%2020s%20on%20a%20snowy%20day&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=Minimal%20outfits%20for%20women%20in%20their%20late%2020s%20on%20a%20snowy%20day&rs=typed",
    
    #20대 - 비
    "https://kr.pinterest.com/search/pins/?q=Minimal%20outfits%20for%20women%20in%20their%20early%2020s%20on%20a%20rainy%20day&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=Minimal%20outfits%20for%20women%20in%20their%20mid%2020s%20on%20a%20rainy%20day&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=Minimal%20outfits%20for%20women%20in%20their%20late%2020s%20on%20a%20rainy%20day&rs=typed"
    
     #30대    

     #40대    
    
    #   모던
      #20대
    "https://kr.pinterest.com/search/pins/?q=modern%20outfit%20for%20women%20in%20their%20early%2020s&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=modern%20outfit%20for%20women%20in%20their%20mid%2020s&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=modern%20outfit%20for%20women%20in%20their%20late%2020s&rs=typed",
    
    #   캐주얼
     #20대
    "https://kr.pinterest.com/search/pins/?q=casual%20outfit%20for%20women%20in%20their%20early%2020s&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=casual%20outfit%20for%20women%20in%20their%20mid%2020s&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=casual%20outfit%20for%20women%20in%20their%20late%2020s&rs=typed",
    
    #   스트릿
     #20대
    "https://kr.pinterest.com/search/pins/?q=streetwear%20outfit%20for%20women%20in%20their%20early%2020s&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=streetwear%20outfit%20for%20women%20in%20their%20mid%2020s&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=streetwear%20outfit%20for%20women%20in%20their%20late%2020s&rs=typed",
    #   러블리
     #20대
    "https://kr.pinterest.com/search/pins/?q=cute%20outfit%20for%20women%20in%20their%20early%2020s&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=cute%20outfit%20for%20women%20in%20their%20mid%2020s&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=cute%20outfit%20for%20women%20in%20their%20late%2020s&rs=typed",
    
    #   럭셔리
       #20대
    "https://kr.pinterest.com/search/pins/?q=elegant%20outfit%20for%20women%20in%20their%20early%2020s&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=elegant%20outfit%20for%20women%20in%20their%20mid%2020s&rs=typed",
    "https://kr.pinterest.com/search/pins/?q=elegant%20outfit%20for%20women%20in%20their%20late%2020s&rs=typed"
    ]
    
    # 시작 인덱스부터 URL 목록 자르기
    urls = urls[start_index:]
    
    username = ""  # 실제 사용자 이름 입력
    password = ""  # 실제 비밀번호 입력
    print(f"크롤링 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")  # 크롤링 시작 시간 출력
    
    try:
        for url in urls:  # URL 목록을 순회
            print(f"크롤링 중: {url}")  # 현재 크롤링 중인 URL 출력
            # 이미지 크롤링 수행
            image_data = crawl_images(url, username, password)  # 이미지 크롤링 함수 호출
            if image_data:
                # 수집된 데이터가 있으면 CSV 파일로 저장
                save_to_csv(image_data)  # 데이터 저장 함수 호출
                print(f"총 {len(image_data)}개의 이미지 정보를 수집했습니다.")  # 수집된 이미지 수 출력
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")  # 크롤링 중 오류 발생 시 메시지 출력

def main():
    """메인 함수"""
    # 시작할 URL 인덱스 설정 (0부터 시작)
    start_index = 21  # 예: 6번째 URL부터 시작 (인덱스는 0부터 시작)
    
    # 프로그램 시작 시 최초 1회 실행 (지정된 인덱스부터)
    job(start_index)
    
    # 이후 실행은 처음부터 다시 시작
    schedule.every(30).minutes.do(job, start_index=0)
    
    # 스케줄러 무한 루프
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
