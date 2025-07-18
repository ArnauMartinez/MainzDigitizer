from dataclasses import dataclass
from .TriggerDTO import TriggerDTO

@dataclass
class SettingsDTO:
    id: int
    digitizer_id: str
    dc_offsets: dict[int, int]
    trigger: TriggerDTO
    window: int
    post_trigger: float
    channels_mask: int

    def copy(self):
        return SettingsDTO(
            id=self.id,
            digitizer_id=self.digitizer_id,
            dc_offsets=self.dc_offsets.copy(),
            trigger=self.trigger.copy() if self.trigger else None,
            window=self.window,
            post_trigger=self.post_trigger,
            channels_mask=self.channels_mask
        )
