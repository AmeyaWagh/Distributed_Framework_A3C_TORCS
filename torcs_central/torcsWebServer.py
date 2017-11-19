import json
import tornado.httpserver
import tornado.ioloop
import tornado.web

global resource
resource=[]

class MyHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        print('Got JSON data:', data)
        global resource
        resource.append(data)
        self.write({ 'got' : 'your data' })

    def get(self):
        # items = ["Item 1", "Item 2", "Item 3"]
        items = resource
        self.render("index.html", title="TORCS_A3C", items=items)    

if __name__ == '__main__':
    app = tornado.web.Application([ tornado.web.url(r'/', MyHandler) ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9090)
    print('Starting server on port 9090')
    tornado.ioloop.IOLoop.instance().start()