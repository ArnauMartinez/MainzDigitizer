import pandas as pd
from .Settings import Settings
from .Digitizer import Digitizer
from datetime import datetime
from enum import Enum, auto
import sys

class MeasureMagnitudeEnum(Enum):
        ADC_COUNTS = auto()
        VOLTAGE = auto()

class TimeMeasurementEnum(Enum):
        CLOCK_TIME = auto()
        TIME_STAMP = auto()


class Event:


    def __init__(self, params):
        self._id: int = params.get("id")
        self._settings: Settings= params.get("settings")
        self._digitizer : Digitizer = params.get("digitizer")
        self._time_stamp: int = params.get("time_stamp") 
        self._clock_time: datetime = params.get("clock_time")
        self._trigger_shift: int = params.get("trigger_shift")
        self._trace: dict[int, pd.DataFrame] = params.get("trace")
        self._measure_magnitude: MeasureMagnitudeEnum = MeasureMagnitudeEnum.ADC_COUNTS


    def set_measure_magnitude(self, magnitude: MeasureMagnitudeEnum):
        if not isinstance(magnitude, MeasureMagnitudeEnum):
            raise ValueError("Invalid measure magnitude type.")
        self._measure_magnitude = magnitude


    def get_channel_data(self, channel: int, magnitude = None) -> pd.DataFrame:
        """
        Returns the trace data for a specific channel as a pandas DataFrame.
        """
        if channel not in self._trace:
            raise ValueError(f"Channel {channel} does not exist in the event trace.")
        
        trace = self._trace[channel].copy()
        
        if magnitude is None:
            magnitude = self._measure_magnitude

        if  magnitude == MeasureMagnitudeEnum.VOLTAGE:
            fract = trace["Amplitude"] / (2 ** self._digitizer.bits - 1)
            trace["Amplitude"] = self._digitizer.voltage_range[0] + fract * (self._digitizer.voltage_range[1] - self._digitizer.voltage_range[0])
        
        if (self._trigger_shift != 0):
            trace["Time"] = (trace.index - self._trigger_shift) / self._digitizer.frequency    
            print(f"Warning: Trigger shift is {self._trigger_shift} samples, adjusting time accordingly.")
        else:
            trace["Time"] = (trace.index - len(trace)*((100 - self._settings._post_trigger)/100)) / self._digitizer.frequency
            print(f"Warning: Trigger shift is {self._trigger_shift} samples, adjusting time accordingly.")

        if len(trace) != self._settings._window:
            import sys
            print(f"Warning: Trace length {len(trace)} doesn't match expected window size {self._settings._window}", file=sys.stderr)

        return trace
        
    def triggered_channels(self) -> list[int]:
        """
        Returns a list of channels that have data in the event trace.
        """
        return list(self._trace.keys())

    @property
    def measure_magnitude(self) -> str:
        return self._measure_magnitude.name.lower()

    @property
    def id(self):
        return self._id
    
    @property
    def settings_id(self):
        return self._settings.id if self._settings else None
    
    @property
    def digitizer_id(self):
        return self._digitizer.id if self._digitizer else None
    
    @property
    def time_stamp(self):
        return self._time_stamp
    
    @property
    def clock_time(self):
        return self._clock_time
    
    @property
    def trigger_shift(self):
        return self._trigger_shift
    
    @property
    def trace(self):
        return self._trace.copy() if self._trace is not None else None
    
    def copy(self):
        new_event = Event({
            "id": self._id,
            "settings": self._settings,
            "digitizer": self._digitizer,
            "time_stamp": self._time_stamp,
            "clock_time": self._clock_time
        })
        new_event._trigger_shift = self._trigger_shift
        new_event._trace = {k: v.copy() for k, v in self._trace.items()} if self._trace is not None else None
        return new_event
    
    def __str__(self):
        return f"Event(id={self._id}, settings_id={self.settings_id}, digitizer_id={self.digitizer_id}, time_stamp={self._time_stamp}, clock_time={self._clock_time}, trigger_shift={self._trigger_shift}), trace_ids = {list(self._trace.keys()) if self._trace else 'None'}"
    
    



   