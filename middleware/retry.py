from io import BytesIO
import socket
import itertools


class Retry:
    def __init__(self, app, tries):
        self.tries = tries
        self.app = app

    def __call__(self, environ, start_response):
        catch_response = []
        written = []
        original_wsgi_input = environ.get('wsgi.input')

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
