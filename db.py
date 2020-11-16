#import mysql.connector
#from mysql.connector import Error
#from mysql.connector import errorcode
import pymysql
#def AddDrive(Drive, Serial, GivenName):
    # try:
    #     mydb = mysql.connector.connect(
    #               host="localhost",
    #                 user="photosynk",
    #                   passwd="password"
    #                   )
    #     mydb.autocommit = false
    #     mycursor = mydb.cursor()
    #     sql = "INSERT INTO Drives (Drive, Serial, GivenName) VALUES (%s, %s, %s)"
    #     val = (Drive, Serial, GivenName)
    #     mycursor.execute(sql, val)
    #     mydb.commit()
    # except mysql.connector.Error as error :
    #     print("Failed to update record to database rollback: {}".format(error))
    #     #reverting changes because of exception
    #     conn.rollback()
    # finally:
    #     #closing database connection.
    #     if(conn.is_connected()):
    #         cursor.close()
    #         conn.close()
    #         print("connection is closed")

mydb = pymysql.connect(host="localhost", user="photosynk", passwd="password")
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS photosynk")

mydb = pymysql.connect(
          host="localhost",
            user="photosynk",
              passwd="password",
              database="photosynk"
              )
mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS Log (DateTime DATETIME, Message VARCHAR(255))")
#mycursor.execute("CREATE TABLE IF NOT EXISTS Files (DateTime DATETIME, Camera VARCHAR(255), Hash VARCHAR(255), FileName VARCHAR(255))")
mycursor.execute("CREATE TABLE IF NOT EXISTS Files (DateTime DATETIME, Make VARCHAR(255), Model VARCHAR(255), GPSCoords VARCHAR(255), Hash VARCHAR(255), FileName VARCHAR(255))")
mycursor.execute("CREATE TABLE IF NOT EXISTS Errors (DateTime DATETIME, Make VARCHAR(255), Model VARCHAR(255), GPSCoords VARCHAR(255), Hash VARCHAR(255), FileName VARCHAR(255), Error VARCHAR(255))")
mycursor.execute("CREATE TABLE IF NOT EXISTS Drives (DateTime DATETIME, Drive VARCHAR(255), SerialNumber VARCHAR(255), GivenName VARCHAR(255))")
