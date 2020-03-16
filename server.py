import os
import json

import tornado.ioloop
from tornado.options import define, options, parse_command_line
import tornado.web

import socketio

define("port", default=8080, help="run on the given port", type=int)

sio = socketio.AsyncServer(async_mode='tornado')

class MainHandler(tornado.web.RequestHandler)  :
    async def get(self):
        self.render("sample_js_chat_room.html")
        # print('args', self.get_arguments())
        # print('body args', self.get_body_arguments())
        print('browser locale', self.get_browser_locale())
        # print('cookie', self.get_cookie())
        print('currnet user', self.get_current_user())
        # print('quary args', self.get_query_arguments())
        print('status', self.get_status())
        print('user locale', self.get_user_locale())
        # await sio.emit('user_joined', {'user': 'random'})
    
    def post(self):
        print('POST')


# Error:
    # AttributeError: 'AsyncServer' object has no attribute 'event'
# @sio.event
# def connect(sid, environ):
#     print('connect ', sid)


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