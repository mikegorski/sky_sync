from enum import Enum, auto

from open_weather_api.api.processor import CurrentProcessor, ForecastProcessor
from open_weather_api.api.exceptions import NonexistentModeSelected


class Mode(Enum):
    CURRENT = auto()
    FORECAST = auto()


class ProcessorHandler:
    def __init__(self):
        self.current_data_processor = CurrentProcessor()
        self.forecast_data_processor = ForecastProcessor()

    def get_data(self, mode: Mode, lat: float, lon: float):
        if mode == Mode.CURRENT:
            return self.current_data_processor.execute(lat=lat, lon=lon)
        elif mode == Mode.FORECAST:
            return self.forecast_data_processor.execute(lat=lat, lon=lon)
        else:
            raise NonexistentModeSelected
