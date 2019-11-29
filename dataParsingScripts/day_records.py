import os
import sys
import calendar
import time

def write_windpowerlib_format(file, rows, header):
        file.write(header)
        current = ['', '', 0]
        for i in rows:
            row = i.split(",")
            date = row[1].split(" ")[0]
            wsid = str(row[0])
            if current[1] != '' and date == current[1] and current[0] != '' and wsid == current[0]:
                current[2] = current[2] + 1
            else if current



            current = current if (current != '' and date == current ) else date

            if val > 0.0:
                data = str(row[0]) + "," + str(row[8]) + "," + str(row[15]) + "," + str(row[19]) + "," + str(row[28]) + ",0.15," + str(row[19]) + "," + str(row[28]) + "\n"
                file.write(data)

if __name__ == "__main__":
    # settings inputs
    rows = [] # array that contains all the rows

    # timestamp
    ts = str(calendar.timegm(time.gmtime())) 

    # path to datasets
    path_dataset_windpowerlib = ts+"_elaborated.csv"

    weather = "../1574881506/dataset.csv"

    # create export folder
    os.makedirs(os.path.dirname(path_dataset_windpowerlib), exist_ok=True)

    # open files
    dataset = open(weather, "r", encoding="utf8")

    # train file
    dataset_windpowerlib = open(path_dataset_windpowerlib, "a")

    # header
    header = "wsid, date, counter\n"

    # load in memory
    for row in dataset:
        rows.append(row)

    del rows[0]
    del rows[0]

    write_windpowerlib_format(dataset_windpowerlib, rows, header)

    # close file
    dataset.close()
    dataset_windpowerlib.close()