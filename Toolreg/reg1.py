import tkinter as tk
from tkinter import ttk, messagebox
import re
import time
import threading
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager  # Import webdriver_manager

# Global variables for table and auto ID

current_id = 1
keyword_entries = {}
threads = []  # List to store threads for stopping them later
stop_event = threading.Event()  # Event to stop all threads when stop button is clicked
root = tk.Tk()
root.title("Quản lý Cookie và Từ Khoá Facebook Marketplace")
root.geometry("1200x600")

# Function to run Selenium task for each browser instance
def start_selenium_task(item_id, cookie, city_code, keyword):
    chrome_options = Options()
    chrome_options.add_argument('--force-device-scale-factor=0.3')  # Tùy chọn điều chỉnh tỷ lệ hiển thị

    # Khởi tạo driver với chrome options sử dụng webdriver_manager
    service = Service(ChromeDriverManager().install())  # Set up Service for ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Automatic chromedriver installation
    driver.set_window_size(1920,1080)

    try:
        # Set cookie in the browser
        driver.get("https://www.facebook.com/")
        driver.delete_all_cookies()

        # Split and add cookie to browser
        cookies = cookie.split(";")
        for c in cookies:
            c = c.strip()  # Ensure no extra spaces
            if "=" in c:
                name, value = c.split("=", 1)
                driver.add_cookie({"name": name.strip(), "value": value.strip(), "domain": "facebook.com"})
        
        driver.refresh()  # Refresh to apply cookie

        # Check login success
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search Facebook"]'))
        )
        print(f"Đã đăng nhập thành công bằng cookie cho ID {item_id}.")
        
        # Navigate to Marketplace with keyword
        driver.get(f"https://www.facebook.com/marketplace/{city_code}/search/?query={keyword}")

        # Scroll settings
        SCROLL_PAUSE_TIME = 2
        MAX_SCROLLS = 500

        saved_ids = set()
        # Create a unique file name based on city and keyword
        filename = f"{city_code}_{keyword.replace(' ', '_')}.txt"
        
        # Try to load existing IDs from file if available
        try:
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    saved_ids = {line.strip() for line in file}
        except FileNotFoundError:
            saved_ids = set()

        with open(filename, "a") as file:
            for i in range(MAX_SCROLLS):
                if stop_event.is_set():  # Check if stop event is triggered
                    print(f"Đã dừng tìm kiếm cho ID {item_id}.")
                    break
                try:
                    div_elements = driver.find_elements(By.CSS_SELECTOR, "div.x9f619.x78zum5.x1r8uery.xdt5ytf.x1iyjqo2.xs83m0k.x1e558r4.x150jy0e.x1iorvi4.xjkvuk6.xnpuxes.x291uyu.x1uepa24")
                    for div in div_elements:
                        a_tags = div.find_elements(By.TAG_NAME, "a")
                        for a in a_tags:
                            href = a.get_attribute("href")
                            if href:
                                match = re.search(r'item/(\d+)', href)
                                if match:
                                    item_id = match.group(1)
                                    if item_id not in saved_ids:
                                        file.write(item_id + "\n")
                                        saved_ids.add(item_id)
                                        print(f"ID đã lưu: {item_id}")
                except Exception as e:
                    print(f"Đã xảy ra lỗi: {e}")

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)

    finally:
        print(f"Hoàn tất tìm kiếm cho ID {item_id}. Đóng trình duyệt.")
        driver.quit()

# Function for Start button
def start_selenium():
    selected_items = tree.get_children()  # Get all items from the table (no need to check selection)

    if not selected_items:
        messagebox.showwarning("Chưa có dữ liệu", "Bảng không có dòng nào để thực hiện hành động.")
        return
    
    start_button.config(state=tk.DISABLED)  # Disable Start button when starting
    stop_button.config(state=tk.NORMAL)     # Enable Stop button when starting
    stop_event.clear()  # Reset stop event before starting

    try:
        for item in selected_items:
            # Get information from table (cookie, city code, keyword)
            cookie = tree.item(item, "values")[1]
            city_code = tree.item(item, "values")[2]
            keyword = tree.item(item, "values")[4]  # Keyword

            if not cookie or not city_code or not keyword:
                messagebox.showwarning("Thiếu dữ liệu", f"Dữ liệu chưa đầy đủ cho ID {tree.item(item, 'values')[0]}")
                continue

            # Open separate browser for each ID
            item_id = tree.item(item, "values")[0]
            thread = threading.Thread(target=start_selenium_task, args=(item_id, cookie, city_code, keyword))
            threads.append(thread)
            thread.start()

    finally:
        print("Hoàn tất bắt đầu tìm kiếm.")
        stop_button.config(state=tk.NORMAL)   # Enable Stop button
        start_button.config(state=tk.DISABLED)    # Disable Start button

