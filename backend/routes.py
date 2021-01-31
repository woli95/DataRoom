from main import app
from flask import request, jsonify, send_file
import userQueries
import basicQueries
import adminQueries
from mail import send_auth_mail_to_reset_password, send_mail_with_new_password
import secrets
import json


@app.route('/application/admin/<session_token>/building/<building_name>/create/floor', methods=['POST'])
@app.route('/application/admin/<session_token>/building/<building_name>/get/floors', methods=['GET'])
@app.route('/application/admin/<session_token>/building/<building_name>/floor/<floor_name>/remove', methods=['PUT'])
@app.route('/application/admin/<session_token>/building/<building_name>/get/users', methods=['GET'])
@app.route('/application/admin/<session_token>/building/<building_name>/user/<target_email>/remove', methods=['PUT'])
@app.route('/application/admin/<session_token>/building/<building_name>/user/add', methods=['POST'])
@app.route('/application/admin/<session_token>/building/<building_name>/floor/<floor_name>/get/data', methods=['GET'])
@app.route('/application/admin/<session_token>/building/<building_name>/floor/<floor_name>/update/xml', methods=['POST'])
@app.route('/application/admin/<session_token>/building/<building_name>/get/data', methods=['GET'])
@app.route('/application/admin/<session_token>/building/<building_name>/update/xml', methods=['POST'])
def application_admin(session_token, building_name=None, floor_name=None, target_email=None):
    if adminQueries.admin_check_auth(session_token, building_name) is not True:
        return jsonify('You have no permission to do this operation'), 202
    if request.path == '/application/admin/{}/building/{}/get/floors'.format(session_token, building_name):
        result = adminQueries.get_all_floors_for_building(building_name)
        if result is False:
            return jsonify('Something gone wrong while getting building floor list'), 202
        else:
            return jsonify(result), 200
    elif request.path == '/application/admin/{}/building/{}/create/floor'.format(session_token, building_name):
        result = adminQueries.create_floor(json.loads(request.data), session_token, building_name)
        if result is True:
            return jsonify('OK'), 200
        elif result is False:
            return jsonify('Cannot create floor'), 202
        else:
            return jsonify(result), 202
    elif request.path == '/application/admin/{}/building/{}/floor/{}/remove'.format(session_token, building_name, floor_name):
        result = adminQueries.delete_floor_in_building(building_name, floor_name)
        if result is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Fail while removing floor'), 202
    elif request.path == '/application/admin/{}/building/{}/get/users'.format(session_token, building_name):
        result = adminQueries.get_all_users_for_building(building_name)
        if result is False:
            return jsonify('Error while getting user list for building'), 202
        else:
            return jsonify(result), 200
    elif request.path == '/application/admin/{}/building/{}/user/{}/remove'.format(session_token, building_name, target_email):
        result = adminQueries.delete_user_from_building(building_name, target_email)
        if result is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Failure while removing user'), 202
    elif request.path == '/application/admin/{}/building/{}/user/add'.format(session_token, building_name):
        result = adminQueries.add_user_to_building(building_name, json.loads(request.data)["target_email"])
        if result is True:
            return jsonify('OK'), 200
        elif result == 'exists':
            return jsonify('User currently exists in building'), 202
        elif result == 'no client with this email':
            return jsonify('There is no account assigned to provided email address'), 202
        else:
            return jsonify('Failure while adding user to building'), 202
    elif request.path == '/application/admin/{}/building/{}/floor/{}/get/data'.format(session_token, building_name, floor_name):
        result = adminQueries.get_floor_full_data(building_name, floor_name)
        if result is not False:
            return jsonify(result), 200
        else:
            return jsonify('Failure while getting full floor data'), 202
    elif request.path == '/application/admin/{}/building/{}/floor/{}/update/xml'.format(session_token, building_name, floor_name):
        result = adminQueries.update_floor_xml_document(building_name, floor_name, json.loads(request.data)['xml_document'])
        if result is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Cannot update xml document'), 202
    elif request.path == '/application/admin/{}/building/{}/get/data'.format(session_token, building_name):
        result = adminQueries.get_building_data(building_name)
        if result is not False:
            return jsonify(result), 200
        else:
            return jsonify('Fail while getting building data'), 202
    elif request.path == '/application/admin/{}/building/{}/update/xml'.format(session_token, building_name):
        result = adminQueries.update_building_xml_document(building_name, json.loads(request.data)['xml_document'])
        if result is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Cannot update building data'), 202


