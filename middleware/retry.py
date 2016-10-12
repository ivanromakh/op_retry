from io import BytesIO
import socket
import itertools


class Retry:
    def __init__(self, app, tries, highwater=2<<20):
        self.tries = tries
        self.app = app
        self.highwater = highwater
        
    def __call__(self, environ, start_response):
        catch_response = []
        written = []
        original_wsgi_input = environ.get('wsgi.input')
        new_wsgi_input = None

        if original_wsgi_input is not None:
            cl = environ.get('CONTENT_LENGTH', '0')
            if cl == '':
                cl = 0
            else:
                cl = int(cl)
            if cl > self.highwater:
                new_wsgi_input = environ['wsgi.input'] = TemporaryFile('w+b')
            else:
                new_wsgi_input = environ['wsgi.input'] = BytesIO()
            rest = cl
            chunksize = 1<<20
            try:
                while rest:
                    if rest <= chunksize:
                        chunk = original_wsgi_input.read(rest)
                        rest = 0
                    else:
                        chunk = original_wsgi_input.read(chunksize)
                        rest = rest - chunksize
                    new_wsgi_input.write(chunk)
            except (socket.error, IOError):
                # Different wsgi servers will generate either socket.error or
                # IOError if there is a problem reading POST data from browser.
                msg = b'Not enough data in request or socket error'
                start_response('400 Bad Request', [
                    ('Content-Type', 'text/plain'),
                    ('Content-Length', str(len(msg))),
                    ]
                )
                return [msg]
            new_wsgi_input.seek(0)

        def replace_start_response(status, headers, exc_info=None):
            catch_response[:] = [status, headers, exc_info]
            return written.append

        i = 0
        while 1:
            app_iter = self.app(environ, replace_start_response)
            print catch_response
            if catch_response[0] == "409 Conflict":
                i += 1
                if i< self.tries:
                    continue
            if catch_response:
                start_response(*catch_response)
            else:
                if hasattr(app_iter, 'close'):
                    app_iter.close()
                raise AssertionError('app must call start_response before '
                                         'returning')
            return close_when_done_generator(written, app_iter)

def close_when_done_generator(written, app_iter):
    try:
        for chunk in itertools.chain(written, app_iter):
            yield chunk
    finally:
        if hasattr(app_iter, 'close'):
            app_iter.close()

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


if __name__ == '__main__':
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
    server.serve_forever()
