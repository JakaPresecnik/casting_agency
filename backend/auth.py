import json
from jose import jwt
from urllib.request import urlopen
from functools import wraps
from flask import request

# helper variables for setting authorization
# from flask import Flask, request
# app = Flask(__name__)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#      _  _   _ _____ _  _  __     ___           __ _
#     /_\| | | |_   _| || |/  \   / __|___ _ _  / _(_)__ _
#    / _ \ |_| | | | | __ | () | | (__/ _ \ ' \|  _| / _` |
#   /_/ \_\___/  |_| |_||_|\__/   \___\___/_||_|_| |_\__, |
#                                                    |___/

AUTH0_DOMAIN = 'dev-bfn-8r1t.eu.auth0.com'
ALGORITMS = ['RS256']
API_AUDIENCE = 'casting_agency'


'''
AuthError Exception
Throwing auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   __   __       _  __        __       ___                 _
#   \ \ / /__ _ _(_)/ _|_  _  / _|___  |   \ ___ __ ___  __| |___
#    \ V / -_) '_| |  _| || | > _|_ _| | |) / -_) _/ _ \/ _` / -_)
#     \_/\___|_| |_|_|  \_, | \_____|  |___/\___\__\___/\__,_\___|
#                       |__/

def verify_decode_jwt(token):
    # get all keys from our provided domain
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # get the data inside the header
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    
    # scan the jwks containing keys to find the one inside the header
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # use rsa_key and token to validate the token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#     ___     _     _       _
#    / __|___| |_  | |_ ___| |_____ _ _
#   | (_ / -_)  _| |  _/ _ \ / / -_) ' \
#    \___\___|\__|  \__\___/_\_\___|_||_|
#

def get_authorization_header_token():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected'
        }, 401)

    auth_header = request.headers['Authorization']
    split_authorization = auth_header.split(' ')

    if len(split_authorization) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif split_authorization[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    return split_authorization[1]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#    ___               _       _               _           _
#   | _ \___ _ _ _ __ (_)_____(_)___ _ _    __| |_  ___ __| |__
#   |  _/ -_) '_| '  \| (_-<_-< / _ \ ' \  / _| ' \/ -_) _| / /
#   |_| \___|_| |_|_|_|_/__/__/_\___/_||_| \__|_||_\___\__|_\_\
#

def check_permission(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permission not included in JWT'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found'
        }, 403)
    return True

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#    ___                      _   _         _                     _
#   | _ \___ __ _   __ _ _  _| |_| |_    __| |___ __ ___ _ _ __ _| |_ ___ _ _
#   |   / -_) _` | / _` | || |  _| ' \  / _` / -_) _/ _ \ '_/ _` |  _/ _ \ '_|
#   |_|_\___\__, | \__,_|\_,_|\__|_||_| \__,_\___\__\___/_| \__,_|\__\___/_|
#              |_|

def requires_auth(permission=''):
    def requires_auth_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            jwt = get_authorization_header_token()
            payload = verify_decode_jwt(jwt)
            check_permission(permission, payload)
            return func(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator

# helper route for setting up authorization
# @app.route('/authsetup')
# @requires_auth('get:something')
# def authsetup(jwt):
#     return jwt