@app.route('/application/user/<session_token>/create/building', methods=['POST'])
@app.route('/application/user/<session_token>/building/getlist', methods=['GET'])
@app.route('/application/user/<session_token>/building/<building_name>/get/floors', methods=['GET'])
@app.route('/application/user/<session_token>/building/<building_name>/floor/<floor_name>/get/rooms', methods=['GET'])
@app.route('/application/user/<session_token>/building/<building_name>/floor/<floor_name>/room/<room_name>/get/files', methods=['GET'])
@app.route('/application/user/<session_token>/building/<building_name>/floor/<floor_name>/room/<room_name>/upload/<file_name>', methods=['POST'])
@app.route('/application/user/<session_token>/building/<building_name>/floor/<floor_name>/room/<room_name>/download/<file_name>', methods=['GET'])
@app.route('/application/user/<session_token>/building/<building_name>/floor/<floor_name>/room/<room_name>/remove/<file_name>', methods=['PUT'])
def application_user(session_token, building_name=None, floor_name=None, room_name=None, file_name=None):
    if request.path == '/application/user/{}/create/building'.format(session_token):
        if userQueries.create_building(json.loads(request.data), session_token) is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Cannot create bucket. Select different name'), 202
    elif request.path == '/application/user/{}/building/getlist'.format(session_token):
        result = userQueries.get_buildings_for_client(session_token)
        if result is not False:
            return jsonify(result), 200
        else:
            return jsonify('Failure while getting client buildings'), 202
    elif request.path == '/application/user/{}/building/{}/get/floors'.format(session_token, building_name):
        result = userQueries.get_floors_for_building_and_client(session_token, building_name)
        if result is not False:
            return jsonify(result), 200
        else:
            return jsonify('Cannot import floors for building'), 202
    elif request.path == '/application/user/{}/building/{}/floor/{}/get/rooms'.format(session_token, building_name, floor_name):
        result = userQueries.get_rooms_for_floor(session_token, floor_name, building_name)
        if result is not False:
            return jsonify(result), 200
        else:
            return jsonify('Fail while getting rooms for building'), 202
    elif request.path == '/application/user/{}/building/{}/floor/{}/room/{}/get/files'.format(session_token, building_name, floor_name, room_name):
        result = userQueries.get_files_for_room(building_name, floor_name, room_name)
        if result is not False:
            return jsonify(result), 200
        else:
            return jsonify('Error while loading room files list'), 202
    elif request.path == '/application/user/{}/building/{}/floor/{}/room/{}/upload/{}'.format(session_token, building_name, floor_name, room_name, file_name):
        result = userQueries.upload_file(building_name, floor_name, room_name, request, file_name)
        if result is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Error while uploading file'), 202
    elif request.path == '/application/user/{}/building/{}/floor/{}/room/{}/download/{}'.format(session_token, building_name, floor_name, room_name, file_name):
        result = userQueries.download_file(building_name, floor_name, room_name, file_name)
        if result is not False:
            return send_file(file_name, as_attachment=True), 200
        else:
            return jsonify('Fail while downloading file'), 202
    elif request.path == '/application/user/{}/building/{}/floor/{}/room/{}/remove/{}'.format(session_token, building_name, floor_name, room_name, file_name):
        result = userQueries.remove_file(building_name, floor_name, room_name, file_name)
        if result is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Cannot delete file'), 202


@app.route('/application/leveladmin/<session_token>/building/<building_name>/floor/<floor_name>/room/<room_name>/delete', methods=['PUT'])
@app.route('/application/leveladmin/<session_token>/building/<building_name>/floor/<floor_name>/create/room', methods=['POST'])
@app.route('/application/leveladmin/<session_token>/building/<building_name>/floor/<floor_name>/get/data', methods=['GET'])
@app.route('/application/leveladmin/<session_token>/building/<building_name>/floor/<floor_name>/update/xml', methods=['POST'])
@app.route('/application/leveladmin/<session_token>/building/<building_name>/get/users', methods=['GET'])
def application_leveladmin(session_token, building_name, floor_name=None, room_name=None):
    if adminQueries.leveladmin_check_auth(session_token, building_name, floor_name) is True:
        if request.path == '/application/leveladmin/{}/building/{}/get/users'.format(session_token, building_name):
            i = 'ok'
        elif request.path == '/application/leveladmin/{}/building/{}/floor/{}/create/room'.format(session_token, building_name, floor_name) and userQueries.check_floor_free_create_room_permission(building_name, floor_name) is True:
            i = 'ok'
        elif adminQueries.admin_check_auth(session_token, building_name, floor_name) is True:
            i = 'ok'
        else:
            return jsonify('You have no permission to do this operation'), 202
    if request.path == '/application/leveladmin/{}/building/{}/floor/{}/room/{}/delete'.format(session_token, building_name, floor_name, room_name):
        result = adminQueries.delete_room(building_name, floor_name, room_name)
        if result is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Cannot delete room'), 202
    elif request.path == '/application/leveladmin/{}/building/{}/floor/{}/create/room'.format(session_token, building_name, floor_name):
        if userQueries.create_room(session_token, building_name, floor_name, json.loads(request.data)) is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Cannot create room'), 202
    elif request.path == '/application/leveladmin/{}/building/{}/floor/{}/get/data'.format(session_token, building_name, floor_name):
        result = adminQueries.get_floor_full_data(building_name, floor_name)
        if result is not False:
            return jsonify(result), 200
        else:
            return jsonify('Cannot get floor data'), 202
    elif request.path == '/application/leveladmin/{}/building/{}/floor/{}/update/xml'.format(session_token, building_name, floor_name):
        result = adminQueries.update_floor_xml_document(building_name, floor_name, json.loads(request.data)['xml_document'])
        if result is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Cannot update floor data'), 202
    elif request.path == '/application/leveladmin/{}/building/{}/get/users'.format(session_token, building_name):
        result = adminQueries.get_all_users_for_building(building_name)
        if result is not False:
            return jsonify(result), 200
        else:
            return jsonify('Cannot get building users'), 202


