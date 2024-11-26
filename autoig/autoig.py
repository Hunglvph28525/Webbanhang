from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import time

# Hàm cài đặt proxy Oxylabs
import zipfile

def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxy Auth Extension",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>"
        ],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """
    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{proxy_host}",
                port: parseInt({proxy_port})
            }},
            bypassList: ["localhost"]
        }}
    }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{
            return {{
                authCredentials: {{
                    username: "{proxy_username}",
                    password: "{proxy_password}"
                }}
            }};
        }},
        {{urls: ["<all_urls>"]}},
        ["blocking"]
    );
    """

    # Lưu file ZIP
    plugin_file = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(plugin_file, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_file
def setup_browser_with_proxy(proxy_username, proxy_password, proxy_address, geo_location):
    proxy_host, proxy_port = proxy_address.split(':')
    plugin_file = create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password)
    
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_extension(plugin_file)
    
    driver = webdriver.Chrome(options=options)
    return driver

# Hàm tạo tài khoản
def create_facebook_account(driver):
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.NAME, "firstname")))

    # Tạo thông tin ngẫu nhiên
    first_name = ''.join(random.choices(string.ascii_letters, k=5))
    last_name = ''.join(random.choices(string.ascii_letters, k=7))
    email = f"{first_name.lower()}{last_name.lower()}@1secmail.com"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    birth_day = str(random.randint(1, 28))
    birth_month = str(random.randint(1, 12))
    birth_year = str(random.randint(1980, 2003))

    # Điền thông tin vào form
    driver.find_element(By.NAME, "firstname").send_keys(first_name)
    driver.find_element(By.NAME, "lastname").send_keys(last_name)
    driver.find_element(By.NAME, "reg_email__").send_keys(email)
    time.sleep(1)
    driver.find_element(By.NAME, "reg_passwd__").send_keys(password)
    driver.find_element(By.NAME, "birthday_day").send_keys(birth_day)
    driver.find_element(By.NAME, "birthday_month").send_keys(birth_month)
    driver.find_element(By.NAME, "birthday_year").send_keys(birth_year)
    driver.find_element(By.XPATH, "//input[@value='2']").click()  # Chọn giới tính nam

    # Submit form
    driver.find_element(By.NAME, "websubmit").click()
    time.sleep(100)

# Main
if __name__ == "__main__":
    proxy_username = "hung1221_4E5DC"
    proxy_password = "Hung1221++++"
    proxy_address = "unblock.oxylabs.io:60000"
    geo_location = "United States"

    driver = setup_browser_with_proxy(proxy_username, proxy_password, proxy_address, geo_location)
    try:
        create_facebook_account(driver)
    except Exception as e:
        print("Lỗi:", e)
    finally:
        driver.quit()
