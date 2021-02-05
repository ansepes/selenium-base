import os
import sys
from tests.utils.page_base import PageBase

TEST_ID = '001'


class TestSample:

  def test_login_pc(self, selenium):
    # - ドライバーの初期化
    selenium.build_pc_driver()

    # - 環境変数の読み込み
    user_id = os.environ['LOGIN_ID']
    pswd = os.environ['PASSWORD']

    page = LoginPagePC(selenium)
    page.open()

    # - headlessモードのON/OFFでHTML要素が変わるため、try exceptで分岐
    try:
      # - headlessモードの場合
      # - ユーザーIDの入力
      page.user_name_next_btn_headless().wait_to_be_clickable()
      page.user_name().input(user_id)
      page.screenshot('01_user')
      page.user_name_next_btn_headless().click()
      # - パスワードの入力
      page.password_next_btn_headless().wait_to_be_clickable()
      page.password_headless().input(pswd)
      page.screenshot('02_pass')
      page.password_next_btn_headless().click()
    except Exception:
      # - not headlessモードの場合
      # - ユーザーIDの入力
      page.user_name_next_btn().wait_to_be_clickable()
      page.user_name().input(user_id)
      page.screenshot('01_user')
      page.user_name_next_btn().click()
      # - パスワードの入力
      page.password_next_btn().wait_to_be_clickable()
      page.password().input(pswd)
      page.screenshot('02_pass')
      page.password_next_btn().click()

    # - メール画面の表示
    page.mail_page_header().wait_to_be_clickable()
    page.screenshot('03_mail_list')


class LoginPagePC(PageBase):
  def __init__(self, selenium):
    super().__init__(selenium,
                     TEST_ID,
                     url='http://mail.google.com/mail/?logout&hl=ja')

  def screenshot(self, suffix, width=0, height=0):
    return super().screenshot(self._test_case_id,
                              suffix, width=width, height=height)

  def user_name(self):
    return self.create_element(
        sys._getframe().f_code.co_name,
        'input[type="email"]'
    )

  def user_name_next_btn_headless(self):
    return self.create_element(
        sys._getframe().f_code.co_name,
        '#next'
    )

  def user_name_next_btn(self):
    return self.create_element(
        sys._getframe().f_code.co_name,
        '#identifierNext > div > button > div.VfPpkd-RLmnJb'
    )

  def password_headless(self):
    return self.create_element(
        sys._getframe().f_code.co_name,
        '#password'
    )

  def password(self):
    return self.create_element(
        sys._getframe().f_code.co_name,
        '#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input'
    )

  def password_next_btn_headless(self):
    return self.create_element(
        sys._getframe().f_code.co_name,
        '#submit'
    )

  def password_next_btn(self):
    return self.create_element(
        sys._getframe().f_code.co_name,
        '#passwordNext > div > button > div.VfPpkd-RLmnJb'
    )

  def mail_page_header(self):
    return self.create_element(
        sys._getframe().f_code.co_name,
        '#gb > div.gb_Ld.gb_5d.gb_Ud > div.gb_Kd.gb_Zc.gb_0c > div.gb_oc > div > a'
    )


class MailPagePC(PageBase):
  def __init__(self, selenium):
    super(selenium, url='http://mail.google.com/mail/?ui=html&zy=e')
    selenium.build_pc_driver()
