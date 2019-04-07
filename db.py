import mysql.connector

mydb = mysql.connector.connect(
          host="localhost",
            user="photosynk",
              passwd="password"
              )

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS photosynk")
mycursor.execute("CREATE TABLE IF NOT EXISTS log (DateTime DATETIME, M:essage VARCHAR(255))")
