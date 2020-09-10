import pymysql
import db

mydb = pymysql.connect(
          host="localhost",
            user="photosynk",
              passwd="password",
              database="photosynk"
              )
cursor = mydb.cursor()

sql = "DELETE FROM `Files`"
cursor.execute(sql)
sql = "DELETE FROM `Errors`"
cursor.execute(sql)