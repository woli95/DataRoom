import psycopg2

def create_connection():
    return psycopg2.connect(
        #host='/cloudsql/dataroom-301309:europe-west1:myinstance',
        host='35.195.203.154',
        database='dr',
        user='postgres',
        password='#Woli1995'
    )


class UniqueUsernameError(Exception):
    pass


class UniqueEmailError(Exception):
    pass



def create_client(data):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT is_email_free('{}');".format(data["email"]))
        if cursor.fetchone()[0] != 1:
            return 0
        cursor.execute("CALL create_client('{}', '{}')".format(data["email"], data["password"]))
        connection.commit()
        return 1
    except:
        return -1


def save_password_reset_token(token, email):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("CALL save_password_reset_token('{}', '{}')".format(token, email))
        connection.commit()
        return True
    except:
        return False


def delete_password_reset_token(email):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM client_password_reset_token WHERE client_id=(SELECT id FROM client WHERE email='{}')".format(email))
        connection.commit()
        return True
    except:
        return False

def verify_password_reset_token(email, token):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT verify_password_reset_token('{}', '{}')".format(token, email))
        if cursor.fetchone()[0] == 1:
            return True
    except:
        return False


def reset_client_password_and_remove_reset_password_token(email, new_password):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE client SET password='{}' WHERE email='{}';".format(new_password, email))
        cursor.execute("CALL delete_password_reset_token('{}');".format(email))
        connection.commit()
        return True
    except:
        return False


def verify_credentials(data):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT verify_credentials('{}', '{}')".format(data["email"], data["password"]))
        x = cursor.fetchone()[0]
        if x == 1:
            return 1
        return 0
    except:
        return -1


def save_session_token(token, email):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("CALL save_session_token('{}', '{}')".format(email, token))
        connection.commit()
        return True
    except:
        return False


def delete_session_token(token):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("CALL delete_session_token('{}')".format(token))
        connection.commit()
        return True
    except:
        return False


def update_client_email(new_email, token):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("CALL update_client_email('{}', '{}')".format(new_email, token))
        connection.commit()
        return True
    except:
        return False


def update_client_password(new_password, token):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("CALL update_client_password('{}', '{}')".format(new_password, token))
        connection.commit()
        return True
    except:
        return False


def update_client_profile(data, token):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("CALL update_client_profile('{}', '{}', '{}', '{}', '{}')".format(data["first_name"],
                                                                                         data["second_name"],
                                                                                         data["phone_number"],
                                                                                         data["birth_date"],
                                                                                         token))
        connection.commit()
        return True
    except:
        return False


def get_client(token):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM get_client_profile('{}')".format(token))
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))
        result[0]["created_date"] = result[0]["created_date"].strftime("%Y-%m-%d")
        if result[0]["birth_date"] is not None:
            result[0]["birth_date"] = result[0]["birth_date"].strftime("%Y-%m-%d")
        return result
    except:
        return False