import os
import sys
import django
from openpyxl import Workbook
from openpyxl.styles import Font

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carprice.settings")
    django.setup()

    # now you have access to your models
    from scrapping.models import Car
    
    # getting all cars information from database
    all_cars = Car.objects.all()
    
    #creating workbook and worksheet to append data in exel file
    wb = Workbook()
    ws = wb.active
    ws.title = "Cars Info"
    
    # adding sheet headers
    headersList = ['id','vin', 'model', 'package', 'mileage', 'price']
    ws.append(headersList)
    # adding bold font size to first row (header)
    ft = Font(bold=True)
    for cell in ws[1]:
        cell.font = ft
        
        
    # adding cars information as each row in sheet
    for car in all_cars:
        car = [car.id , car.vin , car.model ,car.package,car.mileage,car.price,]
        ws.append(car)
        
    #save work book on given url
    wb.save('carsInfo.xlsx')