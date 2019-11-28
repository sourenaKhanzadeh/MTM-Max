import mysql.connector
import random

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

    cursor.execute("CREATE TABLE admin (AdminID INTEGER PRIMARY KEY REFERENCES movie_user(UserID))")

    cursor.execute("CREATE TABLE customer (CustomerID INTEGER PRIMARY KEY REFERENCES movie_user(UserID))")

    cursor.execute("""
    CREATE TABLE product (
        ProductID INTEGER PRIMARY KEY,
        Name VARCHAR(50) NOT NULL,
        Length INTEGER NOT NULL,
        Description VARCHAR(280),
        Genre VARCHAR(50),
        SellPrice FLOAT NOT NULL,
        MaturityRating VARCHAR(10),
        RottenTomatoRating VARCHAR(10),
        ReleaseDate  DATE,
        Country VARCHAR(50),
        Image VARCHAR (300)
    )
    """)

    cursor.execute("""
    CREATE TABLE movie (
        MovieID INTEGER PRIMARY KEY REFERENCES product(ProductID),
        Movie_Cast VARCHAR(100),
        Languages VARCHAR(100),
        Director VARCHAR(50)
    )
    """)

    cursor.execute("""
    CREATE TABLE music (
      SongID INTEGER PRIMARY KEY REFERENCES product(ProductID),
      ArtistName VARCHAR(100) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE tvseries (
        SeriesID INTEGER PRIMARY KEY REFERENCES product(ProductID),
        Seasons INTEGER NOT NULL,
        Episodes INTEGER NOT NULL,
        TV_Cast VARCHAR (100)
    )
    """)

    cursor.execute("""
    CREATE TABLE seasons (
        SeriesID INTEGER REFERENCES product(ProductID),
        SeasonNumber INTEGER NOT NULL,
        NumberOfEpisodes INTEGER NOT NULL,
        PRIMARY KEY(SeriesID, SeasonNumber)
    )
    """)

    cursor.execute("""
    CREATE TABLE subscription (
        Type VARCHAR(20) PRIMARY KEY,
        Price INTEGER NOT NULL,
        TVSeriesPerMonth INTEGER NOT NULL,
        MoviesPerMonth INTEGER NOT NULL,
        MusicPerMonth INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE streams (
        CustomerID INTEGER NOT NULL REFERENCES customer(CustomerID),
        ProductID INTEGER NOT NULL REFERENCES product(ProductID)
    )
    """)

    cursor.execute("""
    CREATE TABLE manages (
        AdminID INTEGER NOT NULL REFERENCES admin(AdminID),
        CustomerID INTEGER REFERENCES customer(CustomerID),
        ProductID INTEGER REFERENCES product(ProductID)
    )
    """)

    cursor.execute("""
    CREATE TABLE purchases (
        CustomerID INTEGER NOT NULL REFERENCES customer(CustomerID),
        SubscriptionType VARCHAR(20) REFERENCES subscription(Type),
        ProductID INTEGER REFERENCES product(ProductID),
        DateOfPurchase DATE
    )
    """)
    print("Tables Created...")
else:
    print("Tables Already Exist...")



def insertUser(fname, lname, email, username,**kwargs):
    user_id = random.randint(10000, 9999999)
    cursor.execute("""
    INSERT INTO movie_user(UserID, FirstName, LastName, Email, Username)
    VALUES({},'{}','{}','{}','{}')
    """.format(user_id, fname, lname, email, username))
    if kwargs.get('admin', False):
        cursor.execute("""
        INSERT INTO admin(AdminID)VALUES({})
        """.format(user_id))
    else:
        cursor.execute("""
                INSERT INTO customer(CustomerID)VALUES({})
                """.format(user_id))

    db.commit()


def checkUserExists(userId):
    cursor.execute("""
         SELECT EXISTS(SELECT * FROM movie_user WHERE 
         UserID=(SELECT UserID FROM movie_user WHERE Username='{0}')) AS 'Users', 
         EXISTS(SELECT * FROM admin WHERE 
         AdminID=(SELECT UserID FROM movie_user WHERE Username='{0}')) AS 'Admin', 
         EXISTS(SELECT * FROM customer WHERE 
         CustomerID=(SELECT UserID FROM movie_user WHERE Username='{0}')) AS 'Customer' 
    """.format(userId))

    return cursor.fetchone()


def insertPorduct(args):
    product_id = random.randint(10000, 9999999)
    cursor.execute("""
        INSERT INTO product(ProductID, Name, Length, Description, 
        Genre, SellPrice,
        MaturityRating,RottenTomatoRating,
        ReleaseDate,Country, Image)VALUES(%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)
    """, (product_id, ) + args)
    db.commit()
    return product_id