from flask import session
from functools import wraps


def gen_response(my_dict: dict):
    """
    Helper function to generate a response object that allows CORS.
    """
    from flask import jsonify
    response = jsonify(my_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def require_admin(func):
    """ require the session to be admin """
    @wraps(func)
    def check_token(*args, **kwargs):
        # obtain the user
        player = session.get("player")
        if player is not None:
            # proceed with original function
            return func(*args, **kwargs)
        else:
            # redirect with login
            return gen_response({"success": "False"})
    return check_token
