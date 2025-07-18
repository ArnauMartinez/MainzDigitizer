from .Digitizer import Digitizer
from .Trigger import Trigger
class Settings:
    def __init__(self, params):
        self._id:int = params.get("id")
        self._digitizer:Digitizer = params.get("digitizer", None)
        self._dc_offsets: dict[int,int] = params.get("dc_offsets", {})
        assert len(self._dc_offsets) <= self._digitizer.num_channels, "DC offsets must match number of channels"
        self._trigger: Trigger = params.get("trigger", None)
        self._window: int = params.get("window", 0)  # Number of samples acquired per trigger in each channel
        self._post_trigger: float = params.get("post_trigger", 0.0)
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
            "window": self._window,
            "post_trigger": self._post_trigger,
            "channels": self._channels
        })
    
    def __str__(self):
        return f"Settings(id={self._id}, digitizer_id={self.digitizer_id}, channels={self._channels}, dc_offsets={self._dc_offsets}, trigger={str(self._trigger)})"

