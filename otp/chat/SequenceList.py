class SequenceList:

    def __init__(self, wordlist):
        self.list = {}
        for line in wordlist.split():
            split = line.split(':')
            self.list[split[0]] = [word.rstrip('\r\n') for word in split[1].split(',')]
    def getList(self, word):
        if word in self.list:
            return self.list[word]
        else:
            return []
