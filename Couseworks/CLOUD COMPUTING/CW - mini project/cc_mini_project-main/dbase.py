import os
import pymysql



# Function return a connection.
def getConnection():
     
    # You can change the connection arguments.
    connection = pymysql.connect(host=os.environ.get('DB_HOST'),
                                 port=3306,
                                 user=os.environ.get('DB_USER'),
                                 password=os.environ.get('DB_PASS'),
                                 database='openuv')
    return connection



def insert_data(city, lat, lng):

    connection = getConnection()
    cursor = connection.cursor()
    query = "INSERT INTO `city` (`city`, `lat`, `lng`) VALUES (%s, %s, %s)"
    cursor.execute(query, (city, lat, lng))
    connection.commit()
    connection.close()



def insert_uv_index(uv, uv_max, uv_max_time, uv_time):

    connection = getConnection()
    cursor = connection.cursor()
    query = "INSERT INTO `uv_index` (`uv`,`uv_max`,`uv_max_time`,`uv_time`) VALUES (%s, %s, %s, %s)"
    cursor.execute(query,(uv, uv_max, uv_max_time, uv_time))
    connection.commit()
    connection.close()
    
    

def select_data(name):

    connection = getConnection()
    cursor = connection.cursor()
    query = "SELECT city, lat, lng FROM city WHERE city like %s"
    cursor.execute(query, (name))
    records = cursor.fetchall() # (('Reading', 51.4542, -0.9731),)
    connection.close()
    return records[0][1], records[0][2]



def insert_user(userName, password, role):
    
    connection = getConnection()
    cursor = connection.cursor()
    query = "INSERT INTO `users` (`Username`, `user_password`, `user_role`) VALUES (%s, %s, %s)"
    cursor.execute(query, (userName, password, role))
    connection.commit()
    connection.close()
    
    
    
def select_user(userName):
    
    connection = getConnection()
    cursor = connection.cursor()
    query = "SELECT Username, user_password, user_role FROM users WHERE Username like %s"
    cursor.execute(query, (userName))
    #records = cursor.fetchall() # (())
    account = cursor.fetchone()
    connection.close()
    return account

if __name__ == '__main__':
    # insert_uv_index(uv=1, uv_max=2, uv_max_time=3, uv_time=4)
    select_data('Reading')