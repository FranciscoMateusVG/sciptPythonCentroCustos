import pyodbc
import contextlib
import re

nomeArquivo = "custo_analitico"

print("Comecei")
with open(nomeArquivo, mode="r", encoding="utf8") as arquivo:

    string_list = arquivo.readlines()
    insertInto = 'INSERT INTO "{}" VALUES'.format(nomeArquivo)
    print(insertInto)
    for index, string in enumerate(string_list):
        string_list[index] = string.replace(
            "),", '\n').replace(
            insertInto, '').replace('(', '').replace(');', '').replace('null', '').replace('NULL', '')
        string_list[index] = re.sub(r'[A-Z],', '. ',  string_list[index])
        string_list[index] = re.sub(r'\'', '', string_list[index])

    with open("data.csv", "w+") as arquivo_convertido:
        new_file_contents = "".join(string_list)
        arquivo_convertido.write(new_file_contents)


print("Inicializando conexão")

connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=DESKTOP-PN08DBU;'
                            'Database=teste;'
                            'Trusted_Connection=yes;')

query = "BULK INSERT {} FROM 'C:\\Users\\Xerox to Xerox Xerox\\Desktop\\scriptPython\\data.csv' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', CODEPAGE = 'ACP')".format(
    nomeArquivo)
print(query)
with contextlib.closing(connection) as conn:
    with contextlib.closing(conn.cursor()) as cursor:
        cursor.execute(query)
    conn.commit()

print("Terminei")
