import csv

if __name__ == "__main__":
    '''
    print("insertCities.sql STARTED...!\n")
    # insertCities.sql from dataset
    #import file
    cities = open('cities.csv', 'r', encoding="utf8")
    insertCities = open('insertCities.sql', mode='w', encoding="utf8")
    #read file
    csvFile = csv.reader(cities)
    #dynamic headers
    header = next(csvFile)
    headers = map((lambda x: x), header)
    insert = 'INSERT INTO city (' + ", ".join(headers) + ") VALUES "
    #copy rows as insert statement
    counter = 0
    for row in csvFile:
        values = map((lambda x: "'"+x+"'"), row)
        #print (insert +"("+ ", ".join(values) +");" )
        if counter%20 == 0:
            print("insertCities.sql: " + str(counter) + " rows processed...\n")
        counter += 1
        insertCities.write(insert +"("+ ", ".join(values) +");\n")
    #close
    cities.close()
    insertCities.close()

    print("insertCities.sql COMPLETE!\n")
    '''

    print("insertWinds.sql STARTED...!\n")

    # insertWinds.sql from dataset
    #import file
    wind = open('wind.csv', 'r', encoding="utf8")
    insertWinds = open('insertWinds.sql', mode='w', encoding="utf8")
    #read file
    csvFile = csv.reader(wind)
    #dynamic headers
    header = next(csvFile)
    headers = map((lambda x: x), header)
    insert = 'INSERT INTO wind (' + ", ".join(headers) + ") VALUES "
    #copy rows as insert statement
    counter = 0
    tmpInsert = insert
    first = True
    for row in csvFile:
        values = map((lambda x: "'"+x+"'"), row)
        if first:
            tmpInsert = tmpInsert + "("+ ", ".join(values) +")"
            first = False
        else:
            tmpInsert = tmpInsert + ", ("+ ", ".join(values) +")"
        #print (insert +"("+ ", ".join(values) +");" )
        if counter%800000 == 0:
            print("insertCities.sql: " + str(counter) + " rows processed...\n")
        if counter%800 == 0:
            insertWinds.write(tmpInsert +";\n")
            tmpInsert = insert
            first = True
        
        counter += 1
        #insertWinds.write(insert +"("+ ", ".join(values) +");\n")
    #close
    insertWinds.write(tmpInsert +";\n")
    wind.close()
    insertWinds.close()

    print("insertWinds.sql COMPLETE!\n")

