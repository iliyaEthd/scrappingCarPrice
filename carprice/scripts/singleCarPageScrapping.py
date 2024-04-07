import re
# import time
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getOneCarInfo(domain,carModel):
    # domain => 'https://www.truecar.com/used-cars-for-sale/listing/WDCYC3HFXFX238727/2015-mercedes-benz-g-class/?sponsoredSourceType=marketplace&sponsoredVehiclePosition=0&zipcode=85251'
    # enable headless mode in Selenium
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=800,600')
    options.page_load_strategy = 'none'
    driver = webdriver.Chrome(
        options=options, 
        # other properties...
    )

    # visit your target site
    driver.get(domain)

    # wait up to 120 seconds until there is the title of car presented in screen
    try:
        # time.sleep(10)
        element = WebDriverWait(driver,120).until(
            EC.visibility_of_any_elements_located((By.XPATH, '//*[@id="mainContent"]/div[1]/div[2]/div[1]/h1/div[1]')))
    except:
        driver.quit()
        return False, False, False, False
    
    # scraping logic...
    # finding year by domain
    yearMatch = re.search(r'\/(\d{4})-',domain)
    year = yearMatch.group(1)
    # finding mileage
    try:
        mileage = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div').text
        mileage = int(''.join(mileage.split(' ')[0].split(',')))
    except:
        mileage = False
    # finding price
    try:
        price =  driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div/div/div[1]').text
        price = int(''.join(price[1:].split(',')))
    except:
        price = False
    #finding package
    try:
        package = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[1]/div[2]/div[1]/h1/div[1]').text
        package = list(map(lambda x:x.lower(),package.split(' ')))
        indexOfCarModel = package.index(carModel)
        package = ' '.join(package[indexOfCarModel+1 :])
    except:
        package = False
    # release the resources allocated by Selenium and shut down the browser
    driver.quit()
    
    return mileage, price, package, year
    