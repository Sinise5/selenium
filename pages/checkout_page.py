from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.checkout_button = (By.ID, "checkout")
        self.confirm_button = (By.ID, "confirm")
    
    def proceed_to_checkout(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.checkout_button)).click()
    
    def confirm_order(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.confirm_button)).click()
