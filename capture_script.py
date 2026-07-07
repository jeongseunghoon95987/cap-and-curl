import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def log_time(label, start):
    now = time.time()
    print(f"[TIME] {label}: {round(now - start, 2)} sec")
    return now

def run_capture():
    total_start = time.time()

    os.makedirs("screenshots", exist_ok=True)
    
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")

    t = log_time("Init options", total_start)

    driver = webdriver.Chrome(options=opts)
    t = log_time("Chrome 실행", t)
    
    try:
        print("페이지 접속 중...")
        driver.get(os.environ.get("TARGET_URL"))
        print(f"TARGET_URL = {os.environ.get("TARGET_URL")}")
        t = log_time("페이지 요청(driver.get)", t)

        time.sleep(5)
        t = log_time("초기 대기(sleep 5)", t)
        
        total_height = driver.execute_script("return document.body.scrollHeight")
        t = log_time("페이지 높이 계산", t)

        driver.set_window_size(1920, total_height)
        t = log_time("윈도우 사이즈 변경", t)

        time.sleep(1)
        t = log_time("렌더링 대기(sleep 1)", t)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/full_{timestamp}.png"

        driver.save_screenshot(filename)
        t = log_time("스크린샷 저장", t)

        print(f"저장 완료: {filename}")

        upload_url = os.environ.get("UPLOAD_URL")
        with open(filename, "rb") as f:
            files = {
                "file": (os.path.basename(filename), f, "image/png")
            }

            print("업로드 중...")
            res = requests.post(upload_url, files=files, timeout=30)

            t = log_time("업로드 요청", t)

            print("응답코드:", res.status_code)
            print("응답내용:", res.text)

            if res.status_code != 200:
                raise Exception("업로드 실패")

        os.remove(filename)
        t = log_time("로컬 파일 삭제", t)

        print("로컬 파일 삭제 완료")

    except Exception as e:
        print(f"오류 발생: {e}")
        raise e

    finally:
        driver.quit()
        log_time("전체 실행 시간", total_start)

if __name__ == "__main__":
    run_capture()
