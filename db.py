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
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS Log (DateTime DATETIME, Message VARCHAR(255))")
mycursor.execute("CREATE TABLE IF NOT EXISTS Files (DateTime DATETIME, Camera VARCHAR(255), Hash VARCHAR(255), FileName VARCHAR(255))")
mycursor.execute("CREATE TABLE IF NOT EXISTS Errors (DateTime DATETIME, Camera VARCHAR(255), Hash VARCHAR(255), FileName VARCHAR(255), Error VARCHAR(255))")
