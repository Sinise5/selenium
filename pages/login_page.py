from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.NAME, "user")
        self.password_input = (By.NAME, "pass")
        self.login_button = (By.ID, "login")
    
    def login(self, username, password):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.username_input)).send_keys(username)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.password_input)).send_keys(password)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.login_button)).click()