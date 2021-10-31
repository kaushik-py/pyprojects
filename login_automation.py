from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
browser = webdriver.Chrome()
browser.get("https://www.stlamartschooluk.com/contact/")
time.sleep(5)
img_elem = browser.find_element_by_id("random-image-REPLACE_TO_ID")
if(img_elem.is_displayed()):
    print("inn------------------------------------------------------------------------------")
    i_con = browser.find_element_by_class_name("eicon-close")
    i_con.click()

name = browser.find_element_by_id("form-field-name")
name.send_keys("Arnav")
phoneno = browser.find_element_by_id("form-field-field_2dd9739")
phoneno.send_keys("9877542136")
email = browser.find_element_by_id("form-field-email")
email.send_keys("arnav12@gmail.com")
message = browser.find_element_by_id('form-field-message')
message.send_keys("Hello i am a student at ggrrschool situated at karnataka and i want to just inspect the fees and curriculum of school....")
button = browser.find_element_by_class_name("elementor-button elementor-size-sm")
button.click()
time.sleep(5)
browser.back()
browser.close()