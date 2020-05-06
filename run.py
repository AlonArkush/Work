"""
This script runs the FlaskWebProject application using a development server.

"""

from os import environ
from FlaskWebProject import app, socketio


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    socketio.run( app, host= '0.0.0.0', port = 5555 , debug = True )