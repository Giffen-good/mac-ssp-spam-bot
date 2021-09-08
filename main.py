from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.common.exceptions import NoSuchElementException

from signal import signal, SIGINT
import yaml
import time


ffprofile = FirefoxProfile()
ffprofile.set_preference('browser.formfill.enable', False)

driver = webdriver.Firefox(firefox_profile=ffprofile)

delay = 8 # seconds
with open('form_fields.yaml', 'r') as file:
    f = yaml.load(file, Loader=yaml.FullLoader)

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    driver.quit()
    exit(0)

def send_valid_keys(id, val):

  el = driver.find_element_by_id(id)
  if type(val) is list:
    if val[0] is not None:
      # Manual click => bug workaround selenium.common.exceptions.ElementNotInteractableException: Message: Element <option> could not be scrolled into view
      for option in el.find_elements_by_tag_name('option'):
        print(option.text)
        if option.text == val[0]:
          option.click()
          break
  else:
    if val is not None and len(driver.find_element_by_id(id).get_attribute('value')) == 0:
      driver.find_element_by_id(id).send_keys("")
      driver.find_element_by_id(id).send_keys(val)
def fill_student_services_form():
  # fill form fields based on input where field is a select box if type returned is List 
  fields =  {
    'field-prechat-ef8b8c36-07d2-4d08-b732-0a58e08e2134' : f["fname"],
    'field-prechat-e6ef8c31-8b4f-4775-90fb-e2aae2efb3a7' : f["lname"],
    'field-prechat-861d1129-873e-4902-9a4d-89d1f30592fc' : f["email"],
    'field-prechat-ff8a8ebb-1892-4295-a909-65e97282baeb' : f["student_number"],
    'field-prechat-91a05634-32dc-45cc-b182-be51a8f72a50' : [f["career_type"]],
    'field-prechat-dd369138-3e89-4dfd-a804-968eafa2eda7' : [f["purpose"]],
    'field-prechat-ac0088fe-04c1-4216-8a4d-231590a211e8' : [f["secondary_issue"]]
  }
  time.sleep(3)
  for k,v in fields.items():
    send_valid_keys(k,v)
  
# submit() not working -- manual click
  driver.find_element_by_id('field-prechat-e6ef8c31-8b4f-4775-90fb-e2aae2efb3a7').submit()
  print('Form Submitted')


# encapsulate a function to determine whether the attribute value exists    
def isElementPresent(by, value):
  try:
      element = driver.find_element(by=by, value=value)
            # except NoSuchElementException, e:
  except NoSuchElementException as e:
    print("High volume wait - cannot join queue... refreshing")

                    # A NoSuchElementException has occurred, indicating that the element was not found in the page, returning False
    return False
  else:                    # No exception occurred, indicating that the element was found on the page and returned True
    return True
def chat_with_chat_bot():
  WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'chat-input-control')))
  driver.find_element_by_id('chat-input-control').send_keys('ssp', Keys.ENTER)
  WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, \"SSP Connect\")]")))
  driver.find_element_by_xpath("//button[contains(@aria-label, \"SSP Connect\")]").click()
  print('SSP request sent')
  time.sleep(5)
  if not isElementPresent(By.CLASS_NAME, "greeting-message window__formGreeting"):
    driver.refresh()
    main()

def main():
  driver.get('https://vue.comm100.com/visitorside/html/chatwindow.8c5433a901d191e25cca73a9250f7a35daeeaf66.html?siteId=30000019&planId=c6e424a3-d7e9-4403-b838-ee32d1e6eb36#')
  print ("page initialized...")
   
  try:
    prechat_fields = EC.visibility_of_all_elements_located((By.ID, 'prechat-fields'))
    WebDriverWait(driver, delay).until(prechat_fields)
    print ("JS Rendered Form successfully loaded")
  except TimeoutException:
    print ("Timed out waiting for page to load")
    driver.quit()
  fill_student_services_form()
  chat_with_chat_bot()
 
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  signal(SIGINT, handler)
  main()
  while True:
    # Do nothing and hog CPU forever until SIGINT received.
    pass