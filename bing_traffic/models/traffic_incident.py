from typing import Dict, List, Any
from datetime import datetime 

# import from root directory to work with binder
# from models.coordinate import Coordinate
from bing_traffic.models.coordinate import Coordinate

class TrafficIncident:
    def __init__(self, traffic_incident: Dict[str, Any]) -> None:
        self.__title = traffic_incident['title'] if 'title' in traffic_incident.keys() else ''
        self.__description = traffic_incident['description']
        self.__severity = traffic_incident['severity']
        self.__road_closed = traffic_incident['roadClosed']
        self.__start_timestamp_in_utc = self.__parse_timestamp(traffic_incident['start'])
        self.__end_timestamp_in_utc = self.__parse_timestamp(traffic_incident['end'])
        self.__origin_coordinate = Coordinate(traffic_incident['point']['coordinates'])
        self.__destination_coordinate = Coordinate(traffic_incident['toPoint']['coordinates'])
    
    def __parse_timestamp(self, timestamp: str) -> datetime:
        unix_time_in_milliseconds = int(timestamp[timestamp.find('(') + 1 : timestamp.find(')')])

        return datetime.fromtimestamp(unix_time_in_milliseconds / 1000)

    @property
    def title(self) -> str:
        return self.__title

    @property
    def description(self) -> str:
        return self.__description

    @property
    def severity(self) -> int:
        return self.__severity
    
    @property
    def road_closed(self) -> bool:
        return self.__road_closed
    
    @property
    def start_timestamp_in_utc(self) -> datetime:
        return self.__start_timestamp_in_utc
    
    @property
    def end_timestamp_in_utc(self) -> datetime:
        return self.__end_timestamp_in_utc

    @property
    def origin_coordinate(self) -> Coordinate:
        return self.__origin_coordinate

    @property
    def destination_coordinate(self) -> Coordinate:
        return self.__destination_coordinate

    @classmethod
    def get_properties(cls) -> List[str]:
        return [
            'title',
            'description',
            'severity',
            'road closed',
            'start timestamp (utc)',
            'end timestamp (utc)',
            'origin coordinate latitude',
            'origin coordinate longitude',
            'destination coordinate latitude',
            'destination coordinate lontitude'
        ]

    def get_summary(self) -> Dict[str, str]:
        return {
            'title': self.title,
            'description': self.description,
            'severity': self.severity,
            'road closed': self.road_closed,
            'start timestamp (utc)': self.start_timestamp_in_utc.strftime("%Y-%m-%d %H:%M:%S"),
            'end timestamp (utc)': self.end_timestamp_in_utc.strftime("%Y-%m-%d %H:%M:%S"),
            'origin coordinate latitude': str(self.origin_coordinate.latitude),
            'origin coordinate longitude': str(self.origin_coordinate.longitude),
            'destination coordinate latitude': str(self.destination_coordinate.latitude),
            'destination coordinate lontitude': str(self.destination_coordinate.longitude)
        }

    
    def __str__(self) -> str:
        return f'''{self.title}, 
                    {self.description},
                    Severity: {self.severity}, 
                    Road closed: {self.road_closed}, 
                    Start timestamp (utc): {self.start_timestamp_in_utc}, 
                    End timestamp (utc): {self.end_timestamp_in_utc}, 
                    Origin coordinate: {self.origin_coordinate}, 
                    Destination coordinate: {self.destination_coordinate}'''