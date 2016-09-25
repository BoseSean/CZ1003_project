import sqlite3
import json




def large_db():
    with open('airports.json') as json_data:
        d = json.load(json_data)
    cursor.execute('CREATE TABLE airport_info (id int, iata char(3), icao char(4), name varchar(40), country varchar(25),city varchar(25))')
    """CREATE TABLE airport_info (id int, iata char(3), icao char(4), name varchar(40),country varchar(25),city varchar(25),)"""
    air_id = 0
    for i in d:
        print(air_id)
        if d[i]["iata"] != "" and d[i]["iata"] != '%':
            command = 'INSERT INTO airport_info (id, iata, icao, name, country, city) VALUES (?,?,?,?,?,?)'
            para = (air_id, d[i]["iata"], d[i]["icao"], d[i]["name"].lower(), d[i]["country"].lower(), d[i]["city"].lower())
            cursor.execute(command, para)
            air_id += 1
            cursor.close()

def mini_db():
    with open('mini_airports.json') as json_data:
        d = json.load(json_data)
    cursor.execute('CREATE TABLE airport_info (id int, iata char(3), city varchar(30))')
    air_id = 0
    for categray in d:
        for i in d[categray]:
            data = i["data"].split('|')[0:2]
            city = data[0].lower()
            iata = data[1][-4:-1]
            command = 'INSERT INTO airport_info (id, iata, city) VALUES (?,?,?)'
            para = (air_id, iata, city)
            cursor.execute(command, para)
            air_id += 1
    cursor.close()






db_conn = sqlite3.connect('db.sqlite3')
cursor = db_conn.cursor()
mini_db()
db_conn.commit()
db_conn.close()