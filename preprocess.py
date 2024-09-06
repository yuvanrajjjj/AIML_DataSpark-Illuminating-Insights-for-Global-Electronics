import pandas as pd
#from sqlalchemy import create_engine

# Load data
customers_df = pd.read_csv(r'D:\Illuminating Insights for Global Electronics\dataset\Customers.csv', encoding='ISO-8859-1')
exchange_rates_df = pd.read_csv(r'D:\Illuminating Insights for Global Electronics\dataset\Exchange_Rates.csv')
products_df = pd.read_csv(r'D:\Illuminating Insights for Global Electronics\dataset\Products.csv')
sales_df = pd.read_csv(r'D:\Illuminating Insights for Global Electronics\dataset\Sales.csv')
stores_df = pd.read_csv(r'D:\Illuminating Insights for Global Electronics\dataset\Stores.csv')

# Display the first few rows of each dataset
print(customers_df.head())
print(exchange_rates_df.head())
print(products_df.head())
print(sales_df.head())
print(stores_df.head())

# Get the number of observations (rows) and variables (columns) for each dataset
print(f"Customers: {customers_df.shape}")
print(f"Exchange Rates: {exchange_rates_df.shape}")
print(f"Products: {products_df.shape}")
print(f"Sales: {sales_df.shape}")
print(f"Stores: {stores_df.shape}")

# Check the data types of each dataset
print(customers_df.dtypes)
print(exchange_rates_df.dtypes)
print(products_df.dtypes)
print(sales_df.dtypes)
print(stores_df.dtypes)

# Check for missing values
print(customers_df.isnull().sum())
print(exchange_rates_df.isnull().sum())
print(products_df.isnull().sum())
print(sales_df.isnull().sum())
print(stores_df.isnull().sum())

# Convert data types
customers_df['Birthday'] = pd.to_datetime(customers_df['Birthday'])
sales_df['Order Date'] = pd.to_datetime(sales_df['Order Date'])
sales_df['Delivery Date'] = pd.to_datetime(sales_df['Delivery Date'])
exchange_rates_df['Date'] = pd.to_datetime(exchange_rates_df['Date'])
stores_df['Open Date'] = pd.to_datetime(stores_df['Open Date'])

# Handle missing values (example: fill with mean/mode or drop)
customers_df.fillna(customers_df.mode().iloc[0], inplace=True)
sales_df.fillna(sales_df.mode().iloc[0], inplace=True)
exchange_rates_df.fillna(exchange_rates_df.mode().iloc[0], inplace=True)
products_df.fillna(products_df.mode().iloc[0], inplace=True)
stores_df.fillna(stores_df.mode().iloc[0], inplace=True)

# Merge datasets

sales_customers = pd.merge(sales_df, customers_df, on='CustomerKey', how='left')
sales_products = pd.merge(sales_customers, products_df, on='ProductKey', how='left')
sales_products_stores = pd.merge(sales_products, stores_df, on='StoreKey', how='left')

sales_products_stores_cleaned = sales_products_stores.dropna()

# Save or use the final_data DataFrame
print('Missing values',sales_products_stores_cleaned.isnull().sum())

sales_products_stores_cleaned.to_csv('Merged_Dataset1.csv', index=False)

