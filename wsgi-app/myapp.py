import sys
import socket

def application(environ, start_response):
    status = '200 OK'
    template = '''
        <h1>Hello World!</h1>
        <h2>Running on:</h2>{hostname}
        <h2>Python version:</h2>{version}
    '''
    html = template.format(
        hostname=socket.gethostname(),
        version=sys.version.replace('\n', '<br>')
    )
    output = html.encode('utf-8')

    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
