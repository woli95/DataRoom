import psycopg2
from main import storage_client
import re
from lxml import etree as ET
import xml_functions as myXML


def create_connection():
    return psycopg2.connect(
        #host='/cloudsql/dataroom-301309:europe-west1:myinstance',
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
        cursor.execute("SELECT xml_document FROM building WHERE name='{}';".format(building_name))
        building_xml = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM client WHERE current_session_token='{}';".format(session_token))
        client_id = str(cursor.fetchone()[0])
        is_super_admin = True if 'admin client_id="{}"'.format(client_id) in building_xml else False
        cursor.execute("SELECT xml_document FROM floor WHERE building_id=(SELECT id FROM building WHERE name='{}');".format(building_name))
        xml_docs = cursor.fetchall()
        results = []
        for xml in xml_docs:
            root = ET.fromstring(xml[0])
            settings = root.findall('settings/setting')
            users = root.findall('users/user')
            level_administrators = root.findall('level_administrators/level_administrator')
            rooms = root.findall('rooms/room')
            tmp = {
                'isSuper': is_super_admin,
                'isUser': None,
                'isAdmin': None,
                'floor_name': root.get('floor_name'),
                'public': True if settings[0].get('public') == "True" else False,
                'hidden': True if settings[1].get('hidden') == "True" else False,
                'everybodyCanCreateRoom': True if settings[2].get('everybodyCanCreateRoom') == "True" else False,
                'creatorCanDeleteRoom': True if settings[3].get('creatorCanDeleteRoom') == "True" else False,
                'room_data': None,
            }
            if tmp['isSuper'] is True or tmp['isAdmin'] is True or tmp['isUser'] is True or tmp['public'] is True:
                for level_administrator in level_administrators:
                    if level_administrator.get('client_id') == client_id:
                        tmp['isAdmin'] = True
                        break
                for user in users:
                    if user.get('client_id') == client_id:
                        tmp['isUser']: True
                        break
                room_data = []
                for room in rooms:
                    room_tmp = {
                        'room_name': room.get('room_name'),
                        'public': room.get('public'),
                        'hidden': room.get('hidden'),
                        'isUser': None,
                        'download': None,
                        'upload': None
                    }
                    users = root.findall('rooms/room[@room_name="{}"]/user'.format(room_tmp['room_name']))
                    for user in users:
                        if user.get('client_id') == client_id:
                            room_tmp['isUser'] = True
                            room_tmp['download'] = user.get('download')
                            room_tmp['upload'] = user.get('upload')
                            break
                    if room_tmp['isUser'] is True or tmp['public'] is True:
                        room_data.append(room_tmp)
                    elif room_tmp['isUser'] is None and tmp['isAdmin'] is True:
                        room_data.append(room_tmp)
                    elif room_tmp['isUser'] is None and tmp['isSuper'] is True:
                        room_data.append(room_tmp)
                tmp['room_data'] = room_data
                results.append(tmp)
            elif tmp['hidden'] is True:
                continue
            elif tmp['hidden'] is False:
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


def create_room(session_token, building_name, floor_name, data):
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
        room = building.blob(floor_name + '/' + data['roomName'] + '/')
        room.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')
        updated_floor_xml = myXML.add_room(floor_xml, data['roomName'], data['public'], data['hidden'])
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
            files[i] = files[i].replace(floor_name + '/' + room_name + '/', '')
        return files
    except:
        return False


def check_floor_free_create_room_permission(building_name, floor_name):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT xml_document FROM floor WHERE name='{}' AND building_id=(SELECT id FROM building WHERE name='{}');".format(floor_name, building_name))
        xml_string = cursor.fetchone()[0]
        if 'setting everybodyCanCreateRoom="True"' in xml_string:
            return True
        else:
            return False
    except:
        return False


def upload_file(building_name, floor_name, room_name, file, file_name):
    try:
        f = file.files['file']
        building_name = storage_client.get_bucket(building_name)
        room = building_name.blob(floor_name + '/' + room_name + '/' + file_name)
        room.upload_from_file(f)
        return True
    except:
        return False


def remove_file(building_name, floor_name, room_name, file_name):
    try:
        building = storage_client.bucket(building_name)
        room_blob = storage_client.list_blobs(building, prefix=floor_name + '/' + room_name + '/')
        for qwe in room_blob:
            if qwe.name.lstrip(floor_name + '/' + room_name + '/') == file_name:
                qwe.delete()
        return True
    except:
        return False


def download_file(building_name, floor_name, room_name, file_name):
    try:
        building = storage_client.bucket(building_name)
        wziu = building.blob(floor_name + '/' + room_name + '/' + file_name)
        wziu.download_to_filename(file_name)
        return file_name
    except:
        return False


