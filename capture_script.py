import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def run_capture():
    os.makedirs("screenshots", exist_ok=True)
    
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")

    # ✅ 변경된 부분 (webdriver-manager 제거)
    driver = webdriver.Chrome(options=opts)
    
    try:
        print("페이지 접속 중...")
        driver.get(os.environ.get("TARGET_URL"))
        time.sleep(5)
        
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, total_height)
        time.sleep(1)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/dailypharm_full_{timestamp}.png"
        driver.save_screenshot(filename)

        print(f"저장 완료: {filename}")

        # ✅ POST 전송
        upload_url = os.environ.get("UPLOAD_URL")
        with open(filename, "rb") as f:
            files = {
                "file": (os.path.basename(filename), f, "image/png")
            }

            print("업로드 중...")
            res = requests.post(upload_url, files=files, timeout=30)

            print("응답코드:", res.status_code)
            print("응답내용:", res.text)

            if res.status_code != 200:
                raise Exception("업로드 실패")

        # ✅ 성공 시 로컬 파일 삭제
        os.remove(filename)
        print("로컬 파일 삭제 완료")

    except Exception as e:
        print(f"오류 발생: {e}")
        raise e

    finally:
        driver.quit()

if __name__ == "__main__":
    run_capture()
