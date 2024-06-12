import csv

colI = {
    "city":1,
    "country":2,
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
            
        i = i +1

            
print(UkCities)