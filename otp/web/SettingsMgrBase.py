from direct.directnotify.DirectNotifyGlobal import directNotify

class SettingsMgrBase():
    __module__ = __name__
    notify = directNotify.newCategory('SettingsMgrBase')

    def announceGenerate(self):
        self._settings = {}
        self._originalValueReprs = {}
        self._currentValueReprs = {}
        self._initSettings()

    def delete(self):
        del self._settings

    def _initSettings(self):
        pass

    def _iterSettingNames--- This code section failed: ---

0	SETUP_LOOP        '30'
3	LOAD_FAST         'self'
6	LOAD_ATTR         '_settings'
9	LOAD_ATTR         'iterkeys'
12	CALL_FUNCTION_0   None
15	GET_ITER          None
16	FOR_ITER          '29'
19	STORE_FAST        'name'

22	LOAD_FAST         'name'
25	YIELD_VALUE       None
26	JUMP_BACK         '16'
29	POP_BLOCK         None
30_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 29

    def _addSettings(self, *settings):
        for setting in settings:
            self._addSetting(setting)

    def _addSetting(self, setting):
        name = setting.getName()
        if name in self._settings:
            self.notify.error('duplicate setting "%s"' % name)
        self._settings[name] = setting
        self._originalValueReprs[name] = repr(setting.getValue())
        self._currentValueReprs[name] = repr(setting.getValue())

    def _getOriginalValueRepr(self, settingName):
        return self._originalValueReprs.get(settingName)

    def _getCurrentValueRepr(self, settingName):
        return self._currentValueReprs.get(settingName)

    def _removeSetting(self, setting):
        del self._settings[setting.getName()]
        del self._originalValueReprs[setting.getName()]
        del self._currentValueReprs[setting.getName()]

    def _getSetting(self, settingName):
        return self._settings[settingName]

    def _isSettingModified(self, settingName):
        return self._getOriginalValueRepr(settingName) != self._getCurrentValueRepr(settingName)

    def _changeSetting(self, settingName, valueStr):
        try:
            val = eval(valueStr)
        except:
            self.notify.warning('error evaling "%s" for setting "%s"' % (valueStr, settingName))
            return

        try:
            setting = self._getSetting(settingName)
        except:
            self.notify.warning('unknown setting %s' % settingName)
            return

        setting.setValue(val)
        self._currentValueReprs[settingName] = valueStr# decompiled 0 files: 0 okay, 1 failed, 0 verify failed

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\web\SettingsMgrBase.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	SETUP_LOOP        '30'
3	LOAD_FAST         'self'
6	LOAD_ATTR         '_settings'
9	LOAD_ATTR         'iterkeys'
12	CALL_FUNCTION_0   None
15	GET_ITER          None
16	FOR_ITER          '29'
19	STORE_FAST        'name'

22	LOAD_FAST         'name'
25	YIELD_VALUE       None
26	JUMP_BACK         '16'
29	POP_BLOCK         None
30_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 29

