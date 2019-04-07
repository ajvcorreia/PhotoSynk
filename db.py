import mysql.connector

mydb = mysql.connector.connect(
          host="localhost",
            user="photosynk",
              passwd="password"
              )

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS photosynk")

mydb = mysql.connector.connect(
          host="localhost",
            user="photosynk",
              passwd="password",
              database="photosynk"
              )
mycursor.execute("CREATE TABLE log (DateTime DATETIME, Message VARCHAR(255))")
