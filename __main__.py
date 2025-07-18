from domain.DomainController import DomainController
from utils import select_file



def main():
    dc = DomainController()
    dc.loadFile(select_file())
    dc.printDigitizers()
    dc.printSettings()
    dc.printEvents()


if __name__ == "__main__":
    main()