
import glob
import os
import time

from tests.utils.html_element import HtmlElement


class PageBase:
  def __init__(self, selenium, test_case_id, sub_dir='', url=''):
    self._selenium = selenium
    self._driver = selenium.driver()
    self._wait_time = selenium.wait_time()

    self._test_case_id = test_case_id

    if sub_dir != '':
      self._url = self._to_url(sub_dir)

    if url != '':
      self._url = url

  def _to_url(self, sub_dir):
    return f"{os.environ['BASE_URL']}/{sub_dir}"

  def create_element(self, prop_name, selector):
    return HtmlElement(
        self._selenium,
        self._test_case_id,
        self.page_name(),
        prop_name,
        selector
    )

  def page_name(self):
    return self.__class__.__name__

  def open(self):
    self._driver.get(self._url)

  def screenshot(self, prefix, suffix, width=0, height=0):
    file_name = f"{prefix}_{self.page_name()}_{suffix}.png"
    screenshot_path = os.path.join(os.environ['DIR_NAME'], file_name)

    page_width = width
    if page_width == 0:
      page_width = self._driver.execute_script(
          'return document.body.scrollWidth')

    page_height = height
    if page_height == 0:
      page_height = self._driver.execute_script(
          'return document.body.scrollHeight')

    self._driver.set_window_size(page_width, page_height)
    self._driver.get_screenshot_as_file(screenshot_path)

  def wait_second(self, sec):
    time.sleep(sec)

  def wait_file_downloaded_with_file_prefix(self, file_name_prefix):
    for i in range(self._wait_time + 1):
      file_name = self.get_file_name_by_prefix(file_name_prefix)

      if file_name != '':
        return
      time.sleep(1)

    raise WaitDownloadFileTimeoutError('ファイルのダウンロードが完了しませんでした')

  def get_file_name_by_prefix(self, file_name_prefix):
    filenames = glob.glob(f'{os.environ["DIR_NAME"]}/*.*')
    files = list(filter(lambda filename: os.path.basename(
        filename).startswith(file_name_prefix), filenames))
    if len(files) == 0:
      return ''

    return os.path.basename(files[0])

  def rename_downloaded_file(self, old_file_name, new_file_name):
    old_full_path = os.path.join(os.environ['DIR_NAME'], old_file_name)
    new_full_path = os.path.join(os.environ['DIR_NAME'], new_file_name)
    os.rename(old_full_path, new_full_path)


class WaitDownloadFileTimeoutError(Exception):
  """
  ダウンロード完了待ちでタイムアウトが発生したことを知らせる例外クラス
  """
  pass
