from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app)

active_sockets = []

@app.route('/')
def index():
    return render_template('index.html')

# use get method to send id of disconected socket
@app.route('/<string:socketId>', methods=['GET'])
def user_disconected(socketId):
    print('user_disconected')
    print('User left ...... ', socketId)
    sio.emit('user_left', socketId)

@sio.on('connect_event')
def connect(data):
    active_sockets.append(data['data'])
    print('New user joined: ', data['data'])
    sio.emit('user_joined', data['data'])

@sio.on('connections')
def connections(data):
    all_users = data['data']
    print('Active users: ', all_users)


# @sio.on('disconnect_event')
# def disconnect(data):
#     print('User left the room', data['data'])
#     sio.emit('user_left', data['data'])


@sio.on('send_message')
def send_message(data):
    print("server received message!", data)
    sio.emit('on_message', data)



if __name__ == '__main__':
    # app.run()
    sio.run(app)