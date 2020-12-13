import json
import time
from pathlib import Path
from typing import List

from models.traffic_incident import TrafficIncident
from models.bounding_box import BoundingBox
from bing_traffic_incidents_api import BingTrafficIncidentsApi

def print_traffic_incidents(traffic_incidents: List[TrafficIncident]) -> None:
    for traffic_incident in traffic_incidents:
        print(traffic_incident)

if __name__ == '__main__':
    config = json.loads(Path("./config.json").read_text())
    north_york_region = config['regions'][1]
    north_york_bounding_box = BoundingBox(north_york_region['south_latitude'], north_york_region['west_longitude'], north_york_region['north_latitude'], north_york_region['east_longitude'])

    api = BingTrafficIncidentsApi(storage_path=Path('./data'))

    print_traffic_incidents(traffic_incidents=api.get_live_traffic_incidents(north_york_bounding_box))
    # print_traffic_incidents(traffic_incidents=api.get_downloaded_traffic_incidents(data_file_name='ontario_2020-09-22_22:17:43.json'))

    # api.reduce_data_files_to_one_csv_file_per_region(config['regions'])

