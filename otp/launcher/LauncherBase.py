import sys
import os
import time
import string
import __builtin__
from pandac.libpandaexpressModules import *
from direct.showbase.MessengerGlobal import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.EventManagerGlobal import *
from direct.task.MiniTask import MiniTask, MiniTaskManager
from direct.directnotify.DirectNotifyGlobal import *

class LogAndOutput():
    __module__ = __name__

    def __init__(self, orig, log):
        self.orig = orig
        self.log = log
        self.console = False

    def write(self, str):
        self.log.write(str)
        self.log.flush()
        if self.console:
            self.orig.write(str)
            self.orig.flush()

    def flush(self):
        self.log.flush()
        self.orig.flush()


class LauncherBase(DirectObject):
    __module__ = __name__
    GameName = 'game'
    ArgCount = 6
    LauncherPhases = [1,
     2,
     3,
     4]
    TmpOverallMap = [0.25,
     0.25,
     0.25,
     0.25]
    BANDWIDTH_ARRAY = [1800,
     3600,
     4200,
     6600,
     8000,
     12000,
     16000,
     24000,
     32000,
     48000,
     72000,
     96000,
     128000,
     192000,
     250000,
     500000,
     750000,
     1000000,
     1250000,
     1500000,
     1750000,
     2000000,
     3000000,
     4000000,
     6000000,
     8000000,
     10000000,
     12000000,
     14000000,
     16000000,
     24000000,
     32000000,
     48000000,
     64000000,
     96000000,
     128000000,
     256000000,
     512000000,
     1024000000]
    win32con_FILE_PERSISTENT_ACLS = 8
    InstallDirKey = 'INSTALL_DIR'
    GameLogFilenameKey = 'GAMELOG_FILENAME'
    PandaWindowOpenKey = 'PANDA_WINDOW_OPEN'
    PandaErrorCodeKey = 'PANDA_ERROR_CODE'
    NewInstallationKey = 'IS_NEW_INSTALLATION'
    LastLoginKey = 'LAST_LOGIN'
    UserLoggedInKey = 'USER_LOGGED_IN'
    PaidUserLoggedInKey = 'PAID_USER_LOGGED_IN'
    ReferrerKey = 'REFERRER_CODE'
    PeriodTimeRemainingKey = 'PERIOD_TIME_REMAINING'
    PeriodNameKey = 'PERIOD_NAME'
    SwidKey = 'SWID'
    PatchCDKey = 'FROM_CD'
    DISLTokenKey = 'DISLTOKEN'
    ProxyServerKey = 'PROXY_SERVER'
    ProxyDirectHostsKey = 'PROXY_DIRECT_HOSTS'
    launcherFileDbFilename = 'launcherFileDb'
    webLauncherFlag = False

    def __init__(self):
        self.started = False
        self.taskMgrStarted = False
        self._downloadComplete = False
        self.pandaErrorCode = 0
        self.WIN32 = os.name == 'nt'
        if self.WIN32:
            if sys.getwindowsversion()[3] == 2:
                self.VISTA = sys.getwindowsversion()[0] == 6
            else:
                self.VISTA = 0
            ltime = time.localtime()
            logSuffix = '%02d%02d%02d_%02d%02d%02d' % (ltime[0] - 2000,
             ltime[1],
             ltime[2],
             ltime[3],
             ltime[4],
             ltime[5])
            logPrefix = ''
            if not self.WIN32:
                logPrefix = os.environ.get('LOGFILE_PREFIX', '')
            logfile = logPrefix + self.getLogFileName() + '-' + logSuffix + '.log'
            self.errorfile = 'errorCode'
            log = open(logfile, 'a')
            logOut = LogAndOutput(sys.__stdout__, log)
            logErr = LogAndOutput(sys.__stderr__, log)
            sys.stdout = logOut
            sys.stderr = logErr
            if sys.platform == 'darwin':
                os.system('/usr/sbin/system_profiler >>' + logfile)
            elif sys.platform == 'linux2':
                os.system('cat /proc/cpuinfo >>' + logfile)
                os.system('cat /proc/meminfo >>' + logfile)
                os.system('/sbin/ifconfig -a >>' + logfile)
            print '\n\nStarting %s...' % self.GameName
            print 'Current time: ' + time.asctime(time.localtime(time.time())) + ' ' + time.tzname[0]
            print 'sys.path = ', sys.path
            print 'sys.argv = ', sys.argv
            if len(sys.argv) >= self.ArgCount:
                Configrc_args = sys.argv[self.ArgCount - 1]
                print "generating configrc using: '" + Configrc_args + "'"
            else:
                Configrc_args = ''
                print 'generating standard configrc'
            if os.environ.has_key('PRC_EXECUTABLE_ARGS'):
                print 'PRC_EXECUTABLE_ARGS is set to: ' + os.environ['PRC_EXECUTABLE_ARGS']
                print 'Resetting PRC_EXECUTABLE_ARGS'
            ExecutionEnvironment.setEnvironmentVariable('PRC_EXECUTABLE_ARGS', '-stdout ' + Configrc_args)
            if os.environ.has_key('CONFIG_CONFIG'):
                print 'CONFIG_CONFIG is set to: ' + os.environ['CONFIG_CONFIG']
                print 'Resetting CONFIG_CONFIG'
            os.environ['CONFIG_CONFIG'] = ':_:configdir_.:configpath_:configname_Configrc.exe:configexe_1:configargs_-stdout ' + Configrc_args
            cpMgr = ConfigPageManager.getGlobalPtr()
            cpMgr.reloadImplicitPages()
            launcherConfig = getConfigExpress()
            __builtin__.config = launcherConfig
            if config.GetBool('log-private-info', 0):
                print 'os.environ = ', os.environ
            elif '__COMPAT_LAYER' in os.environ:
                print '__COMPAT_LAYER = %s' % (os.environ['__COMPAT_LAYER'],)
            self.miniTaskMgr = MiniTaskManager()
            self.VerifyFiles = self.getVerifyFiles()
            self.setServerVersion(launcherConfig.GetString('server-version', 'no_version_set'))
            self.ServerVersionSuffix = launcherConfig.GetString('server-version-suffix', '')
            self.UserUpdateDelay = launcherConfig.GetFloat('launcher-user-update-delay', 0.5)
            self.TELEMETRY_BANDWIDTH = launcherConfig.GetInt('launcher-telemetry-bandwidth', 2000)
            self.INCREASE_THRESHOLD = launcherConfig.GetFloat('launcher-increase-threshold', 0.75)
            self.DECREASE_THRESHOLD = launcherConfig.GetFloat('launcher-decrease-threshold', 0.5)
            self.BPS_WINDOW = launcherConfig.GetFloat('launcher-bps-window', 8.0)
            self.DECREASE_BANDWIDTH = launcherConfig.GetBool('launcher-decrease-bandwidth', 1)
            self.MAX_BANDWIDTH = launcherConfig.GetInt('launcher-max-bandwidth', 0)
            self.nout = MultiplexStream()
            Notify.ptr().setOstreamPtr(self.nout, 0)
            self.nout.addFile(Filename(logfile))
            if launcherConfig.GetBool('console-output', 0):
                self.nout.addStandardOutput()
                sys.stdout.console = True
                sys.stderr.console = True
            self.notify = directNotify.newCategory('Launcher')
            self.clock = TrueClock.getGlobalPtr()
            self.logPrefix = logPrefix
            self.testServerFlag = self.getTestServerFlag()
            self.notify.info('isTestServer: %s' % self.testServerFlag)
            downloadServerString = launcherConfig.GetString('download-server', '')
            if downloadServerString:
                self.notify.info('Overriding downloadServer to %s.' % downloadServerString)
            else:
                downloadServerString = self.getValue('DOWNLOAD_SERVER', '')
            self.notify.info('Download Server List %s' % downloadServerString)
            self.downloadServerList = []
            for name in string.split(downloadServerString, ';'):
                url = URLSpec(name, 1)
                self.downloadServerList.append(url)

            self.nextDownloadServerIndex = 0
            self.getNextDownloadServer()
            self.gameServer = self.getGameServer()
            self.notify.info('Game Server %s' % self.gameServer)
            self.downloadServerRetries = 3
            self.multifileRetries = 1
            self.curMultifileRetry = 0
            self.downloadServerRetryPause = 1
            self.bandwidthIndex = len(self.BANDWIDTH_ARRAY) - 1
            self.everIncreasedBandwidth = 0
            self.goUserName = ''
            self.downloadPercentage = 90
            self.decompressPercentage = 5
            self.extractPercentage = 4
            self.lastLauncherMsg = None
            self.topDir = Filename.fromOsSpecific(self.getValue(self.InstallDirKey, '.'))
            self.setRegistry(self.GameLogFilenameKey, logfile)
            tmpVal = self.getValue(self.PatchCDKey)
            if tmpVal == None:
                self.fromCD = 0
            else:
                self.fromCD = tmpVal
            self.notify.info('patch directory is ' + `(self.fromCD)`)
            self.dbDir = self.topDir
            self.patchDir = self.topDir
            self.mfDir = self.topDir
            self.contentDir = 'content/'
            self.clientDbFilename = 'client.ddb'
            self.compClientDbFilename = self.clientDbFilename + '.pz'
            self.serverDbFilename = 'server.ddb'
            self.compServerDbFilename = self.serverDbFilename + '.pz'
            self.serverDbFilePath = self.contentDir + self.compServerDbFilename
            self.clientStarterDbFilePath = self.contentDir + self.compClientDbFilename
            self.progressFilename = 'progress'
            self.overallComplete = 0
            self.progressSoFar = 0
            self.patchExtension = 'pch'
            self.scanForHacks()
            self.firstPhase = self.LauncherPhases[0]
            self.finalPhase = self.LauncherPhases[-1]
            self.showPhase = 3.5
            self.numPhases = len(self.LauncherPhases)
            self.phaseComplete = {}
            self.phaseNewDownload = {}
            self.phaseOverallMap = {}
            tmpOverallMap = self.TmpOverallMap
            tmpPhase3Map = [0.001,
             0.996,
             0.0,
             0.0,
             0.003]
            phaseIdx = 0
            for phase in self.LauncherPhases:
                percentPhaseCompleteKey = 'PERCENT_PHASE_COMPLETE_' + `phase`
                self.setRegistry(percentPhaseCompleteKey, 0)
                self.phaseComplete[phase] = 0
                self.phaseNewDownload[phase] = 0
                self.phaseOverallMap[phase] = tmpOverallMap[phaseIdx]
                phaseIdx += 1

            self.patchList = []
            self.reextractList = []
            self.byteRate = 0
            self.byteRateRequested = 0
            self.resetBytesPerSecond()
            self.dldb = None
            self.currentMfname = None
            self.currentPhaseIndex = 0
            self.currentPhase = self.LauncherPhases[self.currentPhaseIndex]
            self.currentPhaseName = self.Localizer.LauncherPhaseNames[self.currentPhaseIndex]
            if self.getServerVersion() == 'no_version_set':
                self.setPandaErrorCode(10)
                self.notify.info('Aborting, Configrc did not run!')
                sys.exit()
            self.launcherMessage(self.Localizer.LauncherStartingMessage)
            self.http = HTTPClient()
            if self.http.getProxySpec() == '':
                self.http.setProxySpec(self.getValue(self.ProxyServerKey, ''))
                self.http.setDirectHostSpec(self.getValue(self.ProxyDirectHostsKey, ''))
            self.notify.info('Proxy spec is: %s' % self.http.getProxySpec())
            if self.http.getDirectHostSpec() != '':
                self.notify.info('Direct hosts list is: %s' % self.http.getDirectHostSpec())
            self.httpChannel = self.http.makeChannel(0)
            self.httpChannel.setDownloadThrottle(1)
            connOk = 0
            while not connOk:
                proxies = self.http.getProxiesForUrl(self.downloadServer)
                if proxies == 'DIRECT':
                    self.notify.info('No proxy for download.')
                else:
                    self.notify.info('Download proxy: %s' % proxies)
                testurl = self.addDownloadVersion(self.launcherFileDbFilename)
                connOk = self.httpChannel.getHeader(DocumentSpec(testurl))
                statusCode = self.httpChannel.getStatusCode()
                statusString = self.httpChannel.getStatusString()
                if not connOk:
                    self.notify.warning('Could not contact download server at %s' % testurl.cStr())
                    self.notify.warning('Status code = %s %s' % (statusCode, statusString))
                    if statusCode == 407 or statusCode == 1407 or statusCode == HTTPChannel.SCSocksNoAcceptableLoginMethod:
                        self.setPandaErrorCode(3)
                    elif statusCode == 404:
                        self.setPandaErrorCode(13)
                    elif statusCode < 100:
                        self.setPandaErrorCode(4)
                    elif statusCode > 1000:
                        self.setPandaErrorCode(9)
                    else:
                        self.setPandaErrorCode(6)
                    if not self.getNextDownloadServer():
                        sys.exit()

            self.notify.info('Download server: %s' % self.downloadServer.cStr())
            self.notify.getDebug() and self.accept('page_up', self.increaseBandwidth)
            self.accept('page_down', self.decreaseBandwidth)
        self.httpChannel.setPersistentConnection(1)
        self.foreground()
        self.prepareClient()
        self.setBandwidth()
        self.downloadLauncherFileDb()
        return

    def getTime(self):
        return self.clock.getShortTime()

    def isDummy(self):
        return 0

    def getNextDownloadServer(self):
        if self.nextDownloadServerIndex >= len(self.downloadServerList):
            self.downloadServer = None
            return 0
        self.downloadServer = self.downloadServerList[self.nextDownloadServerIndex]
        self.notify.info('Using download server %s.' % self.downloadServer.cStr())
        self.nextDownloadServerIndex += 1
        return 1

    def getProductName(self):
        config = getConfigExpress()
        productName = config.GetString('product-name', '')
        if productName and productName != 'DisneyOnline-US':
            productName = '_%s' % productName
        else:
            productName = ''
        return productName

    def background(self):
        self.notify.info('background: Launcher now operating in background')
        self.backgrounded = 1

    def foreground(self):
        self.notify.info('foreground: Launcher now operating in foreground')
        self.backgrounded = 0

    def setRegistry(self, key, value):
        self.notify.info('DEPRECATED setRegistry: %s = %s' % (key, value))

    def getRegistry(self, key):
        self.notify.info('DEPRECATED getRegistry: %s' % key)
        return None

    def handleInitiateFatalError(self, errorCode):
        self.notify.warning('handleInitiateFatalError: ' + errorToText(errorCode))
        sys.exit()

    def handleDecompressFatalError(self, task, errorCode):
        self.notify.warning('handleDecompressFatalError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handleDecompressWriteError(self, task, errorCode):
        self.notify.warning('handleDecompressWriteError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handleDecompressZlibError(self, task, errorCode):
        self.notify.warning('handleDecompressZlibError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handleExtractFatalError(self, task, errorCode):
        self.notify.warning('handleExtractFatalError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handleExtractWriteError(self, task, errorCode):
        self.notify.warning('handleExtractWriteError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handlePatchFatalError(self, task, errorCode):
        self.notify.warning('handlePatchFatalError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handlePatchWriteError(self, task, errorCode):
        self.notify.warning('handlePatchWriteError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handleDownloadFatalError(self, task):
        self.notify.warning('handleDownloadFatalError: status code = %s %s' % (self.httpChannel.getStatusCode(), self.httpChannel.getStatusString()))
        self.miniTaskMgr.remove(task)
        statusCode = self.httpChannel.getStatusCode()
        if statusCode == 404:
            self.setPandaErrorCode(5)
        elif statusCode < 100:
            self.setPandaErrorCode(4)
        else:
            self.setPandaErrorCode(6)
        if not self.getNextDownloadServer():
            sys.exit()

    def handleDownloadWriteError(self, task):
        self.notify.warning('handleDownloadWriteError.')
        self.miniTaskMgr.remove(task)
        self.setPandaErrorCode(2)
        sys.exit()

    def handleGenericMultifileError(self):
        if not self.currentMfname:
            sys.exit()
        if self.curMultifileRetry < self.multifileRetries:
            self.notify.info('recover attempt: %s / %s' % (self.curMultifileRetry, self.multifileRetries))
            self.curMultifileRetry += 1
            self.notify.info('downloadPatchDone: Recovering from error.' + ' Deleting files in: ' + self.currentMfname)
            self.dldb.setClientMultifileIncomplete(self.currentMfname)
            self.dldb.setClientMultifileSize(self.currentMfname, 0)
            self.notify.info('downloadPatchDone: Recovering from error.' + ' redownloading: ' + self.currentMfname)
            self.httpChannel.reset()
            self.getMultifile(self.currentMfname)
        else:
            self.setPandaErrorCode(6)
            self.notify.info('handleGenericMultifileError: Failed to download multifile')
            sys.exit()

    def foregroundSleep(self):
        if not self.backgrounded:
            time.sleep(self.ForegroundSleepTime)

    def forceSleep(self):
        if not self.backgrounded:
            time.sleep(3.0)

    def addDownloadVersion(self, serverFilePath):
        url = URLSpec(self.downloadServer)
        origPath = url.getPath()
        if origPath and origPath[-1] == '/':
            origPath = origPath[:-1]
        if self.fromCD:
            url.setPath(self.getCDDownloadPath(origPath, serverFilePath))
        else:
            url.setPath(self.getDownloadPath(origPath, serverFilePath))
        self.notify.info('***' + url.cStr())
        return url

    def download(self, serverFilePath, localFilename, callback, callbackProgress):
        self.launcherMessage(self.Localizer.LauncherDownloadFile % {'name': self.currentPhaseName,
         'current': self.currentPhaseIndex,
         'total': self.numPhases})
        task = MiniTask(self.downloadTask)
        task.downloadRam = 0
        task.serverFilePath = serverFilePath
        task.serverFileURL = self.addDownloadVersion(serverFilePath)
        self.notify.info('Download request: %s' % task.serverFileURL.cStr())
        task.callback = callback
        task.callbackProgress = callbackProgress
        task.lastUpdate = 0
        self.resetBytesPerSecond()
        task.localFilename = localFilename
        self.httpChannel.beginGetDocument(DocumentSpec(task.serverFileURL))
        self.httpChannel.downloadToFile(task.localFilename)
        self.miniTaskMgr.add(task, 'launcher-download')

    def downloadRam(self, serverFilePath, callback):
        self.ramfile = Ramfile()
        task = MiniTask(self.downloadTask)
        task.downloadRam = 1
        task.serverFilePath = serverFilePath
        task.serverFileURL = self.addDownloadVersion(serverFilePath)
        self.notify.info('Download request: %s' % task.serverFileURL.cStr())
        task.callback = callback
        task.callbackProgress = None
        task.lastUpdate = 0
        self.resetBytesPerSecond()
        self.httpChannel.beginGetDocument(DocumentSpec(task.serverFileURL))
        self.httpChannel.downloadToRam(self.ramfile)
        self.miniTaskMgr.add(task, 'launcher-download')
        return

    def downloadTask(self, task):
        self.maybeStartGame()
        if self.httpChannel.run():
            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                task.lastUpdate = now
                self.testBandwidth()
                if task.callbackProgress:
                    task.callbackProgress(task)
                bytesWritten = self.httpChannel.getBytesDownloaded()
                totalBytes = self.httpChannel.getFileSize()
                if totalBytes:
                    pct = int(round(bytesWritten / float(totalBytes) * 100))
                    self.launcherMessage(self.Localizer.LauncherDownloadFilePercent % {'name': self.currentPhaseName,
                     'current': self.currentPhaseIndex,
                     'total': self.numPhases,
                     'percent': pct})
                else:
                    self.launcherMessage(self.Localizer.LauncherDownloadFileBytes % {'name': self.currentPhaseName,
                     'current': self.currentPhaseIndex,
                     'total': self.numPhases,
                     'bytes': bytesWritten})
            self.foregroundSleep()
            return task.cont
        statusCode = self.httpChannel.getStatusCode()
        statusString = self.httpChannel.getStatusString()
        self.notify.info('HTTP status %s: %s' % (statusCode, statusString))
        if self.httpChannel.isValid() and self.httpChannel.isDownloadComplete():
            bytesWritten = self.httpChannel.getBytesDownloaded()
            totalBytes = self.httpChannel.getFileSize()
            if totalBytes:
                pct = int(round(bytesWritten / float(totalBytes) * 100))
                self.launcherMessage(self.Localizer.LauncherDownloadFilePercent % {'name': self.currentPhaseName,
                 'current': self.currentPhaseIndex,
                 'total': self.numPhases,
                 'percent': pct})
            else:
                self.launcherMessage(self.Localizer.LauncherDownloadFileBytes % {'name': self.currentPhaseName,
                 'current': self.currentPhaseIndex,
                 'total': self.numPhases,
                 'bytes': bytesWritten})
            self.notify.info('downloadTask: Download done: %s' % task.serverFileURL.cStr())
            task.callback()
            del task.callback
            return task.done
        else:
            if statusCode == HTTPChannel.SCDownloadOpenError or statusCode == HTTPChannel.SCDownloadWriteError:
                self.handleDownloadWriteError(task)
            elif statusCode == HTTPChannel.SCLostConnection:
                gotBytes = self.httpChannel.getBytesDownloaded()
                self.notify.info('Connection lost while downloading; got %s bytes.  Reconnecting.' % gotBytes)
                if task.downloadRam:
                    self.downloadRam(task.serverFilePath, task.callback)
                else:
                    self.download(task.serverFilePath, task.localFilename, task.callback, None)
            else:
                if self.httpChannel.isValid():
                    self.notify.info('Unexpected situation: no error status, but %s incompletely downloaded.' % task.serverFileURL.cStr())
                self.handleDownloadFatalError(task)
                if task.downloadRam:
                    self.downloadRam(task.serverFilePath, task.callback)
                else:
                    self.download(task.serverFilePath, task.localFilename, task.callback, None)
            return task.done
        return

    def downloadMultifile(self, serverFilename, localFilename, mfname, callback, totalSize, currentSize, callbackProgress):
        if currentSize != 0 and currentSize == totalSize:
            callback()
            return
        self.launcherMessage(self.Localizer.LauncherDownloadFile % {'name': self.currentPhaseName,
         'current': self.currentPhaseIndex,
         'total': self.numPhases})
        task = MiniTask(self.downloadMultifileTask)
        mfURL = self.addDownloadVersion(serverFilename)
        task.mfURL = mfURL
        self.notify.info('downloadMultifile: %s ' % task.mfURL.cStr())
        task.callback = callback
        task.callbackProgress = callbackProgress
        task.lastUpdate = 0
        self.httpChannel.getHeader(DocumentSpec(task.mfURL))
        if self.httpChannel.isFileSizeKnown():
            task.totalSize = self.httpChannel.getFileSize()
        else:
            task.totalSize = totalSize
        self.resetBytesPerSecond()
        task.serverFilename = serverFilename
        task.localFilename = localFilename
        task.mfname = mfname
        if currentSize != 0:
            if task.totalSize == currentSize:
                self.notify.info('already have full file! Skipping download.')
                callback()
                return
            self.httpChannel.beginGetSubdocument(DocumentSpec(task.mfURL), currentSize, task.totalSize)
            self.httpChannel.downloadToFile(task.localFilename, True)
        else:
            self.httpChannel.beginGetDocument(DocumentSpec(task.mfURL))
            self.httpChannel.downloadToFile(task.localFilename)
        self._addMiniTask(task, 'launcher-download-multifile')

    def downloadPatchSimpleProgress(self, task):
        startingByte = self.httpChannel.getFirstByteDelivered()
        bytesDownloaded = self.httpChannel.getBytesDownloaded()
        bytesWritten = startingByte + bytesDownloaded
        totalBytes = self.httpChannel.getFileSize()
        percentPatchComplete = int(round(bytesWritten / float(totalBytes) * self.downloadPercentage))
        self.setPercentPhaseComplete(self.currentPhase, percentPatchComplete)

    def getPercentPatchComplete(self, bytesWritten):
        return int(round((self.patchDownloadSoFar + bytesWritten) / float(self.totalPatchDownload) * self.downloadPercentage))

    def downloadPatchOverallProgress(self, task):
        startingByte = self.httpChannel.getFirstByteDelivered()
        bytesDownloaded = self.httpChannel.getBytesDownloaded()
        bytesWritten = startingByte + bytesDownloaded
        percentPatchComplete = self.getPercentPatchComplete(bytesWritten)
        self.setPercentPhaseComplete(self.currentPhase, percentPatchComplete)

    def downloadMultifileWriteToDisk(self, task):
        self.maybeStartGame()
        startingByte = self.httpChannel.getFirstByteDelivered()
        bytesDownloaded = self.httpChannel.getBytesDownloaded()
        bytesWritten = startingByte + bytesDownloaded
        if self.dldb:
            self.dldb.setClientMultifileSize(task.mfname, bytesWritten)
        percentComplete = 0
        if task.totalSize != 0:
            percentComplete = int(round(bytesWritten / float(task.totalSize) * self.downloadPercentage))
        self.setPercentPhaseComplete(self.currentPhase, percentComplete)

    def downloadMultifileTask(self, task):
        task.totalSize = self.httpChannel.getFileSize()
        if self.httpChannel.run():
            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                task.lastUpdate = now
                self.testBandwidth()
                if task.callbackProgress:
                    task.callbackProgress(task)
                startingByte = self.httpChannel.getFirstByteDelivered()
                bytesDownloaded = self.httpChannel.getBytesDownloaded()
                bytesWritten = startingByte + bytesDownloaded
                percentComplete = 0
                if task.totalSize != 0:
                    percentComplete = int(round(100.0 * bytesWritten / float(task.totalSize)))
                self.launcherMessage(self.Localizer.LauncherDownloadFilePercent % {'name': self.currentPhaseName,
                 'current': self.currentPhaseIndex,
                 'total': self.numPhases,
                 'percent': percentComplete})
            self.foregroundSleep()
            return task.cont
        statusCode = self.httpChannel.getStatusCode()
        statusString = self.httpChannel.getStatusString()
        self.notify.info('HTTP status %s: %s' % (statusCode, statusString))
        if self.httpChannel.isValid() and self.httpChannel.isDownloadComplete():
            if task.callbackProgress:
                task.callbackProgress(task)
            self.notify.info('done: %s' % task.mfname)
            if self.dldb:
                self.dldb.setClientMultifileComplete(task.mfname)
            task.callback()
            del task.callback
            return task.done
        else:
            if statusCode == HTTPChannel.SCDownloadOpenError or statusCode == HTTPChannel.SCDownloadWriteError:
                self.handleDownloadWriteError(task)
            elif statusCode == HTTPChannel.SCLostConnection:
                startingByte = self.httpChannel.getFirstByteDelivered()
                bytesDownloaded = self.httpChannel.getBytesDownloaded()
                bytesWritten = startingByte + bytesDownloaded
                self.notify.info('Connection lost while downloading; got %s bytes.  Reconnecting.' % bytesDownloaded)
                self.downloadMultifile(task.serverFilename, task.localFilename, task.mfname, task.callback, task.totalSize, bytesWritten, task.callbackProgress)
            elif (statusCode == 416 or statusCode == HTTPChannel.SCDownloadInvalidRange) and self.httpChannel.getFirstByteRequested() != 0:
                self.notify.info('Invalid subrange; redownloading entire file.')
                self.downloadMultifile(task.serverFilename, task.localFilename, task.mfname, task.callback, task.totalSize, 0, task.callbackProgress)
            else:
                if self.httpChannel.isValid():
                    self.notify.info('Unexpected situation: no error status, but %s incompletely downloaded.' % task.mfname)
                self.handleDownloadFatalError(task)
                self.downloadMultifile(task.serverFilename, task.localFilename, task.mfname, task.callback, task.totalSize, 0, task.callbackProgress)
            return task.done

    def decompressFile(self, localFilename, callback):
        self.notify.info('decompress: request: ' + localFilename.cStr())
        self.launcherMessage(self.Localizer.LauncherDecompressingFile % {'name': self.currentPhaseName,
         'current': self.currentPhaseIndex,
         'total': self.numPhases})
        task = MiniTask(self.decompressFileTask)
        task.localFilename = localFilename
        task.callback = callback
        task.lastUpdate = 0
        task.decompressor = Decompressor()
        errorCode = task.decompressor.initiate(task.localFilename)
        if errorCode > 0:
            self._addMiniTask(task, 'launcher-decompressFile')
        else:
            self.handleInitiateFatalError(errorCode)

    def decompressFileTask(self, task):
        errorCode = task.decompressor.run()
        if errorCode == EUOk:
            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                task.lastUpdate = now
                progress = task.decompressor.getProgress()
                self.launcherMessage(self.Localizer.LauncherDecompressingPercent % {'name': self.currentPhaseName,
                 'current': self.currentPhaseIndex,
                 'total': self.numPhases,
                 'percent': int(round(progress * 100))})
            self.foregroundSleep()
            return task.cont
        elif errorCode == EUSuccess:
            self.launcherMessage(self.Localizer.LauncherDecompressingPercent % {'name': self.currentPhaseName,
             'current': self.currentPhaseIndex,
             'total': self.numPhases,
             'percent': 100})
            self.notify.info('decompressTask: Decompress done: ' + task.localFilename.cStr())
            del task.decompressor
            task.callback()
            del task.callback
            return task.done
        elif errorCode == EUErrorAbort:
            self.handleDecompressFatalError(task, errorCode)
            return task.done
        elif errorCode == EUErrorWriteOutOfFiles or errorCode == EUErrorWriteDiskFull or errorCode == EUErrorWriteDiskSectorNotFound or errorCode == EUErrorWriteOutOfMemory or errorCode == EUErrorWriteSharingViolation or errorCode == EUErrorWriteDiskFault or errorCode == EUErrorWriteDiskNotFound:
            self.handleDecompressWriteError(task, errorCode)
            return task.done
        elif errorCode == EUErrorZlib:
            self.handleDecompressZlibError(task, errorCode)
            return task.done
        elif errorCode > 0:
            self.notify.warning('decompressMultifileTask: Unknown success return code: ' + errorToText(errorCode))
            return task.cont
        else:
            self.notify.warning('decompressMultifileTask: Unknown return code: ' + errorToText(errorCode))
            self.handleDecompressFatalError(task, errorCode)
            return task.done

    def decompressMultifile(self, mfname, localFilename, callback):
        self.notify.info('decompressMultifile: request: ' + localFilename.cStr())
        self.launcherMessage(self.Localizer.LauncherDecompressingFile % {'name': self.currentPhaseName,
         'current': self.currentPhaseIndex,
         'total': self.numPhases})
        task = MiniTask(self.decompressMultifileTask)
        task.mfname = mfname
        task.localFilename = localFilename
        task.callback = callback
        task.lastUpdate = 0
        task.decompressor = Decompressor()
        errorCode = task.decompressor.initiate(task.localFilename)
        if errorCode > 0:
            self._addMiniTask(task, 'launcher-decompressMultifile')
        else:
            self.handleInitiateFatalError(errorCode)

    def decompressMultifileTask(self, task):
        errorCode = task.decompressor.run()
        if errorCode == EUOk:
            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                task.lastUpdate = now
                progress = task.decompressor.getProgress()
                self.launcherMessage(self.Localizer.LauncherDecompressingPercent % {'name': self.currentPhaseName,
                 'current': self.currentPhaseIndex,
                 'total': self.numPhases,
                 'percent': int(round(progress * 100))})
                percentProgress = int(round(progress * self.decompressPercentage))
                totalPercent = self.downloadPercentage + percentProgress
                self.setPercentPhaseComplete(self.currentPhase, totalPercent)
            self.foregroundSleep()
            return task.cont
        elif errorCode == EUSuccess:
            self.launcherMessage(self.Localizer.LauncherDecompressingPercent % {'name': self.currentPhaseName,
             'current': self.currentPhaseIndex,
             'total': self.numPhases,
             'percent': 100})
            totalPercent = self.downloadPercentage + self.decompressPercentage
            self.setPercentPhaseComplete(self.currentPhase, totalPercent)
            self.notify.info('decompressMultifileTask: Decompress multifile done: ' + task.localFilename.cStr())
            self.dldb.setClientMultifileDecompressed(task.mfname)
            del task.decompressor
            task.callback()
            del task.callback
            return task.done
        elif errorCode == EUErrorAbort:
            self.handleDecompressFatalError(task, errorCode)
            return task.done
        elif errorCode == EUErrorWriteOutOfFiles or errorCode == EUErrorWriteDiskFull or errorCode == EUErrorWriteDiskSectorNotFound or errorCode == EUErrorWriteOutOfMemory or errorCode == EUErrorWriteSharingViolation or errorCode == EUErrorWriteDiskFault or errorCode == EUErrorWriteDiskNotFound:
            self.handleDecompressWriteError(task, errorCode)
            return task.done
        elif errorCode == EUErrorZlib:
            self.handleDecompressZlibError(task, errorCode)
            return task.done
        elif errorCode > 0:
            self.notify.warning('decompressMultifileTask: Unknown success return code: ' + errorToText(errorCode))
            return task.cont
        else:
            self.notify.warning('decompressMultifileTask: Unknown return code: ' + errorToText(errorCode))
            self.handleDecompressFatalError(task, errorCode)
            return task.done

    def extract(self, mfname, localFilename, destDir, callback):
        self.notify.info('extract: request: ' + localFilename.cStr() + ' destDir: ' + destDir.cStr())
        self.launcherMessage(self.Localizer.LauncherExtractingFile % {'name': self.currentPhaseName,
         'current': self.currentPhaseIndex,
         'total': self.numPhases})
        task = MiniTask(self.extractTask)
        task.mfname = mfname
        task.localFilename = localFilename
        task.destDir = destDir
        task.callback = callback
        task.lastUpdate = 0
        task.extractor = Extractor()
        task.extractor.setExtractDir(task.destDir)
        if not task.extractor.setMultifile(task.localFilename):
            self.setPandaErrorCode(6)
            self.notify.info('extract: Unable to open multifile %s' % task.localFilename.cStr())
            sys.exit()
        numFiles = self.dldb.getServerNumFiles(mfname)
        for i in range(numFiles):
            subfile = self.dldb.getServerFileName(mfname, i)
            if not task.extractor.requestSubfile(Filename(subfile)):
                self.setPandaErrorCode(6)
                self.notify.info('extract: Unable to find subfile %s in multifile %s' % (subfile, mfname))
                sys.exit()

        self.notify.info('Extracting %d subfiles from multifile %s.' % (numFiles, mfname))
        self._addMiniTask(task, 'launcher-extract')

    def extractTask(self, task):
        errorCode = task.extractor.step()
        if errorCode == EUOk:
            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                task.lastUpdate = now
                progress = task.extractor.getProgress()
                self.launcherMessage(self.Localizer.LauncherExtractingPercent % {'name': self.currentPhaseName,
                 'current': self.currentPhaseIndex,
                 'total': self.numPhases,
                 'percent': int(round(progress * 100.0))})
                percentProgress = int(round(progress * self.extractPercentage))
                totalPercent = self.downloadPercentage + self.decompressPercentage + percentProgress
                self.setPercentPhaseComplete(self.currentPhase, totalPercent)
            self.foregroundSleep()
            return task.cont
        elif errorCode == EUSuccess:
            self.launcherMessage(self.Localizer.LauncherExtractingPercent % {'name': self.currentPhaseName,
             'current': self.currentPhaseIndex,
             'total': self.numPhases,
             'percent': 100})
            totalPercent = self.downloadPercentage + self.decompressPercentage + self.extractPercentage
            self.setPercentPhaseComplete(self.currentPhase, totalPercent)
            self.notify.info('extractTask: Extract multifile done: ' + task.localFilename.cStr())
            self.dldb.setClientMultifileExtracted(task.mfname)
            del task.extractor
            task.callback()
            del task.callback
            return task.done
        elif errorCode == EUErrorAbort:
            self.handleExtractFatalError(task, errorCode)
            return task.done
        elif errorCode == EUErrorFileEmpty:
            self.handleExtractFatalError(task, errorCode)
            return task.done
        elif errorCode == EUErrorWriteOutOfFiles or errorCode == EUErrorWriteDiskFull or errorCode == EUErrorWriteDiskSectorNotFound or errorCode == EUErrorWriteOutOfMemory or errorCode == EUErrorWriteSharingViolation or errorCode == EUErrorWriteDiskFault or errorCode == EUErrorWriteDiskNotFound:
            self.handleExtractWriteError(task, errorCode)
            return task.done
        elif errorCode > 0:
            self.notify.warning('extractTask: Unknown success return code: ' + errorToText(errorCode))
            return task.cont
        else:
            self.notify.warning('extractTask: Unknown error return code: ' + errorToText(errorCode))
            self.handleExtractFatalError(task, errorCode)
            return task.done

    def patch(self, patchFile, patcheeFile, callback):
        self.notify.info('patch: request: ' + patchFile.cStr() + ' patchee: ' + patcheeFile.cStr())
        self.launcherMessage(self.Localizer.LauncherPatchingFile % {'name': self.currentPhaseName,
         'current': self.currentPhaseIndex,
         'total': self.numPhases})
        task = MiniTask(self.patchTask)
        task.patchFile = patchFile
        task.patcheeFile = patcheeFile
        task.callback = callback
        task.lastUpdate = 0
        task.patcher = Patcher()
        errorCode = task.patcher.initiate(task.patchFile, task.patcheeFile)
        if errorCode > 0:
            self._addMiniTask(task, 'launcher-patch')
        else:
            self.handleInitiateFatalError(errorCode)

    def patchTask(self, task):
        errorCode = task.patcher.run()
        if errorCode == EUOk:
            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                task.lastUpdate = now
                progress = task.patcher.getProgress()
                self.launcherMessage(self.Localizer.LauncherPatchingPercent % {'name': self.currentPhaseName,
                 'current': self.currentPhaseIndex,
                 'total': self.numPhases,
                 'percent': int(round(progress * 100.0))})
            self.foregroundSleep()
            return task.cont
        elif errorCode == EUSuccess:
            self.launcherMessage(self.Localizer.LauncherPatchingPercent % {'name': self.currentPhaseName,
             'current': self.currentPhaseIndex,
             'total': self.numPhases,
             'percent': 100})
            self.notify.info('patchTask: Patch done: ' + task.patcheeFile.cStr())
            del task.patcher
            task.callback()
            del task.callback
            return task.done
        elif errorCode == EUErrorAbort:
            self.handlePatchFatalError(task, errorCode)
            return task.done
        elif errorCode == EUErrorFileEmpty:
            self.handlePatchFatalError(task, errorCode)
            return task.done
        elif errorCode == EUErrorWriteOutOfFiles or errorCode == EUErrorWriteDiskFull or errorCode == EUErrorWriteDiskSectorNotFound or errorCode == EUErrorWriteOutOfMemory or errorCode == EUErrorWriteSharingViolation or errorCode == EUErrorWriteDiskFault or errorCode == EUErrorWriteDiskNotFound:
            self.handlePatchWriteError(task, errorCode)
            return task.done
        elif errorCode > 0:
            self.notify.warning('patchTask: Unknown success return code: ' + errorToText(errorCode))
            return task.cont
        else:
            self.notify.warning('patchTask: Unknown error return code: ' + errorToText(errorCode))
            self.handlePatchFatalError(task, errorCode)
            return task.done

    def getProgressSum(self, phase):
        sum = 0
        for i in xrange(0, len(self.linesInProgress)):
            if self.linesInProgress[i].find(phase) > -1:
                nameSizeTuple = self.linesInProgress[i].split()
                numSize = nameSizeTuple[1].split('L')
                sum += string.atoi(numSize[0])

        return sum

    def readProgressFile(self):
        localFilename = Filename(self.dbDir, Filename(self.progressFilename))
        if not localFilename.exists():
            self.notify.warning('File does not exist: %s' % localFilename.cStr())
            self.linesInProgress = []
        else:
            f = open(localFilename.toOsSpecific())
            self.linesInProgress = f.readlines()
            f.close()
            localFilename.unlink()
        self.progressSum = 0
        token = 'phase_'
        self.progressSum = self.getProgressSum(token)
        self.progressSum -= self.getProgressSum(token + '2')
        self.notify.info('total phases to be downloaded = ' + `(self.progressSum)`)
        self.checkClientDbExists()

    def prepareClient(self):
        self.notify.info('prepareClient: Preparing client for install')
        if not self.topDir.exists():
            self.notify.info('prepareClient: Creating top directory: ' + self.topDir.cStr())
            os.makedirs(self.topDir.toOsSpecific())
        if not self.dbDir.exists():
            self.notify.info('prepareClient: Creating db directory: ' + self.dbDir.cStr())
            os.makedirs(self.dbDir.toOsSpecific())
        if not self.patchDir.exists():
            self.notify.info('prepareClient: Creating patch directory: ' + self.patchDir.cStr())
            os.makedirs(self.patchDir.toOsSpecific())
        if not self.mfDir.exists():
            self.notify.info('prepareClient: Creating mf directory: ' + self.mfDir.cStr())
            os.makedirs(self.mfDir.toOsSpecific())

    def downloadLauncherFileDb(self):
        self.notify.info('Downloading launcherFileDb')
        self.downloadRam(self.launcherFileDbFilename, self.downloadLauncherFileDbDone)

    def downloadLauncherFileDbDone(self):
        self.launcherFileDbHash = HashVal()
        self.launcherFileDbHash.hashRamfile(self.ramfile)
        if self.VerifyFiles:
            self.notify.info('Validating Launcher files')
            for fileDesc in self.ramfile.readlines():
                try:
                    filename, hashStr = fileDesc.split(' ', 1)
                except:
                    self.notify.info('Invalid line: "%s"' % fileDesc)
                    self.failLauncherFileDb('No hash in launcherFileDb')

                serverHash = HashVal()
                if not self.hashIsValid(serverHash, hashStr):
                    self.notify.info('Not a valid hash string: "%s"' % hashStr)
                    self.failLauncherFileDb('Invalid hash in launcherFileDb')
                localHash = HashVal()
                localFilename = Filename(self.topDir, Filename(filename))
                localHash.hashFile(localFilename)
                if localHash != serverHash:
                    self.failLauncherFileDb('%s does not match expected version.' % filename)

        self.downloadServerDbFile()

    def failLauncherFileDb(self, string):
        self.notify.info(string)
        self.setPandaErrorCode(15)
        sys.exit()

    def downloadServerDbFile(self):
        self.notify.info('Downloading server db file')
        self.launcherMessage(self.Localizer.LauncherDownloadServerFileList)
        self.downloadRam(self.serverDbFilePath, self.downloadServerDbFileDone)

    def downloadServerDbFileDone(self):
        self.serverDbFileHash = HashVal()
        self.serverDbFileHash.hashRamfile(self.ramfile)
        self.readProgressFile()

    def checkClientDbExists(self):
        clientFilename = Filename(self.dbDir, Filename(self.clientDbFilename))
        if clientFilename.exists():
            self.notify.info('Client Db exists')
            self.createDownloadDb()
        else:
            self.notify.info('Client Db does not exist')
            self.downloadClientDbStarterFile()

    def downloadClientDbStarterFile(self):
        self.notify.info('Downloading Client Db starter file')
        localFilename = Filename(self.dbDir, Filename(self.compClientDbFilename))
        self.download(self.clientStarterDbFilePath, localFilename, self.downloadClientDbStarterFileDone, None)
        return

    def downloadClientDbStarterFileDone(self):
        localFilename = Filename(self.dbDir, Filename(self.compClientDbFilename))
        decompressor = Decompressor()
        decompressor.decompress(localFilename)
        self.createDownloadDb()

    def createDownloadDb(self):
        self.notify.info('Creating downloadDb')
        self.launcherMessage(self.Localizer.LauncherCreatingDownloadDb)
        clientFilename = Filename(self.dbDir, Filename(self.clientDbFilename))
        self.notify.info('Client file name: ' + clientFilename.cStr())
        self.launcherMessage(self.Localizer.LauncherDownloadClientFileList)
        serverFile = self.ramfile
        decompressor = Decompressor()
        decompressor.decompress(serverFile)
        self.notify.info('Finished decompress')
        self.dldb = DownloadDb(serverFile, clientFilename)
        self.notify.info('created download db')
        self.launcherMessage(self.Localizer.LauncherFinishedDownloadDb)
        self.currentPhase = self.LauncherPhases[0]
        self.currentPhaseIndex = 1
        self.currentPhaseName = self.Localizer.LauncherPhaseNames[self.currentPhase]
        self.updatePhase(self.currentPhase)

    def maybeStartGame(self):
        if not self.started and self.currentPhase >= self.showPhase:
            self.started = True
            self.notify.info('maybeStartGame: starting game')
            self.launcherMessage(self.Localizer.LauncherStartingGame)
            self.background()
            __builtin__.launcher = self
            self.startGame()

    def _runTaskManager(self):
        if not self.taskMgrStarted:
            self.miniTaskMgr.run()
            self.notify.info('Switching task managers.')
        taskMgr.run()

    def _stepMiniTaskManager(self, task):
        self.miniTaskMgr.step()
        if self.miniTaskMgr.taskList:
            return task.cont
        self.notify.info('Stopping mini task manager.')
        self.miniTaskMgr = None
        return task.done

    def _addMiniTask(self, task, name):
        if not self.miniTaskMgr:
            self.notify.info('Restarting mini task manager.')
            self.miniTaskMgr = MiniTaskManager()
            from direct.task.TaskManagerGlobal import taskMgr
            taskMgr.remove('miniTaskManager')
            taskMgr.add(self._stepMiniTaskManager, 'miniTaskManager')
        self.miniTaskMgr.add(task, name)

    def newTaskManager(self):
        self.taskMgrStarted = True
        if self.miniTaskMgr.running:
            self.miniTaskMgr.stop()
        from direct.task.TaskManagerGlobal import taskMgr
        taskMgr.remove('miniTaskManager')
        taskMgr.add(self._stepMiniTaskManager, 'miniTaskManager')

    def mainLoop(self):
        try:
            self._runTaskManager()
        except SystemExit:
            if hasattr(__builtin__, 'base'):
                base.destroy()
            self.notify.info('Normal exit.')
            raise
        except:
            self.setPandaErrorCode(12)
            self.notify.warning('Handling Python exception.')
            if hasattr(__builtin__, 'base') and getattr(base, 'cr', None):
                if base.cr.timeManager:
                    from otp.otpbase import OTPGlobals
                    base.cr.timeManager.setDisconnectReason(OTPGlobals.DisconnectPythonError)
                    base.cr.timeManager.setExceptionInfo()
                base.cr.sendDisconnect()
            if hasattr(__builtin__, 'base'):
                base.destroy()
            self.notify.info('Exception exit.\n')
            import traceback
            traceback.print_exc()
            sys.exit()

        return

    def updatePhase(self, phase):
        self.notify.info('Updating multifiles in phase: ' + `phase`)
        self.setPercentPhaseComplete(self.currentPhase, 0)
        self.phaseMultifileNames = []
        numfiles = self.dldb.getServerNumMultifiles()
        for i in range(self.dldb.getServerNumMultifiles()):
            mfname = self.dldb.getServerMultifileName(i)
            if self.dldb.getServerMultifilePhase(mfname) == phase:
                self.phaseMultifileNames.append(mfname)

        self.updateNextMultifile()

    def updateNextMultifile(self):
        if len(self.phaseMultifileNames) > 0:
            self.currentMfname = self.phaseMultifileNames.pop()
            self.curMultifileRetry = 0
            self.getMultifile(self.currentMfname)
        else:
            if self.currentMfname is None:
                self.notify.warning('no multifile found! See below for debug info:')
                for i in range(self.dldb.getServerNumMultifiles()):
                    mfname = self.dldb.getServerMultifileName(i)
                    phase = self.dldb.getServerMultifilePhase(mfname)
                    print i, mfname, phase

                self.handleGenericMultifileError()
            decompressedMfname = os.path.splitext(self.currentMfname)[0]
            localFilename = Filename(self.mfDir, Filename(decompressedMfname))
            nextIndex = self.LauncherPhases.index(self.currentPhase) + 1
            if nextIndex < len(self.LauncherPhases):
                self.MakeNTFSFilesGlobalWriteable(localFilename)
            else:
                self.MakeNTFSFilesGlobalWriteable()
            vfs = VirtualFileSystem.getGlobalPtr()
            vfs.mount(localFilename, '.', VirtualFileSystem.MFReadOnly)
            self.setPercentPhaseComplete(self.currentPhase, 100)
            self.notify.info('Done updating multifiles in phase: ' + `(self.currentPhase)`)
            self.progressSoFar += int(round(self.phaseOverallMap[self.currentPhase] * 100))
            self.notify.info('progress so far ' + `(self.progressSoFar)`)
            messenger.send('phaseComplete-' + `(self.currentPhase)`)
            if nextIndex < len(self.LauncherPhases):
                self.currentPhase = self.LauncherPhases[nextIndex]
                self.currentPhaseIndex = nextIndex + 1
                self.currentPhaseName = self.Localizer.LauncherPhaseNames[self.currentPhase]
                self.updatePhase(self.currentPhase)
            else:
                self.notify.info('ALL PHASES COMPLETE')
                self.maybeStartGame()
                messenger.send('launcherAllPhasesComplete')
                self.cleanup()
        return

    def isDownloadComplete(self):
        return self._downloadComplete

    def updateMultifileDone(self):
        self.updateNextMultifile()

    def downloadMultifileDone(self):
        self.getDecompressMultifile(self.currentMfname)

    def getMultifile(self, mfname):
        self.notify.info('Downloading multifile: ' + mfname)
        if not self.dldb.clientMultifileExists(mfname):
            self.maybeStartGame()
            self.notify.info('Multifile does not exist in client db,' + 'creating new record: ' + mfname)
            self.dldb.addClientMultifile(mfname)
            curHash = self.dldb.getServerMultifileHash(mfname)
            self.dldb.setClientMultifileHash(mfname, curHash)
            localFilename = Filename(self.mfDir, Filename(mfname))
            if localFilename.exists():
                curSize = localFilename.getFileSize()
                self.dldb.setClientMultifileSize(mfname, curSize)
                if curSize == self.dldb.getServerMultifileSize(mfname):
                    self.dldb.setClientMultifileComplete(mfname)
        decompressedMfname = os.path.splitext(mfname)[0]
        decompressedFilename = Filename(self.mfDir, Filename(decompressedMfname))
        if (not self.dldb.clientMultifileComplete(mfname) or not self.dldb.clientMultifileDecompressed(mfname)) and decompressedFilename.exists():
            clientMd5 = HashVal()
            clientMd5.hashFile(decompressedFilename)
            clientVer = self.dldb.getVersion(Filename(decompressedMfname), clientMd5)
            if clientVer != -1:
                self.notify.info('Decompressed multifile is already on disk and correct: %s (version %s)' % (mfname, clientVer))
                self.dldb.setClientMultifileComplete(mfname)
                self.dldb.setClientMultifileDecompressed(mfname)
                compressedFilename = Filename(self.mfDir, Filename(mfname))
                compressedFilename.unlink()
                extractedOk = True
                numFiles = self.dldb.getServerNumFiles(mfname)
                for i in range(numFiles):
                    subfile = self.dldb.getServerFileName(mfname, i)
                    fn = Filename(self.mfDir, Filename(subfile))
                    if fn.compareTimestamps(decompressedFilename) <= 0:
                        extractedOk = False
                        break

                if extractedOk:
                    self.notify.info('Multifile appears to have been extracted already.')
                    self.dldb.setClientMultifileExtracted(mfname)
        if not self.dldb.clientMultifileComplete(mfname) or not decompressedFilename.exists():
            self.maybeStartGame()
            currentSize = self.dldb.getClientMultifileSize(mfname)
            totalSize = self.dldb.getServerMultifileSize(mfname)
            localFilename = Filename(self.mfDir, Filename(mfname))
            if not localFilename.exists():
                currentSize = 0
            else:
                currentSize = min(currentSize, localFilename.getFileSize())
            if currentSize == 0:
                self.notify.info('Multifile has not been started, ' + 'downloading new file: ' + mfname)
                curHash = self.dldb.getServerMultifileHash(mfname)
                self.dldb.setClientMultifileHash(mfname, curHash)
                self.phaseNewDownload[self.currentPhase] = 1
                self.downloadMultifile(self.contentDir + mfname, localFilename, mfname, self.downloadMultifileDone, totalSize, 0, self.downloadMultifileWriteToDisk)
            else:
                clientHash = self.dldb.getClientMultifileHash(mfname)
                serverHash = self.dldb.getServerMultifileHash(mfname)
                if clientHash.eq(serverHash):
                    self.notify.info('Multifile is not complete, finishing download for %s, size = %s / %s' % (mfname, currentSize, totalSize))
                    self.downloadMultifile(self.contentDir + mfname, localFilename, mfname, self.downloadMultifileDone, totalSize, currentSize, self.downloadMultifileWriteToDisk)
                elif self.curMultifileRetry < self.multifileRetries:
                    self.notify.info('recover attempt: %s / %s' % (self.curMultifileRetry, self.multifileRetries))
                    self.curMultifileRetry += 1
                    self.notify.info('Multifile is not complete, and is out of date. ' + 'Restarting download with newest multifile')
                    self.dldb.setClientMultifileIncomplete(self.currentMfname)
                    self.dldb.setClientMultifileSize(self.currentMfname, 0)
                    self.dldb.setClientMultifileHash(self.currentMfname, serverHash)
                    self.getMultifile(self.currentMfname)
                else:
                    self.setPandaErrorCode(6)
                    self.notify.info('getMultifile: Failed to download multifile')
                    sys.exit()
        else:
            self.notify.info('Multifile already complete: ' + mfname)
            self.downloadMultifileDone()

    def updateMultifileDone(self):
        self.updateNextMultifile()

    def downloadMultifileDone(self):
        self.getDecompressMultifile(self.currentMfname)

    def getMultifile(self, mfname):
        self.notify.info('Downloading multifile: ' + mfname)
        if not self.dldb.clientMultifileExists(mfname):
            self.maybeStartGame()
            self.notify.info('Multifile does not exist in client db,' + 'creating new record: ' + mfname)
            self.dldb.addClientMultifile(mfname)
            if self.DecompressMultifiles:
                curHash = self.dldb.getServerMultifileHash(mfname)
                self.dldb.setClientMultifileHash(mfname, curHash)
                localFilename = Filename(self.mfDir, Filename(mfname))
                if localFilename.exists():
                    curSize = localFilename.getFileSize()
                    self.dldb.setClientMultifileSize(mfname, curSize)
                    if curSize == self.dldb.getServerMultifileSize(mfname):
                        self.dldb.setClientMultifileComplete(mfname)
        decompressedMfname = os.path.splitext(mfname)[0]
        decompressedFilename = Filename(self.mfDir, Filename(decompressedMfname))
        if self.DecompressMultifiles:
            if (not self.dldb.clientMultifileComplete(mfname) or not self.dldb.clientMultifileDecompressed(mfname)) and decompressedFilename.exists():
                clientMd5 = HashVal()
                clientMd5.hashFile(decompressedFilename)
                clientVer = self.dldb.getVersion(Filename(decompressedMfname), clientMd5)
                if clientVer != -1:
                    self.notify.info('Decompressed multifile is already on disk and correct: %s (version %s)' % (mfname, clientVer))
                    self.dldb.setClientMultifileComplete(mfname)
                    self.dldb.setClientMultifileDecompressed(mfname)
                    compressedFilename = Filename(self.mfDir, Filename(mfname))
                    compressedFilename.unlink()
                    extractedOk = True
                    numFiles = self.dldb.getServerNumFiles(mfname)
                    for i in range(numFiles):
                        subfile = self.dldb.getServerFileName(mfname, i)
                        fn = Filename(self.mfDir, Filename(subfile))
                        if fn.compareTimestamps(decompressedFilename) <= 0:
                            extractedOk = False
                            break

                    if extractedOk:
                        self.notify.info('Multifile appears to have been extracted already.')
                        self.dldb.setClientMultifileExtracted(mfname)
        if not self.dldb.clientMultifileComplete(mfname) or not decompressedFilename.exists():
            self.maybeStartGame()
            currentSize = self.dldb.getClientMultifileSize(mfname)
            totalSize = self.dldb.getServerMultifileSize(mfname)
            localFilename = Filename(self.mfDir, Filename(mfname))
            if not localFilename.exists():
                currentSize = 0
            if currentSize == 0:
                self.notify.info('Multifile has not been started, ' + 'downloading new file: ' + mfname)
                curHash = self.dldb.getServerMultifileHash(mfname)
                self.dldb.setClientMultifileHash(mfname, curHash)
                self.phaseNewDownload[self.currentPhase] = 1
                self.downloadMultifile(self.contentDir + mfname, localFilename, mfname, self.downloadMultifileDone, totalSize, 0, self.downloadMultifileWriteToDisk)
            else:
                clientHash = self.dldb.getClientMultifileHash(mfname)
                serverHash = self.dldb.getServerMultifileHash(mfname)
                if clientHash.eq(serverHash):
                    self.notify.info('Multifile is not complete, finishing download for %s, size = %s / %s' % (mfname, currentSize, totalSize))
                    self.downloadMultifile(self.contentDir + mfname, localFilename, mfname, self.downloadMultifileDone, totalSize, currentSize, self.downloadMultifileWriteToDisk)
                elif self.curMultifileRetry < self.multifileRetries:
                    self.notify.info('recover attempt: %s / %s' % (self.curMultifileRetry, self.multifileRetries))
                    self.curMultifileRetry += 1
                    self.notify.info('Multifile is not complete, and is out of date. ' + 'Restarting download with newest multifile')
                    self.dldb.setClientMultifileIncomplete(self.currentMfname)
                    self.dldb.setClientMultifileSize(self.currentMfname, 0)
                    if self.DecompressMultifiles:
                        self.dldb.setClientMultifileHash(self.currentMfname, serverHash)
                    self.getMultifile(self.currentMfname)
                else:
                    self.setPandaErrorCode(6)
                    self.notify.info('getMultifile: Failed to download multifile')
                    sys.exit()
        else:
            self.notify.info('Multifile already complete: ' + mfname)
            self.downloadMultifileDone()

    def getDecompressMultifile(self, mfname):
        if not self.DecompressMultifiles:
            self.decompressMultifileDone()
        elif not self.dldb.clientMultifileDecompressed(mfname):
            self.maybeStartGame()
            self.notify.info('decompressMultifile: Decompressing multifile: ' + mfname)
            localFilename = Filename(self.mfDir, Filename(mfname))
            self.decompressMultifile(mfname, localFilename, self.decompressMultifileDone)
        else:
            self.notify.info('decompressMultifile: Multifile already decompressed: ' + mfname)
            self.decompressMultifileDone()

    def decompressMultifileDone(self):
        if self.phaseNewDownload[self.currentPhase]:
            self.setPercentPhaseComplete(self.currentPhase, 95)
        self.extractMultifile(self.currentMfname)

    def extractMultifile(self, mfname):
        if not self.dldb.clientMultifileExtracted(mfname):
            self.maybeStartGame()
            self.notify.info('extractMultifile: Extracting multifile: ' + mfname)
            decompressedMfname = os.path.splitext(mfname)[0]
            localFilename = Filename(self.mfDir, Filename(decompressedMfname))
            destDir = Filename(self.topDir)
            self.notify.info('extractMultifile: Extracting: ' + localFilename.cStr() + ' to: ' + destDir.cStr())
            self.extract(mfname, localFilename, destDir, self.extractMultifileDone)
        else:
            self.notify.info('extractMultifile: Multifile already extracted: ' + mfname)
            self.extractMultifileDone()

    def extractMultifileDone(self):
        if self.phaseNewDownload[self.currentPhase]:
            self.setPercentPhaseComplete(self.currentPhase, 99)
        self.notify.info('extractMultifileDone: Finished updating multifile: ' + self.currentMfname)
        self.patchMultifile()

    def getPatchFilename(self, fname, currentVersion):
        return fname + '.v' + `currentVersion` + '.' + self.patchExtension

    def downloadPatches(self):
        if len(self.patchList) > 0:
            self.currentPatch, self.currentPatchee, self.currentPatchVersion = self.patchList.pop()
            self.notify.info(self.contentDir)
            self.notify.info(self.currentPatch)
            patchFile = self.currentPatch + '.pz'
            serverPatchFilePath = self.contentDir + patchFile
            self.notify.info(serverPatchFilePath)
            localPatchFilename = Filename(self.patchDir, Filename(patchFile))
            if self.currentPhase > 3:
                self.download(serverPatchFilePath, localPatchFilename, self.downloadPatchDone, self.downloadPatchSimpleProgress)
            else:
                self.download(serverPatchFilePath, localPatchFilename, self.downloadPatchDone, self.downloadPatchOverallProgress)
        else:
            self.notify.info('applyNextPatch: Done patching multifile: ' + `(self.currentPhase)`)
            self.patchDone()

    def downloadPatchDone(self):
        self.patchDownloadSoFar += self.httpChannel.getBytesDownloaded()
        self.notify.info('downloadPatchDone: Decompressing patch file: ' + self.currentPatch + '.pz')
        self.decompressFile(Filename(self.patchDir, Filename(self.currentPatch + '.pz')), self.decompressPatchDone)

    def decompressPatchDone(self):
        self.notify.info('decompressPatchDone: Patching file: ' + self.currentPatchee + ' from ver: ' + `(self.currentPatchVersion)`)
        patchFile = Filename(self.patchDir, Filename(self.currentPatch))
        patchFile.setBinary()
        patchee = Filename(self.mfDir, Filename(self.currentPatchee))
        patchee.setBinary()
        self.patch(patchFile, patchee, self.downloadPatches)

    def patchDone(self):
        self.notify.info('patchDone: Patch successful')
        del self.currentPatch
        del self.currentPatchee
        del self.currentPatchVersion
        decompressedMfname = os.path.splitext(self.currentMfname)[0]
        localFilename = Filename(self.mfDir, Filename(decompressedMfname))
        destDir = Filename(self.topDir)
        self.extract(self.currentMfname, localFilename, destDir, self.updateMultifileDone)

    def startReextractingFiles(self):
        self.notify.info('startReextractingFiles: Reextracting ' + `(len(self.reextractList))` + ' files for multifile: ' + self.currentMfname)
        self.launcherMessage(self.Localizer.LauncherRecoverFiles)
        self.currentMfile = Multifile()
        decompressedMfname = os.path.splitext(self.currentMfname)[0]
        self.currentMfile.openRead(Filename(self.mfDir, Filename(decompressedMfname)))
        self.reextractNextFile()

    def reextractNextFile(self):
        failure = 0
        while not failure and len(self.reextractList) > 0:
            currentReextractFile = self.reextractList.pop()
            subfileIndex = self.currentMfile.findSubfile(currentReextractFile)
            if subfileIndex >= 0:
                destFilename = Filename(self.topDir, Filename(currentReextractFile))
                result = self.currentMfile.extractSubfile(subfileIndex, destFilename)
                if not result:
                    self.notify.warning('reextractNextFile: Failure on reextract.')
                    failure = 1
            else:
                self.notify.warning('reextractNextFile: File not found in multifile: ' + `currentReextractFile`)
                failure = 1

        if failure:
            sys.exit()
        self.notify.info('reextractNextFile: Done reextracting files for multifile: ' + `(self.currentPhase)`)
        del self.currentMfile
        self.updateMultifileDone()

    def patchMultifile(self):
        self.launcherMessage(self.Localizer.LauncherCheckUpdates % {'name': self.currentPhaseName,
         'current': self.currentPhaseIndex,
         'total': self.numPhases})
        self.notify.info('patchMultifile: Checking for patches on multifile: ' + self.currentMfname)
        self.patchList = []
        clientMd5 = HashVal()
        decompressedMfname = os.path.splitext(self.currentMfname)[0]
        localFilename = Filename(self.mfDir, Filename(decompressedMfname))
        clientMd5.hashFile(localFilename)
        clientVer = self.dldb.getVersion(Filename(decompressedMfname), clientMd5)
        if clientVer == 1:
            self.patchAndHash()
            return
        elif clientVer == -1:
            self.notify.info('patchMultifile: Invalid hash for file: ' + self.currentMfname)
            self.maybeStartGame()
            if self.curMultifileRetry < self.multifileRetries:
                self.notify.info('recover attempt: %s / %s' % (self.curMultifileRetry, self.multifileRetries))
                self.curMultifileRetry += 1
                self.notify.info('patchMultifile: Restarting download with newest multifile')
                self.dldb.setClientMultifileIncomplete(self.currentMfname)
                self.dldb.setClientMultifileSize(self.currentMfname, 0)
                self.getMultifile(self.currentMfname)
            else:
                self.setPandaErrorCode(6)
                self.notify.info('patchMultifile: Failed to download multifile')
                sys.exit()
            return
        elif clientVer > 1:
            self.notify.info('patchMultifile: Old version for multifile: ' + self.currentMfname + ' Client ver: ' + `clientVer`)
            self.maybeStartGame()
            self.totalPatchDownload = 0
            self.patchDownloadSoFar = 0
            for ver in range(1, clientVer):
                patch = self.getPatchFilename(decompressedMfname, ver + 1)
                patchee = decompressedMfname
                patchVersion = ver + 1
                self.patchList.append((patch, patchee, patchVersion))
                if self.currentPhase == 3:
                    self.totalPatchDownload += self.getProgressSum(patch)

            self.notify.info('total patch to be downloaded = ' + `(self.totalPatchDownload)`)
            self.downloadPatches()
            return

    def patchAndHash(self):
        self.reextractList = []
        self.PAHClean = 1
        self.PAHNumFiles = self.dldb.getServerNumFiles(self.currentMfname)
        self.PAHFileCounter = 0
        if self.PAHNumFiles > 0:
            task = MiniTask(self.patchAndHashTask)
            task.cleanCallback = self.updateMultifileDone
            task.uncleanCallback = self.startReextractingFiles
            self._addMiniTask(task, 'patchAndHash')
        else:
            self.updateMultifileDone()

    def patchAndHashTask(self, task):
        self.launcherMessage(self.Localizer.LauncherVerifyPhase)
        if self.PAHFileCounter == self.PAHNumFiles:
            if self.PAHClean:
                task.cleanCallback()
            else:
                task.uncleanCallback()
            return task.done
        else:
            i = self.PAHFileCounter
            self.PAHFileCounter += 1
        fname = self.dldb.getServerFileName(self.currentMfname, i)
        fnameFilename = Filename(self.topDir, Filename(fname))
        if not os.path.exists(fnameFilename.toOsSpecific()):
            self.notify.info('patchAndHash: File not found: ' + fname)
            self.reextractList.append(fname)
            self.PAHClean = 0
            return task.cont
        if self.VerifyFiles and self.dldb.hasVersion(Filename(fname)):
            clientMd5 = HashVal()
            clientMd5.hashFile(fnameFilename)
            clientVer = self.dldb.getVersion(Filename(fname), clientMd5)
            if clientVer == 1:
                return task.cont
            else:
                self.notify.info('patchAndHash: Invalid hash for file: ' + fname)
                self.reextractList.append(fname)
                self.PAHClean = 0
        return task.cont

    def launcherMessage(self, msg):
        if msg != self.lastLauncherMsg:
            self.lastLauncherMsg = msg
            self.notify.info(msg)

    def isTestServer(self):
        return self.testServerFlag

    def recordPeriodTimeRemaining(self, secondsRemaining):
        self.setValue(self.PeriodTimeRemainingKey, int(secondsRemaining))

    def recordPeriodName(self, periodName):
        self.setValue(self.PeriodNameKey, periodName)

    def recordSwid(self, swid):
        self.setValue(self.SwidKey, swid)

    def getGoUserName(self):
        return self.goUserName

    def setGoUserName(self, userName):
        self.goUserName = userName

    def getInstallDir(self):
        return self.topDir.cStr()

    def setPandaWindowOpen(self):
        self.setValue(self.PandaWindowOpenKey, 1)

    def setPandaErrorCode(self, code):
        self.notify.info('setting panda error code to %s' % code)
        self.pandaErrorCode = code
        errorLog = open(self.errorfile, 'w')
        errorLog.write(str(code) + '\n')
        errorLog.flush()
        errorLog.close()

    def getPandaErrorCode(self):
        return self.pandaErrorCode

    def setDisconnectDetailsNormal(self):
        self.notify.info('Setting Disconnect Details normal')
        self.disconnectCode = 0
        self.disconnectMsg = 'normal'

    def setDisconnectDetails(self, newCode, newMsg):
        self.notify.info('New Disconnect Details: %s - %s ' % (newCode, newMsg))
        self.disconnectCode = newCode
        self.disconnectMsg = newMsg

    def setServerVersion(self, version):
        self.ServerVersion = version

    def getServerVersion(self):
        return self.ServerVersion

    def getIsNewInstallation(self):
        result = self.getValue(self.NewInstallationKey, 1)
        result = base.config.GetBool('new-installation', result)
        return result

    def setIsNotNewInstallation(self):
        self.setValue(self.NewInstallationKey, 0)

    def getLastLogin(self):
        return self.getValue(self.LastLoginKey, '')

    def setLastLogin(self, login):
        self.setValue(self.LastLoginKey, login)

    def setUserLoggedIn(self):
        self.setValue(self.UserLoggedInKey, '1')

    def setPaidUserLoggedIn(self):
        self.setValue(self.PaidUserLoggedInKey, '1')

    def getReferrerCode(self):
        return self.getValue(self.ReferrerKey, None)

    def getPhaseComplete(self, phase):
        percentDone = self.phaseComplete[phase]
        return percentDone == 100

    def setPercentPhaseComplete(self, phase, percent):
        self.notify.info('phase updating %s, %s' % (phase, percent))
        oldPercent = self.phaseComplete[phase]
        if oldPercent != percent:
            self.phaseComplete[phase] = percent
            messenger.send('launcherPercentPhaseComplete', [phase,
             percent,
             self.getBandwidth(),
             self.byteRate])
            percentPhaseCompleteKey = 'PERCENT_PHASE_COMPLETE_' + `phase`
            self.setRegistry(percentPhaseCompleteKey, percent)
            self.overallComplete = int(round(percent * self.phaseOverallMap[phase])) + self.progressSoFar
            self.setRegistry('PERCENT_OVERALL_COMPLETE', self.overallComplete)

    def getPercentPhaseComplete(self, phase):
        return self.phaseComplete[phase]
        dr = finalRequested - startRequested
        if dt <= 0.0:
            return -1
        self.byteRate = db / dt
        self.byteRateRequested = dr / dt
        return self.byteRate

    def addPhasePostProcess(self, phase, func, taskChain = 'default'):
        if self.getPhaseComplete(phase):
            func()
            return
        self.acceptOnce('phaseComplete-%s' % phase, func)

    def testBandwidth(self):
        self.recordBytesPerSecond()
        byteRate = self.getBytesPerSecond()
        if byteRate < 0:
            return
        if byteRate >= self.getBandwidth() * self.INCREASE_THRESHOLD:
            self.increaseBandwidth(byteRate)
        elif byteRate < self.byteRateRequested * self.DECREASE_THRESHOLD:
            self.decreaseBandwidth(byteRate)

    def getBandwidth(self):
        if self.backgrounded:
            bandwidth = self.BANDWIDTH_ARRAY[self.bandwidthIndex] - self.TELEMETRY_BANDWIDTH
        else:
            bandwidth = self.BANDWIDTH_ARRAY[self.bandwidthIndex]
        if self.MAX_BANDWIDTH > 0:
            bandwidth = min(bandwidth, self.MAX_BANDWIDTH)
        return bandwidth

    def increaseBandwidth(self, targetBandwidth = None):
        maxBandwidthIndex = len(self.BANDWIDTH_ARRAY) - 1
        if self.bandwidthIndex == maxBandwidthIndex:
            self.notify.debug('increaseBandwidth: Already at maximum bandwidth')
            return 0
        self.bandwidthIndex += 1
        self.everIncreasedBandwidth = 1
        self.setBandwidth()
        return 1

    def decreaseBandwidth(self, targetBandwidth = None):
        if not self.DECREASE_BANDWIDTH:
            return 0
        if self.backgrounded and self.everIncreasedBandwidth:
            return 0
        if self.bandwidthIndex == 0:
            return 0
        else:
            self.bandwidthIndex -= 1
            if targetBandwidth:
                while self.bandwidthIndex > 0 and self.BANDWIDTH_ARRAY[self.bandwidthIndex] > targetBandwidth:
                    self.bandwidthIndex -= 1

            self.setBandwidth()
            return 1

    def setBandwidth(self):
        self.resetBytesPerSecond()
        self.httpChannel.setMaxBytesPerSecond(self.getBandwidth())

    def resetBytesPerSecond(self):
        self.bpsList = []

    def recordBytesPerSecond--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'httpChannel'
6	LOAD_ATTR         'getBytesDownloaded'
9	CALL_FUNCTION_0   None
12	STORE_FAST        'bytesDownloaded'

15	LOAD_FAST         'self'
18	LOAD_ATTR         'httpChannel'
21	LOAD_ATTR         'getBytesRequested'
24	CALL_FUNCTION_0   None
27	STORE_FAST        'bytesRequested'

30	LOAD_FAST         'self'
33	LOAD_ATTR         'getTime'
36	CALL_FUNCTION_0   None
39	STORE_FAST        't'

42	LOAD_FAST         'self'
45	LOAD_ATTR         'bpsList'
48	LOAD_ATTR         'append'
51	LOAD_FAST         't'
54	LOAD_FAST         'bytesDownloaded'
57	LOAD_FAST         'bytesRequested'
60	BUILD_TUPLE_3     None
63	CALL_FUNCTION_1   None
66	POP_TOP           None

67	SETUP_LOOP        '160'

70	LOAD_GLOBAL       'len'
73	LOAD_FAST         'self'
76	LOAD_ATTR         'bpsList'
79	CALL_FUNCTION_1   None
82	LOAD_CONST        0
85	COMPARE_OP        '=='
88	JUMP_IF_FALSE     '95'

91	BREAK_LOOP        None
92	JUMP_FORWARD      '95'
95_0	COME_FROM         '92'

95	LOAD_FAST         'self'
98	LOAD_ATTR         'bpsList'
101	LOAD_CONST        0
104	BINARY_SUBSCR     None
105	UNPACK_SEQUENCE_3 None
108	STORE_FAST        'ft'
111	STORE_FAST        'fb'
114	STORE_FAST        'fr'

117	LOAD_FAST         'ft'
120	LOAD_FAST         't'
123	LOAD_FAST         'self'
126	LOAD_ATTR         'BPS_WINDOW'
129	BINARY_SUBTRACT   None
130	COMPARE_OP        '<'
133	JUMP_IF_FALSE     '155'

136	LOAD_FAST         'self'
139	LOAD_ATTR         'bpsList'
142	LOAD_ATTR         'pop'
145	LOAD_CONST        0
148	CALL_FUNCTION_1   None
151	POP_TOP           None
152	JUMP_BACK         '70'

155	BREAK_LOOP        None
156	JUMP_BACK         '70'
159	POP_BLOCK         None
160_0	COME_FROM         '67'

Syntax error at or near `POP_BLOCK' token at offset 159

    def getBytesPerSecond(self):
        if len(self.bpsList) < 2:
            return -1
        startTime, startBytes, startRequested = self.bpsList[0]
        finalTime, finalBytes, finalRequested = self.bpsList[-1]
        dt = finalTime - startTime
        db = finalBytes - startBytes
        dr = finalRequested - startRequested
        if dt <= 0.0:
            return -1
        self.byteRate = db / dt
        self.byteRateRequested = dr / dt
        return self.byteRate

    def testBandwidth(self):
        self.recordBytesPerSecond()
        byteRate = self.getBytesPerSecond()
        if byteRate < 0:
            return
        if byteRate >= self.getBandwidth() * self.INCREASE_THRESHOLD:
            self.increaseBandwidth(byteRate)
        elif byteRate < self.byteRateRequested * self.DECREASE_THRESHOLD:
            self.decreaseBandwidth(byteRate)

    def getBandwidth(self):
        if self.backgrounded:
            bandwidth = self.BANDWIDTH_ARRAY[self.bandwidthIndex] - self.TELEMETRY_BANDWIDTH
        else:
            bandwidth = self.BANDWIDTH_ARRAY[self.bandwidthIndex]
        if self.MAX_BANDWIDTH > 0:
            bandwidth = min(bandwidth, self.MAX_BANDWIDTH)
        return bandwidth

    def increaseBandwidth(self, targetBandwidth = None):
        maxBandwidthIndex = len(self.BANDWIDTH_ARRAY) - 1
        if self.bandwidthIndex == maxBandwidthIndex:
            return 0
        self.bandwidthIndex += 1
        self.everIncreasedBandwidth = 1
        self.setBandwidth()
        return 1

    def decreaseBandwidth(self, targetBandwidth = None):
        if not self.DECREASE_BANDWIDTH:
            return 0
        if self.backgrounded and self.everIncreasedBandwidth:
            return 0
        if self.bandwidthIndex == 0:
            return 0
        else:
            self.bandwidthIndex -= 1
            if targetBandwidth:
                while self.bandwidthIndex > 0 and self.BANDWIDTH_ARRAY[self.bandwidthIndex] > targetBandwidth:
                    self.bandwidthIndex -= 1

            self.setBandwidth()
            return 1

    def setBandwidth(self):
        self.resetBytesPerSecond()
        self.httpChannel.setMaxBytesPerSecond(self.getBandwidth())

    def MakeNTFSFilesGlobalWriteable(self, pathToSet = None):
        if not self.WIN32:
            return
        import win32api
        if pathToSet == None:
            pathToSet = self.getInstallDir()
        else:
            pathToSet = pathToSet.cStr() + '*'
        DrivePath = pathToSet[0:3]
        try:
            volname, volsernum, maxfilenamlen, sysflags, filesystemtype = win32api.GetVolumeInformation(DrivePath)
        except:
            return

        if self.win32con_FILE_PERSISTENT_ACLS & sysflags:
            self.notify.info('NTFS detected, making files global writeable\n')
            win32dir = win32api.GetWindowsDirectory()
            cmdLine = win32dir + '\\system32\\cacls.exe "' + pathToSet + '" /T /E /C /G Everyone:F > nul'
            os.system(cmdLine)
        return

    def cleanup(self):
        self.notify.info('cleanup: cleaning up Launcher')
        self.ignoreAll()
        del self.clock
        del self.dldb
        del self.httpChannel
        del self.http

    def scanForHacks--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'WIN32'
6	JUMP_IF_TRUE      '16'

9	LOAD_CONST        None
12	RETURN_VALUE      None
13	JUMP_FORWARD      '16'
16_0	COME_FROM         '13'

16	LOAD_CONST        None
19	IMPORT_NAME       '_winreg'
22	STORE_FAST        '_winreg'

25	BUILD_MAP         None
28	STORE_FAST        'hacksInstalled'

31	BUILD_MAP         None
34	STORE_FAST        'hacksRunning'

37	LOAD_CONST        '!xSpeed.net'
40	LOAD_CONST        'A Speeder'
43	LOAD_CONST        'Speed Gear'
46	BUILD_LIST_3      None
49	STORE_FAST        'hackName'

52	BUILD_MAP         None
55	DUP_TOP           None
56	LOAD_FAST         'hackName'
59	LOAD_CONST        0
62	BINARY_SUBSCR     None
63	LOAD_FAST         '_winreg'
66	LOAD_ATTR         'HKEY_LOCAL_MACHINE'
69	LOAD_CONST        'Software\\Microsoft\\Windows\\CurrentVersion\\Run\\!xSpeed'
72	BUILD_LIST_2      None
75	LOAD_FAST         '_winreg'
78	LOAD_ATTR         'HKEY_CURRENT_USER'
81	LOAD_CONST        'Software\\!xSpeednethy'
84	BUILD_LIST_2      None
87	LOAD_FAST         '_winreg'
90	LOAD_ATTR         'HKEY_CURRENT_USER'
93	LOAD_CONST        'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MenuOrder\\Start Menu\\Programs\\!xSpeednet'
96	BUILD_LIST_2      None
99	LOAD_FAST         '_winreg'
102	LOAD_ATTR         'HKEY_LOCAL_MACHINE'
105	LOAD_CONST        'Software\\Gentee\\Paths\\!xSpeednet'
108	BUILD_LIST_2      None
111	LOAD_FAST         '_winreg'
114	LOAD_ATTR         'HKEY_LOCAL_MACHINE'
117	LOAD_CONST        'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\!xSpeed.net 2.0'
120	BUILD_LIST_2      None
123	BUILD_LIST_5      None
126	ROT_THREE         None
127	STORE_SUBSCR      None
128	DUP_TOP           None
129	LOAD_FAST         'hackName'
132	LOAD_CONST        1
135	BINARY_SUBSCR     None
136	LOAD_FAST         '_winreg'
139	LOAD_ATTR         'HKEY_CURRENT_USER'
142	LOAD_CONST        'Software\\aspeeder'
145	BUILD_LIST_2      None
148	LOAD_FAST         '_winreg'
151	LOAD_ATTR         'HKEY_LOCAL_MACHINE'
154	LOAD_CONST        'Software\\aspeeder'
157	BUILD_LIST_2      None
160	LOAD_FAST         '_winreg'
163	LOAD_ATTR         'HKEY_LOCAL_MACHINE'
166	LOAD_CONST        'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\aspeeder'
169	BUILD_LIST_2      None
172	BUILD_LIST_3      None
175	ROT_THREE         None
176	STORE_SUBSCR      None
177	STORE_FAST        'knownHacksRegistryKeys'

180	SETUP_EXCEPT      '295'

183	SETUP_LOOP        '291'
186	LOAD_FAST         'knownHacksRegistryKeys'
189	LOAD_ATTR         'keys'
192	CALL_FUNCTION_0   None
195	GET_ITER          None
196	FOR_ITER          '290'
199	STORE_FAST        'prog'

202	SETUP_LOOP        '287'
205	LOAD_FAST         'knownHacksRegistryKeys'
208	LOAD_FAST         'prog'
211	BINARY_SUBSCR     None
212	GET_ITER          None
213	FOR_ITER          '286'
216	STORE_FAST        'key'

219	SETUP_EXCEPT      '276'

222	LOAD_FAST         '_winreg'
225	LOAD_ATTR         'OpenKey'
228	LOAD_FAST         'key'
231	LOAD_CONST        0
234	BINARY_SUBSCR     None
235	LOAD_FAST         'key'
238	LOAD_CONST        1
241	BINARY_SUBSCR     None
242	CALL_FUNCTION_2   None
245	STORE_FAST        'h'

248	LOAD_CONST        1
251	LOAD_FAST         'hacksInstalled'
254	LOAD_FAST         'prog'
257	STORE_SUBSCR      None

258	LOAD_FAST         '_winreg'
261	LOAD_ATTR         'CloseKey'
264	LOAD_FAST         'h'
267	CALL_FUNCTION_1   None
270	POP_TOP           None

271	BREAK_LOOP        None
272	POP_BLOCK         None
273	JUMP_BACK         '213'
276_0	COME_FROM         '219'

276	POP_TOP           None
277	POP_TOP           None
278	POP_TOP           None

279	JUMP_BACK         '213'
282	END_FINALLY       None
283_0	COME_FROM         '282'
283	JUMP_BACK         '213'
286	POP_BLOCK         None
287_0	COME_FROM         '202'
287	JUMP_BACK         '196'
290	POP_BLOCK         None
291_0	COME_FROM         '183'
291	POP_BLOCK         None
292	JUMP_FORWARD      '302'
295_0	COME_FROM         '180'

295	POP_TOP           None
296	POP_TOP           None
297	POP_TOP           None

298	JUMP_FORWARD      '302'
301	END_FINALLY       None
302_0	COME_FROM         '292'
302_1	COME_FROM         '301'

302	BUILD_MAP         None
305	DUP_TOP           None
306	LOAD_CONST        '!xspeednet'
309	LOAD_FAST         'hackName'
312	LOAD_CONST        0
315	BINARY_SUBSCR     None
316	ROT_THREE         None
317	STORE_SUBSCR      None
318	DUP_TOP           None
319	LOAD_CONST        'aspeeder'
322	LOAD_FAST         'hackName'
325	LOAD_CONST        1
328	BINARY_SUBSCR     None
329	ROT_THREE         None
330	STORE_SUBSCR      None
331	DUP_TOP           None
332	LOAD_CONST        'speed gear'
335	LOAD_FAST         'hackName'
338	LOAD_CONST        2
341	BINARY_SUBSCR     None
342	ROT_THREE         None
343	STORE_SUBSCR      None
344	STORE_FAST        'knownHacksMUI'

347	LOAD_CONST        0
350	STORE_FAST        'i'

353	SETUP_EXCEPT      '521'

356	LOAD_FAST         '_winreg'
359	LOAD_ATTR         'OpenKey'
362	LOAD_FAST         '_winreg'
365	LOAD_ATTR         'HKEY_CURRENT_USER'
368	LOAD_CONST        'Software\\Microsoft\\Windows\\ShellNoRoam\\MUICache'
371	CALL_FUNCTION_2   None
374	STORE_FAST        'rh'

377	SETUP_LOOP        '504'

380	LOAD_FAST         '_winreg'
383	LOAD_ATTR         'EnumValue'
386	LOAD_FAST         'rh'
389	LOAD_FAST         'i'
392	CALL_FUNCTION_2   None
395	UNPACK_SEQUENCE_3 None
398	STORE_FAST        'name'
401	STORE_FAST        'value'
404	STORE_FAST        'type'

407	LOAD_FAST         'i'
410	LOAD_CONST        1
413	INPLACE_ADD       None
414	STORE_FAST        'i'

417	LOAD_FAST         'type'
420	LOAD_CONST        1
423	COMPARE_OP        '=='
426	JUMP_IF_FALSE     '500'

429	LOAD_FAST         'value'
432	LOAD_ATTR         'lower'
435	CALL_FUNCTION_0   None
438	STORE_FAST        'val'

441	SETUP_LOOP        '500'
444	LOAD_FAST         'knownHacksMUI'
447	GET_ITER          None
448	FOR_ITER          '496'
451	STORE_FAST        'hackprog'

454	LOAD_FAST         'val'
457	LOAD_ATTR         'find'
460	LOAD_FAST         'hackprog'
463	CALL_FUNCTION_1   None
466	LOAD_CONST        -1
469	COMPARE_OP        '!='
472	JUMP_IF_FALSE     '493'

475	LOAD_CONST        1
478	LOAD_FAST         'hacksInstalled'
481	LOAD_FAST         'knownHacksMUI'
484	LOAD_FAST         'hackprog'
487	BINARY_SUBSCR     None
488	STORE_SUBSCR      None

489	BREAK_LOOP        None
490	JUMP_BACK         '448'
493	JUMP_BACK         '448'
496	POP_BLOCK         None
497_0	COME_FROM         '441'
497	JUMP_BACK         '380'
500	JUMP_BACK         '380'
503	POP_BLOCK         None
504_0	COME_FROM         '377'

504	LOAD_FAST         '_winreg'
507	LOAD_ATTR         'CloseKey'
510	LOAD_FAST         'rh'
513	CALL_FUNCTION_1   None
516	POP_TOP           None
517	POP_BLOCK         None
518	JUMP_FORWARD      '528'
521_0	COME_FROM         '353'

521	POP_TOP           None
522	POP_TOP           None
523	POP_TOP           None

524	JUMP_FORWARD      '528'
527	END_FINALLY       None
528_0	COME_FROM         '518'
528_1	COME_FROM         '527'

528	SETUP_EXCEPT      '544'

531	LOAD_CONST        None
534	IMPORT_NAME       'otp.launcher.procapi'
537	STORE_FAST        'otp'
540	POP_BLOCK         None
541	JUMP_FORWARD      '551'
544_0	COME_FROM         '528'

544	POP_TOP           None
545	POP_TOP           None
546	POP_TOP           None

547	JUMP_FORWARD      '674'
550	END_FINALLY       None
551_0	COME_FROM         '541'

551	BUILD_MAP         None
554	DUP_TOP           None
555	LOAD_CONST        '!xspeednet.exe'
558	LOAD_FAST         'hackName'
561	LOAD_CONST        0
564	BINARY_SUBSCR     None
565	ROT_THREE         None
566	STORE_SUBSCR      None
567	DUP_TOP           None
568	LOAD_CONST        'aspeeder.exe'
571	LOAD_FAST         'hackName'
574	LOAD_CONST        1
577	BINARY_SUBSCR     None
578	ROT_THREE         None
579	STORE_SUBSCR      None
580	DUP_TOP           None
581	LOAD_CONST        'speedgear.exe'
584	LOAD_FAST         'hackName'
587	LOAD_CONST        2
590	BINARY_SUBSCR     None
591	ROT_THREE         None
592	STORE_SUBSCR      None
593	STORE_FAST        'knownHacksExe'

596	SETUP_EXCEPT      '667'

599	SETUP_LOOP        '663'
602	LOAD_GLOBAL       'procapi'
605	LOAD_ATTR         'getProcessList'
608	CALL_FUNCTION_0   None
611	GET_ITER          None
612	FOR_ITER          '662'
615	STORE_FAST        'p'

618	LOAD_FAST         'p'
621	LOAD_ATTR         'name'
624	STORE_FAST        'pname'

627	LOAD_FAST         'knownHacksExe'
630	LOAD_ATTR         'has_key'
633	LOAD_FAST         'pname'
636	CALL_FUNCTION_1   None
639	JUMP_IF_FALSE     '659'

642	LOAD_CONST        1
645	LOAD_FAST         'hacksRunning'
648	LOAD_FAST         'knownHacksExe'
651	LOAD_FAST         'pname'
654	BINARY_SUBSCR     None
655	STORE_SUBSCR      None
656	JUMP_BACK         '612'
659	JUMP_BACK         '612'
662	POP_BLOCK         None
663_0	COME_FROM         '599'
663	POP_BLOCK         None
664	JUMP_FORWARD      '674'
667_0	COME_FROM         '596'

667	POP_TOP           None
668	POP_TOP           None
669	POP_TOP           None

670	JUMP_FORWARD      '674'
673	END_FINALLY       None
674_0	COME_FROM         '550'
674_1	COME_FROM         '664'
674_2	COME_FROM         '673'

674	LOAD_GLOBAL       'len'
677	LOAD_FAST         'hacksInstalled'
680	CALL_FUNCTION_1   None
683	LOAD_CONST        0
686	COMPARE_OP        '>'
689	JUMP_IF_FALSE     '750'

692	LOAD_FAST      
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\launcher\LauncherBase.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'WIN32'
6	JUMP_IF_TRUE      '16'

9	LOAD_CONST        None
12	RETURN_VALUE      None
13	JUMP_FORWARD      '16'
16_0	COME_FROM         '13'

16	LOAD_CONST        None
19	IMPORT_NAME       '_winreg'
22	STORE_FAST        '_winreg'

25	BUILD_MAP         None
28	STORE_FAST        'hacksInstalled'

31	BUILD_MAP         None
34	STORE_FAST        'hacksRunning'

37	LOAD_CONST        '!xSpeed.net'
40	LOAD_CONST        'A Speeder'
43	LOAD_CONST        'Speed Gear'
46	BUILD_LIST_3      None
49	STORE_FAST        'hackName'

52	BUILD_MAP         None
55	DUP_TOP           None
56	LOAD_FAST         'hackName'
59	LOAD_CONST        0
62	BINARY_SUBSCR     None
63	LOAD_FAST         '_winreg'
66	LOAD_ATTR         'HKEY_LOCAL_MACHINE'
69	LOAD_CONST        'Software\\Microsoft\\Windows\\CurrentVersion\\Run\\!xSpeed'
72	BUILD_LIST_2      None
75	LOAD_FAST         '_winreg'
78	LOAD_ATTR         'HKEY_CURRENT_USER'
81	LOAD_CONST        'Software\\!xSpeednethy'
84	BUILD_LIST_2      None
87	LOAD_FAST         '_winreg'
90	LOAD_ATTR         'HKEY_CURRENT_USER'
93	LOAD_CONST        'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MenuOrder\\Start Menu\\Programs\\!xSpeednet'
96	BUILD_LIST_2      None
99	LOAD_FAST         '_winreg'
102	LOAD_ATTR         'HKEY_LOCAL_MACHINE'
105	LOAD_CONST        'Software\\Gentee\\Paths\\!xSpeednet'
108	BUILD_LIST_2      None
111	LOAD_FAST         '_winreg'
114	LOAD_ATTR         'HKEY_LOCAL_MACHINE'
117	LOAD_CONST        'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\!xSpeed.net 2.0'
120	BUILD_LIST_2      None
123	BUILD_LIST_5      None
126	ROT_THREE         None
127	STORE_SUBSCR      None
128	DUP_TOP           None
129	LOAD_FAST         'hackName'
132	LOAD_CONST        1
135	BINARY_SUBSCR     None
136	LOAD_FAST         '_winreg'
139	LOAD_ATTR         'HKEY_CURRENT_USER'
142	LOAD_CONST        'Software\\aspeeder'
145	BUILD_LIST_2      None
148	LOAD_FAST         '_winreg'
151	LOAD_ATTR         'HKEY_LOCAL_MACHINE'
154	LOAD_CONST        'Software\\aspeeder'
157	BUILD_LIST_2      None
160	LOAD_FAST         '_winreg'
163	LOAD_ATTR         'HKEY_LOCAL_MACHINE'
166	LOAD_CONST        'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\aspeeder'
169	BUILD_LIST_2      None
172	BUILD_LIST_3      None
175	ROT_THREE         None
176	STORE_SUBSCR      None
177	STORE_FAST        'knownHacksRegistryKeys'

180	SETUP_EXCEPT      '295'

183	SETUP_LOOP        '291'
186	LOAD_FAST         'knownHacksRegistryKeys'
189	LOAD_ATTR         'keys'
192	CALL_FUNCTION_0   None
195	GET_ITER          None
196	FOR_ITER          '290'
199	STORE_FAST        'prog'

202	SETUP_LOOP        '287'
205	LOAD_FAST         'knownHacksRegistryKeys'
208	LOAD_FAST         'prog'
211	BINARY_SUBSCR     None
212	GET_ITER          None
213	FOR_ITER          '286'
216	STORE_FAST        'key'

219	SETUP_EXCEPT      '276'

222	LOAD_FAST         '_winreg'
225	LOAD_ATTR         'OpenKey'
228	LOAD_FAST         'key'
231	LOAD_CONST        0
234	BINARY_SUBSCR     None
235	LOAD_FAST         'key'
238	LOAD_CONST        1
241	BINARY_SUBSCR     None
242	CALL_FUNCTION_2   None
245	STORE_FAST        'h'

248	LOAD_CONST        1
251	LOAD_FAST         'hacksInstalled'
254	LOAD_FAST         'prog'
257	STORE_SUBSCR      None

258	LOAD_FAST         '_winreg'
261	LOAD_ATTR         'CloseKey'
264	LOAD_FAST         'h'
267	CALL_FUNCTION_1   None
270	POP_TOP           None

271	BREAK_LOOP        None
272	POP_BLOCK         None
273	JUMP_BACK         '213'
276_0	COME_FROM         '219'

276	POP_TOP           None
277	POP_TOP           None
278	POP_TOP           None

279	JUMP_BACK         '213'
282	END_FINALLY       None
283_0	COME_FROM         '282'
283	JUMP_BACK         '213'
286	POP_BLOCK         None
287_0	COME_FROM         '202'
287	JUMP_BACK         '196'
290	POP_BLOCK         None
291_0	COME_FROM         '183'
291	POP_BLOCK         None
292	JUMP_FORWARD      '302'
295_0	COME_FROM         '180'

295	POP_TOP           None
296	POP_TOP           None
297	POP_TOP           None

298	JUMP_FORWARD      '302'
301	END_FINALLY       None
302_0	COME_FROM         '292'
302_1	COME_FROM         '301'

302	BUILD_MAP         None
305	DUP_TOP           None
306	LOAD_CONST        '!xspeednet'
309	LOAD_FAST         'hackName'
312	LOAD_CONST        0
315	BINARY_SUBSCR     None
316	ROT_THREE         None
317	STORE_SUBSCR      None
318	DUP_TOP           None
319	LOAD_CONST        'aspeeder'
322	LOAD_FAST         'hackName'
325	LOAD_CONST        1
328	BINARY_SUBSCR     None
329	ROT_THREE         None
330	STORE_SUBSCR      None
331	DUP_TOP           None
332	LOAD_CONST        'speed gear'
335	LOAD_FAST         'hackName'
338	LOAD_CONST        2
341	BINARY_SUBSCR     None
342	ROT_THREE         None
343	STORE_SUBSCR      None
344	STORE_FAST        'knownHacksMUI'

347	LOAD_CONST        0
350	STORE_FAST        'i'

353	SETUP_EXCEPT      '521'

356	LOAD_FAST         '_winreg'
359	LOAD_ATTR         'OpenKey'
362	LOAD_FAST         '_winreg'
365	LOAD_ATTR         'HKEY_CURRENT_USER'
368	LOAD_CONST        'Software\\Microsoft\\Windows\\ShellNoRoam\\MUICache'
371	CALL_FUNCTION_2   None
374	STORE_FAST        'rh'

377	SETUP_LOOP        '504'

380	LOAD_FAST         '_winreg'
383	LOAD_ATTR         'EnumValue'
386	LOAD_FAST         'rh'
389	LOAD_FAST         'i'
392	CALL_FUNCTION_2   None
395	UNPACK_SEQUENCE_3 None
398	STORE_FAST        'name'
401	STORE_FAST        'value'
404	STORE_FAST        'type'

407	LOAD_FAST         'i'
410	LOAD_CONST        1
413	INPLACE_ADD       None
414	STORE_FAST        'i'

417	LOAD_FAST         'type'
420	LOAD_CONST        1
423	COMPARE_OP        '=='
426	JUMP_IF_FALSE     '500'

429	LOAD_FAST         'value'
432	LOAD_ATTR         'lower'
435	CALL_FUNCTION_0   None
438	STORE_FAST        'val'

441	SETUP_LOOP        '500'
444	LOAD_FAST         'knownHacksMUI'
447	GET_ITER          None
448	FOR_ITER          '496'
451	STORE_FAST        'hackprog'

454	LOAD_FAST         'val'
457	LOAD_ATTR         'find'
460	LOAD_FAST         'hackprog'
463	CALL_FUNCTION_1   None
466	LOAD_CONST        -1
469	COMPARE_OP        '!='
472	JUMP_IF_FALSE     '493'

475	LOAD_CONST        1
478	LOAD_FAST         'hacksInstalled'
481	LOAD_FAST         'knownHacksMUI'
484	LOAD_FAST         'hackprog'
487	BINARY_SUBSCR     None
488	STORE_SUBSCR      None

489	BREAK_LOOP        None
490	JUMP_BACK         '448'
493	JUMP_BACK         '448'
496	POP_BLOCK         None
497_0	COME_FROM         '441'
497	JUMP_BACK         '380'
500	JUMP_BACK         '380'
503	POP_BLOCK         None
504_0	COME_FROM         '377'

504	LOAD_FAST         '_winreg'
507	LOAD_ATTR         'CloseKey'
510	LOAD_FAST         'rh'
513	CALL_FUNCTION_1   None
516	POP_TOP           None
517	POP_BLOCK         None
518	JUMP_FORWARD      '528'
521_0	COME_FROM         '353'

521	POP_TOP           None
522	POP_TOP           None
523	POP_TOP           None

524	JUMP_FORWARD      '528'
527	END_FINALLY       None
528_0	COME_FROM         '518'
528_1	COME_FROM         '527'

528	SETUP_EXCEPT      '544'

531	LOAD_CONST        None
534	IMPORT_NAME       'otp.launcher.procapi'
537	STORE_FAST        'otp'
540	POP_BLOCK         None
541	JUMP_FORWARD      '551'
544_0	COME_FROM         '528'

544	POP_TOP           None
545	POP_TOP           None
546	POP_TOP           None

547	JUMP_FORWARD      '674'
550	END_FINALLY       None
551_0	COME_FROM         '541'

551	BUILD_MAP         None
554	DUP_TOP           None
555	LOAD_CONST        '!xspeednet.exe'
558	LOAD_FAST         'hackName'
561	LOAD_CONST        0
564	BINARY_SUBSCR     None
565	ROT_THREE         None
566	STORE_SUBSCR      No   'self'
695	LOAD_ATTR         'notify'
698	LOAD_ATTR         'info'
701	LOAD_CONST        'Third party programs installed:'
704	CALL_FUNCTION_1   None
707	POP_TOP           None

708	SETUP_LOOP        '750'
711	LOAD_FAST         'hacksInstalled'
714	LOAD_ATTR         'keys'
717	CALL_FUNCTION_0   None
720	GET_ITER          None
721	FOR_ITER          '746'
724	STORE_FAST        'hack'

727	LOAD_FAST         'self'
730	LOAD_ATTR         'notify'
733	LOAD_ATTR         'info'
736	LOAD_FAST         'hack'
739	CALL_FUNCTION_1   None
742	POP_TOP           None
743	JUMP_BACK         '721'
746	POP_BLOCK         None
747_0	COME_FROM         '708'
747	JUMP_FORWARD      '750'
750_0	COME_FROM         '747'

750	LOAD_GLOBAL       'len'
753	LOAD_FAST         'hacksRunning'
756	CALL_FUNCTION_1   None
759	LOAD_CONST        0
762	COMPARE_OP        '>'
765	JUMP_IF_FALSE     '849'

768	LOAD_FAST         'self'
771	LOAD_ATTR         'notify'
774	LOAD_ATTR         'info'
777	LOAD_CONST        'Third party programs running:'
780	CALL_FUNCTION_1   None
783	POP_TOP           None

784	SETUP_LOOP        '823'
787	LOAD_FAST         'hacksRunning'
790	LOAD_ATTR         'keys'
793	CALL_FUNCTION_0   None
796	GET_ITER          None
797	FOR_ITER          '822'
800	STORE_FAST        'hack'

803	LOAD_FAST         'self'
806	LOAD_ATTR         'notify'
809	LOAD_ATTR         'info'
812	LOAD_FAST         'hack'
815	CALL_FUNCTION_1   None
818	POP_TOP           None
819	JUMP_BACK         '797'
822	POP_BLOCK         None
823_0	COME_FROM         '784'

823	LOAD_FAST         'self'
826	LOAD_ATTR         'setPandaErrorCode'
829	LOAD_CONST        8
832	CALL_FUNCTION_1   None
835	POP_TOP           None

836	LOAD_GLOBAL       'sys'
839	LOAD_ATTR         'exit'
842	CALL_FUNCTION_0   None
845	POP_TOP           None
846	JUMP_FORWARD      '849'
849_0	COME_FROM         '846'

Syntax error at or near `POP_BLOCK' token at offset 503

    def getBlue(self):
        return None

    def getPlayToken(self):
        return None

    def getDISLToken(self):
        DISLToken = self.getValue(self.DISLTokenKey)
        self.setValue(self.DISLTokenKey, '')
        if DISLToken == 'NO DISLTOKEN':
            DISLToken = None
        return DISLToken
ne
567	DUP_TOP           None
568	LOAD_CONST        'aspeeder.exe'
571	LOAD_FAST         'hackName'
574	LOAD_CONST        1
577	BINARY_SUBSCR     None
578	ROT_THREE         None
579	STORE_SUBSCR      None
580	DUP_TOP           None
581	LOAD_CONST        'speedgear.exe'
584	LOAD_FAST         'hackName'
587	LOAD_CONST        2
590	BINARY_SUBSCR     None
591	ROT_THREE         None
592	STORE_SUBSCR      None
593	STORE_FAST        'knownHacksExe'

596	SETUP_EXCEPT      '667'

599	SETUP_LOOP        '663'
602	LOAD_GLOBAL       'procapi'
605	LOAD_ATTR         'getProcessList'
608	CALL_FUNCTION_0   None
611	GET_ITER          None
612	FOR_ITER          '662'
615	STORE_FAST        'p'

618	LOAD_FAST         'p'
621	LOAD_ATTR         'name'
624	STORE_FAST        'pname'

627	LOAD_FAST         'knownHacksExe'
630	LOAD_ATTR         'has_key'
633	LOAD_FAST         'pname'
636	CALL_FUNCTION_1   None
639	JUMP_IF_FALSE     '659'

642	LOAD_CONST        1
645	LOAD_FAST         'hacksRunning'
648	LOAD_FAST         'knownHacksExe'
651	LOAD_FAST         'pname'
654	BINARY_SUBSCR     None
655	STORE_SUBSCR      None
656	JUMP_BACK         '612'
659	JUMP_BACK         '612'
662	POP_BLOCK         None
663_0	COME_FROM         '599'
663	POP_BLOCK         None
664	JUMP_FORWARD      '674'
667_0	COME_FROM         '596'

667	POP_TOP           None
668	POP_TOP           None
669	POP_TOP           None

670	JUMP_FORWARD      '674'
673	END_FINALLY       None
674_0	COME_FROM         '550'
674_1	COME_FROM         '664'
674_2	COME_FROM         '673'

674	LOAD_GLOBAL       'len'
677	LOAD_FAST         'hacksInstalled'
680	CALL_FUNCTION_1   None
683	LOAD_CONST        0
686	COMPARE_OP        '>'
689	JUMP_IF_FALSE     '750'

692	LOAD_FAST         'self'
695	LOAD_ATTR         'notify'
698	LOAD_ATTR         'info'
701	LOAD_CONST        'Third party programs installed:'
704	CALL_FUNCTION_1   None
707	POP_TOP           None

708	SETUP_LOOP        '750'
711	LOAD_FAST         'hacksInstalled'
714	LOAD_ATTR         'keys'
717	CALL_FUNCTION_0   None
720	GET_ITER          None
721	FOR_ITER          '746'
724	STORE_FAST        'hack'

727	LOAD_FAST         'self'
730	LOAD_ATTR         'notify'
733	LOAD_ATTR         'info'
736	LOAD_FAST         'hack'
739	CALL_FUNCTION_1   None
742	POP_TOP           None
743	JUMP_BACK         '721'
746	POP_BLOCK         None
747_0	COME_FROM         '708'
747	JUMP_FORWARD      '750'
750_0	COME_FROM         '747'

750	LOAD_GLOBAL       'len'
753	LOAD_FAST         'hacksRunning'
756	CALL_FUNCTION_1   None
759	LOAD_CONST        0
762	COMPARE_OP        '>'
765	JUMP_IF_FALSE     '849'

768	LOAD_FAST         'self'
771	LOAD_ATTR         'notify'
774	LOAD_ATTR         'info'
777	LOAD_CONST        'Third party programs running:'
780	CALL_FUNCTION_1   None
783	POP_TOP           None

784	SETUP_LOOP        '823'
787	LOAD_FAST         'hacksRunning'
790	LOAD_ATTR         'keys'
793	CALL_FUNCTION_0   None
796	GET_ITER          None
797	FOR_ITER          '822'
800	STORE_FAST        'hack'

803	LOAD_FAST         'self'
806	LOAD_ATTR         'notify'
809	LOAD_ATTR         'info'
812	LOAD_FAST         'hack'
815	CALL_FUNCTION_1   None
818	POP_TOP           None
819	JUMP_BACK         '797'
822	POP_BLOCK         None
823_0	COME_FROM         '784'

823	LOAD_FAST         'self'
826	LOAD_ATTR         'setPandaErrorCode'
829	LOAD_CONST        8
832	CALL_FUNCTION_1   None
835	POP_TOP           None

836	LOAD_GLOBAL       'sys'
839	LOAD_ATTR         'exit'
842	CALL_FUNCTION_0   None
845	POP_TOP           None
846	JUMP_FORWARD      '849'
849_0	COME_FROM         '846'

Syntax error at or near `POP_BLOCK' token at offset 503

