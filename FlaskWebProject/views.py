"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request, Response, jsonify
from FlaskWebProject import app, socketio
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import random
import sqlite3



def get_sentences():
    cursor = conn.execute('SELECT * from sentences')
    rows = cursor.fetchall()
    row = random.choice(rows)
    return row
conn = sqlite3.connect('example.db')
print ("Opened Database succesfully")
s = get_sentences()
print (s)
the_sentence = s[1]
#def start_timer():
#    return datetime.datetime.now().time()
    
#def end_timer(start_time):
#    return datetime.datetime.now().time()-
    
#def calculate_wpm(finish_time):
#    return the_sentence/finish_time

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS sentences(number, sentence)')

def data_entry():
    c.execute('INSERT INTO sentences VALUES(1, "He put heat on the wound to see what would grow.")')
    c.execute('INSERT INTO sentences VALUES(2, "He found the end of the rainbow and was surprised at what he found there.")')
    c.execute('INSERT INTO sentences VALUES(3, "Be careful with that butter knife.")')
    c.execute('INSERT INTO sentences VALUES(4, "I was very proud of my nickname throughout high school but today- I couldn’t be any different to what my nickname was.")')
    c.execute('INSERT INTO sentences VALUES(5, "Each person who knows you has a different perception of who you are.")')
    c.execute('INSERT INTO sentences VALUES(6, "Beach-combing replaced wine tasting as his new obsession.")')
    c.execute('INSERT INTO sentences VALUES(7, "She tilted her head back and let whip cream stream into her mouth while taking a bath.")')
    c.execute('INSERT INTO sentences VALUES(8, "The pet shop stocks everything you need to keep your anaconda happy.")')
    c.execute('INSERT INTO sentences VALUES(9, "Seek success, but always be prepared for random cats.")')
    c.execute('INSERT INTO sentences VALUES(10, "Writing a list of random sentences is harder than I initially thought it would be.")')
    conn.commit()
    c.close()
    conn.close()

#create_table()
#data_entry()

@app.route('/')
def index():
    print("1212")
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/add1')
def add1():
    print("2123")
    return render_template(
        'add1.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/add2')
def add2():
    print("3432")
    return render_template(
        'add2.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/add3', methods=[ 'GET', 'POST'])
def add3():
    print("1111")
    if request.method == 'POST':
        yosi = request.form['yosi']
        moshe = request.form['moshe']
        a = str(int(yosi)+int(moshe))
        return Response('''<h1>OK '''+a+'''</h1>''')
    elif request.method == 'GET':
        return render_template(
        'add3.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/add4', methods=[ 'GET','POST'])
def add4():
    print("2222")
    if request.method == 'POST':
        value1 = request.form.get('yosi')
        value1 = int(value1)
        value2 = request.form.get('moshe')
        value2 = int(value2)
        result = value1 + value2
        print("aaa",value1, value2)
        return render_template(
            'add4.html',
            nmb1 = value1,
            nmb2 = value2,
            result = result,
            title='Home Page',
            year=datetime.now().year,
        )
    elif request.method == 'GET':
        return render_template(
            'add4.html',
            nmb1 = 12,
            nmb2 = 3,
            title='Home Page',
            year=datetime.now().year,
        ) 

@app.route('/add5', methods=[ 'GET', 'POST'])
def add5():
    print("5555")
    if request.method == 'POST':       
        value1 = request.form.get('val1')
        value1 = int(value1)
        value2 = request.form.get('val2')
        value2 = int(value2)
        value3 = value1 + value2
        print("aaa",value1, value2)
        return jsonify({'data':value3})
    elif request.method == 'GET':
        return render_template(
            'add5.html',
            title='Home Page',
            year=datetime.now().year,
        )  

@app.route('/add6', methods=[ 'GET'])
def add6():
    print("666666666666666666666")
    return render_template(
        'add6.html',
        title='Home Page',
        year=datetime.now().year,
    )
        
def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')    
    
@socketio.on('my event')
def handle_my_custom_event(data, methods=['GET', 'POST']):
    print("888",data)
    if "val1" in data :
        val1 = int(data["val1"])
        val2 = int(data["val2"])
        val3 = val1 + val2
        data = {"val3":val3}
        #print('received my event: ' + str(json))
        socketio.emit('my response', data, callback=messageReceived)        
        


     

            
@app.route('/add7', methods=[ 'GET'])
def add7():
    print("add7")
    return render_template(
        'add7.html',
        title='Home Page',
        theText = the_sentence,
        year=datetime.now().year,
        #start_timer()
        i = 0
    )

i = 0
flag = 0
@socketio.on('keypress')
def handle_keypress_event(data, methods=['GET', 'POST']):
    print("1243",data)
    if "val1" in data:
        global flag
        flag = 0
        val4 = ""
        list = the_sentence.split()
        list_with_spaces = [item + ' ' for item in list]
        global i
        word = list_with_spaces[i]
        val1 = data["val1"] #get the word
        length = len(val1) #get the length of the word
        w = word[:length] #shortened word
        if val1 != w:
            val4="red"
        if val1 == w:
            val4="black"
        if val1 == word:
            print ("entered")
            i += 1
            flag = 1
        data = {"val3":val1,"val4":val4,"flag":flag}
        socketio.emit('keypress_response', data, callback=messageReceived)        
        