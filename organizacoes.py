import mysql.connector
import csv
import time
import os
from dotenv import load_dotenv, find_dotenv
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

extensao = ".csv"
i = 1
while i < 15:
    caminho = "files/outputs/numeros-achados-"
    numeracao = str(i)
    with open((caminho + numeracao + extensao), 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        next(csv_reader)

        ids = []

        for line in csv_reader:
            fields = line[0].split("\t")
            ids.append(fields[0])
    csv_file.close()
    caminho = "files/organizacoes/organizacoes"
    clientes = []
    for id in ids:
        id = str(id)
        query = "SELECT id, tipo_cliente, tipo_prospect, razao_social, data, telefone FROM organizacoes WHERE id =" + id
        mycursor.execute(query)

        clientes.append(mycursor.fetchall())
   
    with open((caminho + extensao), 'a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['id_cliente', 'tipo_cliente', 'tipo_prospect', 'razao_social', 'data', 'telefone']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')
        csv_writer.writeheader()
        for cliente in clientes:
            if cliente:
                csv_writer.writerow({'id_cliente': cliente[0][0], 'tipo_cliente': cliente[0][1], 'tipo_prospect': cliente[0][2], 'razao_social': cliente[0][3], 'data': cliente[0][4], 'telefone': cliente[0][5]})
    csv_file.close()
    print("--- %s segundos ---" % round(time.time() - start_time, 2))
    i += 1