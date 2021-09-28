import mysql.connector
import re
import csv
import time
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
start_time = time.time()

host = os.getenv('HOST_DB')
user = os.getenv('USER')
pwd = os.getenv('PWD_DB')
db = os.getenv('DB')

mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=pwd,
  database=db
)

mycursor = mydb.cursor()

mycursor.execute("SELECT id_cliente, phone FROM users WHERE phone IS NOT NULL")

myresult = mycursor.fetchall()

i = 1
while i < 15:
  extensao = ".csv"
  numeracao = str(i)

  caminho = "files/numeros-"
  with open((caminho + numeracao + extensao), 'r') as csv_file:
      csv_reader = csv.reader(csv_file)

      next(csv_reader)

      telefones_csv = []

      for line in csv_reader:
          telefones_csv.append(line[0])
  csv_file.close()

  caminho = "files/outputs/numeros-achados-"

  with open((caminho + numeracao + extensao), 'w', newline='', encoding='utf-8') as csv_file:
      fieldnames = ['id_cliente', 'telefone']
      csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')
      csv_writer.writeheader()
      for x in myresult:
          numero = re.sub("\D", "", x[1])
          id = x[0]
          if numero in telefones_csv:
            csv_writer.writerow({'id_cliente': id, 'telefone': numero})
  csv_file.close()
  print("--- %s segundos ---" % round(time.time() - start_time, 2))
  i += 1