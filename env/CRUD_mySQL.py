# CRUD (Create, Read, Update, Delete)
# unutma:
# $ python3 -m venv env
# $ source env/bin/activate
# $ pip install mysql-connector-python
# $ pip show mysql-connector-python
import mysql.connector

yerelSQL = mysql.connector.connect(
  host="localhost",
  user="gurol",
  password="040404",
  database="pythonDB"
)

# database yarat
# mycursor = yerelSQL.cursor()
# mycursor.execute("CREATE DATABASE pythonDB")

# database listele
# mycursor = yerelSQL.cursor()
# mycursor.execute("SHOW DATABASES")
# for x in mycursor:
#   print(x)

# table yarat - execute örneği
# mycursor = yerelSQL.cursor()
# mycursor.execute("CREATE TABLE telefonRehberi (id INT AUTO_INCREMENT PRIMARY KEY, isim VARCHAR(255), telefon VARCHAR(255))")

# table listele
# mycursor = yerelSQL.cursor()
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#   print(x)

# table drop - execute örneği
# mycursor = yerelSQL.cursor()
# mycursor.execute("DROP TABLE telefonRehberi")


# insert - execute örneği
# isim = input("İsim:")
# telefon = input("Telefon:")
# mycursor = yerelSQL.cursor()
# sql = "INSERT INTO telefonRehberi (isim, telefon) VALUES (%s, %s)"
# val = (isim, telefon)
# mycursor.execute(sql, val)
# yerelSQL.commit()
# print(mycursor.rowcount, "record inserted, ID:", mycursor.lastrowid)

mycursor = yerelSQL.cursor()
mycursor.execute("SELECT * FROM telefonRehberi ORDER BY ID ASC")

# myresult = mycursor.fetchall()
# for x in myresult:
#   print(x)
# print("-------------------------")
myresult = mycursor.fetchone() 
print(myresult)
print("-------------------------")

yerelSQL.close()
print("MySQL connection is closed")
print("Done.")