# @author lmiguelmh
# @since 

import sys

from webdriverwrapper.driver import WebDriver
from webdriverwrapper.listener import WebDriverEventListener
from page.google.base import GooglePage
from page.google.news import NewsGooglePage
from selenium.webdriver.support.events import AbstractEventListener, EventFiringWebDriver

sys.path.append('.')

desired_capabilities = {'browserName': 'chrome'}
command_executor = "http://127.0.0.1:4444/wd/hub"
google_url = "https://news.google.com/?ned=us"  # ned=us for us edition

remote_webdriver = WebDriver(desired_capabilities=desired_capabilities, command_executor=command_executor)
driver = EventFiringWebDriver(remote_webdriver, WebDriverEventListener())
google = NewsGooglePage(driver)
google.open(google_url)

google.input_text = 'bitcoin\n'
# google.input_text = 'bitcoin location:China\n'
# google.input_text = 'bitcoin allintitle:bitcoin location:China\n'
# google.input_text = 'bitcoin allintitle:bitcoin location:China site:coindesk.com\n'
# google.input_text = 'bitcoin allintitle:bitcoin location:China site:coindesk.com source:BBC\n'
google.wait_for_results()

hrefs = []
for page in range(1, 5+1):
    print("PAGE #", page)
    e = google.next_result_a()
    while e is not None:
        href = e.get_attribute("href")
        hrefs.append(e.get_attribute("href"))
        e = google.next_result_a()
    google.next_page()

print(len(hrefs))
print(hrefs)
