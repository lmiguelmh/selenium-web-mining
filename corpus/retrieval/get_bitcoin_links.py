# @author lmiguelmh
# @since
#
# use this notepad++ regex to get the links from a saved page from firefox (as txt):
# replace:[^<]*<([^>]*)>[^<]*
# with:$1\n
#

import codecs
import os
import pickle
import random
import sys
import time
from datetime import date

from selenium.webdriver.support.events import EventFiringWebDriver
from webdriverwrapper.driver import WebDriver

import _corpus.retrieval.page.google.news
from _corpus.retrieval.page.google.news import NewsGooglePage
from _corpus.retrieval.webdriverwrapper.listener import WebDriverEventListener


def get_bitcoin_urls_text_from_pkz():
    update = False
    words = ["bitcoin"]  # 'bitcoin allintitle:bitcoin location:China site:coindesk.com source:BBC'
    start_date = date(2016, 10, 5)
    end_date = date(2016, 10, 10)

    desired_capabilities = {'browserName': 'chrome'}
    command_executor = "http://127.0.0.1:4444/wd/hub"
    news_us = "https://news.google.com/?ned=us"  # ned=us for us edition
    news_pe = "https://news.google.com/?ned=es_pe"

    remote_webdriver = WebDriver(desired_capabilities=desired_capabilities, command_executor=command_executor)
    driver = EventFiringWebDriver(remote_webdriver, WebDriverEventListener())
    google = NewsGooglePage(driver)

    for ordinal in range(start_date.toordinal(), end_date.toordinal()):
        d = date.fromordinal(ordinal)

        for word in words:
            file = "pkz/" + word + "_" + d.strftime("%Y-%m-%d") + ".pkz"
            news_pe = _corpus.retrieval.page.google.news.make_news_url_between(word, d, d)
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

sys.path.append('.')

get_bitcoin_urls_text_from_pkz()
