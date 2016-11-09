# @author lmiguelmh
# @since 20161105
from selenium.common.exceptions import NoSuchElementException

from webdriverwrapper.errors import ExpectedElementError
from .base import GooglePage
from .base import InputText
from webdriverwrapper.elements.text import Text
import random

default_page_url = "https://news.google.com/?ned=us"
locators = {
    'input': 'name=q',
    'search': 'id=gbqfb',
    'results_div': 'id=ires',
    'results_tag_a': 'css=._HId',
    'next_button': 'id=pnnext',
    # 'current_page': 'css=td.cur'
    'current_page': 'css=.cur'
}


class NewsGooglePage(GooglePage):
    input_text = InputText(locators['input'])
    results = None
    results_index = 0
    results_locator = ""

    def open(self, page_url=default_page_url):
        self.driver.get(page_url)
        return self.wait_until_loaded()

    def wait_until_loaded(self):
        self.wait_for_available(locators['search'])
        return self

    def wait_for_results(self):
        self.wait_for_available(locators['results_div'])

    def next_result_a(self):
        return self.next(locators['results_tag_a'])

    def next(self, locator):
        if self.results is None or locator != self.results_locator:
            self.results = self.find_elements_by_locator(locator)
            self.results_index = 0
            self.results_locator = locator

        if len(self.results) > self.results_index:
            e = self.results[self.results_index]
            self.results_index += 1
            return e

        else:
            self.results = None
            self.results_index = 0
            self.results_locator = ""
            return None

    def next_page(self):
        current = self.find_element_by_locator(locators['current_page'])
        if current is None:
            raise ExpectedElementError('current_page locator does not exist')

        try:
            e = self.find_element_by_locator(locators['next_button'])
            if e is not None and e.tag_name == 'a':
                e.click()
            else:
                raise ExpectedElementError('next_button locator is not a link')

            self.wait_for_change(locators['current_page'], current.text)
            return True

        except NoSuchElementException as e:
            pass
            return False

    def get_results_links(self, query, startpage=1, endpage=1, wait=False):
        self.input_text = query + '\n'
        self.wait_for_results()

        links = []
        for page in range(startpage, endpage + 1):
            e = self.next_result_a()
            if e is None:
                break

            while e is not None:
                href = e.get_attribute("href")
                links.append(e.get_attribute("href"))
                e = self.next_result_a()

            if wait:
                self.sleep(random.uniform(1., 3.))

            if not self.next_page():
                break

        return links