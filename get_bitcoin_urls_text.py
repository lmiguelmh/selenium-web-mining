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
from datetime import datetime, date, time
from selenium.webdriver.common.keys import Keys
from webdriverwrapper.driver import WebDriver
from webdriverwrapper.listener import WebDriverEventListener
from page.google.base import GooglePage
from page.google.news import NewsGooglePage
from selenium.webdriver.support.events import AbstractEventListener, EventFiringWebDriver
from selenium.webdriver.common.action_chains import ActionChains

from webdriverwrapper.page import Page
import langdetect  # https://pypi.python.org/pypi/langdetect? port of google's library


def get_contents(driver, link, timeout=5):
    page = Page(driver)
    page.open_and_wait_for_ready_state(link, timeout=timeout)
    body = page.find_element_by_locator("tag=body")
    return {'body': body.text, 'title': driver.title, 'url': driver.current_url}


def get_contents_from_links(basedir='links',
                            outdir='links_contents',
                            command_executor="http://127.0.0.1:4444/wd/hub",
                            desired_capabilities=None):
    if not desired_capabilities: desired_capabilities = {'browserName': 'chrome'}
    remote_webdriver = WebDriver(desired_capabilities=desired_capabilities, command_executor=command_executor)
    driver = EventFiringWebDriver(remote_webdriver, WebDriverEventListener())

    files = [f for f in os.listdir(basedir) if os.path.isfile(os.path.join(basedir, f))]
    for file in files:

        with open(os.path.join(basedir, file), 'r') as f:
            links = list(set([line.rstrip('\n') for line in f]))
        print("%d links in %s" % (len(links), file))

        for link in links:
            content = get_contents(driver, link, timeout=10)
            print(content['url'])

            lang = langdetect.detect(content['title'])
            if lang != 'en':
                print('ignoring lang="%s" title="%s"' % (lang, content['title']))
                continue

            if ".google." in content['url']:
                print('ignoring google :P')
                continue

            outfile = os.path.join(outdir, "%s-%s.txt" % (file[:-4], parse.quote("_".join(content['title'].split()[:10]), safe='')))
            if not os.path.exists(outfile):
                with open(outfile, 'wb') as f:
                    f.write(bytes(content['url'], encoding='utf8'))
                    f.write(bytes("\n", encoding='utf8'))
                    f.write(bytes(content['title'], encoding='utf8'))
                    f.write(bytes("\n", encoding='utf8'))
                    f.write(bytes(content['body'], encoding='utf8'))

        break
    driver.close()


def get_contents_from_pkz():
    desired_capabilities = {'browserName': 'chrome'}
    command_executor = "http://127.0.0.1:4444/wd/hub"

    remote_webdriver = WebDriver(desired_capabilities=desired_capabilities, command_executor=command_executor)
    driver = EventFiringWebDriver(remote_webdriver, WebDriverEventListener())
    page = Page(driver)

    words = ["bitcoin"]
    start_date = date(2016, 10, 1)
    end_date = date(2016, 10, 3)

    for ordinal in range(start_date.toordinal(), end_date.toordinal()):
        d = date.fromordinal(ordinal)

        for word in words:
            file = "pkz/" + word + "_" + d.strftime("%Y-%m-%d") + ".pkz"
            if not os.path.exists(file):
                continue

            with open(file, 'rb') as f:
                compressed_content = f.read()
            links = pickle.loads(codecs.decode(compressed_content, 'zlib_codec'))
            print("links:", len(links), "word:", "'" + word + "'")

            for link in links:
                txt = "txt/" + word + "_" + parse.quote(link[:100], safe='') + ".txt"
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

    page.driver.close()


sys.path.append('.')
get_contents_from_links()
