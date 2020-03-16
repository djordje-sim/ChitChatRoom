import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class ChatHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("sample_js_chat_room.html")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/chat-room", ChatHandler)
    ])


if __name__ == "__main__":
    port = 8888
    
    app = make_app()
    app.listen(port)
    print("Listening on port {}".format(port))
    tornado.ioloop.IOLoop.current().start()
