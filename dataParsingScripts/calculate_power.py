import csv
from datetime import datetime
from windpowerlib.modelchain import ModelChain
from windpowerlib.wind_turbine import WindTurbine
from windpowerlib import wind_turbine as wt
import os
import pandas as pd
import json

from multiprocessing import Process

def get_weather_data(filename='./weather.csv', **kwargs):
    if 'datapath' not in kwargs:
        kwargs['datapath'] = os.path.dirname(__file__)
    file = os.path.join(kwargs['datapath'], filename)
    # read csv file
    weather_df = pd.read_csv(file, index_col=0, header=[0, 1])
    l0 = [_[0] for _ in weather_df.columns]
    #print('l0: ' + str(l0))
    l1 = [int(_[1]) for _ in weather_df.columns]
    #print('l1: ' + str(l1))
    weather_df.columns = [l0, l1]

    return weather_df


class CalculatePower (Process):
   def __init__(self, number, turbine, modelchain_data):
      Process.__init__(self)
      self.input_file = number
      self.turbine=turbine
      self.modelchain_data=modelchain_data

   def run(self):
      print ("Thread " + str(self.input_file))
      weather = get_weather_data(filename="weather"+str(self.input_file)+".csv")
      #print(weather[['wind_speed', 'temperature', 'pressure']][0:3])

      # initialize WindTurbine object
      t = WindTurbine(**self.turbine)

      # initialize ModelChain with own specifications and use run_model method to
      # calculate power output
      mc_t = ModelChain(t, **self.modelchain_data).run_model(weather)
      # write power output time series to WindTurbine object
      t.power_output = mc_t.power_output

      power_file = open("power"+str(self.input_file)+".csv","w")
      power_file.write(t.power_output.to_csv())
      print("Thread "+str(self.input_file) +" finished")





def create_weather_csv(input_filename, output_filename):
    header = "variable_name,pressure,temperature,wind_speed,roughness_length,temperature,wind_speed\n" + "height,0,2,10,0,10,80\n"
    index=0
    output_file = open(output_filename+str(index)+".csv","w")
    output_file.write(header)

    with open(input_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        counter=0

        for row in csv_reader:
            if line_count == 0:
                line_count+=1
            else:
                if(row[0]!="366" and row[0]!="369" and row[0]!="386" and row[0]!="391" and row[0]!="367" and row[0]!="390" and row[0]!="368"):

                    try:
                        temperature = float(row[4])
                        pressure = float(row[3])
                        wind_speed = float(row[5])
                        if(temperature>0 and pressure>0 and wind_speed>0):
                            temperature = temperature + 273
                            pressure = pressure * 100

                            data =  row[0] + " " + row[1] + " " + row[2] + "," + str(pressure) + "," + str(temperature) + "," + str(wind_speed) + ",1," + str(temperature) + "," + str(wind_speed) + "\n"
                            output_file.write(data)
                            line_count+=1
                    except:
                        #print("failed to convert line "+str(row))
                        pass

                    if(line_count%9000000==0):
                        print("reached limit of 9000000")
                        break
                    if(line_count%1000000==0):
                        print("processed "+str(line_count)+" lines")
                        index+=1
                        output_file = open(output_filename+str(index)+".csv","w")
                        output_file.write(header)






if __name__ == "__main__":

    start = datetime.timestamp(datetime.now())
    weather = "weather"
    all_files = True
    for i in range(8):
        if(not os.path.exists(weather+str(i)+".csv")):
            all_files=False

    if(not all_files):
        print("creating file "+weather)
        create_weather_csv("wind.csv",weather)

    for i in range(8):
        if(not os.path.exists("power"+str(i)+".csv")):
            all_files=False

    turbine_conf_file=open("turbine.json","r")
    turbine_conf=json.load(turbine_conf_file)
    turbine=turbine_conf[0]
    print("Loaded model "+turbine["turbine_type"])
    modelchain=turbine_conf[1]
    if(modelchain["density_correction"]=="True"):
        modelchain["density_correction"]=True
    else:
        modelchain["density_correction"]=False

    if(not all_files):
        threads=[]
        for i in range(8):
            threads.append(CalculatePower(i, turbine, modelchain))
            threads[i].start()
        for i in range(8):
            threads[i].join()


    city="0"
    counter=0
    sum=0.0
    mean=[]
    for i in range(8):
        power_file=open("power"+str(i)+".csv", "r")
        csv_reader = csv.reader(power_file, delimiter=',')
        for row in csv_reader:
            row_city=row[0].split(" ")[0]
            if(city=="0"):
                city=row_city
            if(city!=row_city):
                if(counter!=0):
                    sum=sum/counter
                    mean.append({"wsid":city, turbine["turbine_type"]:sum})
                else:
                    print("division by zero")
                city=row_city
                sum=float(row[1])
                counter=0
            else:
                sum+=float(row[1])
                counter+=1

    data=None
    if(os.path.exists("mean_power.json")):
        mean_power_file=open("mean_power.json", "r")
        data=json.load(mean_power_file)
        for i in range(len(mean)):
            for element in data:
                if(element["wsid"] == mean[i]["wsid"]):
                    element[turbine["turbine_type"]]=mean[i][turbine["turbine_type"]]
        mean_power_file.close()


    if(not data is None):
        mean=data
    mean_power_file=open("mean_power.json", "w")
    json.dump(mean, mean_power_file, indent=4)

    print("executed in "+str(int(datetime.timestamp(datetime.now())-start))+" seconds")
