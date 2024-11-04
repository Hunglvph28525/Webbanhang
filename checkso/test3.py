import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Đường dẫn đến chromedriver
chrome_driver_path = r'C:\Users\Admin\Music\test1\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Mở Chrome
driver.get('https://web.whatsapp.com/')  # Mở WhatsApp Web

# Chờ quét mã QR
time.sleep(30)

whatsapp = []

# Hàm cập nhật file để xóa ID đã kiểm tra
def update_file_after_check(filename, checked_id):
    with open(filename, 'r') as file:
        ids = file.readlines()
    # Ghi lại danh sách ID ngoại trừ ID đã kiểm tra
    with open(filename, 'w') as file:
        for id in ids:
            if id.strip() != checked_id:
                file.write(id)

# Đọc danh sách ID từ file .txt
with open('SDT3.txt', 'r') as file:
    ids = [line.strip() for line in file.readlines()]

# Duyệt qua từng ID
for id in ids:
    url = f'http://web.whatsapp.com/send/?phone=%2B{id}'
    driver.get(url)
    try:
        # Chờ trang tải xong
        time.sleep(8)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))  # Chờ đến khi phần thân trang tải xong
        )
         
        # Trường hợp 1: Số điện thoại không hợp lệ
        try:
            error_message = driver.find_element(By.CSS_SELECTOR, 'div.x12lqup9.x1o1kx08')
            if "Số điện thoại được chia sẻ qua URL không hợp lệ." in error_message.text:
                print(f'ID {id} gặp trường hợp 1: Số điện thoại không hợp lệ. Chuyển sang ID tiếp theo.')
                update_file_after_check('SDT3.txt', id)  # Xóa ID đã kiểm tra
                continue  # Nhảy sang ID tiếp theo
        except NoSuchElementException:
            # Không có thông báo lỗi, tiếp tục kiểm tra
            pass

        # Trường hợp 2: Tìm thấy "Sử dụng WhatsApp trên máy tính của bạn"
        try:
            use_on_pc_div = driver.find_element(By.XPATH, '//div[contains(text(),"Sử dụng WhatsApp trên máy tính của bạn") and contains(@class, "x1q74xe4")]')
            if use_on_pc_div.is_displayed():
                print(f'ID {id} gặp trường hợp 2: Sử dụng WhatsApp trên máy tính của bạn. Đã lưu vào file.')
                update_file_after_check('SDT3.txt', id)  # Xóa ID đã kiểm tra
                break
        except NoSuchElementException:
            # Không tìm thấy div, tiếp tục kiểm tra
            pass

        # Trường hợp 3: Số điện thoại không đăng ký WhatsApp hoặc có thể gửi tin nhắn
        try:
            message_box = driver.find_element(By.XPATH, '//div[@aria-placeholder="Soạn tin nhắn" and @contenteditable="true" and contains(@class, "x1hx0egp")]')
            if message_box.is_displayed():
                # Lưu ID vào file
                with open('SDTLOC3.txt', 'a') as output_file:
                    output_file.write(f"{id}\n")
                    print(f'ID {id} gặp trường hợp 3: Tin nhắn có thể được soạn thảo. Đã lưu vào file.')
                update_file_after_check('SDT3.txt', id)  # Xóa ID đã kiểm tra
        except NoSuchElementException:
            # Không tìm thấy div, tiếp tục kiểm tra
            pass

    except TimeoutException:
        print(f'Timeout khi tải ID {id}.')

# Đóng trình duyệt
driver.quit()
