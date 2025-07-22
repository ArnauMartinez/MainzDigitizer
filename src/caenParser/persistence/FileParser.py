from  .dtos import DigitizerDTO, SettingsDTO, EventDTO, TriggerDTO


class FileParser:
    def __init__(self):
        self._digitizers: list[DigitizerDTO] = []
        self._settings: list[SettingsDTO] = []
        self._events: list[EventDTO] = []
        self._fileObj = None


    def open(self, file_path: str):
        pass 
    def parse(self, file_path):
        # Parsing logic here
        pass

    def close(self):
        self._fileObj = None
        self._digitizers.clear()
        self._settings.clear()
        self._events.clear()

    @property
    def digitizers(self):
        return [d.copy() for d in self._digitizers]
    
    @property
    def settings(self):
        return [s.copy() for s in self._settings]
    
    @property
    def events(self):
        return [e.copy() for e in self._events]
