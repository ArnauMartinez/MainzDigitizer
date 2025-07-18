from persistence.FileParserXML import FileParserXML
from utils.DeepDict import DeepDict


class TestFileParserXML:
    def test_parse_xml(self, test_data_dir):
        parser = FileParserXML()
        file_path = test_data_dir / "testFileParserXML.xml"
        parser.parse_xml(file_path)
        assert parser.digitizers == [self.digitizer_expected_result()]
        assert parser.settings == [self.settings_expected_result()]
        assert parser.events == [self.event_expected_result()]

    
    """
    XML are parsed in the following way:
    - The XML file is parsed into a tree structure.
    - Each node is traversed recursively.
    - The first level is separated individually, in events, digitizers and settings
    - From there, each element is a dictionary, with the contents of the dictionary being:
        - Each tag attrib becomes a key-value pair
        - Each children tag (present in the body) becomes a key-value pair
    """

    def digitizer_expected_result(self):
        digitizer = {
            "id": "230",
            "family": "xx740",
            "version": "80",
            "serial": "174",
            "channels": {"value":"32"},
            "voltagerange": {"low": "0.0", "hi": "2.0"},
            "windows": {
            "window": [
                {"size": "192"},
                {"size": "384"},
                {"size": "768"},
                {"size": "1536"},
                {"size": "3072"},
                {"size": "6144"},
                {"size": "12288"},
                {"size": "24576"},
                {"size": "49152"},
                {"size": "98304"},
                {"size": "196608"}
            ]
            }
        }
        return digitizer
    
    def settings_expected_result(self):
        settings = {
            "id": "1",
            "digitizer": "9641E17EA872CAED059B06194120AE02",
            "dcoffsets": {
                "dcoffset": [{"channel": "0", "value":"32768"},
                             {"channel": "1", "value":"32768"},
                             {"channel": "2", "value":"32768"},
                             {"channel": "3", "value":"32768"}]
            },
            "trigger": {
                "direction": "rising",
                "mask": "0",
                "external": "acq",
                "level": [{"channel": "0", "value":"0"},
                          {"channel": "1", "value":"0"},
                          {"channel": "2", "value":"0"},
                          {"channel": "3", "value":"0"}]
            },
            "window": {"size": "192"},
            "posttrigger": {"value": "5.0%"},
            "channels": {"mask": "0"}
        }
        return settings
    
    def event_expected_result(self):
        event = {'triggershift': {'samples': '0'}, 
                 'trace': {'channel': '0', 
                           'body': '8144 8142 8148 8141 8142 8144'}, 
                 'id': '1', 
                 'settings': '2', 
                 'digitizer': '0A708183A6AB2BF6A3D944461802EAA8', 
                 'timestamp': '21109891', 
                 'clocktime': '1558428702'}
        return event
        
        
       
       