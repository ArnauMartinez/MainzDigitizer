import xml.etree.ElementTree as ET
from typing import Optional

from utils.DeepDict import DeepDict

class FileParserXML:

    def __init__(self):
        self._level = 0
        self._digitizers: list [DeepDict] = []
        self._settings: list[DeepDict] = []
        self._events: list[DeepDict] = []


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
        
    
    def traverse_tree(self, node: ET.Element) -> Optional[DeepDict]:
        """
        Recursively traverses the XML tree and converts it to a dictionary.
        
        :param node: Current XML node.
        :return: Dictionary representation of the node and its children.
        """
        result = DeepDict()
        for child in node:
            child_result = self.traverse_tree(child)
            if (child.tag not in result):
                result[child.tag] = child_result
            elif not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag], child_result]
            else:
                result[child.tag].append(child_result)
        
        result.update(node.attrib)
        if node.tag == "trace":
            result["body"] = node.text
        if node.tag in ["digitizer", "settings", "event", "caendigitizer"]:
            if node.tag == "digitizer":
                self._digitizers.append(result)
            elif node.tag == "settings":
                self._settings.append(result)
            elif node.tag == "event":
                self._events.append(result)
            return None
        else:
            return result
    
    @property
    def digitizers(self):
        return [d.copy() for d in self._digitizers]
    
    @property
    def settings(self):
        return [s.copy() for s in self._settings]
    
    @property
    def events(self):
        return [e.copy() for e in self._events]
    
    
    
if __name__ == "__main__":
    file_path = "/Users/arnaumartinezara/Documents/Mainz/Parser/tests/.TEST_DATA/testFileParserXML.xml"
    parser = FileParserXML()
    parser.parse_xml(file_path)
    print("Digitizers:", parser.digitizers)
    print("Settings:", parser.settings)
    print("Events:", parser.events)