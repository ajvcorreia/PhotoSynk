import mysql.connector

mydb = mysql.connector.connect(
          host="localhost",
            user="photosynk",
              passwd="password"
              )

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE photosynk")
