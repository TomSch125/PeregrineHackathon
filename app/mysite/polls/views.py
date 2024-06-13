from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import csv



colI = {
    "city":1,
    "country":2,
    "beer": 29,
    "buss_p":33,
    "util":40,
    "internet":42,
    "gym":43,
    "rent-inner":52,
    "rent-outer":53,
}

UkCities = []

path = 'C:/Users/schof/PeregrineHackathon/app/mysite/polls/cost-of-living.csv'
# path = 'C:/Users/TomSchofield/PeregrineHackathon/app/mysite/polls/cost-of-living.csv'
# Open the CSV file in read mode
with open(path, 'r') as csvfile:
# Create a reader object
    csv_reader = csv.reader(csvfile)

    # Iterate through the rows in the CSV file
    for row in csv_reader:
        # Access each element in the row
        if row[colI["country"]] == "United Kingdom":
            UkCities.append(row)   

@csrf_exempt
def index(request):
    return render(request, 'polls/index.html')




@csrf_exempt
def display(request):
    
    context = None
    
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        request.session['form_body'] = body

        return JsonResponse({'redirect_url': reverse('display')})

    else:
        body = request.session.get('form_body', None)
        
        inner =  findInner(body)
        outer = findOuter(body)
        context = {
            "inner":inner,
            "outer":outer
        }

        return render(request, 'polls/display.html', context)


def findInner(body):
    cities = []
    
    income = body['income'] * 1.28
    rentPercentage = body['rentPercentage']
    savingsPercentage = body['savingsPercentage']
    gymChecked = body['gymChecked']
    transportChecked = body['transportChecked']
    nightsOut = body['nightsOut']            
    rentAmount = (income * rentPercentage) / 100
    savingsAmount = (income * savingsPercentage) / 100
    
    monthRent = rentAmount/12
    monthincome = income / 12
        
    for city in UkCities:
        total = (savingsAmount/12) + f_Num(city,colI["util"]) + f_Num(city,colI["rent-inner"]) + f_Num(city,colI["internet"])
        total = total + f_Num(city,colI["beer"])*nightsOut*3 # assume 3 drinks a night
        if(gymChecked):
            total = total + f_Num(city,colI['gym'])
            
        if(transportChecked):
            total = total + f_Num(city,colI['buss_p'])
            
        if total < monthincome:
            if monthRent > f_Num(city,colI["rent-inner"]) and f_Num(city,colI["rent-inner"]) != 0:
                instance = {
                    'city':city[colI["city"]],
                    'beer':f_Num(city,colI["beer"]),
                    'gym':f_Num(city,colI['gym']),
                    'gym_bool':False,
                    'rent':f_Num(city,colI["rent-inner"]),
                    'util':f_Num(city,colI["util"]),
                    'internet':f_Num(city,colI["internet"]),
                    'transport':f_Num(city,colI['buss_p']),
                    'transport_bool':False
                }
            
                if(gymChecked):
                    instance['gym_bool'] = True
                    
                if(transportChecked):
                    instance['transport'] = True
                    
                cities.append(instance)
    
    return cities                
            
        
    
def findOuter(body):
    cities = []
    
    income = body['income'] * 1.28
    rentPercentage = body['rentPercentage']
    savingsPercentage = body['savingsPercentage']
    gymChecked = body['gymChecked']
    transportChecked = body['transportChecked']
    nightsOut = body['nightsOut']            
    rentAmount = (income * rentPercentage) / 100
    savingsAmount = (income * savingsPercentage) / 100
    
    monthRent = rentAmount/12
    monthincome = income / 12
        
    for city in UkCities:
        total = (savingsAmount/12) + f_Num(city,colI["util"]) + f_Num(city,colI['rent-outer']) + f_Num(city,colI["internet"])
        total = total + f_Num(city,colI["beer"])*nightsOut*3 # assume 3 drinks a night
        if(gymChecked):
            total = total + f_Num(city,colI['gym'])
            
        if(transportChecked):
            total = total + f_Num(city,colI['buss_p'])
            
        if total < monthincome:
            if monthRent < f_Num(city,colI["rent-inner"]) and monthRent > f_Num(city,colI["rent-outer"]) and f_Num(city,colI["rent-inner"]) != 0 and f_Num(city,colI["rent-outer"]) != 0:
                instance = {
                    'city':city[colI["city"]],
                    'beer':f_Num(city,colI["beer"]),
                    'gym':f_Num(city,colI['gym']),
                    'gym_bool':False,
                    'rent':f_Num(city,colI["rent-outer"]),
                    'util':f_Num(city,colI["util"]),
                    'internet':f_Num(city,colI["internet"]),
                    'transport':f_Num(city,colI['buss_p']),
                    'transport_bool':False
                }
            
                if(gymChecked):
                    instance['gym_bool'] = True
                    
                if(transportChecked):
                    instance['transport'] = True
                    
                cities.append(instance)
    
    return cities   

def f_Num(city, index):
    if city[index] == '':
        return 0
    else:
        return float(city[index])
    
    

