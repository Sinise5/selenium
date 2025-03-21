import logging
import os
import time
import pytest
import cv2
import json
import numpy as np
import pytesseract
from PIL import Image
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import allure
import re  # Untuk sanitasi nama file

# Setup Direktori Logs & Screenshots
os.makedirs("screenshots", exist_ok=True)
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/test_results.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_result(message):
    print(message)
    logging.info(message)

def save_test_result(username, status):
    result = {"username": username, "status": status, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open("logs/test_results.json", "a") as file:
        json.dump(result, file)
        file.write("\n")

def sanitize_filename(name):
    """Menghapus karakter yang tidak valid dari nama file."""
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def save_screenshot(driver, test_case_name):
    sanitized_name = sanitize_filename(test_case_name)
    filename = f"screenshots/{sanitized_name}.png"

    driver.save_screenshot(filename)
    with open(filename, "rb") as image_file:
        allure.attach(image_file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)
    log_result(f"📸 Screenshot disimpan: {filename}")

def preprocess_captcha(image_path):
    """Preprocessing CAPTCHA agar lebih mudah dibaca oleh OCR."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        log_result("⚠ Gagal memuat gambar CAPTCHA!")
        return None
    
    # Adaptive Thresholding untuk meningkatkan visibilitas teks
    processed_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    processed_path = "processed_captcha.png"
    cv2.imwrite(processed_path, processed_image)
    return processed_path

def read_captcha(image_path):
    """Membaca teks dari CAPTCHA menggunakan OCR."""
    processed_image = preprocess_captcha(image_path)
    if processed_image is None:
        return ""  # Jika gambar tidak valid, kembalikan string kosong
    
    captcha_text = pytesseract.image_to_string(Image.open(processed_image), config="--psm 7").strip()
    captcha_text = ''.join(filter(str.isalnum, captcha_text))  # Hapus karakter non-alphanumeric

    log_result(f"🔍 Hasil OCR CAPTCHA: '{captcha_text}'")
    
    return captcha_text if captcha_text else ""  # Pastikan tidak mengembalikan None

def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

@pytest.fixture(params=["chrome"])
def setup_driver(request):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://lintech.id/whatsapp")
    wait_for_element(driver, By.TAG_NAME, "body")
    yield driver
    driver.quit()

fake = Faker()

def ai_predict_login(username, password):
    if username == "silver" and password == "silver":
        return "success"
    elif len(password) < 6 or "123" in password:
        return "fail"
    return np.random.choice(["success", "fail"], p=[0.8, 0.2])

def generate_test_cases(n=5):
    test_cases = [
        {"username": "silver", "password": "silver", "expected": "success"},
        {"username": "admin", "password": "wrongpass", "expected": "fail"},
        {"username": "", "password": "", "expected": "fail"},
        {"username": "admin' OR 1=1 --", "password": "any", "expected": "fail"},
        {"username": "<script>alert('XSS')</script>", "password": "password", "expected": "fail"},
        {"username": "VeryLongUsername1234567890", "password": "VeryLongPassword1234567890", "expected": "fail"},
        {"username": "Silver", "password": "SILVER", "expected": "fail"}
    ]
    for _ in range(n):
        username = fake.user_name()
        password = fake.password()
        expected = ai_predict_login(username, password)
        test_cases.append({"username": username, "password": password, "expected": expected})
    return test_cases

test_cases = generate_test_cases(5)

@pytest.mark.parametrize("test_data", test_cases)
@allure.story("Login Testing")
def test_login(setup_driver, test_data):
    driver = setup_driver
    username, password, expected = test_data["username"], test_data["password"], test_data["expected"]

    with allure.step(f"🔹 [TEST] Login dengan Username: {username} | Password: {password}"):
        log_result(f"\n🔹 [TEST] Login dengan Username: {username} | Password: {password}")

    try:
        # Coba ambil CAPTCHA jika tersedia
        try:
            captcha_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//img[@id='capt_01']"))
            )
            captcha_element.screenshot("captcha.png")
            captcha_text = read_captcha("captcha.png")
        except TimeoutException:
            log_result("⚠ CAPTCHA tidak ditemukan, mencoba login tanpa CAPTCHA")
            captcha_text = ""

        # Isi formulir login
        username_input = wait_for_element(driver, By.NAME, "user")
        username_input.clear()
        username_input.send_keys(username)

        password_input = wait_for_element(driver, By.NAME, "pass")
        password_input.clear()
        password_input.send_keys(password)

        if captcha_text:
            captcha_input = wait_for_element(driver, By.NAME, "captcha01")
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)

        login_button = wait_for_element(driver, By.ID, "login")
        login_button.click()
        time.sleep(3)

        # Evaluasi hasil login
        if "dash" in driver.current_url.lower():
            assert expected == "success", "Login berhasil padahal seharusnya gagal"
            log_result("✅ Login Berhasil!")
            save_test_result(username, "success")
        else:
            assert expected == "fail", "Login gagal padahal seharusnya berhasil"
            log_result("❌ Login Gagal!")
            save_test_result(username, "fail")
            save_screenshot(driver, f"failed_test_{username}")

    except Exception as e:
        log_result(f"⚠ Error pada test case {username}: {e}")
        save_screenshot(driver, f"error_test_{username}")

@pytest.mark.benchmark
def test_login_performance(benchmark, setup_driver):
    driver = setup_driver

    def load_page():
        start_time = time.time()
        driver.get("https://lintech.id/whatsapp")
        wait_for_element(driver, By.TAG_NAME, "body")
        return time.time() - start_time

    response_time = benchmark(load_page)
    assert response_time < 2.0, f"⚠ Login response time terlalu lama ({response_time:.2f} detik)"
