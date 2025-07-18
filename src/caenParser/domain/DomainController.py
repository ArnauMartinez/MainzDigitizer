from .Digitizer import Digitizer
from .Settings import Settings
from .Trigger import Trigger, TriggerMode, ExternalTrigger
from .Event import Event
from typing import Optional, cast
from caenParser.persistence.PersistenceController import PersistenceController
from caenParser.persistence.dtos import DigitizerDTO, SettingsDTO, EventDTO, TriggerDTO
import pandas as pd



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

        for digitizer_dto in digitizers_raw:
            d = self.digitizer_translator(digitizer_dto)
            self._digitizer[d.id] = d

        for setting_dto in settings_raw:
            s = self.settings_translator(setting_dto)
            self._settings[s.id] = s

        for event_dto in events_raw:
            e = self.event_translator(event_dto)
            self._events[e.id] = e


    def digitizer_translator(self,digitizer: DigitizerDTO) -> Digitizer:

        params = {
            "id": digitizer.id,
            "family": digitizer.family,
            "version": digitizer.version,
            "serial_number": digitizer.serial,
            "num_channels": digitizer.channels,
            "bits": digitizer.resolution,
            "frequency": digitizer.frequency,
            "max_samples": digitizer.max_samples,
            "channel_groups": digitizer.channel_groups,
            "zero_suppression": digitizer.zero_suppression,
            "inspection": digitizer.inspection,
            "dual_edge": digitizer.dual_edge,
            "voltage_range": digitizer.voltage_range,
            "windows": digitizer.windows,
        }
        return Digitizer(params)
    

    def event_translator(self,event: EventDTO) -> Event:

        params = {
            "id": event.id,
            "settings": self._settings.get(event.settings_id),
            "digitizer": self._digitizer.get(event.digitizer_id),
            "time_stamp": event.time_stamp,
            "clock_time": event.clock_time,
            "trigger_shift": event.trigger_shift,
            "trace": {k: pd.DataFrame(t) for k, t in event.trace.items()}
        }
        assert len(event.trace) < self._digitizer.get(event.digitizer_id).num_channels
        return Event(params)
    


    def settings_translator(self, settings: SettingsDTO) -> Settings:
        T: Trigger = self._trigger_translator(settings.trigger)

        params = {
            "id": settings.id,
            "digitizer": self._digitizer.get(settings.digitizer_id),
            "dc_offsets": settings.dc_offsets,
            "trigger": T,
            "window": settings.window,
            "post_trigger": settings.post_trigger,
            "channels": settings.channels_mask,

        }

        return Settings(params)
    

    def _trigger_translator(self, trigger: TriggerDTO) -> Trigger:

        translateDir = {
            "rising": TriggerMode.RISING_EDGE,
            "falling": TriggerMode.FALLING_EDGE,
        }
        translateExternal = {
            "acq": ExternalTrigger.ACQ,
            "both": ExternalTrigger.BOTH,
            "disabled": ExternalTrigger.DISABLED
        }
        
        params = {
            "direction": translateDir.get(trigger.direction, TriggerMode.RISING_EDGE),
            "bitmask": trigger.bitmask,
            "external": translateExternal.get(trigger.external, ExternalTrigger.DISABLED),
            "thresholds": trigger.thresholds
        }
        return Trigger(params)
    

    def printDigitizers(self):
        for digitizer in self._digitizer.values():
            print(digitizer)
    
    def printSettings(self):
        for setting in self._settings.values():
            print(setting)
    
    def printEvents(self):
        for event in self._events.values():
            print(event)