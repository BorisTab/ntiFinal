import socket
import requests


class AssetLoader:

    host_url = ''

    def send_object(self, whom):
        r = requests.get(whom)

