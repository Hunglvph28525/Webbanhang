import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyautogui
import threading

class FacebookAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Automation")
        self.is_running = False
        self.drivers = []
        self.lock = threading.Lock()  # Lock để đồng bộ truy cập ID
        self.processed_ids = set()    # Lưu trữ các ID đã xử lý để tránh trùng lặp
        self.success_count = 0
        self.error_count = 0
        self.create_widgets()

    def create_widgets(self):
        # Text widget để nhập cookie
        self.cookie_input = tk.Text(self.root, height=5, width=50)
        self.cookie_input.pack(padx=10, pady=10)

        # Treeview để hiển thị cookie và trạng thái
        self.tree = ttk.Treeview(self.root, columns=("ID", "Cookie", "Status"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cookie", text="Cookie")
        self.tree.heading("Status", text="Status")
        self.tree.pack(padx=10, pady=10)

        # Button thêm cookie
        self.add_cookie_button = tk.Button(self.root, text="Add Cookie", command=self.add_cookie)
        self.add_cookie_button.pack(pady=10)

        # Button bắt đầu automation
        self.start_button = tk.Button(self.root, text="Start Automation", command=self.start_automation)
        self.start_button.pack(pady=10)

        # Button dừng automation
        self.stop_button = tk.Button(self.root, text="Stop Automation", command=self.stop_automation, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Button xoá toàn bộ cookie
        self.clear_cookies_button = tk.Button(self.root, text="Clear Cookies", command=self.clear_cookies)
        self.clear_cookies_button.pack(pady=10)

    def add_cookie(self):
        cookie_text = self.cookie_input.get("1.0", "end-1c")
        if not cookie_text:
            messagebox.showwarning("Invalid Cookie", "Please add a valid cookie.")
            return

        # Hiển thị cookie trong Treeview
        cookie_id = len(self.tree.get_children()) + 1  # Tự động tăng ID
        self.tree.insert("", "end", values=(cookie_id, cookie_text.strip(), "Stopped"))
        
        # Xoá trường nhập cookie sau khi thêm
        self.cookie_input.delete("1.0", "end")

    def update_status(self, cookie_id, status):
    # Cập nhật trạng thái của dòng tương ứng trong Treeview
    # Đảm bảo rằng cookie_id được chuyển đổi thành chuỗi
        self.tree.item(cookie_id, values=(str(cookie_id), self.tree.item(cookie_id, "values")[1], status))


    def start_automation(self):
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        cookies_from_tree = []

        # Lấy tất cả cookie từ Treeview
        for item in self.tree.get_children():
            cookie = self.tree.item(item, "values")[1]
            cookies_from_tree.append((item, cookie))  # Lưu cả ID của Treeview

        if not cookies_from_tree:
            messagebox.showwarning("No Cookies", "Please add cookies before starting.")
            return

        # Đọc ID từ file
        with open("ID.txt", "r") as file:
            self.id_list = [line.strip() for line in file]  # Lưu vào self.id_list

        # Khởi động một thread cho mỗi cookie
        for cookie_id, cookie in cookies_from_tree:
            thread = threading.Thread(target=self.run_chrome_instance, args=(cookie_id, cookie))
            thread.start()

    def run_chrome_instance(self, cookie_id, cookie_text):
        chrome_options = Options()
        chrome_options.add_argument('--force-device-scale-factor=0.3')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.drivers.append(driver)

        # Mở Facebook và thiết lập cookie
             
        driver.set_window_size(1920, 1080)
        driver.get("https://www.facebook.com/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.delete_all_cookies()
        try:
            cookie_parts = cookie_text.split(";")
            for cookie in cookie_parts:
                # Kiểm tra cookie hợp lệ
                if "=" in cookie:
                    name, value = cookie.split("=", 1)
                    driver.add_cookie({"name": name.strip(), "value": value.strip()})
                else:
                    print(f"Invalid cookie part: {cookie}")
        except Exception as e:
            print(f"Error adding cookie: {e}")

        # Refresh lại để áp dụng cookie
        driver.refresh()

        # Gửi tin nhắn
        self.send_message(driver, cookie_id)

    def send_message(self, driver, cookie_id):
        # Đọc nội dung tin nhắn từ file
        with open("conten.txt", "r", encoding="utf-8") as file:
            content = file.read()

        print("Starting to send messages.")

        while self.is_running:
            id = self.get_next_id()  # Lấy ID duy nhất tiếp theo

            if id is None:
                print("No more IDs to process.")
                break

            print(f"Attempting to send message to ID: {id}")
            self.update_status(cookie_id, f"Đang gửi ID: {id}")
            url = f"https://www.facebook.com/marketplace/item/{id}"
            driver.get(url)

            try:
                # Nhấn nút "Message"
                message_button = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Message"]'))
                )
                message_button.click()

                # Chờ hộp văn bản và nhập nội dung tin nhắn
                self.update_status(cookie_id,"Đang nhập nội dung")
                textarea = WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@id, ':r')]"))
                )

                textarea.clear()
                textarea.send_keys(content)

                # Nhấn nút "Send message"
                send_button = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Send message"]'))
                )
                send_button.click()

                self.success_count += 1
                print(f"Message sent to ID: {id}")
                self.update_status(cookie_id, f"Tổng số đã gửi: {self.success_count}")
                time.sleep(4)

                # Xóa ID khỏi danh sách và file
                self.remove_id_from_file(id)

            except Exception as e:
                self.error_count += 1
                print(f"Error with ID {id}: {e}")
                self.update_status(cookie_id, f"Tổng lỗi: {self.error_count}")
                continue

    def get_next_id(self):
        # Đảm bảo rằng chỉ một luồng có thể truy cập vào danh sách ID
        with self.lock:
            while self.id_list:
                id = self.id_list.pop(0)
                if id not in self.processed_ids:  # Kiểm tra ID chưa được xử lý
                    self.processed_ids.add(id)  # Đánh dấu ID là đã xử lý
                    return id
            return None  # Không còn ID nào để xử lý

    def remove_id_from_file(self, id):
        with self.lock:  # Đảm bảo không trùng lặp trong các luồng
            with open("ID.txt", "w") as file:
                for remaining_id in self.id_list:
                    file.write(remaining_id + "\n")
        print(f"ID {id} đã được xóa khỏi file.")

    def stop_automation(self):
        # Dừng tất cả luồng
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        # Đóng tất cả các trình duyệt đang mở
        for driver in self.drivers:
            driver.quit()
        self.drivers.clear()
        print("Automation stopped.")

    def clear_cookies(self):
        # Xóa toàn bộ cookie trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        print("All cookies have been cleared.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FacebookAutomationApp(root)
    root.mainloop()
