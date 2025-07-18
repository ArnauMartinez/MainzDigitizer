import pandas as pd
from Settings import Settings
from Digitizer import Digitizer
from datetime import datetime

class Event:
    def __init__(self, params):
        self._id: int = params.get("id")
        self._settings: Settings= params.get("settings")
        self._digitizer : Digitizer = params.get("digitizer")
        self._time_stamp: int = params.get("time_stamp") 
        self._clock_time: datetime = params.get("clock_time")
        self._trigger_shift: int = params.get("trigger_shift", 0)
        self._trace: pd.DataFrame = params.get("trace")


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
        new_event._trace = self._trace.copy() 
        return new_event
    
    



   