from src.persistence.FileParserXML import FileParserXML



class PersistenceController:

    def __init__(self):
        pass

    def load_xml(self, file_path: str):
        """
        Loads an XML file and returns its content as a dictionary.
        
        :param file_path: Path to the XML file.
        :return: Dictionary representation of the XML content.
        """
        parser = FileParserXML()
        parser.parse_xml(file_path)
        return [parser.digitizers, parser.settings, parser.events]
    
    
    