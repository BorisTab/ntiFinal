import os
import requests


class ModelGatherer:
    @staticmethod
    def get_model(max_latitude, max_longitude, min_latitide, min_longitude):
        url = 'https://www.openstreetmap.org/api/0.6/map?bbox=' + str(min_longitude) + \
              ',' + str(min_latitide) + \
              ',' + str(max_longitude) + \
              ',' + str(max_latitude)

        r = requests.get(url)
        with open('map.osm', 'w') as f:
            f.write(r.text)

        if 'too many' in r.text:
            print('Too many nodes')
            return '400'
        elif 'node' not in r.text:
            print('No nodes selected')
            return '400'
        else:
            os.chdir('model_gatherer')
            os.system(
                'java -Djava.library.path="lib/jogl/linux-i586" -Xmx2G -jar OSM2World.jar -i ../map.osm -o ../map.obj --config config')
            os.chdir('..')
