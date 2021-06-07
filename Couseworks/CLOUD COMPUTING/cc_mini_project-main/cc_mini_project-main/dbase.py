import os
import json
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
    query = "SELECT `city`, `lat`, `lng` FROM city WHERE city like %s"
    cursor.execute(query, (name))
    records = cursor.fetchall() # (('Reading', 51.4542, -0.9731),)
    print(records)
    connection.close()
    if not records:
        return 'No record found', ''
    else:
        return records[0][1], records[0][2]


def delete_record(city):
    connection = getConnection()
    cursor = connection.cursor()
    query = "SELECT `city` FROM city WHERE `city`=%s"
    cursor.execute(query, (city))
    records = cursor.fetchall()
    if records:
        query = "DELETE FROM city where `city` like %s"  
        cursor.execute(query, (city))
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False


def modify_record(city, lat, lng):
    connection = getConnection()
    cursor = connection.cursor()
    query = "SELECT `city` FROM city WHERE `city`=%s"
    cursor.execute(query, (city))
    records = cursor.fetchall()
    if records:
        query = "UPDATE city SET lat = %s, lng = %s WHERE `city` = %s"    
        cursor.execute(query, (lat, lng, city))
        connection.commit()
        connection.close()
        return f'Modified record for {city}'
    else:
        query = "INSERT INTO `city` (`city`, `lat`, `lng`) VALUES (%s, %s, %s)"    
        cursor.execute(query, (city, lat, lng))
        connection.commit()
        connection.close()
        return f'Created new record for {city}'

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
    insert_data(city='Paris', lat=51.5074, lng=0.1278)
    lat, lng = select_data('Paris')
    print(lat, lng)
    modify_record(city='Paris', lat=48.864716, lng=2.349014)
    lat, lng = select_data('Paris')
    print(lat, lng)
    status = delete_record(city='Paris')
    print(status)
