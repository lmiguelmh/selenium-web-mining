# based on https://github.com/dakotasmith/page-object-examples

import time
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

from .errors import WaitForElementError


class Page(object):
    def __init__(self, driver):
        self.driver = driver

    @property
    def referrer(self):
        return self.driver.execute_script('return document.referrer')

    def sleep(self, seconds=0.25):
        time.sleep(seconds)

    def find_element_by_locator(self, locator):
        return self.driver.find_element_by_locator(locator)

    def find_elements_by_locator(self, locator):
        return self.driver.find_elements_by_locator(locator)

    def wait_for_available(self, locator, timeout_tries=80, sleep_interval=.25):
        for i in range(timeout_tries):
            if self.driver.is_element_available(locator):
                break
            self.sleep(sleep_interval)
        else:
            raise WaitForElementError('Wait for available timed out')
        return True

    def wait_for_visible(self, locator, timeout_tries=80, sleep_interval=.25):
        for i in range(timeout_tries):
            if self.driver.is_visible(locator):
                break
            self.sleep(sleep_interval)
        else:
            raise WaitForElementError('Wait for visible timed out')
        return True

    def wait_for_change(self, locator, text, timeout_tries=80, sleep_interval=.25):
        for i in range(timeout_tries):
            try:
                e = self.driver.find_element_by_locator(locator)
                if e is not None and text != e.text:
                    break
                self.sleep(sleep_interval)
            # except NoSuchElementException as e,StaleElementReferenceException as e:
            except:
                pass
        else:
            raise WaitForElementError('Wait for visible timed out')
        return True

    def wait_for_hidden(self, locator, timeout_tries=80, sleep_interval=.25):
        for i in range(timeout_tries):
            if self.driver.is_visible(locator):
                self.sleep(sleep_interval)
            else:
                break
        else:
            raise WaitForElementError('Wait for hidden timed out')
        return True

    def wait_for_alert(self, timeout_tries=80, sleep_interval=.25):
        for i in range(timeout_tries):
            try:
                alert = self.driver.switch_to_alert()
                if alert.text:
                    break
            except NoAlertPresentException as nape:
                pass
            self.sleep(sleep_interval)
        else:
            raise NoAlertPresentException(msg='Wait for alert timed out')
        return True

    def _dispatch(self, l_call, l_args, d_call, d_args):
        pass

    def open_and_wait_for_ready_state(self, page_url, timeout=10, sleep_interval=0.5):
        self.driver.get(page_url)
        self.wait_for_load(timeout=timeout, sleep_interval=sleep_interval)

    def wait_for_load(self, timeout=10, sleep_interval=0.25, ready_state='interactive'):
        """
        :param timeout:
        :param sleep_interval:
        :param ready_state: interactive, complete https://developer.mozilla.org/en-US/docs/Web/API/Document/readyState
        :return:
        """
        WebDriverWait(self.driver, timeout, sleep_interval) \
            .until(lambda d: d.execute_script('return document.readyState') == 'complete' or
                             d.execute_script('return document.readyState') == 'interactive')
