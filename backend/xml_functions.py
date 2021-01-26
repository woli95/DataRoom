from lxml import etree as ET
import re


def create_initial_building_xml_document(client_id):
    root = ET.Element('root')
    admins = ET.SubElement(root, 'admins')
    ET.SubElement(admins, 'admin', client_id=client_id)
    tree = ET.ElementTree(root)
    x = ET.tostring(tree)
    x = x.decode('ascii')
    return x


def create_initial_floor_xml_document(client_id, default_permissions, floor_name, building_name):
    root = ET.Element('root', building_name=building_name, floor_name=floor_name)
    settings = ET.SubElement(root, 'settings')
    ET.SubElement(settings, 'setting', public=str(default_permissions[0]))
    ET.SubElement(settings, 'setting', hidden=str(default_permissions[1]))
    ET.SubElement(settings, 'setting', everybodyCanCreateRoom=str(default_permissions[2]))
    ET.SubElement(settings, 'setting', creatorCanDeleteRoom=str(default_permissions[3]))
    users = ET.SubElement(root, 'users')
    ET.SubElement(users, 'user', client_id=client_id)
    level_administrators = ET.SubElement(root, 'level_administrators')
    ET.SubElement(level_administrators, 'level_administrator', client_id=client_id)
    ET.SubElement(root, 'rooms')
    tree = ET.ElementTree(root)
    x = ET.tostring(tree).decode('ascii')
    return x


def add_room(xml_document, room_name):
    root = ET.fromstring(xml_document)
    rooms = root.findall('rooms')[0]
    ET.SubElement(rooms, 'room', room_name=room_name)
    tree = ET.ElementTree(root)
    return ET.tostring(tree).decode('ascii')