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
    "1-bed-rent":53,
}

UkCities = []

#path = 'C:/Users/schof/PeregrineHackathon/app/mysite/polls/cost-of-living.csv'
path = 'C:/Users/TomSchofield/PeregrineHackathon/app/mysite/polls/cost-of-living.csv'
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
        income = body['income'] * 1.28
        rentPercentage = body['rentPercentage']
        savingsPercentage = body['savingsPercentage']
        gymChecked = body['gymChecked']
        nightsOut = body['nightsOut']
        
        print(income) 
            
        rentAmount = (income * rentPercentage) / 100
        savingsAmount = (income * savingsPercentage) / 100
        
        results = []

        for row in UkCities:
            if row[colI["1-bed-rent"]] != '':
                if float(row[colI["1-bed-rent"]]) <= rentAmount/12:
                    line = [row[colI["city"]], row[colI["1-bed-rent"]], row[colI["beer"]]]
                    results.append(line)
                
        context = {
            'city_name': results[0][0],
            'rent': results[0][1],
            'beer_price': results[0][2]
        }

        return render(request, 'polls/display.html', context)

