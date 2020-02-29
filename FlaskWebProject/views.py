"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request, Response, jsonify
from FlaskWebProject import app, socketio
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect





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
        year=datetime.now().year,
    )


@socketio.on('keypress')
def handle_keypress_event(data, methods=['GET', 'POST']):
    print("1243",data)
    if "val1" in data :
        val1 = data["val1"]
        data = {"val3":val1}
        socketio.emit('keypress_response', data, callback=messageReceived)        
        