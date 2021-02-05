
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select


class HtmlElement():
  def __init__(self, selenium, test_case_id, page_name, prop_name, selector):
    self._driver = selenium.driver()
    self._wait = selenium.waiter()
    self._test_case_id = test_case_id
    self._page_name = page_name
    self._prop_name = prop_name
    self._selector = selector

  def _element(self):
    elements = self._driver.find_elements_by_css_selector(self._selector)
    if len(elements) == 0:
      self._raise_element_not_found()

    return elements[0]

  def _raise_element_not_found(self):
    message = (
        '要素が見つかりませんでした\n'
        f'case: {self._test_case_id}\n'
        f'page: {self._page_name}\n'
        f'prop: {self._prop_name}\n'
        f'selector: {self._selector}'
    )
    raise ElementNotFoundError(message)

  def _wait_until(self, condition, func_name):
    try:
      self._wait.until(condition)
    except Exception as err:
      self._raise_wait_err(err, func_name)

  def _raise_wait_err(self, err, func_name):
    message = (
        '待機中にエラーが発生しました\n'
        f'case: {self._test_case_id}\n'
        f'page: {self._page_name}\n'
        f'prop: {self._prop_name}\n'
        f'selector: {self._selector}\n'
        f'func: {func_name}\n'
        f'exception: {err}'
    )
    raise WaitError(message)

  def text(self):
    """
    inner text を取得する
    """
    return self._element().text

  def get_attr(self, attr_name):
    """
    パラメータの属性値を取得する
    """
    return self._element().get_attribute(attr_name)

  def input(self, value):
    """
    パラメータのテキストを入力する
    """
    self._element().send_keys(value)

  def select_text(self, text):
    """
    対象のセレクトボックスでパラメータのテキストを選択する
    """
    Select(self._element()).select_by_visible_text(text)

  def select_index(self, index):
    """
    対象のセレクトボックスでパラメータのインデックスの要素を選択する
    """
    Select(self._element()).select_by_index(index)

  def click(self):
    """
    対象の要素をクリックする
    """
    element = self._element()
    self._driver.execute_script(
        f"window.scrollTo(0, {element.location['y']});")
    element.click()

  def wait_to_be_clickable(self):
    """
    対象の要素がクリック可能になるまで待機する
    """
    self._wait_until(
        expected_conditions.element_to_be_clickable(
            (By.CSS_SELECTOR, self._selector)),
        sys._getframe().f_code.co_name)

  def wait_to_be_visible(self):
    """
    対象の要素が表示されるまで待機する
    """
    self._wait_until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, self._selector)),
        sys._getframe().f_code.co_name)

  def wait_to_be_present_in_element(self, text):
    """
    対象の要素にパラメータのテキストが表示されるまで待機する
    """
    self._wait_until(
        expected_conditions.text_to_be_present_in_element(
            (By.CSS_SELECTOR, self._selector), text),
        sys._getframe().f_code.co_name)


class ElementNotFoundError(Exception):
  """
  要素が見つからなかった場合のエラー
  """
  pass


class WaitError(Exception):
  """
  待機処理で発生したエラー
  """
  pass
