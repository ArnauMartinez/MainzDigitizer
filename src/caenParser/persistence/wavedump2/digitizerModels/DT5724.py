
from caenParser.persistence.wavedump2 import ParserWBIN 
from caenParser.persistence.dtos import EventDTO, DigitizerDTO, SettingsDTO, TriggerDTO
import io
import struct


class DT5724Parser(ParserWBIN):
    """
    Class to handle DT5724 events.
    Inherits from FileParser to utilize file parsing capabilities.
    """

    def __init__(self):
        super().__init__()
        self.enabled_channels_mask: int = None



    def _read_data(self, open_file: io.BufferedReader):
        self._read_data_header()
        self._read_data_trace()


    def  _read_data_header(self):
        header_fmt = '@ I I I I'
        read_size = struct.calcsize(header_fmt)
        header = self._fileObj

    def _translate_objects():
        pass

