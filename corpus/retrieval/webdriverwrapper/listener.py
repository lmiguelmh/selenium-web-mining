# based on https://github.com/dakotasmith/page-object-examples

from selenium.webdriver.support.events import AbstractEventListener
import subprocess


class WebDriverEventListener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        print("Before navigate to %s" % url)
        # pass

    def after_navigate_to(self, url, driver):
        print("After navigate to %s" % url)
        # pass

    def before_quit(self, driver):
        # print("Quitting Selenium")
        # subprocess.call(['say', '"quitting selenium!!!"'])
        pass

    def before_find(self, by, value, driver):
        # print("looking by %s for %s" % by, value)
        # subprocess.call('say "looking by {0} for {1}"'.format(by, value).split())
        pass

    def before_click(self, element, driver):
        # print("clicking on %s tag" % element.tag_name)
        # subprocess.call('say "clicking on a {0} tag"'.format(element.tag_name, element.text).split())
        pass

