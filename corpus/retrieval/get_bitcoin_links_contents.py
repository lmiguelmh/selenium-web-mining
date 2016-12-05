# @author lmiguelmh
# @since 20161109

import codecs
import glob
import hashlib
import os
import pickle
import sys
from datetime import date
from urllib import parse

import langdetect  # https://pypi.python.org/pypi/langdetect? port of google's library
from selenium.webdriver.support.events import EventFiringWebDriver
from webdriverwrapper.driver import WebDriver
from webdriverwrapper.page import Page

from _corpus.retrieval.webdriverwrapper.listener import WebDriverEventListener


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


def write_link_contents(driver, link, outdir, file):
    l = glob.glob(outdir + '/%s-%s-*' % (file[:-4], shortest_hash(bytes(link, encoding='utf8'))))
    if l or len(l) > 0:
        print('file already exists')
        return True

    if "google" in link:
        print('ignoring google: they block :P')
        return False

    content = get_contents(driver, link, timeout=5)
    lang = langdetect.detect(content['title'])
    if lang != 'en':
        print('ignoring lang="%s" title="%s"' % (lang, content['title']))
        return False

    outfile = os.path.join(outdir, '%s-%s-%s.txt' % (
        file[:-4],
        shortest_hash(bytes(link, encoding='utf8')),
        parse.quote('_'.join(content['title'].split()[:10]), safe='')))

    if not os.path.exists(outfile):
        with open(outfile, 'wb') as f:
            f.write(bytes(content['url'], encoding='utf8'))
            f.write(bytes("\n", encoding='utf8'))
            f.write(bytes(content['title'], encoding='utf8'))
            f.write(bytes("\n", encoding='utf8'))
            f.write(bytes(content['body'], encoding='utf8'))
    return True


def get_contents_from_links(basedir='links',
                            outdir='links_contents',
                            command_executor="http://127.0.0.1:4444/wd/hub",
                            desired_capabilities=None):
    if not desired_capabilities: desired_capabilities = {'browserName': 'chrome'}
    remote_webdriver = WebDriver(desired_capabilities=desired_capabilities, command_executor=command_executor)
    driver = EventFiringWebDriver(remote_webdriver, WebDriverEventListener())

    files = [f for f in os.listdir(basedir) if os.path.isfile(os.path.join(basedir, f))]
    for file in files:

        # get the link list
        with open(os.path.join(basedir, file), 'r') as f:
            links = list(set([line.rstrip('\n') for line in f]))
        print("%d links in %s" % (len(links), file))

        processed_links = []
        for link in links:
            print(link)
            try:
                if write_link_contents(driver, link, outdir, file):
                    processed_links.append(link)

            except BaseException as e:
                print(e)

        # save only the processed links
        with open(os.path.join(basedir, file), 'wb') as f:
            lines = "\n".join(processed_links)
            f.write(bytes(lines, encoding='utf8'))

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
