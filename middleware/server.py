from pyramid.response import Response
from pyramid.request import Request
from pyramid.view import view_config
from wsgiref.simple_server import make_server

from retry import Retry


def test3(request):
    return Response("test3", "409 Conflict")

def test2(request):
    if request.registry.count2 > 0:
        request.registry.count2 -= 1
        return Response("test1", "409 Conflict")
    return Response("test2", "200 OK")

def test1(request):
    if request.registry.count1 > 0:
        request.registry.count1 -= 1
        return Response("test1", "409 Conflict")
    return Response("hello", "200 OK")


from pyramid.config import Configurator
config = Configurator()
    
config.registry.count1 = 1
config.registry.count2 = 2
config.add_route('test3', '/test3')
config.add_view(test3, route_name='test3')

config.add_route('test2', '/test2')
config.add_view(test2, route_name='test2')

config.add_route('test1', '/test1',)
config.add_view(test1, route_name='test1')

config.scan()

app = config.make_wsgi_app()
# Put middleware
app = Retry(app,3)
server = make_server('0.0.0.0', 8080, app)
if __name__ == "__main__":
    server.serve_forever()
