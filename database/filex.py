import pypyodbc
import struct
import json
from datetime import datetime, date
import decimal

print("running as {0}-bit".format(struct.calcsize("P") * 8))

def normalize(s):
    """A simple function to normalize table names"""
    return s.lower().replace(" ", "_")


conn = pypyodbc.connect(
     r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
    + r'Dbq=.\\mydb.accdb;'
)
cur = conn.cursor()
tables = []
for row in cur.tables(tableType="TABLE"):
    # Only get the table names
    tables.append(row[2])

# data will contain the data of all tables. It will have the following structure:
# {"table_1": [{"column_1": value, "column_2": value}, ...], "table_2": ...}
data = {}
# descriptions will have  a description of all the tables. It will have the following structure:
# [
#   {
#       "table_name": "table 1",
#       "fixed_table_name": "table_1",
#       "columns": [
#           {"name": "column_1", "fixed_name": "column_1","type": "str"},
#           {"name": "column_2", "fixed_name": "column_2","type": "int"},
# ]
descriptions = []

for table_name in tables:
    fixed_table_name = normalize(table_name)
    print(f"~~~~~~~~~~~~~{table_name} {fixed_table_name}~~~~~~~~~~~~~")
    q = f'SELECT * FROM "{table_name}"'
    description = {
        "table_name": table_name,
        "fixed_table_name": fixed_table_name,
        "columns": [],
    }
    descriptions.append(description)

    cur.execute(q)
    # Here we get the description of the columns of the table from the cursor; we'll use that to fill the description.columns list
    columns = cur.description
    for c in columns:
        description["columns"].append(
            {"name": c[0], "fixed_name": normalize(c[0]), "type": c[1].__name__}
        )

    print("")

    # And here we retrieve the data of the whole table
    # Notice we use some double for loop comprehension to 
    # create a json object with a column_name: value structure
    # for each row
    data[fixed_table_name] = [
        {normalize(columns[index][0]): column for index, column in enumerate(value)}
        for value in cur.fetchall()
    ]

cur.close()
conn.close()

# This is a function to serialize datetime and decimal objects 
# to json; without it the json.dump function will fail if the 
# results contain dates or decimals
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError("Type %s not serializable" % type(obj))


with open("..\\access_description.json", "w") as outfile:
    # Notice the default=json_serial 
    json.dump(descriptions, outfile, default=json_serial)

with open("..\\access_data.json", "w") as outfile:
    json.dump(data, outfile, default=json_serial)