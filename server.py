import sys

from waitress import serve
from app.app import app
from getopt import getopt, GetoptError


def print_help(exit_code=None):
    path = sys.argv[0]
    idx = path.rfind('/')
    if idx >= 0:
        path = path[idx+1:]
    print(f'Usage: python3 {path} [-h|--help] [-p|--port <port_number>]')

    if exit_code is not None:
        sys.exit(exit_code)


def main(argv):
    port = 8000
    host = '0.0.0.0'

    try:
        opts, args = getopt(argv, 'hdp:', ['help', 'debug', 'port='])
    except GetoptError:
        print_help(2)

    debug = False
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help(0)
        elif opt in ('-d', '--debug'):
            debug = True
        elif opt in ('-p', '--port'):
            try:
                port = int(arg)
            except ValueError:
                print(f'Error: "{arg}" is not a valid port number')
                sys.exit(2)

    # print(f'Serving on port {port}')
    if debug:
        app.run(host=host, port=port, debug=True)
    else:
        serve(app, host=host, port=port)


if __name__ == '__main__':
    main(sys.argv[1:])
