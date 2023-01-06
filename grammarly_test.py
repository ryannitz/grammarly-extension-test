from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import time

import constants
import selector_strings

def get_driver():
    chrome_options = Options()
    chrome_options.add_extension(constants.grammarly_extension_path)
    return webdriver.Chrome(options=chrome_options)

def before_all(driver):
    driver.get(constants.chrome_extensions_url)
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def input_text_and_await_grammarly(driver, input_str):
    driver.get(constants.word_counter_url)
    time.sleep(2)
    text_area = driver.find_element(By.ID, selector_strings.wc_text_area)
    text_area.send_keys(input_str)
    text_area.click()
    time.sleep(10)

def get_grammarly_suggested_correction_element(driver):
    grammarly_highlight = driver.execute_script(selector_strings.grammarly_highlight)
    a = ActionChains(driver)
    a.move_to_element(grammarly_highlight).perform()
    time.sleep(10)
    return driver.execute_script(selector_strings.grammarly_suggested_correction)

def test_grammarly_installed_and_active():
    driver = get_driver()
    before_all(driver)
    menu_bars = driver.execute_script(selector_strings.menu_bars)
    extension_list_container = driver.execute_script(selector_strings.extension_list_container)
    grammarly_card = driver.execute_script(selector_strings.grammarly_card)
    grammarly_card_check = driver.execute_script(selector_strings.grammarly_card_check)
    assert grammarly_card.is_displayed()
    assert extension_list_container.is_displayed()
    assert grammarly_card_check.get_attribute('class') == 'enabled'
    driver.quit()

def test_grammarly_correct_suggestion():
    driver = get_driver()
    before_all(driver)

    input_str = "Prtchy"
    expected_correction_str = "Patchy"
    input_text_and_await_grammarly(driver, input_str)
    grammarly_suggested_correction = get_grammarly_suggested_correction_element(driver)
    assert grammarly_suggested_correction.text == expected_correction_str
    driver.quit()

def test_grammarly_incorrect_suggestion():
    driver = get_driver()
    before_all(driver)

    input_str = "Boison"
    expected_correction_str = "Boisson"
    actual_correction_str = "Poison"
    input_text_and_await_grammarly(driver, input_str)
    grammarly_suggested_correction = get_grammarly_suggested_correction_element(driver)
    assert grammarly_suggested_correction.text != expected_correction_str
    assert grammarly_suggested_correction.text == actual_correction_str
    driver.quit()

def main():
    test_grammarly_installed_and_active()
    test_grammarly_correct_suggestion()
    test_grammarly_incorrect_suggestion()

if __name__ == '__main__':
    main()
