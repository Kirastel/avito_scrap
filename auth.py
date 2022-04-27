import time
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()

# dusable web driver
options.add_argument("--disable-blink-features=AutomationControlled")

# driver = webdriver.Chrome(
#     executable_path='C:\\Users\\Марк\\Desktop\\avito scrap\\chromedriver.exe',
#     options=options
# )
driver = webdriver.Chrome(service=Service('C:\\Users\\Марк\\Desktop\\avito scrap\\chromedriver.exe'), options=options)


# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def autorisation(login=None, password=None):
    autorisation_url = 'https://www.avito.ru/#login?authsrc=h'
    try:
        driver.get(url=autorisation_url)

        login_input = driver.find_element(by=By.XPATH, value="//innput[@data-marker='login-form/login']")
        login_input.clear()
        login_input.send_keys(login)

        password_input = driver.find_element(by=By.XPATH, value="//innput[@data-marker='login-form/password']")
        password_input.clear()
        password_input.send_keys(password)

        login_button = driver.find_element(by=By.XPATH, value="//button[@data-marker='login-form/submit']").click()

        return True

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


autorisation(login='mylogin', password='mypassword')
