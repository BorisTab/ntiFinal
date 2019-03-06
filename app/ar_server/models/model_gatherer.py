# -*- coding: utf-8 -*-
import requests

from pathlib import Path

from os import chdir
from os import system
from os import getcwd


class ModelGatherer:
    @staticmethod
    def get_model(max_latitude, max_longitude, min_latitide, min_longitude):
        url = 'https://www.openstreetmap.org/api/0.6/map?bbox=' + str(min_longitude) + \
              ',' + str(min_latitide) + \
              ',' + str(max_longitude) + \
              ',' + str(max_latitude)

        r = requests.get(url)
        with open('map.osm', 'w') as f:
            f.write(str(r.text.encode("utf-8")))

        if 'too many' in r.text:
            print('Too many nodes')
            return '400'
        elif 'node' not in r.text:
            print('No nodes selected')
            return '400'
        else:
            cwd = Path(getcwd() + '/app/ar_server/models/').as_posix()
            chdir(cwd)
            system(
                'java -Djava.library.path="lib/jogl/linux-i586" -Xmx2G -jar OSM2World.jar '
                '-i map.osm -o map.obj --config config'
            )
            chdir('..')
