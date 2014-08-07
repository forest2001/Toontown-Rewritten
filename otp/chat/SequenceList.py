class SequenceList:

    def __init__(self, wordlist):
        self.list = {}
        for line in wordlist.split('\r\n'):
            if line is '':
                continue
            split = line.split(':')
            self.list[split[0].lower()] = [word.rstrip('\r\n').lower() for word in split[1].split(',')]
            
    def getList(self, word):
        if word in self.list:
            return self.list[word]
        else:
            return []