from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep


def check_exists_by_locator(locator):
    locator = locator.is_displayed()
    assert locator == bool(True), "element does not exist"
    return locator


def check_exists_by_text(locator, expected):
    locator = locator.text
    assert locator == expected, "element does not exist"


def test_task():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)

    driver.get("https://tbcpay.ge/")

    # ჰედერის ნავიგაცია:  ელემენტების არსებობა
    for i in range(2, 6):
        head_element = driver.find_element_by_xpath("//*[@class='container flex-start']/a[" + str(i) + "]")
        check_exists_by_locator(head_element)
    # სერვისების ნავიგაცია: ელემენტების არსებობა
    for i in range(2, 10):
        service_element = driver.find_element_by_xpath("//*[@class='flex-start']/ul/li[" + str(i) + "]/a")
        check_exists_by_locator(service_element)
    # საძიებო ველი ღილაკით „ძიება“  ელემენტის არსებობა
    search_input = driver.find_element_by_css_selector(".search-wrapper input")
    if check_exists_by_locator(search_input):
        # ძიების ველში 'მობილური' ჩაწერა
        search_input.send_keys("მობილური")
    # 'მობილური ბალანსის შევსება' ელემენტის არსებობა
    search_field = driver.find_element_by_css_selector(".search-wrapper ul")
    search_element = search_field.find_element_by_xpath("//*[text()='მობილური ბალანსის შევსება']")
    check_exists_by_locator(search_element)
    # 'მობილური ბალანსის შევსება' ელემენტზე დაჭერა
    search_element.click()
    # ბალანსის შევსების ელემენტების შემოწმება
    wait.until(EC.url_contains("mobiluri-balansis-shevseba"))
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "input-container")))
    balance_input = driver.find_element_by_xpath("//*[@class='input-container']//input[@type='tel']")
    # wait.until(EC.visibility_of(balance_input))
    check_exists_by_locator(balance_input)
    balance_button = driver.find_element_by_xpath("//button//span[text()='შემოწმება']")
    check_exists_by_locator(balance_button)
    # ნომრის შეყვანა და ღილაკზე დაჭერა
    balance_input.send_keys("555122334")
    balance_button.click()
    # სერვისის არჩევა და სიის შემოწმება
    wait.until(EC.invisibility_of_element(balance_button))
    service_input = driver.find_element_by_css_selector("label[title='აირჩიეთ სერვისი']")
    service_input.click()
    add_balance = driver.find_element_by_css_selector("#BONUS a[title='ბალანსის შევსება']")
    meti8 = driver.find_element_by_xpath("//*[@id='BONUS']/a//span[contains(text(),'- 8')]")
    meti10 = driver.find_element_by_xpath("//*[@id='BONUS']/a//span[contains(text(),'- 10')]")
    check_exists_by_locator(add_balance)
    check_exists_by_locator(meti8)
    check_exists_by_locator(meti10)
    #  "მეტი" - 10 ლ  არჩევა და არსებული ტექსტის შემოწმება
    meti10.click()
    sleep(5)
    actual_list = []
    spans = driver.find_elements_by_xpath("//div[@class='ded17e-0 iiRqkB']//span")

    for i in range(len(spans)):
        actual_list.insert(i, spans[i].text)
    expected_list = ["დავალიანება", "c", "თანხის ოდენობა", "c", "საკომისიო", "0.12", "c", "ჯამში გადასახდელი", "c",
                     "გადახდა", "სხვა გადახდის დამატება"]
    a = set(actual_list)
    b = set(expected_list)
    assert a == b, "this spans do not  exist"

    debt = driver.find_element_by_class_name("debt")
    check_exists_by_text(debt, "10.00 c")

    amount = driver.find_element_by_xpath("//*[@class='readOnly']").get_attribute("value")
    assert amount == "10"

    total_amount = driver.find_element_by_xpath("//*[@class='info']//b")
    check_exists_by_text(total_amount, "10.12 c")

    # გადახდა

    pay = driver.find_element_by_xpath("//*[@class='pay-btn sc-9g6oqq-0 goRuDt']")
    pay.click()

    wait.until(EC.invisibility_of_element(pay))

    # უნდა ჩაიტვირთოს გვერდი ახალი დომენზე: ecommerce.ufc.ge
    if "ecommerce.ufc.ge" in driver.current_url:
        print("new domain opened")
