"""Module for storage responses"""
from flask import make_response, jsonify

NOT_FOUND = "Object Not Found."
WAS_DELETED = "Object Was Deleted."
ALREADY_EXISTS = "Object Already Exists."
CANT_UPDATE = "Can't Update Object."
WAS_CREATED = "Object Was Created."
CANT_CREATE = "Can't Create Object."
UPDATED = "Object Was Updated."
NO_RIGHTS = "No Rights For Operation."


def response_with(response, value=None, message=None, error=None, headers={}):
    """Returns response with value, message and error"""
    result = {'message': response['message']}

    if value:
        result.update({'value': value})

    if message:
        result.update({'message': message})

    result.update({'code': response['code']})

    if error:
        result.update({'errors': error})

    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'Flask REST API'})

    return make_response(jsonify(result), response['http_code'], headers)


INVALID_FIELD_NAME_SENT_422 = {
    "http_code": 422,
    "code": "invalidField",
    "message": "Invalid fields found"
}

INVALID_INPUT_422 = {
    "http_code": 422,
    "code": "invalidInput",
    "message": "Invalid input"
}

METHOD_NOT_ALLOWED_405 = {
    "http_code": 405,
    "code": "MethodNotAllowed",
    "message": "The method is not allowed for the requested URL"
}

MISSING_PARAMETERS_422 = {
    "http_code": 422,
    "code": "missingParameter",
    "message": "Missing parameters"
}

BAD_REQUEST_400 = {
    "http_code": 400,
    "code": "badRequest",
    "message": "Bad request"
}

ALREADY_EXIST_400 = {
    "http_code": 400,
    "code": "AlreadyExist",
    "message": "Field already exist"
}

SERVER_ERROR_500 = {
    "http_code": 500,
    "code": "serverError",
    "message": "Server error"
}

NOT_FOUND_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "Resource not found"
}

UNAUTHORIZED_401 = {
    "http_code": 401,
    "code": "notAuthorized",
    "message": "You are not authorised to execute this."
}

SUCCESS_200 = {
    'http_code': 200,
    'code': 'success',
    "message": "Ok."
}

SUCCESS_201 = {
    'http_code': 201,
    'code': 'success',
    "message": "Created."
}

SUCCESS_204 = {
    'http_code': 204,
    'code': 'success',
    "message": "Successful request."
}
