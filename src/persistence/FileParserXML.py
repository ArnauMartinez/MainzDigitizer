import xml.etree.ElementTree as ET
from typing import Optional, cast
import re 
from datetime import datetime

from src.utils import DeepDict
from src.persistence.dtos import DigitizerDTO, SettingsDTO, EventDTO, TriggerDTO

class FileParserXML:

    def __init__(self):
        self._level = 0
        self._digitizers: list[DigitizerDTO] = []
        self._settings: list[SettingsDTO] = []
        self._events: list[EventDTO] = []


    def parse_xml(self, file_path: str) -> None:
        """
        Parses an XML file and returns its content as a dictionary.
        
        :param file_path: Path to the XML file.
        :return: Dictionary representation of the XML content.
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Error parsing XML file: {e}")

        self.traverse_tree(root)
        
    
    def traverse_tree(self, node: ET.Element) -> None:
        """
        Recursively traverses the XML tree and converts it to a dictionary.
        
        :param node: Current XML node.
        :return: Dictionary representation of the node and its children.
        """
        assert node.tag == "caendigitizer"

        for child in node:
            if child.tag == "digitizer":
                self._digitizers.append(self._traverse_digitizer(child))
            elif child.tag == "settings":
                self._settings.append(self._traverse_settings(child))
            elif child.tag == "event":
                self._events.append(self._traverse_event(child))
            else:
                raise ValueError(f"Unknown tag: {child.tag}")
    
    @property
    def digitizers(self):
        return [d.copy() for d in self._digitizers]
    
    @property
    def settings(self):
        return [s.copy() for s in self._settings]
    
    @property
    def events(self):
        return [e.copy() for e in self._events]
    
    def _traverse_digitizer(self, node: ET.Element) -> DigitizerDTO:
        """
        Converts a digitizer XML node to a DigitizerDTO.
        
        :param node: XML node representing a digitizer.
        :return: DigitizerDTO object.
        """
        return DigitizerDTO(
            id=str(node.get("id")),
            family=str(node.get("family")),
            version=str(node.get("version")),
            serial=str(node.get("serial")),
            channels=int(node.find("channels").get("value", 0)),
            resolution=float(node.find("resolution").get("bits", 0.0)),
            frequency = float(node.find("frequency").get("hz", 0.0)),
            max_samples = int(node.find("maxsamples").get("maxsamples", 0)),
            channel_groups=int(node.find("channelgroups").get("capable", 0)),
            zero_suppression=bool(node.find("zerosuppression").get("capable", False)),
            inspection=bool(node.find("inspection").get("capable", False)),
            dual_edge=bool(len(node.find("dualedge").get("capable", ""))>0),

            # Assuming voltagerange is a child element with attributes low and hi
            voltage_range=(
                float(node.find("voltagerange").get("low", 0.0)),
                float(node.find("voltagerange").get("hi", 0.0))
            ),
            windows=[int(window.get("size")) for window in node.findall("windows/window")]
        )
    
    def _traverse_settings(self, node: ET.Element) -> SettingsDTO:

        """
        Converts a settings XML node to a SettingsDTO.
        
        :param node: XML node representing settings.
        :return: SettingsDTO object.
        """
        T = self._traverse_trigger(node.find("trigger"))


        return SettingsDTO(
            id=int(node.get("id")),
            digitizer_id=str(node.get("digitizer")),
            dc_offsets={
                int(dc.get("channel")): int(dc.get("value"))
                for dc in node.findall("dcoffsets/dcoffset")
            },
            trigger=T,

            window=int(node.find("window").get("size", 0)),
            post_trigger=float(node.find("posttrigger").get("value", 0.0).strip('%')),
            channels_mask= int(node.find("channels").get("mask", 0))
        )
    

    def _traverse_event(self, node: ET.Element) -> EventDTO:
        """
        Converts an event XML node to an EventDTO.
        
        :param node: XML node representing an event.
        :return: EventDTO object.
        """

        traces = {}
        for trace in node.findall("trace"):
            key = trace.get("channel")
            if key is None:
                raise ValueError("Trace channel attribute is missing")
            
            trace_body =  re.split(r"[ \n]", trace.text)
            trace_data = [int(x) for x in trace_body if x.isdigit()]
            traces[key] = trace_data
        

        return EventDTO(
            
            id=int(node.get("id")),
            settings_id=int(node.get("settings")),
            digitizer_id=str(node.get("digitizer")),
            time_stamp=int(node.get("timestamp")),
            clock_time=datetime.fromtimestamp(int(node.get("clocktime"))),  
            trigger_shift=int(node.find("triggershift").get("samples", 0)),
            trace= traces
        )

    
    def _traverse_trigger(self, node: ET.Element) -> TriggerDTO:
        """
        Converts a trigger XML node to a TriggerDTO.
        
        :param node: XML node representing a trigger.
        :return: TriggerDTO object.
        """
        return TriggerDTO(
            direction=str(node.get("direction")),
            bitmask=int(node.get("mask")),
            external=str(node.get("external")),
            thresholds={int(threshold.get("channel")): int(threshold.get("value")) for threshold in node.findall("level")},
        )
    
 
if __name__ == "__main__":
    file_path = "/Users/arnaumartinezara/Documents/Mainz/Parser/tests/.TEST_DATA/testFileParserXML.xml"
    parser = FileParserXML()
    parser.parse_xml(file_path)
    print("Digitizers:", parser.digitizers)
    print("Settings:", parser.settings)
    print("Events:", parser.events)