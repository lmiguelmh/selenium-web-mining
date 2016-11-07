# @author lmiguelmh
# @since 20161105
from webdriverwrapper.errors import ExpectedElementError
from .base import GooglePage
from .base import InputText
from webdriverwrapper.elements.text import Text

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

        e = self.find_element_by_locator(locators['next_button'])
        if e is not None and e.tag_name == 'a':
            e.click()
        else:
            raise ExpectedElementError('next_button locator is not a link')

        self.wait_for_change(locators['current_page'], current.text)
