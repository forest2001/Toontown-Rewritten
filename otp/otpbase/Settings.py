import json

class Settings:
    """
    This is the class that reads JSON formatted settings files, and
    returns the values back to whatever requested them.

    This class should be generated in the OTPBase, and then accessed
    via base.settings
    """

    def __init__(self):
        self.fileName = 'settings.json'
        try:
            with open(self.fileName, 'r') as file:
                self.settings = json.load(file)
        except:
            self.settings = {}

    def updateSetting(self, type, attribute, value):
        """
        Update the json file with the new data specified.
        """
        with open(self.fileName, 'w+') as file:
            if not self.settings.get(type):
                self.settings[type] = {}
            self.settings[type][attribute] = value
            json.dump(self.settings, file)

    def getOption(self, type, attribute, default):
        """
        Generic method to fetch the saved configuration settings.
        """
        return self.settings.get(type, {}).get(attribute, default)

    def getString(self, type, attribute, default=''):
        """
        Fetch a string type from the json file, but use default if it
        returns the incorrect type or doesn't exist.
        """
        value = self.getOption(type, attribute, default)
        if isinstance(value, basestring):
            return value
        else:
            return default

    def getInt(self, type, attribute, default=0):
        """
        Fetch a integer type from the json file, but use default if it
        returns the incorrect type or doesn't exist.
        """
        value = self.getOption(type, attribute, default)
        if isinstance(value, (int, long)):
            return int(value)
        else:
            return default

    def getBool(self, type, attribute, default=False):
        """
        Fetch a boolean type from the json file, but use default if it
        returns the incorrect type or doesn't exist.
        """
        value = self.getOption(type, attribute, default)
        if isinstance(value, bool):
            return value
        else:
            return default

    def getList(self, type, attribute, default=[], expectedLength=2):
        """
        Fetch a list type from the json file, but use default if it
        returns the incorrect type or doesn't exist.
        """
        value = self.getOption(type, attribute, default)
        if isinstance(value, list) and len(value) == expectedLength:
            return value
        else:
            return default
