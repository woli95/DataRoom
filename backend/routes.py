from main import app
from flask import request, jsonify
from database_queries import loginQueries, tokenQueries
from mail import send_auth_mail_to_reset_password, send_mail_with_new_password
import secrets
import json


@app.route('/test', methods=['GET'])
def test():
    return jsonify('OK DZIALA')


@app.route('/client/create', methods=['POST'])
@app.route('/client/login', methods=['POST'])
@app.route('/client/<session_token>/logout', methods=['PUT'])
@app.route('/client/<session_token>/update/email', methods=['POST'])
@app.route('/client/<session_token>/update/password', methods=['POST'])
@app.route('/client/<session_token>/update/profile', methods=['POST'])
@app.route('/client/<session_token>/get/profile', methods=['GET'])
def client(session_token=None):
    if request.path == '/client/create':
        result = loginQueries.create_client(json.loads(request.data))
        if result == 1:
            return jsonify('OK'), 200
        elif result == 0:
            return jsonify('Account with this email already exists'), 202
        elif result == -1:
            return jsonify('Other error'), 202
    elif request.path == '/client/login':
        result = loginQueries.verify_credentials(json.loads(request.data))
        if result == 1:
            session_token = secrets.token_hex(10)
            if loginQueries.save_session_token(session_token, json.loads(request.data)["email"]) is True:
                return jsonify(session_token), 200
            else:
                return jsonify('Other error while saving session token'), 202
        elif result == 0:
            return jsonify('Bad credentials'), 202
        elif result == -1:
            return jsonify('Other error'), 202
    elif request.path == '/client/{}/logout'.format(session_token):
        if loginQueries.delete_session_token(session_token) is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Other error while processing logout'), 202
    elif request.path == '/client/{}/update/email'.format(session_token):
        if loginQueries.update_client_email(json.loads(request.data)["email"], session_token) is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Email change failure'), 202
    elif request.path == '/client/{}/update/password'.format(session_token):
        if loginQueries.update_client_password(json.loads(request.data)["password"], session_token) is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Password change failure'), 202
    elif request.path == '/client/{}/update/profile'.format(session_token):
        if loginQueries.update_client_profile(json.loads(request.data), session_token) is True:
            return jsonify('OK'), 200
        else:
            return jsonify('Profile update failure'), 202
    elif request.path == '/client/{}/get/profile'.format(session_token):
        result = loginQueries.get_client(session_token)
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
        result = send_auth_mail_to_reset_password(email_address)
        if result is False:
            return jsonify('Error while sending email'), 202
        else:
            if loginQueries.save_password_reset_token(result, email_address) is True:
                return jsonify('Email sent'), 200
        return jsonify('Other error'), 202
    elif request.path == '/mail/{}/{}'.format(email_address, token):
        if loginQueries.verify_password_reset_token(email_address, token) is True:
            new_password = secrets.token_hex(5)
            if loginQueries.reset_client_password_and_remove_reset_password_token(email_address, new_password) is True:
                if send_mail_with_new_password(email_address, new_password) is True:
                    return 'Password has been changed. New password has been sent to your email address'
                else:
                    return 'Error while sending mail with new password'
            else:
                return 'Db error'
        else:
            return 'Token error'
