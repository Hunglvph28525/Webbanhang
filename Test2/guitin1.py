from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time


# Đọc danh sách ID từ file IDdaloc.txt
with open("IDdaloc1.txt", "r") as file:
    id_list = [line.strip() for line in file]
print("đọc file ID thành công")
# Đọc nội dung tin nhắn từ file conten.txt
iddagui = 0
idguiloi = 0

with open("conten.txt", "r", encoding="utf-8") as file:
    content = file.read()
print("đọc file Conten thành công")
# Khởi động trình duyệt
chrome_driver_path = r'C:\Users\Admin\Music\Test2\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Truy cập và đăng nhập Facebook
print("đăng nhập facebook ")
driver.get("https://www.facebook.com/")
WebDriverWait(driver, 3000).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search Facebook"]'))
)
print("đăng nhập facebook thành công")
# Lặp qua từng ID trong danh sách
for id in id_list[:]:  # Sao chép danh sách để không ảnh hưởng khi xóa phần tử
    url = f"https://www.facebook.com/marketplace/item/{id}"
    driver.get(url)
    print(f'Spam ID : {id}')
    try:
        # Chờ nút "Nhắn tin" xuất hiện và nhấn vào
        message_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Message"]'))
        )
        print("bấm vào nhắn tin")
        message_button.click()

        # Chờ textarea để nhập nội dung xuất hiện
        print("nhập conten tin nhắn ")
        textarea = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@id, ':r')]"))
        )

        # Dán nội dung vào textarea
        textarea.clear()  # Xóa nội dung cũ nếu có
        textarea.send_keys(content)  # Sử dụng send_keys để nhập nội dung

        # Trigger sự kiện input nếu cần thiết
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", textarea)

        # Chờ nút "Gửi tin nhắn" xuất hiện và nhấn vào
        print("gửi tin nhắn đi")
        send_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Send message"]'))
        )
        send_button.click()
        iddagui = iddagui + 1
        print(f"tổng id đã gửi : {iddagui}\ntổng id gửi lỗi : {idguiloi}")
        time.sleep(4)  # Thêm thời gian chờ trước khi chuyển đến ID tiếp theo

        # Xóa ID đã xử lý khỏi danh sách và ghi đè tệp
        id_list.remove(id)
        with open("IDdaloc1.txt", "w") as file:
            for remaining_id in id_list:
                file.write(remaining_id + "\n")
        print(f"xong xoá ID : {id}")

    except Exception as e:
        print(f"Lỗi xảy ra khi thao tác với ID {id}")
        id_list.remove(id)
        with open("IDdaloc1.txt", "w") as file:
            for remaining_id in id_list:
                file.write(remaining_id + "\n")
        print(f"gặp lỗi xoá ID Lỗi {id}")
        idguiloi = idguiloi + 1
        

# Đóng trình duyệt sau khi hoàn thành
driver.quit()
