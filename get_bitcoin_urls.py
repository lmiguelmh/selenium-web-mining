# @author lmiguelmh
# @since 

import codecs
import os
import pickle
import sys
import time
import random
from datetime import date

from selenium.webdriver.support.events import EventFiringWebDriver

import page.google.news
from page.google.news import NewsGooglePage
from webdriverwrapper.driver import WebDriver
from webdriverwrapper.listener import WebDriverEventListener

sys.path.append('.')

desired_capabilities = {'browserName': 'chrome'}
command_executor = "http://127.0.0.1:4444/wd/hub"
news_us = "https://news.google.com/?ned=us"  # ned=us for us edition
news_pe = "https://news.google.com/?ned=es_pe"

remote_webdriver = WebDriver(desired_capabilities=desired_capabilities, command_executor=command_executor)
driver = EventFiringWebDriver(remote_webdriver, WebDriverEventListener())
google = NewsGooglePage(driver)

update = False
words = ["bitcoin"]  # 'bitcoin allintitle:bitcoin location:China site:coindesk.com source:BBC'
start_date = date(2016, 3, 1)
end_date = date(2016, 11, 22)

for ordinal in range(start_date.toordinal(), end_date.toordinal()):
    d = date.fromordinal(ordinal)

    for word in words:
        file = "pkz/" + word + "_" + d.strftime("%Y-%m-%d") + ".pkz"
        news_pe = page.google.news.make_news_url_between(word, d, d)
        if not os.path.exists(file) or update:
            t = random.uniform(2., 5.)
            print("sleeping for", t)
            time.sleep(t)

            google.open_and_wait_for_ready_state(news_pe)
            links = google.get_links(1, 2, True)
            print("links:", len(links), "word:", "'" + word + "'", "file:", "'" + file + "'")

            pkz = codecs.encode(pickle.dumps(links), 'zlib_codec')
            with open(file, 'wb') as f:
                f.write(pkz)

driver.close()
