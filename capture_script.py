import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_capture():
    # 1. 저장할 폴더 만들기
    os.makedirs("screenshots", exist_ok=True)
    
    # 2. 브라우저 옵션 (서버용)
    opts = Options()
    opts.add_argument("--headless=new") # 화면 없이 실행
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")

    # 3. 드라이버 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    
    try:
        print("페이지 접속 중...")
        driver.get("https://www.dailypharm.com") # 대상 주소
        time.sleep(10) # 페이지가 완전히 로딩될 때까지 대기
        
        # --- 전체 스크롤 길이를 계산하여 창 크기 조절 ---
        # 1. 자바스크립트로 문서 전체의 높이를 가져옵니다.
        total_height = driver.execute_script("return document.body.scrollHeight")
        
        # 2. 브라우저 창의 너비는 1920, 높이는 전체 높이(total_height)로 재설정합니다.
        driver.set_window_size(1920, total_height)
        time.sleep(1) # 크기 변경 후 잠시 대기
        
        # 3. 파일 저장
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/dailypharm_full_{timestamp}.png"
        
        # 이제 창 크기 자체가 길어졌으므로 전체가 찍힙니다.
        driver.save_screenshot(filename)
        print(f"전체 페이지 저장 완료: {filename} (높이: {total_height}px)")
        
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_capture()
