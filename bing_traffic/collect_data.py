import json
import time
from pathlib import Path

from models.bounding_box import BoundingBox
from bing_traffic_incidents_api import BingTrafficIncidentsApi

if __name__ == '__main__':
    config = json.loads(Path("./config.json").read_text())
    api = BingTrafficIncidentsApi(storage_path=Path('./data'))

    while True:
        for region in config['regions']:
            bounding_box = BoundingBox(region['south_latitude'], region['west_longitude'], region['north_latitude'], region['east_longitude'])
            api.download_traffic_incidents(bounding_box, region['name'])

        time.sleep(60 * config['data_collection_rate_in_minutes'])
