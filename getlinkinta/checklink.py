import re
import time
import pickle  # Thư viện để lưu và nạp cookie
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Đọc danh sách ID từ file UID.txt
with open("UID.txt", "r") as file:
    id_list = [line.strip() for line in file]
    if not id_list:
        print("hết UID")
    else:
        print("Đọc file ID thành công")
        pass


chrome_driver_path = r'C:\Users\Admin\Music\Test2\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Đường dẫn file cookie
cookie_file_path = "facebook_cookies.pkl"
output_file_path = "instagram_links.txt"  # File để lưu các đường dẫn Instagram

# Hàm kiểm tra và nạp cookie
def load_cookies(driver, cookie_file_path):
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
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search Facebook"]'))
    )
    print("Đã đăng nhập thủ công thành công.")
    
    # Lưu cookie sau khi đăng nhập thành công
    with open(cookie_file_path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("Đã lưu cookie thành công.")

# Mở file để lưu các đường dẫn Instagram
with open(output_file_path, "w") as output_file:
    # Sau khi xác nhận đã đăng nhập, điều hướng đến từng ID
    for id in id_list[:]:  # Sao chép danh sách để không ảnh hưởng khi xóa phần tử
        url = f"https://www.facebook.com/profile.php?id={id}"
        driver.get(url)
        print(f'Check ID: {id}')
        try:
            # Chờ cho trang tải hoàn toàn
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))  # Ví dụ: chờ cho tiêu đề của trang tải
            )
            
            unavailable_message = driver.find_elements(By.XPATH, "//span[contains(text(), \"This content isn't available right now\")]")
            if unavailable_message:
                print(f"Nội dung không khả dụng cho ID {id}. Đang xóa ID...")
                id_list.remove(id)
                with open("UID.txt", "w") as file:
                    for remaining_id in id_list:
                        file.write(remaining_id + "\n")
                continue  # Tiếp tục vòng lặp mà không kiểm tra thêm
            
            # Tìm tất cả các thẻ <a> chứa 'instagram.com'
            links = driver.find_elements(By.TAG_NAME, 'a')
            instagram_links = []

            for link in links:
                href = link.get_attribute('href')
                if href and 'instagram.com' in href:
                    instagram_links.append(href)

            # In ra các liên kết Instagram tìm thấy
            if instagram_links:
                print(f"Các liên kết Instagram tìm thấy cho ID {id}:")
                for idx, link in enumerate(instagram_links):
                    print(f"{idx + 1}: {link}")
                    
                    # Truy cập vào từng liên kết Instagram và lấy URL cuối
                    driver.get(link)
                    time.sleep(3)  # Đợi một chút cho trang tải
                    final_url = driver.current_url
                    print(f"Đường dẫn cuối cho link Instagram {link}: {final_url}")

                    # Lưu đường dẫn vào file
                    output_file.write(final_url + "\n")
                
                # Xóa ID đã tìm thấy và lưu lại vào UID.txt
                id_list.remove(id)
                with open("UID.txt", "w") as file:
                    for remaining_id in id_list:
                        file.write(remaining_id + "\n")

            else:
                id_list.remove(id)
                with open("UID.txt", "w") as file:
                    for remaining_id in id_list:
                        file.write(remaining_id + "\n")
                print(f"Không tìm thấy liên kết Instagram nào cho ID {id}.")
                
        except Exception as e:
            id_list.remove(id)
            with open("UID.txt", "w") as file:
                for remaining_id in id_list:
                    file.write(remaining_id + "\n")
            print(f"Lỗi xảy ra khi thao tác với ID {id}")
            continue

print("xong ")
time.sleep(3)
# Đóng trình duyệt sau khi hoàn thành
driver.quit()
