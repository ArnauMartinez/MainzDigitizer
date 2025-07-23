from caenParser.persistence import FileParser 
import io


class DT5724Event:
    """
    Class to handle DT5724 events.
    Inherits from FileParser to utilize file parsing capabilities.
    """

    def __init__(self):

    def read_event(self, open_file: io.BufferedReader) -> None:
        """
        Reads a single event from the DT5724 data.
        This method should be implemented to parse the event data.
        """
    

    def read_header(self, open_file: io.BufferedReader) -> None:
        """
        Reads the header of the DT5724 event.
        This method should be implemented to parse the header data.
        """
        words= [int.from_bytes(open_file.read(4), 'little') for _ in range(4)]
        event_size = words[0] & 0x0FFFFFFF
        zle_flag = bool(words[1] & 0x01000000)
        tr
