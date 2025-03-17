from parser import Parser

parserBot = Parser("https://www.prospektmaschine.de/hypermarkte/")

if __name__ == "__main__":
    #main work func of the parser
    parserBot.mainAction()