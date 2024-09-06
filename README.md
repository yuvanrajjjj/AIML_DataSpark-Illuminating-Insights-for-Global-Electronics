# AIML_DataSpark-Illuminating-Insights-for-Global-Electronics
Prerequisites
#Python 3.x: Ensure you have Python installed.
#MySQL: Ensure MySQL is installed and running on your system.
#Power BI: Required to open and view the .pbix file.
Python Packages
Install the required Python packages by running:


pip install pandas mysql-connector-python
MySQL Configuration
Ensure you have MySQL running locally with the following credentials (adjust if needed):

Host: localhost
User: root
Password: 123456789
Database: Global
Preprocessing the Data
Run the preprocess.py script to load, clean, and merge the datasets:


#python preprocess.py
This script will:

Load data from CSV files.
Handle missing values and data type conversions.
Merge the datasets into a single DataFrame.
Save the cleaned data to Merged_Dataset1.csv.
Inserting Data into MySQL
After preprocessing, run the sqlInsert.py script to insert the cleaned data into a MySQL database:

#python sqlInsert.py
This script will:

Create a connection to MySQL.
Create the Global database (if not already present).
Create the sales_data table.
Insert the cleaned data into the table.
Power BI Analysis
The Global_electronic.pbix file contains the Exploratory Data Analysis (EDA) performed using Power BI. Open this file with Power BI to explore the visualizations and insights generated.

Debugging and Troubleshooting
Common Issues
Database Connection Error: Ensure that MySQL is running and the credentials in sqlInsert.py match your local setup.
File Paths: Ensure the file paths in preprocess.py and sqlInsert.py match the location of your datasets.
License
This project is licensed under the MIT License - see the LICENSE file for details.
