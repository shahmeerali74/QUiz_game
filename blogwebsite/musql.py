import mysql.connector as mysql


db= mysql.connect(
    host="localhost",
    user="root",
    passwd="",
)

print (db)

cursor= db.cursor()

cursor.execute("SHOW DATABASES")
databases=cursor.fetchall()



print(databases)
# cursor.execute("CREATE DATABASE alishah")

database_exists=False

for database in databases:
    if 'loginqzgame' == database[0].lower():
        database_exists=True
        break

if not database_exists:
    cursor.execute("CREATE DATABASE loginqzgame")

else:
    print("database you are trying to create already exists")

db= mysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="loginqzgame"
)


cursor=db.cursor()

cursor.execute("USE loginqzgame")
cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   name VARCHAR(255),
                   email VARCHAR(255) UNIQUE,
                   password VARCHAR(255)
        )
""")    



# signup_part

def signup(name, email, password):
    try:
        cursor.execute("""
    INSERT INTO users (name,email,password) VALUES (%s, %s, %s)
""", (name,email,password))
        db.commit()
        print("SIgnup successsfully!")
    except mysql.Error as err:
        print(f"Error: {err}")


name= "john dow"
email="jogn@example.com"
password= "password123"
signup(name,email, password)