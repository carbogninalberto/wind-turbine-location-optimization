import csv
from datetime import datetime


start = datetime.timestamp(datetime.now())

with open('sudeste.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    cities = []
    lastcity = "0"
    wind_file = open("wind.csv","w")
    cities_file = open("cities.csv","w")
    for row in csv_reader:
        if line_count == 0:
            cities_file.write(row[0]+","+ row[1]+","+ row[2]+","+ row[3]+","+row[4]+","+row[5]+","+ row[6]+","+ row[7]+"\n")
            wind_file.write(row[0]+","+ row[9]+","+ row[13]+","+row[15]+","+row[19]+","+row[28]+"\n")
            line_count += 1
        else:
            #ignoring three cities: two are too far from the others and one has invalid coordinates
            if(row[0]!="418" and row[0]!="387" and row[0]!="178"):
                if (lastcity!=row[0]):
                    #when the id of the weather station changes it will add its data to the cities file
                    cities_file.write(row[0]+","+ row[1]+","+ row[2]+","+ row[3]+","+row[4]+","+row[5]+","+ row[6]+","+ row[7]+"\n")
                    lastcity=row[0]
                
                wind_file.write(row[0]+","+ row[9]+","+ row[13]+","+row[15]+","+row[19]+","+row[28]+"\n")
            line_count += 1
            
            if(line_count%1000000==0):
                print("processrd "+str(line_count)+" lines")

    print("executed in "+str(int(datetime.timestamp(datetime.now())-start))+" seconds")
