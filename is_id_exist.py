import mysql.connector
import os
import time
from dotenv import load_dotenv, find_dotenv
import csv
load_dotenv(find_dotenv())
start_time = time.time()

host = os.getenv('HOST_DB_ERP')
user = os.getenv('USER_ERP')
pwd = os.getenv('PWD_DB')
db = os.getenv('DB_ERP')

mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=pwd,
  database=db
)

mycursor = mydb.cursor()

i = 40000

while i < 44481:

    query = "SELECT id FROM organizacoes WHERE id = " + str(i)
    mycursor.execute(query)

    myresult = mycursor.fetchall()
    if i == 1:
        with open("files/ids/ids.csv", 'a', newline='', encoding='utf-8') as csv_file:
            fieldname = ['id_cliente']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldname, delimiter='\t')
            csv_writer.writeheader()
        csv_file.close()
    if not myresult:
        with open("files/ids/ids.csv", 'a', newline='', encoding='utf-8') as csv_file:
            fieldname = ['id_cliente']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldname, delimiter='\t')
            csv_writer.writerow({'id_cliente': i})
        csv_file.close()
    if i % 1000 == 0:
        print("--- %s segundos ---" % round(time.time() - start_time, 2))
    i += 1

print("--- %s segundos ---" % round(time.time() - start_time, 2))

