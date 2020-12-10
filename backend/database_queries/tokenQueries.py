import psycopg2

def create_connection():
    return psycopg2.connect(
        host='/cloudsql/data-room-293312:europe-west1:data-room-instance',
        # host = '35.233.111.140',
        database='DataRoomDB',
        user='backend_server',
        password='backend'
    )

#todo: generowanie tokenow
def generateTokens(uid):
    return True

#todo: usun wszystkie tokeny
def deleteTokens(uid):
    return True
