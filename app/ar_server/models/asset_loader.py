import socket


class AssetLoader:

    host_url = '127.0.0.1'
    host_port = 50007
    soc = socket.socket()

    def __init__(self):
        self.soc.bind((self.host_url, self.host_port))

    def send_object(self):
        self.soc.listen()
        self.soc.accept()

        with open('map.osm', 'wb') as file:
            batch = file.read(1024)
            while batch:
                self.soc.send(batch)
                batch = file.read(1024)

        self.soc.close()
