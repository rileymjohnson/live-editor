import tornado.ioloop
import tornado.web
import sockjs.tornado

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class ChatConnection(sockjs.tornado.SockJSConnection):
    participants = set()
    def on_open(self, info):
        self.broadcast(self.participants, "Someone joined.")
        self.participants.add(self)
    def on_message(self, message):
        self.broadcast(self.participants, message)
    def on_close(self):
        self.participants.remove(self)

ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/chat')
app = tornado.web.Application(
    [(r"/", IndexHandler)] + ChatRouter.urls
)
app.listen(8080)
tornado.ioloop.IOLoop.instance().start()