from Digitizer import Digitizer
from Settings import Settings
from Trigger import Trigger
from Event import Event
from typing import Optional, cast
from persistence.PersistenceController import PersistenceController
from datetime import datetime
import pandas as pd
import re


class DomainController:
    def __init__(self):
        self._digitizer: dict[str, Digitizer] = dict()
        self._settings: dict[int, Settings] = dict()
        self._events: dict[int, Event] = dict()
        self._persistence_controller = PersistenceController()

    @property
    def digitizer(self):
        return {k: v.copy() for k, v in self._digitizer.items()}

    @property
    def settings(self):
        return {k: v.copy() for k, v in self._settings.items()}

    @property
    def events(self):
        return {k: v.copy() for k, v in self._events.items()}

    def get_digitizer(self, id: str) -> Optional[Digitizer]:
        return self._digitizer.get(id, None)

    def get_settings(self, id: int) -> Optional[Settings]:
        return self._settings.get(id, None)

    def get_event(self, id: int) -> Optional[Event]:
        return self._events.get(id, None)

    def loadFile(self, file_path: str) -> None:
        # Example implementation, adjust as needed
        [digitizers_raw, settings_raw, events_raw] = self._persistence_controller.load_xml(file_path)

        for digitizer_raw in digitizers_raw:
            d = self.digitizer_translator(digitizer_raw)
            self._digitizer[d.id] = d

        for setting_raw in settings_raw:
            s = self.settings_translator(setting_raw)
            self._settings[s.id] = s

        for event_raw in events_raw:
            e = self.event_translator(event_raw)
            self._events[e.id] = e


    def digitizer_translator(self,digitizer: dict) -> Digitizer:

        params = {
            "id": digitizer.get("id"),
            "family": digitizer.get("family"),
            "version": digitizer.get("version"),
            "serial_number": digitizer.get("serial"),
            "num_channels": int(digitizer.get("channels", {}).get("value", 0)),
            "bits": int(digitizer.get("resolution", {}).get("bits", 0)),
            "frequency": float(digitizer.get("frequency", {}).get("hz", 0)),
            "max_samples": int(digitizer.get("maxsamples", {}).get("maxsamples",0)),
            "channel_groups": digitizer.get("channelgroups", {}).get("capable", 0),
            "zero_supression": bool(digitizer.get("zerosupression", {}).get("capable", 0)),
            "inspection": bool(digitizer.get("inspection", {}).get("capable", 0)),
            "dual_edge": bool(digitizer.get("dualedge", {}).get("capable", 0)),
            "voltage_range": (
                float(digitizer.get("voltagerange", {}).get("low", 0.0)),
                float(digitizer.get("voltagerange", {}).get("hi", 0.0))
            ),
            "windows": [int(w.get("size")) for w in digitizer.get("windows", {}).get("window", [])]
        }
        return Digitizer(params)
    

    def event_translator(self,event: dict) -> Event:
        trace: list[int] = [int(x) for x in re.split(r"[ \n]",cast(str, event.get("trace",0)))]
        params = {
            "id": cast(int,event.get("id")),
            "settings": self._settings.get(cast(int,event.get("settings"))),
            "digitizer": self._digitizer.get(cast(str,event.get("digitizer"))),
            "time_stamp": cast(int,event.get("time_stamp")),
            "clock_time": datetime.fromtimestamp(int(event.get("clocktime") / 100)), #type: ignore
            "trigger_shift": int(event.get("triggershift", {}).get("samples", 0)),
            "trace": pd.DataFrame(trace) if trace is not None else pd.DataFrame()
        }
        return Event(params)


    def settings_translator(self, settings: dict) -> Settings:
        trigger_dir: dict = cast(dict,settings.get("trigger"))
        trigger_params = {
            "direction": cast(str,trigger_dir.get("direction")),
            "bitmask": cast(int, trigger_dir.get("mask")),
            "external": cast(str, trigger_dir.get("external")),
            "thresholds": [cast(int,cast(dict,x).get("value")) for x in cast(list,trigger_dir.get("level"))],
            "window": cast(int, settings.get("window", {}).get("size")),
            "post_trigger": float(cast(str,settings.get("posttrigger", {}).get("value")).strip('%'))
        }
        
        params = {
            "id": cast(int, settings.get("id")),
            "digitizer": self._digitizer.get(cast(str, settings.get("digitizer"))),
            "dc_offsets": [cast(int,cast(dict,x).get("value")) for x in cast(list,cast(dict,trigger_dir.get("dcoffsets")).get("dcoffset"))],
            "trigger": Trigger(trigger_params),
            "channels": cast(int, settings.get("channels", {}).get("mask"))
        }

        return Settings(params)