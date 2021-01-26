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


#OK
def create_building(data, session_token):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM client WHERE current_session_token='{}';".format(session_token))
        client_id = str(cursor.fetchone()[0])
        xml_in_string = myXML.create_initial_building_xml_document(client_id)
        cursor.execute("INSERT INTO building(name, xml_document) VALUES ('{}', XMLPARSE(DOCUMENT '{}')) RETURNING id".format(data["name"], xml_in_string))
        building_id = str(cursor.fetchone()[0])
        cursor.execute("INSERT INTO building_client VALUES ({}, {});".format(client_id, building_id))
        storage_client.create_bucket(data["name"])
        connection.commit()
        return True
    except:
        return False


#OK
def get_buildings_for_client(session_token):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM client WHERE current_session_token='{}';".format(session_token))
        client_id = cursor.fetchone()[0]
        cursor.execute("SELECT name FROM building "
                       "INNER JOIN building_client ON building.id=building_client.building_id "
                       "WHERE building_client.client_id={}".format(client_id))
        building_names = [result[0] for result in cursor.fetchall()]
        results = []
        for building_name in building_names:
            tmp = {
                "building_name": building_name,
                "isAdmin": False
            }
            cursor.execute("SELECT xml_document FROM building WHERE name='{}'".format(building_name))
            xml_document = cursor.fetchone()[0]
            if 'admin client_id="{}"'.format(client_id) in xml_document:
                tmp["isAdmin"] = True
            results.append(tmp)
        return results
    except:
        return False


def get_floors_for_building_and_client(session_token, building_name):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM client WHERE current_session_token='{}';".format(session_token))
        client_id = str(cursor.fetchone()[0])
        cursor.execute("SELECT xml_document FROM floor WHERE building_id=(SELECT id FROM building WHERE name='{}');".format(building_name))
        results = []
        for xml_doc in cursor.fetchall():
            tmp = {
                "floor_name": re.findall('floor_name="([^"]*)"', xml_doc[0])[0],
                "isAdmin": False
            }
            if 'level_administrator client_id="{}"'.format(client_id) in xml_doc[0]:
                tmp["isAdmin"] = True
            results.append(tmp)
        return results
    except:
        return False


def get_rooms_for_floor(session_token, floor_name, building_name):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM client WHERE current_session_token='{}';".format(session_token))
        client_id = cursor.fetchone()[0]
        cursor.execute("SELECT xml_document FROM floor WHERE name='{}' AND "
                       "building_id=(SELECT id FROM building WHERE name='{}');".format(floor_name, building_name))
        floor_xml = cursor.fetchone()[0]
        rooms = re.findall('room_name="([^"]*)"', floor_xml)
        return rooms
    except:
        return False


def create_room(session_token, building_name, floor_name, room_name):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM client WHERE current_session_token='{}';".format(session_token))
        client_id = cursor.fetchone()[0]
        cursor.execute(
            "SELECT xml_document FROM floor WHERE name='{}' AND building_id=(SELECT id FROM building WHERE name='{}');".format(
                floor_name, building_name))
        floor_xml = cursor.fetchone()[0]
        building = storage_client.get_bucket(building_name)
        floor = building.get_blob(floor_name + '/')
        room = building.blob(floor_name + '/' + room_name + '/')
        room.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')
        updated_floor_xml = myXML.add_room(floor_xml, room_name)
        cursor.execute("UPDATE floor SET xml_document=XMLPARSE(DOCUMENT '{}') WHERE "
                       "name='{}' AND building_id=(SELECT id fROM building WHERE name='{}')".format(updated_floor_xml, floor_name, building_name))
        connection.commit()
        return True
    except:
        return False


def get_files_for_room(building_name, floor_name, room_name):
    try:
        building = storage_client.get_bucket(building_name)
        room_blob = storage_client.list_blobs(building, prefix=floor_name + '/' + room_name + '/')
        files = [file.name for file in room_blob]
        files = files[1:]
        for i in range(len(files)):
            files[i] = files[i].lstrip(floor_name + '/' + room_name + '/')
        return files
    except:
        return False