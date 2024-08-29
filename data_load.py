import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "cell_data"
)
cursor = conn.cursor()

# creating overview table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cell_overview(
        cell_id INT PRIMARY KEY,
        discharge_capacity FLOAT,
        nominal_capacity FLOAT
    )
               
""")

# detailed data table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cell_data(
        cell_id INT,
        sheet_no INT,
        column_no INT,
        current_data FLOAT,
        voltage_data FLOAT,
        capacity_data FLOAT,
        temperature_data FLOAT,
        time_data DATETIME,
        PRIMARY KEY (cell_id, time_data)
    )
""")
# inserting overview data
overview_data = {
    5308 : {'discharge_capacity' : 2992.02, 'nominal_capacity' : 3000},
    5329 : {'discharge_capacity' : 2822.56, 'nominal_capacity' : 3000}
}

for cell_id, capacities in overview_data.items():
    discharge_capacity = capacities['discharge_capacity']
    nominal_capacity = capacities['nominal_capacity']
    cursor.execute(
        "INSERT INTO cell_overview (cell_id, discharge_capacity, nominal_capacity) VALUES (%s, %s, %s)",
        (cell_id, discharge_capacity, nominal_capacity)
    )

# inserting data into the detailed data table
def insert_cell_data(cell_id, sheet_no, column_no, current_data, voltage_data, capacity_data, temperature_data, time_data):
    cell_id = int(cell_id)
    sheet_no = int(sheet_no)
    column_no = int(column_no)
    current_data = float(current_data)
    voltage_data = float(voltage_data)
    capacity_data = float(capacity_data)
    temperature_data = float(temperature_data)

    cursor.execute("""
        SELECT COUNT(*) FROM cell_data WHERE cell_id = %s AND time_data = %s
    """, (cell_id, time_data))
    
    if cursor.fetchone()[0] == 0:  # No duplicate found
        cursor.execute(
            """INSERT INTO cell_data
            (cell_id, sheet_no, column_no, current_data, voltage_data, capacity_data, temperature_data, time_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (cell_id, sheet_no, column_no, current_data, voltage_data, capacity_data, temperature_data, time_data)
        )

  

files = ['./5308.xlsx', './5329.xlsx']
for file in files:
    cell_id = int(file.split('/')[-1].split('.')[0])

    df4 = pd.read_excel(file, sheet_name=3)
    df6 = pd.read_excel(file, sheet_name=5)

    for i in range(len(df4)):
        current_data = df4.iloc[i, 5]
        voltage_data = df4.iloc[i, 6]
        capacity_data = df4.iloc[i, 7]
        time_data = df4.iloc[i, 10]
        temperature_data = df4.iloc[i, 4]
       
        insert_cell_data(cell_id, 4, 6, current_data, voltage_data, capacity_data, temperature_data, time_data)

conn.commit()

cursor.close()
conn.close()