# 2013.08.22 22:14:36 Pacific Daylight Time
# Embedded file name: direct.showbase.JobManager
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task.TaskManagerGlobal import taskMgr
from direct.showbase.Job import Job
from direct.showbase.PythonUtil import getBase

class JobManager():
    __module__ = __name__
    notify = directNotify.newCategory('JobManager')
    TaskName = 'jobManager'

    def __init__(self, timeslice = None):
        self._timeslice = timeslice
        self._pri2jobId2job = {}
        self._pri2jobIds = {}
        self._jobId2pri = {}
        self._jobId2timeslices = {}
        self._jobId2overflowTime = {}
        self._useOverflowTime = None
        self._jobIdGenerator = None
        self._highestPriority = Job.Priorities.Normal
        return

    def destroy(self):
        taskMgr.remove(JobManager.TaskName)
        del self._pri2jobId2job

    def add(self, job):
        pri = job.getPriority()
        jobId = job._getJobId()
        self._pri2jobId2job.setdefault(pri, {})
        self._pri2jobId2job[pri][jobId] = job
        self._jobId2pri[jobId] = pri
        self._pri2jobIds.setdefault(pri, [])
        self._pri2jobIds[pri].append(jobId)
        self._jobId2timeslices[jobId] = pri
        self._jobId2overflowTime[jobId] = 0.0
        self._jobIdGenerator = None
        if len(self._jobId2pri) == 1:
            taskMgr.add(self._process, JobManager.TaskName)
            self._highestPriority = pri
        elif pri > self._highestPriority:
            self._highestPriority = pri
        self.notify.debug('added job: %s' % job.getJobName())
        return

    def remove(self, job):
        jobId = job._getJobId()
        pri = self._jobId2pri.pop(jobId)
        self._pri2jobIds[pri].remove(jobId)
        del self._pri2jobId2job[pri][jobId]
        job._cleanupGenerator()
        self._jobId2timeslices.pop(jobId)
        self._jobId2overflowTime.pop(jobId)
        if len(self._pri2jobId2job[pri]) == 0:
            del self._pri2jobId2job[pri]
            if pri == self._highestPriority:
                if len(self._jobId2pri) > 0:
                    priorities = self._getSortedPriorities()
                    self._highestPriority = priorities[-1]
                else:
                    taskMgr.remove(JobManager.TaskName)
                    self._highestPriority = 0
        self.notify.debug('removed job: %s' % job.getJobName())

    def finish(self, job):
        jobId = job._getJobId()
        pri = self._jobId2pri[jobId]
        job = self._pri2jobId2job[pri][jobId]
        gen = job._getGenerator()
        job.resume()
        while True:
            try:
                result = gen.next()
            except StopIteration:
                self.notify.warning('job %s never yielded Job.Done' % job)
                result = Job.Done

            if result is Job.Done:
                job.suspend()
                self.remove(job)
                job._setFinished()
                messenger.send(job.getFinishedEvent())
                break

    @staticmethod
    def getDefaultTimeslice():
        return getBase().config.GetFloat('job-manager-timeslice-ms', 0.5) / 1000.0

    def getTimeslice(self):
        if self._timeslice:
            return self._timeslice
        return self.getDefaultTimeslice()

    def setTimeslice(self, timeslice):
        self._timeslice = timeslice

    def _getSortedPriorities(self):
        priorities = self._pri2jobId2job.keys()
        priorities.sort()
        return priorities

    def _process(self, task = None):
        if self._useOverflowTime is None:
            self._useOverflowTime = config.GetBool('job-use-overflow-time', 1)
        if len(self._pri2jobId2job):
            endT = globalClock.getRealTime() + self.getTimeslice() * 0.9
            while True:
                if self._jobIdGenerator is None:
                    self._jobIdGenerator = flywheel(self._jobId2timeslices.keys(), countFunc=lambda jobId: self._jobId2timeslices[jobId])
                try:
                    jobId = self._jobIdGenerator.next()
                except StopIteration:
                    self._jobIdGenerator = None
                    continue

                pri = self._jobId2pri.get(jobId)
                if pri is None:
                    continue
                if self._useOverflowTime:
                    overflowTime = self._jobId2overflowTime[jobId]
                    timeLeft = endT - globalClock.getRealTime()
                    if overflowTime >= timeLeft:
                        self._jobId2overflowTime[jobId] = max(0.0, overflowTime - timeLeft)
                        break
                job = self._pri2jobId2job[pri][jobId]
                gen = job._getGenerator()
                job.resume()
                while globalClock.getRealTime() < endT:
                    try:
                        result = gen.next()
                    except StopIteration:
                        self.notify.warning('job %s never yielded Job.Done' % job)
                        result = Job.Done

                    if result is Job.Sleep:
                        job.suspend()
                        break
                    elif result is Job.Done:
                        job.suspend()
                        self.remove(job)
                        job._setFinished()
                        messenger.send(job.getFinishedEvent())
                        break
                else:
                    job.suspend()
                    overflowTime = globalClock.getRealTime() - endT
                    if overflowTime > self.getTimeslice():
                        self._jobId2overflowTime[jobId] += overflowTime
                    break

                if len(self._pri2jobId2job) == 0:
                    break

        return task.cont

    def __repr__(self):
        s = '======================================================='
        s += '\nJobManager: active jobs in descending order of priority'
        s += '\n======================================================='
        pris = self._getSortedPriorities()
        if len(pris) == 0:
            s += '\n    no jobs running'
        else:
            pris.reverse()
            for pri in pris:
                jobId2job = self._pri2jobId2job[pri]
                for jobId in self._pri2jobIds[pri]:
                    job = jobId2job[jobId]
                    s += '\n%5d: %s (jobId %s)' % (pri, job.getJobName(), jobId)

        s += '\n'
        return s
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\JobManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:36 Pacific Daylight Time
