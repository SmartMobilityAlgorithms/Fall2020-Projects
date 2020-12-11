import requests
import json
import os
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from models.bounding_box import BoundingBox
from models.traffic_incident import TrafficIncident


class BingTrafficIncidentsApi:
    def __init__(self, storage_path: Path) -> None:
        self.__base_url = 'http://dev.virtualearth.net/REST/v1/Traffic/Incidents'
        self.__key = self.__get_env_var('smartmobility_bing_maps_key')
        self.__storage_path = storage_path
        self.__storage_path.mkdir(parents=True, exist_ok=True)

    def __get_env_var(self, name: str) -> str:
        value = os.environ.get(name)
        if not value:
            raise Exception(f"Undefined environment variable: '{name}'.")

        return value

    def download_traffic_incidents(self, bounding_box: BoundingBox, region_name: str) -> None:
        timestamp = self.__get_current_timestamp_string()
        file_name = f'{region_name}_{timestamp}.json'
        print(f'Downloading traffic incidents in {region_name} on {timestamp}.')
        with open(self.__storage_path / file_name, "wb") as file:
            response = self.__call_api(bounding_box)
            file.write(response.content)

    def __get_current_timestamp_string(self) -> str:
        return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    def __call_api(self, bounding_box: BoundingBox) -> requests.Response:
        return requests.get(f'{self.__base_url}/{bounding_box}?key={self.__key}')

    def get_live_traffic_incidents(self, bounding_box: BoundingBox) -> List[TrafficIncident]:
        response = self.__call_api(bounding_box)
        traffic_incidents = self.__parse_traffic_incidents_from_response(response)

        return [TrafficIncident(traffic_incident) for traffic_incident in traffic_incidents]

    def __parse_traffic_incidents_from_response(self, response: requests.Response) -> List[Dict[str, Any]]:
        return json.loads(response.text)['resourceSets'][0]['resources']

    def get_downloaded_traffic_incidents(self, data_file_name: str) -> List[TrafficIncident]:
        traffic_incidents = self.__parse_downloaded_traffic_incidents(self.__storage_path / data_file_name)

        return [TrafficIncident(traffic_incident) for traffic_incident in traffic_incidents]

    def __parse_downloaded_traffic_incidents(self, data_file_path: Path) -> List[Dict[str, Any]]:
        text_data = data_file_path.read_text()
        if not text_data:
            return []

        json_data = json.loads(text_data)

        return json_data['resourceSets'][0]['resources'] if json_data else []

    def reduce_data_files_to_one_csv_file_per_region(self, regions: List[Dict[str, str]]) -> None:
        csv_files = {region['name']: self.__create_csv_file(region['name']) for region in regions}
        data_file_paths = [p for p in self.__storage_path.iterdir() if p.suffix == '.json']
        print(f'Preparing to process data files: {data_file_paths}')

        data_files_processed = 1
        for data_file_path in data_file_paths:
            region_name = self.__get_region_name_from_data_file_path(data_file_path)
            print(f'({data_files_processed}/{len(data_file_paths)}) Merging {data_file_path} to {region_name}')
            csv_file_path = csv_files[region_name]
            traffic_incidents = self.get_downloaded_traffic_incidents(data_file_path.name)
            for traffic_incident in traffic_incidents:
                self.__append_traffic_incident_data_to_csv_file(csv_file_path, traffic_incident)
            data_files_processed += 1

        print(f'Finished processing all data files')

    def __create_csv_file(self, region_name: str) -> Path:
        timestamp = self.__get_current_timestamp_string()
        csv_file_path = Path(self.__storage_path / f'{region_name}_{timestamp}.csv')

        self.__write_csv_header(csv_file_path)

        return csv_file_path

    def __write_csv_header(self, csv_file_path: Path) -> None:
        with open(csv_file_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(TrafficIncident.get_properties())

    def __get_region_name_from_data_file_path(self, data_file_path: str) -> str:
        return data_file_path.stem.split('_')[0]

    def __append_traffic_incident_data_to_csv_file(self, csv_file_path: Path, traffic_incident: TrafficIncident) -> None:
        with open(csv_file_path, 'a') as file:
            writer = csv.writer(file)
            traffic_incident_summary = traffic_incident.get_summary()
            row_data = [traffic_incident_summary[prop] for prop in TrafficIncident.get_properties()]
            writer.writerow(row_data)
