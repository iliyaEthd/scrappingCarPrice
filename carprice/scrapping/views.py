from django.shortcuts import render
from rest_framework import generics
from scrapping.models import Car
from scrapping.serializers import CarSerializer
from scripts.guessPrice import guess_price


# Create your views here.
class InfoList(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

  
def guess(request):
    #call function 
    context = {"gussed_price": '---'}
    if request.method == "POST":
        model = request.POST.get('model')
        year = request.POST.get('year')
        mileage = request.POST.get('milage')
        result= guess_price(model,year,mileage)
        context = {"gussed_price": result}
    return render(request, "scrapping/form.html", context)