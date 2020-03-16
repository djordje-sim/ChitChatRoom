import os
import json

import tornado.ioloop
from tornado.options import define, options, parse_command_line
import tornado.web

import socketio

define("port", default=8080, help="run on the given port", type=int)

sio = socketio.AsyncServer(async_mode='tornado')

class MainHandler(tornado.web.RequestHandler)  :
    def get(self):
        self.render("sample_js_chat_room.html")
        print('GET')
    
    def post(self):
        # self.set_header("Content-Type", "text/plain")
        # self.write("You wrote " + self.get_body_argument("message"))
        print('POST')

class SimpleWebSocket(tornado.websocket.WebSocketHandler):

    def get(self):
        self.render("sample_js_chat_room.html")
        print('GET')
    
    def post(self):
        print('Simple Web Socket - POST')
        print('...')

    # async def user_joined(self, message):
    #     print('user joined', message)
    #     await sio.emit('my response', {'response': 'my response'})

    # async def user_left(self, message):
    #     print('print_message')
    #     await sio.emit('my response', {'response': 'my response'})

    
    # async def on_message(self, sid, data):
    #     print('Simple web socket - on message')
    #     await sio.emit('on_message', {sid: data})

    # @sio.on('send_message')
    # async def send_message(self, data):
    #     print("server received message!", data)
        # await sio.emit('', data)


# @sio.on("user_joined")
# def user_joined(self, message):
#     print('user joined', message)
#     sio.emit('my response', {'response': 'my response'})

# @sio.on("user_left")
# def user_left(self, message):
#     print('print_message')
#     sio.emit('my response', {'response': 'my response'})

async def on_message(msg):
    print('Message: ' + msg)
    await sio.emit(msg, broadcast=True)
    return msg

# works
@sio.on('send_message')
async def send_message(sid, data):
    print("server received message!", data)
    await sio.emit('on_message', data)

def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/socket.io/", socketio.get_tornado_handler(sio)),
        ]
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()