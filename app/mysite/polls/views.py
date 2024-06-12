from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import csv


colI = {
    "city":1,
    "country":2,
    "beer": 29,
    "1-bed-rent":53,
}

UkCities = []

# Open the CSV file in read mode
with open('C:/Users/schof/PeregrineHackathon/app/mysite/polls/cost-of-living.csv', 'r') as csvfile:
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
    
    print('hello')
    context = None
    
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # print(body)
        income = body['income'] * 1.28
        rentPercentage = body['rentPercentage']
        savingsPercentage = body['savingsPercentage']
        gymChecked = body['gymChecked']
        nightsOut = body['nightsOut']
        
        print(income)
        # print(rentPercentage)
        # print(savingsPercentage)
        # print(gymChecked)
        # print(nightsOut)    
            
        rentAmount = (income * rentPercentage) / 100
        savingsAmount = (income * savingsPercentage) / 100
        
        print(rentAmount/12)
        # print(savingsAmount)  
        
        results = []

        for row in UkCities:
            if row[colI["1-bed-rent"]] != '':
                if float(row[colI["1-bed-rent"]]) <= rentAmount/12:
                    line = [row[colI["city"]], row[colI["1-bed-rent"]]]
                    results.append(line)
                
        # print(results)   
        # print(len(results[0]))     
        context = {
            'city_name': results[0][0],
            'rent': results[0][1]#,
            # 'beer_price': results[0][2]
        }
        
        return render(request, 'polls/display.html',context)
        
    return render(request, 'polls/display.html',context)