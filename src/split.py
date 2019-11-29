'''
BIO INSPIRED AI

Used fields:
Row: {
    wsid, 0
    wsnm, 1
    mdct, 8
    lat, 3
    lon, 4
    stp, 15
    temp, 19
    wdsp, 28

}

OUTPUT:
wsid,variable_name,pressure,temperature,wind_speed,roughness_length,temperature,wind_speed
height,0,2,10,0,10,80
2010-01-01 00:00:00+01:00,98405.7,267.6,5.32697,0.15,267.57,7.80697
2010-01-01 01:00:00+01:00,98382.7,267.6,5.46199,0.15,267.55,7.86199

0, 8, 15, 19, 28, {0.15}, 19, 28


418
'''
import os
import sys
import calendar
import time

def print_rows(rows):
    counter = 0
    for row in rows:
        counter += 1
        print("[", counter, ":", row.replace("\n", "").replace("\r", ""), "]")

# assuming an opened file in appen mode
def write_dataset(file, rows):
    for row in rows:
        file.write(row)

def write_windpowerlib_format(file, rows, header):
        file.write(header)
        for i in rows:
            row = i.split(",")
            val = float(row[28]) if row[28] != "" else 0.0           
           
            if val > 0.0:
                try:
                    kelvin = float(row[19])+273 # C to K
                    pressure = float(row[15])*100 # hPa to Pa
                    #data = str(row[0]) + "," + str(row[8]) + "," + str(pressure) + "," + str(kelvin) + "," + str(row[28]) + ",0.15," + str(kelvin) + "," + str(row[28]) + "\n"
                    data =  str(row[8]) + "," + str(pressure) + "," + str(kelvin) + "," + str(row[28]) + ",0.15," + str(kelvin) + "," + str(row[28]) + "\n"
                    file.write(data)
                except:
                    print("missing temp, skipped!")
                

if __name__ == "__main__":
    # settings inputs
    rows = [] # array that contains all the rows

    # timestamp
    ts = str(calendar.timegm(time.gmtime())) 

    # path to datasets
    path_dataset_windpowerlib = "../datasets/"+ts+"/dataset.csv"

    weather = "C:/Users/Alberto/Desktop/Progetto/hourly-weather-surface-brazil-southeast-region/sudeste.csv"

    # create export folder
    os.makedirs(os.path.dirname(path_dataset_windpowerlib), exist_ok=True)

    # open files
    dataset = open(weather, "r", encoding="utf8")

    # train file
    dataset_windpowerlib = open(path_dataset_windpowerlib, "a")

    # header
    #header = "wsid,variable_name,pressure,temperature,wind_speed,roughness_length,temperature,wind_speed\n" + "wsid,height,0,2,10,0,10,80\n"
    header = "variable_name,pressure,temperature,wind_speed,roughness_length,temperature,wind_speed\n" + "height,0,2,10,0,10,80\n"

    # load in memory
    counter = 0
    for row in dataset:
        if counter < 50000:
            rows.append(row)
            counter = counter + 1

    label = rows[0]
    del rows[0]
    

    write_windpowerlib_format(dataset_windpowerlib, rows, header)


    # close file
    dataset.close()
    dataset_windpowerlib.close()