# @author lmiguelmh
# @since 

import sys
import os
import codecs
import pickle
import page.google.news
from datetime import datetime, date, time
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
words = ["bitcoin"]
start_date = date(2016, 11, 1)
end_date = date(2016, 11, 2)

for ordinal in range(start_date.toordinal(), end_date.toordinal()):
    d = date.fromordinal(ordinal)

    for word in words:
        file = "pkz/" + word + "_" + d.strftime("%Y-%m-%d") + ".pkz"
        news_pe = page.google.news.make_news_url_between(word, d, d)
        if not os.path.exists(file) or update:
            google.open(news_pe)
            links = google.get_links(1, 2, True)
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