@app.route('/client/create', methods=['POST'])
@app.route('/client/login', methods=['POST'])
@app.route('/client/<session_token>/logout', methods=['PUT'])
@app.route('/client/<session_token>/update/email', methods=['POST'])
@app.route('/client/<session_token>/update/password', methods=['POST'])
@app.route('/client/<session_token>/update/profile', methods=['POST'])
@app.route('/client/<session_token>/get/profile', methods=['GET'])
def client(session_token=None):
    if request.path == '/client/create':
        result = basicQueries.create_client(json.loads(request.data))
        if result == 1:
            return jsonify('OK'), 200
        elif result == 0:
            return jsonify('Account with this email already exists'), 202
        elif result == -1:
            return jsonify('Other error'), 202
    elif request.path == '/client/login':
        result = basicQueries.verify_credentials(json.loads(request.data))
        if result == 1:
            session_token = secrets.token_hex(10)
            if basicQueries.save_session_token(session_token, json.loads(request.data)["email"]) is True:
                return jsonify(session_token), 200
            else:
                return jsonify('Other error while saving session token'), 202
        elif result == 0:
            return jsonify('Bad credentials'), 202
        elif result == -1:
            return jsonify('Other error'), 202
    elif request.path == '/client/{}/logout'.format(session_token):
        if basicQueries.delete_session_token(session_token) is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Other error while processing logout'), 202
    elif request.path == '/client/{}/update/email'.format(session_token):
        if basicQueries.update_client_email(json.loads(request.data)["email"], session_token) is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Email change failure'), 202
    elif request.path == '/client/{}/update/password'.format(session_token):
        if basicQueries.update_client_password(json.loads(request.data)["password"], session_token) is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Password change failure'), 202
    elif request.path == '/client/{}/update/profile'.format(session_token):
        if basicQueries.update_client_profile(json.loads(request.data), session_token) is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Profile update failure'), 202
    elif request.path == '/client/{}/get/profile'.format(session_token):
        result = basicQueries.get_client(session_token)
        if result is not False:
            return jsonify(result), 200
        else:
            return jsonify('Error while getting client'), 202

    else:
        return 405


@app.route('/mail/<email_address>/send/link', methods=['GET'])
@app.route('/mail/<email_address>/<token>', methods=['GET'])
def mail(email_address=None, token=None):
    if request.path == '/mail/{}/send/link'.format(email_address):
        basicQueries.delete_password_reset_token(email_address)
        result = send_auth_mail_to_reset_password(email_address)
        if result is False:
            return jsonify('Error while sending email'), 202
        else:
            if basicQueries.save_password_reset_token(result, email_address) is True:
                return jsonify('Email sent'), 200
            else:
                return jsonify('Error while saving token')
    elif request.path == '/mail/{}/{}'.format(email_address, token):
        if basicQueries.verify_password_reset_token(email_address, token) is True:
            new_password = secrets.token_hex(5)
            if basicQueries.reset_client_password_and_remove_reset_password_token(email_address, new_password) is True:
                if send_mail_with_new_password(email_address, new_password) is True:
                    return 'Password has been changed. New password has been sent to your email address'
                else:
                    return 'Error while sending mail with new password'
            else:
                return 'Db error'
        else:
            return 'Token error'


@app.route('/callback/f/<fn>', methods=['PUT'])
def other(fn):
    import os
    os.remove(fn)
    return jsonify('OK'), 200
