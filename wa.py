from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pytesseract
import cv2
import numpy as np
from PIL import Image
import logging
import os

# Konfigurasi logging
logging.basicConfig(
    filename="test_results.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Fungsi untuk logging hasil test
def log_result(message):
    print(message)
    logging.info(message)

# Membuat folder screenshot jika belum ada
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# Fungsi untuk menyimpan screenshot saat gagal
def save_screenshot(driver, test_case_name):
    filename = f"screenshots/{test_case_name}.png"
    driver.save_screenshot(filename)
    print(f"📸 Screenshot disimpan: {filename}")

# Fungsi untuk preprocessing CAPTCHA agar OCR lebih akurat
def preprocess_captcha(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((1, 1), np.uint8)
    clean_image = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    processed_path = "processed_captcha.png"
    cv2.imwrite(processed_path, clean_image)
    return processed_path

# Fungsi untuk membaca teks CAPTCHA dengan OCR
def read_captcha(image_path):
    processed_image = preprocess_captcha(image_path)
    captcha_text = pytesseract.image_to_string(Image.open(processed_image), config="--psm 7")
    captcha_text = ''.join(filter(str.isalnum, captcha_text))
    return captcha_text.strip()

# Fungsi untuk menunggu elemen dengan Fluent Wait
def wait_for_element(driver, by, value, timeout=10, poll_frequency=0.5):
    wait = WebDriverWait(driver, timeout, poll_frequency)
    return wait.until(EC.presence_of_element_located((by, value)))

# Konfigurasi Selenium WebDriver dengan Headless Mode
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(service=service, options=options)

# Buka halaman login
driver.get("https://lintech.id/whatsapp")
wait_for_element(driver, By.TAG_NAME, "body")

log_result(f"Title saat ini: {driver.title}")

# Pastikan title halaman sesuai
expected_title = "Chatbot Rujukan Kesehatan Anak Kota Bandung"
assert expected_title in driver.title, f"Error: Title tidak sesuai, ditemukan: {driver.title}"

# Data uji dengan berbagai kombinasi username & password
test_cases = [
    {"username": "testuser", "password": "testpassword", "expected": "success"},
    {"username": "admin", "password": "wrongpass", "expected": "fail"},
    {"username": "unknown", "password": "123456", "expected": "fail"},
    {"username": "silver", "password": "silver", "expected": "success"},
]

# Looping untuk testing login
for index, test in enumerate(test_cases):
    log_result(f"\n🔹 [TEST CASE {index+1}] Login dengan Username: {test['username']} | Password: {test['password']}")

    try:
        # Ambil screenshot CAPTCHA
        captcha_element = wait_for_element(driver, By.XPATH, "//img[@id='capt_01']")
        captcha_element.screenshot("captcha.png")

        # Gunakan OCR untuk membaca CAPTCHA
        captcha_text = read_captcha("captcha.png")
        log_result(f"CAPTCHA yang dibaca: {captcha_text}")

        # Masukkan username
        username_input = wait_for_element(driver, By.NAME, "user")
        username_input.clear()
        username_input.send_keys(test["username"])

        # Masukkan password
        password_input = wait_for_element(driver, By.NAME, "pass")
        password_input.clear()
        password_input.send_keys(test["password"])

        # Masukkan CAPTCHA
        captcha_input = wait_for_element(driver, By.NAME, "captcha01")
        captcha_input.clear()
        captcha_input.send_keys(captcha_text)

        # Tekan tombol login
        login_button = wait_for_element(driver, By.ID, "login")
        login_button.click()

        # Tunggu sampai halaman berubah setelah login
        time.sleep(3)

        # Verifikasi apakah login berhasil
        if "dash" in driver.current_url.lower():
            log_result("✅ Login Berhasil!")
        else:
            log_result("❌ Login Gagal!")
            save_screenshot(driver, f"failed_test_{index+1}")

    except Exception as e:
        log_result(f"⚠ Error pada test case {index+1}: {e}")
        save_screenshot(driver, f"error_test_{index+1}")

# Tutup browser setelah selesai
driver.quit()
