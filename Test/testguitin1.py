import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Đường dẫn đến chromedriver
chrome_driver_path = r'C:\Users\Admin\Music\test\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)


# Mở Chrome
driver.get('https://web.whatsapp.com/')  # Mở một trang bất kỳ

# Chờ 1 phút
time.sleep(60)

with open('conten.txt', 'r', encoding='utf-8') as file:
    conten = file.read()
# Đọc danh sách ID từ file .txt
with open('SDT2.txt', 'r') as file:
    ids = [line.strip() for line in file.readlines()]

# Lưu thời gian bắt đầu
start_time = datetime.now()
timeout_duration = timedelta(minutes=300)

# Duyệt qua từng ID
for id in ids:
    url = f'http://web.whatsapp.com/send/?phone=%2B{id}'
    driver.get(url)
    time.sleep(10)
    # Kiểm tra thời gian đã trôi qua
    if datetime.now() - start_time > timeout_duration:
        print("Timeout: Không tìm thấy cả trường hợp 1 và 2 trong 3 phút.")
        break

    try:
        # Chờ trang tải xong
        WebDriverWait(driver, 10).until(
        
            EC.presence_of_element_located((By.TAG_NAME, 'body'))  # Chờ đến khi phần thân trang tải xong
        )
        
        # Kiểm tra xem có thông báo lỗi không
        try:
            error_message = driver.find_element(By.CSS_SELECTOR, 'div.x12lqup9.x1o1kx08')
            if "Số điện thoại được chia sẻ qua URL không hợp lệ." in error_message.text:
                print(f'ID {id} gặp trường hợp 1: Số điện thoại không hợp lệ. Chuyển sang ID tiếp theo.')
                continue  # Nhảy sang ID tiếp theo
        except NoSuchElementException:
            # Không có thông báo lỗi, tiếp tục kiểm tra
            pass

        # Kiểm tra trường hợp 2
        try:
            input_box = driver.find_element(By.XPATH, '//div[@aria-placeholder="Soạn tin nhắn"]')
            if input_box.is_displayed():
                input_box.click()  # Nhấp vào input box để đưa con trỏ vào
                input_box.send_keys(conten)  # Dán nội dung vào input
                
                # Nhấp vào nút gửi
                send_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Gửi"]')
                send_button.click()  # Nhấp vào nút gửi
                print(f'ID {id} đã gửi nội dung.')
                time.sleep(3)
        except NoSuchElementException:
            print(f'ID {id} không gặp trường hợp 2.')

    except TimeoutException:
        print(f'Timeout khi tải ID {id}.')

# Đóng trình duyệt
driver.quit()
