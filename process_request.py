from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException
import logging
import json

class App(object):

    def __init__(self):
        self.url_map = Map([
            Rule('/<action>',endpoint='api_handler')
        ])

    def not_found(self, req, args):
        resp={
                'status':"failed",
                'code':"404",
                'transaction_code':'',
                'message':'Requested functionality not found'
            }
        return Response(json.dumps(resp),mimetype='application/json')

    def api_handler(self,req,args):
        try:            
            return self.not_found(req, args)
        except Exception as err:
            logging.error("API_HANDLER_EXCEPTION : "+str(err))

    def dispatch_request(self, req):
        adapter = self.url_map.bind_to_environ(req.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, endpoint)(req, values)
        except HTTPException:
            return self.not_found(req, req.args)

    def wsgi_app(self, env, start_resp):
        try:
            request = Request(env)
            resp = self.dispatch_request(request)
            return resp(env,start_resp)
        except Exception as err:
            logging.error("REQUEST_ERROR : "+str(err))
            resp['message']="Error"
            return Response(json.dumps(resp),mimetype='application/json')

    def __call__(self, env, start_resp):
        return self.wsgi_app(env, start_resp)

def make_app():
    app = App()
    return app