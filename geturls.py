# @author lmiguelmh
# @since 20161109

# @author lmiguelmh
# @since

import sys
import os
import codecs
import pickle
import time
from urllib import parse
from sendinput import sendinput

from selenium.webdriver.common.keys import Keys

from webdriverwrapper.driver import WebDriver
from webdriverwrapper.listener import WebDriverEventListener
from page.google.base import GooglePage
from page.google.news import NewsGooglePage
from selenium.webdriver.support.events import AbstractEventListener, EventFiringWebDriver
from selenium.webdriver.common.action_chains import ActionChains

from webdriverwrapper.page import Page

sys.path.append('.')

desired_capabilities = {'browserName': 'chrome'}
# desired_capabilities = {'browserName': 'firefox'}
command_executor = "http://127.0.0.1:4444/wd/hub"
news_us = "https://news.google.com/?ned=us"  # ned=us for us edition
news_pe = "https://news.google.com/?ned=es_pe"

remote_webdriver = WebDriver(desired_capabilities=desired_capabilities, command_executor=command_executor)
driver = EventFiringWebDriver(remote_webdriver, WebDriverEventListener())
page = Page(driver)

words = ["chambear", "bamba", "jama", "chancar", "chela", "papayita", "jatear", "jato", "tombo", "tranca",
         "huasca", "choborra", "cacharro", "chongo", "chupodromo", "fercho", "huachimán", "latear", "lompa",
         "mitra", "jeta", "moquear", "ni michi", "ñanga", "ñoba", "telo", "panudo"]
for word in words:

    file = "pkz/" + word + ".pkz"
    if not os.path.exists(file):
        continue

    with open(file, 'rb') as f:
        compressed_content = f.read()
    links = pickle.loads(codecs.decode(compressed_content, 'zlib_codec'))
    print("links:", len(links), "word:", "'" + word + "'")

    for link in links:

        txt = "txt/" + word + "_" + parse.quote(link[:200], safe='') + ".txt"
        if os.path.exists(txt):
            continue

        try:
            page.open_and_wait_for_ready_state(link, timeout=5)
            e = page.find_element_by_locator("tag=body")

            encoding = "utf8"
            with open(txt, 'wb') as f:
                f.write(bytes(driver.current_url, encoding=encoding))
                f.write(bytes("\n", encoding=encoding))
                f.write(bytes(driver.title, encoding=encoding))
                f.write(bytes("\n", encoding=encoding))
                f.write(bytes(e.text, encoding=encoding))

        except Exception as e:
            print(e)
            pass

        # sending ctrl+s doesnt work
        # ActionChains(driver).key_down(Keys.CONTROL).perform()
        # time.sleep(0.2)
        # ActionChains(driver).key_down("S").perform()
        # time.sleep(0.2)
        # ActionChains(driver).key_up("S").perform()
        # time.sleep(0.2)
        # ActionChains(driver).key_up(Keys.CONTROL).perform()

        # sending ctrl+s does work, but browser windows must be in foreground
        # sendinput.Ctrl(sendinput.VK_S)
        # time.sleep(0.5)
        # sendinput.Key(sendinput.VK_RETURN)

    # break

page.driver.close()
