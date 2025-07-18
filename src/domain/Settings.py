from Digitizer import Digitizer
from DomainController import DomainController
from Trigger import Trigger
class Settings:
    def __init__(self, params):
        self._id:int = params.get("id")
        self._digitizer:Digitizer = params.get("digitizer", None)
        self._dc_offsets: list[int] = params.get("dc_offsets", [])
        assert len(self._dc_offsets) == self._digitizer.num_channels, "DC offsets must match number of channels"
        self._trigger: Trigger = params.get("trigger", None)
        self._channels: int = params.get("channels", 0) # Mask of channels enabled to take data

    @property
    def id(self):
        return self._id
    
    @property
    def digitizer_id(self):
        return self._digitizer.id if self._digitizer else None
    
    @property
    def dc_offsets(self):
        return self._dc_offsets.copy()
    
    @property
    def trigger(self):
        return self._trigger.copy()
    
    @property
    def channels(self):
        return self._channels

    def copy(self):
        return Settings({
            "id": self._id,
            "digitizer": self._digitizer,
            "dc_offsets": self._dc_offsets.copy(),
            "trigger": self._trigger.copy() if self._trigger else None,
            "channels": self._channels
        })
    

