import psycopg2
import datetime

def create_connection():
    return psycopg2.connect(
        # host='/cloudsql/data-room-293312:europe-west1:data-room-instance',
        host = '35.233.111.140',
        database='DataRoomDB',
        user='backend_server',
        password='backend'
    )


def createClient(uid):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO client(uid, create_date) VALUES(" +
                       "'{}', ".format(uid) +
                       "now()::date);")
        connection.commit()
        connection.close()
        return True
    except psycopg2.Error:
        return False


def getClient(uid):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM client WHERE uid='{}';".format(uid))
        result = [item for item in cursor.fetchall()[0]]
        result[4] = str(result[4])
        if(result[3] is not None):
            result[3] = str(result[3])
        return result
    except psycopg2.Error:
        return False


def updateClient(data, uid):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        client = getClient(uid)
        print(client)
        print(data["first_name"])
        print(data["second_name"])
        print(data["phone_number"])
        print(data["birth_date"])
        print(uid)
        cursor.execute("UPDATE client SET " +
                       "first_name = '{}', ".format(data["first_name"]) +
                       "second_name = '{}', ".format(data["second_name"]) +
                       "phone_number = '{}', ".format(data["phone_number"]) +
                       "birth_date = '{}' ".format(data["birth_date"]) +
                       "WHERE uid = '{}';".format(uid))
        connection.commit()
        connection.close()
        return True
    except psycopg2.Error:
        return False
