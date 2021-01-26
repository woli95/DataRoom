import psycopg2
from main import storage_client
import re
from lxml import etree as ET
import xml_functions as myXML


def create_connection():
    return psycopg2.connect(
        # host='/cloudsql/dataroom-301309:europe-west1:myinstance',
        host='35.195.203.154',
        database='dr',
        user='postgres',
        password='#Woli1995'
    )


def get_all_floors_for_building(building_name):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM floor WHERE building_id=(SELECT id FROM building WHERE name='{}');".format(building_name))
        results = [result[0] for result in cursor.fetchall()]
        return results
    except:
        return False


def create_floor(data, session_token, buildingName):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM client WHERE current_session_token='{}';".format(session_token))
        client_id = str(cursor.fetchone()[0])
        cursor.execute("SELECT COUNT(*) FROM floor WHERE name='{}' AND building_id=(SELECT id FROM building WHERE "
                       "name='{}');".format(data["floorName"], buildingName))
        ifexists = cursor.fetchone()[0]
        if ifexists > 0:
            return 'Floor with this name already exists in this building'
        xml_in_string = myXML.create_initial_floor_xml_document(client_id, data["defaultPermissions"], data["floorName"], buildingName)
        cursor.execute("INSERT INTO floor(building_id, name, xml_document) VALUES "
                       "((SELECT id FROM building WHERE name='{}'), '{}', XMLPARSE(DOCUMENT '{}'));".format(buildingName, data["floorName"], xml_in_string))
        building = storage_client.get_bucket(buildingName)
        blob = building.blob(data["floorName"] + '/')
        blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')
        connection.commit()
        return True
    except:
        return False


def delete_floor_in_building(building_name, floor_name):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM floor WHERE name='{}' AND building_id=(SELECT id FROM building WHERE name='{}');".format(floor_name, building_name))
        building = storage_client.get_bucket(building_name)
        floor = storage_client.list_blobs(building, prefix=floor_name+'/')
        for object in floor:
            object.delete()
        connection.commit()
        return True
    except:
        return False


def get_all_users_for_building(building_name):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, email, first_name, second_name FROM client "
                       "INNER JOIN building_client ON building_client.client_id=client.id "
                       "WHERE building_client.building_id=(SELECT id FROM building WHERE name='{}');".format(building_name))
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))
        return result
    except:
        return False


def add_user_to_building(building_name, target_email):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM client WHERE email='{}'".format(target_email))
        if cursor.fetchone()[0] == 0:
            return 'no client with this email'
        cursor.execute("SELECT COUNT(*) FROM building_client "
                       "WHERE building_id=(SELECT id FROM building WHERE name='{}') AND "
                       "client_id=(SELECT id FROM client WHERE email='{}')".format(building_name, target_email))
        if cursor.fetchone()[0] > 0:
            return 'exists'
        cursor.execute("INSERT INTO building_client VALUES"
                       "((SELECT id FROM client WHERE email='{}'), (SELECT id FROM building WHERE name='{}'));".format(target_email, building_name))
        connection.commit()
        return True
    except:
        return False

#todo: trzeba usunac dane o kliencie ze wszystkich xmlów
def delete_user_from_building(building_name, target_email):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM building_client "
                       "WHERE building_id=(SELECT id FROM building WHERE name='{}') AND "
                       "client_id=(SELECT id FROM client WHERE email='{}');".format(building_name, target_email))
        connection.commit()
        return True
    except:
        return False


def get_floor_full_data(building_name, floor_name):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT floor.name, floor.xml_document FROM floor "
                       "INNER JOIN building ON floor.building_id = building.id "
                       "WHERE floor.name='{}' AND building.id=(SELECT id FROM building WHERE name='{}');".format(floor_name, building_name))
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))
        return result
    except:
        return False


def update_floor_xml_document(building_name, floor_name, xml_document):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE floor SET xml_document=XMLPARSE(DOCUMENT '{}') WHERE name='{}' "
                       "AND building_id=(SELECT id FROM building WHERE name='{}');".format(xml_document, floor_name, building_name))
        connection.commit()
        return True
    except:
        return False

#todo:
# def update_floor_in_building(building_name, floor_name, data):
#     try:
#         connection = create_connection()
#         cursor = connection.cursor()
#         cursor.execute("SELECT xml_document FROM floor WHERE name='{}';".format(floor_name))
#         xml_document = cursor.fetchone()[0]
#         xml_document = myXML.update_floor(xml_document, data)
#         cursor.execute("UPDATE floor SET xml_document=XMLPARSE(DOCUMENT '{}') WHERE name='{}';".format(xml_document, floor_name))
#         if data["floor_name"] != floor_name:
#             cursor.execute("UPDATE floor SET name='{}' WHERE name='{}';".format(data["name"], floor_name))
#         connection.commit()
#         return True
#     except:
#         return False