# Function for Stop action
def stop_action():
    print("Stop hành động đã được kích hoạt.")
    stop_event.set()  # Set stop event to stop all threads
    stop_button.config(state=tk.DISABLED)  # Disable Stop button
    start_button.config(state=tk.NORMAL)   # Enable Start button again

    # Wait for all threads to complete before resetting
    for thread in threads:
        thread.join()

    print("Tất cả các luồng đã dừng.")

# Add a row to the table
def add_row():
    global current_id

    cookie = cookie_entry.get()
    city_code = city_entry.get()
    keyword = keyword_input_entry.get()

    if not cookie or not city_code or not keyword:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ cookie, mã thành phố và từ khoá.")
        return

    tree.insert("", "end", values=(current_id, cookie, city_code, "Chưa bắt đầu", keyword))

    # Increment the ID for the next row
    current_id += 1

    # Clear only the keyword input field after adding
    keyword_input_entry.delete(0, tk.END)

# Update a row in the table
def update_row():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Chưa chọn dòng", "Vui lòng chọn dòng cần cập nhật.")
        return

    cookie = cookie_entry.get()
    city_code = city_entry.get()
    keyword = keyword_input_entry.get()

    if not cookie or not city_code or not keyword:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ cookie, mã thành phố và từ khoá.")
        return

    tree.item(selected_item, values=(tree.item(selected_item, "values")[0], cookie, city_code, "Đang chạy", keyword))

    # Clear input fields after updating
    cookie_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    keyword_input_entry.delete(0, tk.END)

# Delete a row from the table
def delete_row():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Chưa chọn dòng", "Vui lòng chọn dòng cần xóa.")
        return
    tree.delete(selected_item)

# UI layout

# Main frame
main_frame = tk.Frame(root)
main_frame.pack(pady=10, fill="both", expand=True)

# Top frame for input fields and buttons
top_frame = tk.Frame(main_frame)
top_frame.pack(padx=20, pady=10, anchor="w")

# Input fields for Cookie and City Code
cookie_label = tk.Label(top_frame, text="Cookie:")
cookie_label.grid(row=0, column=0, padx=5, pady=5)
cookie_entry = tk.Entry(top_frame, width=40)
cookie_entry.grid(row=0, column=1, padx=5, pady=5)

city_label = tk.Label(top_frame, text="Mã Thành Phố:")
city_label.grid(row=1, column=0, padx=5, pady=5)
city_entry = tk.Entry(top_frame, width=40)
city_entry.grid(row=1, column=1, padx=5, pady=5)

# CRUD buttons
add_button = tk.Button(top_frame, text="Thêm", command=add_row)
add_button.grid(row=2, column=0, padx=5, pady=5)

update_button = tk.Button(top_frame, text="Cập nhật", command=update_row)
update_button.grid(row=2, column=1, padx=5, pady=5)

delete_button = tk.Button(top_frame, text="Xóa", command=delete_row)
delete_button.grid(row=2, column=2, padx=5, pady=5)

# Keyword input
keyword_label = tk.Label(top_frame, text="Từ Khoá:")
keyword_label.grid(row=3, column=0, padx=5, pady=5)
keyword_input_entry = tk.Entry(top_frame, width=40)
keyword_input_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons for Start and Stop actions
start_button = tk.Button(top_frame, text="Start", command=start_selenium)
start_button.grid(row=4, column=0, padx=5, pady=5)

stop_button = tk.Button(top_frame, text="Stop", command=stop_action, state=tk.DISABLED)
stop_button.grid(row=4, column=1, padx=5, pady=5)

# Table to display data
tree = ttk.Treeview(main_frame, columns=("ID", "Cookie", "Mã Thành Phố", "Tình Trạng", "Từ Khoá"), show="headings", height=8)
tree.heading("ID", text="ID")
tree.heading("Cookie", text="Cookie")
tree.heading("Mã Thành Phố", text="Mã Thành Phố")
tree.heading("Tình Trạng", text="Tình Trạng")
tree.heading("Từ Khoá", text="Từ Khoá")
tree.pack(padx=20, pady=10, fill="both", expand=True)

root.mainloop()
