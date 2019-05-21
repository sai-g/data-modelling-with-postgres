## Data Modelling with Postgres

This project is developed to help the app Sparkify to analyze the data collected on their music streaming app. 
Basically, we are provided with the analytics of songs & user activity on their app. Our objective is to help the 
analytics team in build an ETL pipeline to load data from JSON metadata to PostGres database. I have followed star 
schema to define fact and dimension tables

#### Database Schema diagram
 
![alt text][logo]

[logo]: sparkifydb.png "SparkifyDB schema"


#### Project Structure
`create_tables.py` -> To create all the necessary tables in Postgres database
`etl.ipynb`        -> Steps to follow in developing ETL pipeline 
`etl.py`           -> ETL Pipeline implementation to load metadata from JSON files
`sql_queries.py`   -> All the SQL statements (SELECT/INSERT/DROP) 
`test.ipynb`       -> Test file to verify creating tables in Postgres is working as expected

### Getting Started

#### Create Tables
`python create_tables.py -> all the necessary tables will be created`
#### Running ETL pipleline
`python etl.py -> all the database tables will be populated with data from JSON files`
 