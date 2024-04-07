import os
import sys
import django
# import time
import re
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from singleCarPageScrapping import getOneCarInfo

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carprice.settings")
    django.setup()

    # now you have access to your models
    from scrapping.serializers import CarSerializer
    from scrapping.models import Car
    
    
    def getAllListInfo(carFactory,carModel):
        
        # request and get data for the first page
        model=carFactory+'/'+carModel
        listingPageDomain = f'https://www.truecar.com/used-cars-for-sale/listings/{model}/'
        # enable headless mode in Selenium
        options = Options()
        options.add_argument('--headless=new')
        options.page_load_strategy = 'none'
        options.add_argument('--window-size=800,600')
        driver = webdriver.Chrome(
        options=options, 
            # other properties...
        )

        # visit your target site
        driver.get(listingPageDomain)
        #wait 5 second to ensure page loads
        # time.sleep(5)
        element = WebDriverWait(driver,30).until(
            EC.visibility_of_any_elements_located((By.XPATH, '//*[@id="mainContent"]/div/div[3]/div[1]/div/div/div[3]/nav/ul/li[12]/a')))
        # start from page one
        page = 1
        # checking for number of pages
        numberOfPages = int(driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[3]/div[1]/div/div/div[3]/nav/ul/li[12]/a').text)
        print(f'Total listing pages: {numberOfPages}')
        for page in range(16,numberOfPages+1):
            if page > 1 :
                nextListingPageDomain = f'https://www.truecar.com/used-cars-for-sale/listings/{model}/?page={page}'
                driver.get(nextListingPageDomain)
                element = WebDriverWait(driver,30).until(EC.visibility_of_any_elements_located((By.XPATH, '//*[@id="mainContent"]/div/div[3]/div[1]/div/div/div[1]/div/h2/span[1]')))
                                                                                                           
            cards = driver.find_elements(By.CSS_SELECTOR, 'a[ data-test = "vehicleCardLink" ]')
            print(f'Now getting information of page {page} of {numberOfPages}')
            print(f'In this page we have {len(cards)} cards of car')
            
            for card in cards :
                carSinglePageDomain=card.get_attribute("href")
                # finding vin number by domain
                vinMatch = re.search(r'listing\/(.{17})\/',carSinglePageDomain)
                vin = vinMatch.group(1)
                # checking that the car is not exist in django model,if the car does not exist ,getting car information
                carInfo = Car.objects.filter(vin = vin).exists()
                # if car does not exist in data base save new car Info
                if not(carInfo):
                    # run seleniumScrapping file to get information
                    mileage, price, package, year = getOneCarInfo(carSinglePageDomain,carModel)
                    # checking for getting mileage and price properly
                    if mileage == False or price == False or package == False:
                        continue
                    
                    #prepare data for data base 
                    data = {'vin':vin,'model':carModel,'package':package,'year':year,'mileage':mileage,'price':price}

                    # print sample of data 
                    print(vin,carModel,package,year,mileage,price)

                    # saving data to django car model
                    serializer = CarSerializer(data=data)
                    serializer.is_valid()
                    serializer.validated_data
                    serializer.save()

        # release the resources allocated by Selenium and shut down the browser
        driver.quit()
        return 'sucssess'
    
    #https://www.truecar.com/used-cars-for-sale/listings/mercedes-benz/g-class/
    getAllListInfo('mercedes-benz','g-class')





