from .scope import FileParserXML
from .scope import FileParserRAW


class PersistenceController:

    def __init__(self):
        pass

    def load(self, file_path: str):

        if file_path.endswith('.xml'):
            parser = FileParserXML()
        elif file_path.endswith('.bin'):
            parser = FileParserRAW()
        parser.open(file_path)
        parser.parse()
        info = [parser.digitizers, parser.settings, parser.events]
        parser.close()
        return info
    
    

    
    
    
    