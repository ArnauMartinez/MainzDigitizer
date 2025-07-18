from caenParser import select_file, Parser



def main():
    dc = Parser()
    dc.loadFile(select_file())
    dc.printDigitizers()
    dc.printSettings()
    dc.printEvents()


if __name__ == "__main__":
    main()