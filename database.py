import sqlite3  
  
con = sqlite3.connect("users.db")  
db=con.cursor()

#User Data table
#db.execute("create table users (username TEXT PRIMARY KEY , password TEXT NOT NULL)")

#Pothole information table
#db.execute("CREATE TABLE POTHOLES (name text not null,phone id,street text,city text,depth number,description text)")

#db.execute('ALTER TABLE POTHOLES ADD LATITUDE TEXT ')

#db.execute('ALTER TABLE POTHOLES ADD LONGITUDE TEXT ')

db.execute('ALTER TABLE PTHOLES MODIFY PHONE NUMBER')
  
con.close()  