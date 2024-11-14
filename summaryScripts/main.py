from pymongo import MongoClient
import mysql.connector
from environs import Env
import schedule
import time

#init env
env = Env()
env.read_env()

cluster = env.str("CLUSTER_IP")

mongo_uri = env.str("MONGO_URI")


mysql_port = env.str("MYSQL_PORT")
mysql_user = env.str("MYSQL_USER")
mysql_pw = env.str("MYSQL_PW")

# Mongo DB Connection
mongo = MongoClient(mongo_uri)
mongo_db = mongo["local"]
collections = mongo_db.list_collection_names()
print(collections)

# MySQL Connection

sql = mysql.connector.connect(
    host=cluster,
    user=mysql_user,
    password=mysql_pw,
    port=mysql_port,
    collation="utf8mb4_general_ci"
)

if sql.is_connected():
    print("Connected to MySQL")

cursor = sql.cursor()

cursor.execute("SHOW DATABASES")
databases = cursor.fetchall()
print(databases)

# while loop that will only trigger every hour
schedule.every().hour.do()
while True:
    schedule.run_pending()
    time.sleep(1)

sql.close()
