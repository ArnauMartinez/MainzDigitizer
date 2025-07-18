from dataclasses import dataclass


@dataclass
class TriggerDTO:
    direction: str
    bitmask: int
    external: str
    thresholds: dict[int,int]
    
    def copy(self):
        return TriggerDTO(
            direction=self.direction,
            bitmask=self.bitmask,
            external=self.external,
            thresholds=self.thresholds.copy()  # Ensure a shallow copy of the dictionary
        )
    