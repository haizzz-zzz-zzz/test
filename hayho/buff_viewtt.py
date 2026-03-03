from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
from fake_useragent import UserAgent
import threading
import time, random, os

# === Nhập cấu hình từ người dùng ===
video_url = input("🔗 Nhập URL video TikTok cần tăng view: ").strip()

# Xác nhận và kiểm tra số lượng view
while True:
    try:
        total_views = int(input("📈 Nhập số lượng view cần tăng: "))
        if total_views > 0:
            break
        else:
            print("❗ Vui lòng nhập số lớn hơn 0.")
    except ValueError:
        print("❗ Số không hợp lệ, vui lòng nhập lại.")

# === Tham số cố định ===
max_threads = 5
watch_time = 10  # giây xem mỗi video
delay_between_runs = 1  # giây chờ giữa các view

# === Tải danh sách user-agent và proxy từ file ===
def load_lines_from_file(filename):
    if not os.path.exists(filename):
        print(f"[!] File {filename} không tồn tại.")
        return []
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

user_agents = load_lines_from_file("user_agents.txt")
proxies = load_lines_from_file("proxies.txt")

# === Biến đếm kết quả dùng Lock để tránh lỗi đa luồng ===
success_count = 0
fail_count = 0
counter_lock = threading.Lock()

# === Hàm cấu hình trình duyệt với proxy và user-agent ===
def setup_driver(proxy=None, user_agent=None):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")

    if user_agent:
        options.add_argument(f"user-agent={user_agent}")
    if proxy:
        if "@" in proxy:
            print(f"[!] Proxy có auth chưa được hỗ trợ: {proxy}")
        else:
            options.add_argument(f"--proxy-server=http://{proxy}")

    return webdriver.Chrome(options=options)

# === Hàm mô phỏng 1 lượt xem video ===
def simulate_view(view_id):
    global success_count, fail_count
    driver = None
    proxy = random.choice(proxies) if proxies else None
    user_agent = random.choice(user_agents) if user_agents else UserAgent().random

    print(f"[🔁] View #{view_id} - Proxy: {proxy}, UA: {user_agent[:40]}...")

    try:
        driver = setup_driver(proxy, user_agent)
        driver.set_page_load_timeout(20)
        driver.get(video_url)

        try:
            # Chờ cho video tải xong
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
        except:
            print(f"[!] View #{view_id} không tìm thấy phần tử video.")

        time.sleep(watch_time)

        with counter_lock:
            success_count += 1
        print(f"[✓] View #{view_id} thành công.")
    except Exception as e:
        with counter_lock:
            fail_count += 1
        print(f"[✗] View #{view_id} thất bại: {e}")
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        time.sleep(delay_between_runs)

# === Hàm chạy đa luồng các lượt xem ===
def run_multi_views():
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(simulate_view, i + 1) for i in range(total_views)]
        for future in as_completed(futures):
            pass

# === Main ===
if __name__ == "__main__":
    print(f"\n🚀 Bắt đầu tăng {total_views} view với {max_threads} luồng...")
    run_multi_views()
    print(f"\n📊 Kết quả:")
    print(f"  ✅ Thành công: {success_count}")
    print(f"  ❌ Thất bại:   {fail_count}")
    print("🎉 Hoàn thành!")