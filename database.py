import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="So3859123456",
    database="Movie",
    auth_plugin='mysql_native_password'
)

cursor = db.cursor()


cursor.execute("SHOW TABLES")


tables = []
for table in cursor:
    tables.append(table)


if len(tables) == 0:
    cursor.execute("""
    CREATE TABLE movie_user (
        UserID INTEGER PRIMARY KEY,
        FirstName VARCHAR(30) NOT NULL,
        LastName VARCHAR(30) NOT NULL,
        Email VARCHAR(50) NOT NULL,
        Username VARCHAR(30) NOT NULL
    )
""")
    
    print("Tables Created...")
