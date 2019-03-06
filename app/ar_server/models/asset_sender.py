import socket


def collect_files():
    files = [
        open('map_.obj'),
        open('map_.mtl'),
        open('map_.jpg'),
    ]
    return files


class AssetSender(object):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, host='127.0.0.1', port=12311):
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc.bind((host, port))
        self.soc.listen(3)

    def send(self):
        connection, address = self.soc.accept()
        connection.send('HELLO!!!'.encode('ascii'))
