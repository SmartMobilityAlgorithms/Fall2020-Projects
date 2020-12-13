class BoundingBox:
    def __init__(self, south_latitude: str, west_longitude: str, north_latitude: str, east_longitude: str) -> None:
        self.__south_latitude = south_latitude
        self.__west_longitude = west_longitude
        self.__north_latitude = north_latitude
        self.__east_longitude = east_longitude

    def __str__(self):
        return f'{self.__south_latitude},{self.__west_longitude},{self.__north_latitude},{self.__east_longitude}'
