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
        driver.get("https://www.google.com") # 캡처하고 싶은 주소로 변경
        time.sleep(5) 
        
        # 4. 파일 저장
        filename = f"screenshots/capture_{int(time.time())}.png"
        driver.save_screenshot(filename)
        print(f"저장 완료: {filename}")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_capture()
