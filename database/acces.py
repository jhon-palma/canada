import pypyodbc, pyodbc

pypyodbc.lowercase = False
conn = pypyodbc.connect(
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
    + r'Dbq=.\\mydb.accdb;'
)
cur = conn.cursor()

for row in cur.tables(tableType="TABLE"):
    print(row)

# conn_str = (
#     r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
#     r'DBQ=.\\mydb.accdb;'
#     )
# cnxn = pyodbc.connect(conn_str)
# crsr = cnxn.cursor()
# for table_info in crsr.tables(tableType='TABLE'):
#     print(table_info.table_name)