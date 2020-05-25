"""
This script runs the FlaskWebProject application using a development server.

"""

# from os import environ
# from FlaskWebProject import app, socketio

# if __name__ == '__main__':
#     HOST = environ.get('SERVER_HOST', 'localhost')
#     try:
#         PORT = int(environ.get('SERVER_PORT', '5555'))
#     except ValueError:
#         PORT = 5555
#     socketio.run(app, host='0.0.0.0', port=5555, debug=True)

from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, Response, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect, send
import time
import random
import sqlite3

val1 = ""
flag = 0


def get_sentences():  # function to get the sentences from the DB
    conn = sqlite3.connect('example.db')
    print("Opened Database succesfully")
    cursor = conn.execute('SELECT * from sentences')
    rows = cursor.fetchall()
    row = random.choice(rows)
    conn.close()
    return row


def get_table():  # function to get the table scores to display the highest and recent scores
    conn = sqlite3.connect('example.db')
    print("Opened Database successfully")
    cursor = conn.execute('SELECT * from scores')
    allscores = cursor.fetchall()
    conn.close()
    return allscores


def create_table():  # a function that was used to create the DB
    c.execute('CREATE TABLE IF NOT EXISTS sentences(number, sentence)')


def data_entry():  # a function that used to input the sentences to the DB
    c.execute('INSERT INTO sentences VALUES(1, "He put heat on the wound to see what would grow.")')
    c.execute(
        'INSERT INTO sentences VALUES(2, "He found the end of the rainbow and was surprised at what he found there.")')
    c.execute('INSERT INTO sentences VALUES(3, "Be careful with that butter knife.")')
    c.execute(
        'INSERT INTO sentences VALUES(4, "I was very proud of my nickname throughout high school but today- I '
        'couldn’t be any different to what my nickname was.")')
    c.execute('INSERT INTO sentences VALUES(5, "Each person who knows you has a different perception of who you are.")')
    c.execute('INSERT INTO sentences VALUES(6, "Beach-combing replaced wine tasting as his new obsession.")')
    c.execute(
        'INSERT INTO sentences VALUES(7, "She tilted her head back and let whip cream stream into her mouth while '
        'taking a bath.")')
    c.execute('INSERT INTO sentences VALUES(8, "The pet shop stocks everything you need to keep your anaconda happy.")')
    c.execute('INSERT INTO sentences VALUES(9, "Seek success, but always be prepared for random cats.")')
    c.execute(
        'INSERT INTO sentences VALUES(10, "Writing a lst of random sentences is harder than I initially thought it '
        'would be.")')
    conn.commit()
    c.close()
    conn.close()


# create_table()
# data_entry()


def takelast(elem):  # function the take the last of an element, in my case a list
    return elem[-2]


@app.route('/')
def index():  # function that supposedly opens the first page 127.0.0.1/5555
    print("1212")
    table = get_table()
    # recentscores
    print(table)
    recent_scores1 = table[-4:]
    # topscores
    top_scores1 = sorted(table, key=takelast)
    top_scores2 = top_scores1[-4:]
    print(top_scores2)

    return render_template(
        'index.html',
        title='Home Page',
        topscores=top_scores2,
        recentscores=recent_scores1,
        year=datetime.now().year,
    )


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(data, methods=['GET', 'POST']):  # connect the client (play) to the views
    print("888", data)
    if "val1" in data:
        global val1
        val1 = int(data["val1"])
        val2 = int(data["val2"])
        val3 = val1 + val2
        data = {"val3": val3}
        # print('received my event: ' + str(json))
        socketio.emit('my response', data, callback=messageReceived)


@socketio.on('send score')
def add_to_table(data, methods=['GET', 'POST']):  # adds score from play to the DB scores
    print(data)
    name = data["username"]
    wpm = data["wpm"]
    conn = sqlite3.connect('example.db')
    print("Opened Database succesfully")
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    c = conn.cursor()
    c.execute('INSERT INTO scores (day, month, year, wpm, name) VALUES (?, ?, ?, ?, ?)', (day, month, year, wpm, name))
    conn.commit()
    c.close()


@app.route('/play', methods=['GET'])
def play():  # open the page play
    print("play")
    s = get_sentences()
    print(s)
    the_sentence = s[1]
    return render_template(
        'play.html',
        title='Home Page',
        theText=the_sentence,
        year=datetime.now().year,
    )


@app.route('/enter-room', methods=['GET'])
def enter_room():
    roomnum = request.args['roomnum']
    return render_template(
        'room.html',
        title='Room' + roomnum,
        roomnum=roomnum
    )


@socketio.on('join')
def on_join(data):
    room = data['room']
    print('on join', room)
    join_room(room)
    emit('response', f'Welcome to room: {room}', room=room)


@socketio.on('leave')
def on_leave(data):
    room = data['room']
    print('on leave', room)
    leave_room(room)
    emit('someone has left the room.', room=room)


@socketio.on('start')
def on_start(data):
    print('on start')
    s = get_sentences()
    print(s)
    the_sentence = s[1]
    emit('start game', {'theText': the_sentence, 'year': datetime.now().year}, room=data['room'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
