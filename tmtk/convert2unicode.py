
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
tqdm.monitor_interval = 0
logger = logging.getLogger(__name__)


class Converter():
    options = webdriver.ChromeOptions()
    options.add_argument(
        '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25')
    options.add_argument('--headless')

    driver = webdriver.Chrome(
        # executable_path="/u02/work/corpus/crawl_holvoo/chromedriver/chromedriver",
        chrome_options=options)

    text = "asdf"

    js_get_text = """
    return (function() {
    return document.getElementById('outPutTraditonalM_ID').innerText
    })();
    """

    js_set_text = """
    return (function(text) {
    document.getElementById('inputCyrillic_ID').innerHTML=text
    })(arguments[0]);
    """

    def __init__(self):
        self.driver.get("http://mtg.mglip.com/")
        self.driver.implicitly_wait(5)

    def quit(self):
        self.driver.quit()
    #driver is a webdriver instance

    def _get_text(self):
        try:
            el = self.driver.find_element_by_css_selector(
                "#outPutTraditonalM_ID")
            if not el.text:
                return ""
            return el.text
        except:
            return None

    def _input_text(self, text):
        try:
            self.driver.execute_script(self.js_set_text, text)
            btn = self.driver.find_element_by_css_selector("#ButtonTran_ID")
            btn.send_keys(Keys.ENTER)
            return True
        except Exception:
            return False

    def convert2unicode(self, text):
        input_text_success = False
        count = 0
        while not input_text_success and count < 3:
            input_text_success = self._input_text(text)
            self.driver.implicitly_wait(5)
            count += 1

        if not input_text_success:
            return None

        text = None
        count = 0
        while text is None and count < 3:
            self.driver.implicitly_wait(5)
            text = self._get_text()
            count += 1
        return text
