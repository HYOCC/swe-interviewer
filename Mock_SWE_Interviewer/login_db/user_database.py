import mysql.connector
import bcrypt

salt = bcrypt.gensalt()# Creates the salt AKA the hashing algo 

# Connects to the database
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Oscarsgyang123',
    database = 'user_db'
)

# Creates the cursor
cursor = conn.cursor()

# Inserts the login username and password into the DB
def insert_data(username:str, password:str):
    # Encrypts the password first 
    password = password.encode()# Turns to bits first
    encrypt_password = bcrypt.hashpw(password , salt)
    
    print(f'inserting login info into database\nuser: {username} pass: {password} encrypted: {encrypt_password} | insert_data')# Log
    
    # Sets up the execution for inserting data
    query = 'INSERT INTO users (username,password) VALUES (%s, %s)'
    values = (username, encrypt_password)
    cursor.execute(query, values)
    conn.commit()

# Checks if user and password matches in the DB
def check_data(username:str, password:str):
    
    print('checking username and password with database | check_data')# Log
    
    password = password.encode()# Turn to bits first
    
    # Gets the data from the db first
    query = f'SELECT password FROM users WHERE username = \'{username}\';'
    cursor.execute(query)
    data = cursor.fetchall()
    if data:
        db_password = data[0][0]# Process the data 
    else:
        print('username not found | check_data')# Log 
        return False
    db_password = db_password.encode()# Transforms to Bytes
    
    result =  bcrypt.checkpw(password, db_password)
    if result:    
        return True 
    else:
        print('password wrong | check_data')# Log
        return False

# Check if user exists in the DB
def check_for_user(username:str):
    
    print(f'Checking for user in DB, user: {username} | check_for_user')# Log
    
    query = f'SELECT EXISTS(SELECT 1 FROM users WHERE username = \'{username}\');'
    cursor.execute(query)
    data = cursor.fetchall()[0][0]
    return True if data == 1 else False

    



    
    
    