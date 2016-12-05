# @author lmiguelmh
# @since 20161105

from webdriverwrapper.page import Page

from _corpus.retrieval.webdriverwrapper.elements.text import Text

locators = {
    'input': 'id=lst-ib',
    'search': 'name=btnK'
}

default_page_url = "https://www.google.com"


class InputText(Text):
    def __init__(self, locator):
        self.locator = locator


class GooglePage(Page):
    input_text = InputText(locators['input'])

    def open(self, page_url=default_page_url):
        self.driver.get(page_url)
        return self.wait_until_loaded()

    def wait_until_loaded(self):
        self.wait_for_available(locators['search'])
        return self
