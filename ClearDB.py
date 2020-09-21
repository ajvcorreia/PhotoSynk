import pymysql

mydb = pymysql.connect(
          host="localhost",
            user="photosynk",
              passwd="password",
              database="photosynk"
              )
mycursor = mydb.cursor()

mycursor.execute("DELETE FROM Files")
mycursor.execute("DELETE FROM Errors")
