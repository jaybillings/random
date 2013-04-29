import tornado.httpserver
import tornado.ioloop
import tornado.web
import couch
import time
import anyjson

class MainHandlerPublic(tornado.web.RequestHandler):
    def get(self):
        tmp = get_status('updatedoc', 5)
        result = tmp['updatedoc'][5]['sum']
        self.render('dashboard_template.html', updates=result, inserts=0)
        
class MainHandlerPrivate(tornado.web.RequestHandler):
    def get(self):
        myvars = {'name' : 'asdf'}
        self.render('dashboard_template.html', **myvars)
        
class UpdateDocsHandler(tornado.web.RequestHandler):
    def get(self):
        tmp = get_status('updatedoc', 5)
        result = tmp['updatedoc'][5]['sum']
        self.write(anyjson.serialize(result))

class InsertDocsHandler(tornado.web.RequestHandler):
    def get(self):
        tmp = get_status('insertdoc', 5)
        result = tmp['insertdoc'][5]['sum']
        self.write(anyjson.serialize(result))

def get_status(label, period):
    intervals = {period : [label]}
    ret = {}
    for interval in intervals:
        response = couch.multiple_interval_stats(
                                    intervals[interval],
                                    [interval])
        for doctype in response:
            if not ret.get(doctype):
                ret[doctype] = {}
            ret[doctype][interval] = response[doctype]
    return ret
    
application = tornado.web.Application([
    (r"/", MainHandlerPublic),
    (r"/private", MainHandlerPrivate),
    (r"/updatedocs", UpdateDocsHandler),
    (r"/insertdocs", InsertDocsHandler),
])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
	
