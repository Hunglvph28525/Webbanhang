import re
import time
import pickle  # Thư viện để lưu và nạp cookie
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Khởi tạo trình duyệt
chrome_driver_path = r'C:\Users\Admin\Music\Test2\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Đường dẫn file cookie
cookie_file_path = "facebook_cookies.pkl"







# Hàm kiểm tra và nạp cookie
def load_cookies(driver, cookie_file_path):
    # Kiểm tra nếu file cookie tồn tại và không rỗng
    if os.path.exists(cookie_file_path) and os.path.getsize(cookie_file_path) > 0:
        try:
            with open(cookie_file_path, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
                print("Đã nạp cookie thành công.")
                return True
        except EOFError:
            print("File cookie bị lỗi. Xóa file để tạo lại.")
            os.remove(cookie_file_path)
    else:
        print("Không tìm thấy file cookie hoặc file rỗng. Thực hiện đăng nhập thủ công.")
    return False

# Truy cập trang Facebook
driver.get("https://www.facebook.com/")

# Kiểm tra nếu có cookie thì nạp cookie và làm mới trang
cookies_loaded = load_cookies(driver, cookie_file_path)
driver.refresh()  # Làm mới trang để áp dụng cookie nếu có

# Kiểm tra xem người dùng đã đăng nhập thành công chưa
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search Facebook"]'))
    )
    print("Đã đăng nhập thành công bằng cookie.")
except:
    if not cookies_loaded:
        print("Không có cookie hợp lệ. Yêu cầu đăng nhập thủ công.")
    
    # Đợi người dùng đăng nhập thủ công và kiểm tra lại trạng thái đăng nhập
    WebDriverWait(driver, 3000).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search Facebook"]'))
    )
    print("Đã đăng nhập thủ công thành công.")
    
    # Lưu cookie sau khi đăng nhập thành công
    with open(cookie_file_path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("Đã lưu cookie thành công.")

# Sau khi xác nhận đã đăng nhập, điều hướng đến Marketplace
driver.get("https://www.facebook.com/marketplace/taichung/search/?query=櫃子%20二手")

# Thiết lập thời gian và giới hạn số lần cuộn
SCROLL_PAUSE_TIME = 2  # Thời gian chờ cho trang tải thêm nội dung
MAX_SCROLLS = 500  # Giới hạn số lần cuộn, có thể điều chỉnh

# Đọc các ID đã có trong file "ID1.txt" vào một tập hợp để tránh trùng lặp
try:
    with open("ID1.txt", "r") as file:
        saved_ids = {line.strip() for line in file}
except FileNotFoundError:
    # Nếu file không tồn tại, tạo một tập hợp trống
    saved_ids = set()

# Mở file ở chế độ "append" để ghi các ID mới
with open("ID1.txt", "a") as file:
    # Hàm cuộn trang và lấy ID
    for i in range(MAX_SCROLLS):
        try:
            # Tìm các div chứa link với href cần lấy
            div_elements = driver.find_elements(By.CSS_SELECTOR, "div.x9f619.x78zum5.x1r8uery.xdt5ytf.x1iyjqo2.xs83m0k.x1e558r4.x150jy0e.x1iorvi4.xjkvuk6.xnpuxes.x291uyu.x1uepa24")
            for div in div_elements:
                a_tags = div.find_elements(By.TAG_NAME, "a")
                for a in a_tags:
                    href = a.get_attribute("href")
                    if href:  # Kiểm tra nếu href không rỗng
                        # Sử dụng biểu thức chính quy để lấy ID từ URL
                        match = re.search(r'item/(\d+)', href)
                        if match:
                            item_id = match.group(1)
                            if item_id not in saved_ids:  # Kiểm tra ID đã tồn tại chưa
                                # Ghi ID vào tệp và thêm vào tập hợp
                                file.write(item_id + "\n")
                                saved_ids.add(item_id)
                                print("ID đã lưu:", item_id)  # In ra để theo dõi tiến trình

        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")

        # Cuộn trang xuống cuối để tải thêm nội dung
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Đợi cho trang tải thêm nội dung
        time.sleep(SCROLL_PAUSE_TIME)

# Đóng trình duyệt sau khi hoàn tất
driver.quit()
