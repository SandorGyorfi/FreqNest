import psycopg2
import json
import os

# Get credentials from environment variables
dbname = os.environ.get('DB_NAME')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')

# Connect to your database
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host
)
cursor = conn.cursor()

# Load and insert data from 'categories.json'
with open('synths\\fixtures\\categories.json', 'r') as file:
    categories_data = json.load(file)

# Insert data into the category table
for item in categories_data:
    cursor.execute("INSERT INTO synths_category (id, name, friendly_name) VALUES (%s, %s, %s)", 
                   (item['pk'], item['fields']['name'], item['fields']['friendly_name']))

# Load and insert data from 'synths.json'
with open('synths\\fixtures\\synths.json', 'r') as file:
    synths_data = json.load(file)

# Insert data into the synth table
for item in synths_data:
    # Replace column names with those in your synths_product table
    cursor.execute("INSERT INTO synths_product (name, description, price, category_id, image_url) VALUES (%s, %s, %s, %s, %s)", 
                   (item['fields']['name'], item['fields']['description'], item['fields']['price'], item['fields']['category'], item['fields']['image_url']))

# Commit and close
conn.commit()
cursor.close()
conn.close()
