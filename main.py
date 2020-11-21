import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="greg",
  password="password",
  database="cs425test"
)

mycursor = mydb.cursor()

