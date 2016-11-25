# @author lmiguelmh
# @since 20161109

# @author lmiguelmh
# @since

import codecs
import glob
import hashlib
import os
import pickle
import sys
from datetime import date
from urllib import parse

import langdetect  # https://pypi.python.org/pypi/langdetect? port of google's library
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.support.events import EventFiringWebDriver

from webdriverwrapper.driver import WebDriver
from webdriverwrapper.listener import WebDriverEventListener
from webdriverwrapper.page import Page


# # http://stackoverflow.com/questions/1303021/shortest-hash-in-python-to-name-cache-files
# def shortest_base64_hash(s):
#     """ does not return the same hash in different sessions!
#     :param s: string or repr(obj)
#     :return:
#     """
#     h = format(abs(hash(s)), 'x')  # abs because python doesnt support binary digits
#     b = bytes("".join(chr(int(h[i:i + 2], 16)) for i in range(0, len(h), 2)), encoding='utf-8')
#     return base64.urlsafe_b64encode(b).decode('utf-8').rstrip('=')
# def shortest_hash(s, applyabs=False):
#     """
#     :param applyabs:
#     :param s:
#     :return: maybe a negative hexstring!
#     """
#     if applyabs:
#         return format(abs(hash(s)), 'x')
#     else:
#         return format(hash(s), 'x')


def shortest_hash(b):
    """
    :param b: bytes(s, encoding='utf-8')
    :return: md5 hexstr
    """
    return hashlib.md5(b).hexdigest()[::2]


def get_contents(driver, link, timeout=5):
    page = Page(driver)
    # try:
    driver.get(link)
    # page.open_and_wait_for_ready_state(link, timeout=timeout)
    # except Exception as e:
    #     pass
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
            print(link)

            l = glob.glob('links/%s-%s-*' % (file[:-4], shortest_hash(bytes(link, encoding='utf8'))))
            if l or len(l) > 0:
                print('file already exists')
                continue

            content = get_contents(driver, link, timeout=5)
            lang = langdetect.detect(content['title'])
            if lang != 'en':
                print('ignoring lang="%s" title="%s"' % (lang, content['title']))
                continue

            if "google" in content['url']:
                print('ignoring google they block :P')
                continue

            outfile = os.path.join(outdir, '%s-%s-%s.txt' % (
                file[:-4], shortest_hash(bytes(link, encoding='utf8')),
                parse.quote('_'.join(content['title'].split()[:10]), safe='')))
            if not os.path.exists(outfile):
                with open(outfile, 'wb') as f:
                    f.write(bytes(content['url'], encoding='utf8'))
                    f.write(bytes("\n", encoding='utf8'))
                    f.write(bytes(content['title'], encoding='utf8'))
                    f.write(bytes("\n", encoding='utf8'))
                    f.write(bytes(content['body'], encoding='utf8'))

        break  # only the first links from now on
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

# http://stackoverflow.com/questions/28879950/how-to-avoid-google-search-detect-selenium-webdriver-as-unusual-behaviour
# ProfilesIni allProfiles = new ProfilesIni();
# WebDriver driver = new FirefoxDriver(allProfiles.getProfile("default"));

import threading
class Test(threading.Thread):
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        threading.Thread.__init__(self)

    def run(self):
        self.driver.get(self.url)


# get_contents_from_links()
# remote_webdriver = WebDriver(desired_capabilities={'browserName': 'firefox'},
#                              command_executor="http://127.0.0.1:4444/wd/hub")
# driver = EventFiringWebDriver(remote_webdriver, WebDriverEventListener())

fp = webdriver.FirefoxProfile()
fp.set_preference("webdriver.load.strategy", "unstable") # according to this https://github.com/SeleniumHQ/selenium/issues/2873 it only works in Firefox <46
# according to this http://stackoverflow.com/a/21967923/2692914 there are conservative, eager, normal, and none "pageLoadingStrategy"
driver = webdriver.Firefox(fp)

# c = get_contents(driver, 'http://utero.pe/')
# print("%s loaded!" % c['url'])

# driver.get('http://intranet.reniec.gob.pe')
# t = Test(driver, 'http://www.reniec.gob.pe')
t = Test(driver, 'https://www.reniec.gob.pe/portal/intro.htm')
t.start()

import time

for i in range(1, 10):
    try:
        print(driver.execute_script('return document.readyState'))
    except BaseException as e:
        print(e)
    time.sleep(0.25)

t.join()

# driver.close()
