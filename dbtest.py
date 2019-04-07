import mysql.connector
from mysql.connector import errorcode
def getDeveloperDetails(ID):
    try:
        mySQLConnection = mysql.connector.connect(host='localhost',
                                             database='photosynk',
                                             user='photosynk',
                                             password='password')
        cursor = mySQLConnection.cursor(prepared=True)
        sql_select_query = """select * from Files where Hash = %s"""
        cursor.execute(sql_select_query, (ID, ))
        record = cursor.fetchall()
        print cursor.Count
        for row in record:
            print("DateTime = ", row[0], )
            print("Camera = ", row[1])
            print("hash = ", row[2])
            print("FileName  = ", row[3], "\n")
    except mysql.connector.Error as error:
        print("Failed to get record from database: {}".format(error))
    finally:
        # closing database connection.
        if (mySQLConnection.is_connected()):
            cursor.close()
            mySQLConnection.close()
            print("connection is closed")
id1 = "19c29c3516a1fffd8e7e2143125e15ae"
id2 = "54e95adc093634976316ce497b8bfd22"
getDeveloperDetails(id1)
getDeveloperDetails(id2)
