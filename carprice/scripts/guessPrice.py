import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carprice.settings")
django.setup()

def guess_price(carModel,year,milage):
    # get all data for that carModel from django db
    # learn base on data
    # guess the price
    # return price
    return f'{carModel} guessing price for {year} year and {milage} milage is 20000'    

