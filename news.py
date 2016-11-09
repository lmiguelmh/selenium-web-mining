# @author lmiguelmh
# @since 

import sys
import os
import codecs
import pickle

from webdriverwrapper.driver import WebDriver
from webdriverwrapper.listener import WebDriverEventListener
from page.google.base import GooglePage
from page.google.news import NewsGooglePage
from selenium.webdriver.support.events import AbstractEventListener, EventFiringWebDriver

sys.path.append('.')

desired_capabilities = {'browserName': 'chrome'}
command_executor = "http://127.0.0.1:4444/wd/hub"
news_us = "https://news.google.com/?ned=us"  # ned=us for us edition
news_pe = "https://news.google.com/?ned=es_pe"

remote_webdriver = WebDriver(desired_capabilities=desired_capabilities, command_executor=command_executor)
driver = EventFiringWebDriver(remote_webdriver, WebDriverEventListener())
google = NewsGooglePage(driver)

update = False
words = ["chambear", "bamba", "jama", "chancar", "chela", "papayita", "jatear", "jato", "tombo", "tranca",
         "huasca", "choborra", "cacharro", "chongo", "chupodromo", "fercho", "huachimán", "latear", "lompa",
         "mitra", "jeta", "moquear", "ni michi", "ñanga", "ñoba", "telo", "panudo"]
for word in words:
    file = "pkz/" + word + ".pkz"
    if not os.path.exists(file) or update:
        google.open(news_pe)
        links = google.get_results_links(word, 1, 2, True)
        print("links:", len(links), "word:", "'" + word + "'")

        pkz = codecs.encode(pickle.dumps(links), 'zlib_codec')
        with open(file, 'wb') as f:
            f.write(pkz)

# google.input_text = 'bitcoin\n'
# # google.input_text = 'bitcoin location:China\n'
# # google.input_text = 'bitcoin allintitle:bitcoin location:China\n'
# # google.input_text = 'bitcoin allintitle:bitcoin location:China site:coindesk.com\n'
# # google.input_text = 'bitcoin allintitle:bitcoin location:China site:coindesk.com source:BBC\n'
# google.wait_for_results()
#
# hrefs = []
# start = 1
# end = 5
# for page in range(1, 5+1):
#     print("PAGE #", page)
#     e = google.next_result_a()
#     while e is not None:
#         href = e.get_attribute("href")
#         hrefs.append(e.get_attribute("href"))
#         e = google.next_result_a()
#     google.next_page()
#
# print(len(hrefs))
# print(hrefs)
