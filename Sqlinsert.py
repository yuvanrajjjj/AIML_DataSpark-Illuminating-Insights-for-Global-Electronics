import pandas as pd
import mysql.connector
from mysql.connector import Error

# Load the dataset
file_path = r'D:\Illuminating Insights for Global Electronics\Merged_Dataset1.csv'
df = pd.read_csv(file_path)

# Clean the DataFrame
df.columns = [col.replace(' ', '_').replace('$', '').replace('(', '').replace(')', '') for col in df.columns]

# Remove currency symbols and convert to numeric
df['Unit_Cost_USD'] = df['Unit_Cost_USD'].replace('[\$,]', '', regex=True).astype(float)
df['Unit_Price_USD'] = df['Unit_Price_USD'].replace('[\$,]', '', regex=True).astype(float)

# Convert date columns to ISO format, handling errors and missing values
def parse_dates(column, format):
    return pd.to_datetime(df[column], format=format, errors='coerce').dt.strftime('%Y-%m-%d')

df['Order_Date'] = parse_dates('Order_Date', '%d-%m-%Y')
df['Delivery_Date'] = parse_dates('Delivery_Date', '%d-%m-%Y')
df['Birthday'] = parse_dates('Birthday', '%d-%m-%Y')
df['Open_Date'] = parse_dates('Open_Date', '%d-%m-%Y')

# Check for any rows with invalid date parsing
print(df[['Order_Date', 'Delivery_Date', 'Birthday', 'Open_Date']].head())
print(df[['Order_Date', 'Delivery_Date', 'Birthday', 'Open_Date']].isnull().sum())

# MySQL connection details
host = 'localhost'
user = 'root'
password = '123456789'
database = 'Global'

# Function to create a connection
def create_connection():
    try:
        connection = mysql.connector.connect(host=host, user=user, password=password)
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to create a database if it does not exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cursor.execute(f"USE {database}")
        print(f"Database '{database}' selected")
    except Error as e:
        print(f"Error: {e}")

# Function to create the table
def create_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sales_data (
        OrderNumber INT,
        LineItem INT,
        OrderDate DATE,
        DeliveryDate DATE,
        CustomerKey INT,
        StoreKey INT,
        ProductKey INT,
        Quantity INT,
        CurrencyCode VARCHAR(10),
        Gender VARCHAR(10),
        Name VARCHAR(100),
        City VARCHAR(100),
        StateCode VARCHAR(10),
        StateX VARCHAR(100),
        ZipCode VARCHAR(10),
        CountryX VARCHAR(100),
        Continent VARCHAR(50),
        Birthday DATE,
        ProductName VARCHAR(100),
        Brand VARCHAR(50),
        Color VARCHAR(50),
        UnitCostUSD DECIMAL(10, 2),
        UnitPriceUSD DECIMAL(10, 2),
        SubcategoryKey INT,
        Subcategory VARCHAR(100),
        CategoryKey INT,
        Category VARCHAR(100),
        CountryY VARCHAR(100),
        StateY VARCHAR(100),
        SquareMeters DECIMAL(10, 2),
        OpenDate DATE
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print("Table created successfully")
    except Error as e:
        print(f"Error: {e}")

# Function to insert data into the table
def insert_data(connection, dataframe):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO sales_data (
        OrderNumber, LineItem, OrderDate, DeliveryDate, CustomerKey, StoreKey, ProductKey, Quantity,
        CurrencyCode, Gender, Name, City, StateCode, StateX, ZipCode, CountryX, Continent, Birthday,
        ProductName, Brand, Color, UnitCostUSD, UnitPriceUSD, SubcategoryKey, Subcategory, CategoryKey,
        Category, CountryY, StateY, SquareMeters, OpenDate
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = dataframe.fillna('').values.tolist()

    # Debugging output
    print(f"Number of columns in DataFrame: {len(dataframe.columns)}")
    print(f"Number of rows in DataFrame: {len(data)}")
    print(f"Number of values to insert per row: {len(data[0])}")

    # Inspect the first few rows of data
    print("Sample data rows:")
    for row in data[:5]:
        print(row)

    try:
        cursor.executemany(insert_query, data)
        connection.commit()
        print(f"{cursor.rowcount} rows inserted successfully")
    except Error as e:
        print(f"Error: {e}")
        # Print out the problematic data if available
        print(f"Error data: {data[0]}")

# Main script
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_database(conn)
        conn.database = database  # Switch to the newly created database
        create_table(conn)
        insert_data(conn, df)
        conn.close()
