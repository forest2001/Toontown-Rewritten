# 2013.08.22 22:14:54 Pacific Daylight Time
# Embedded file name: direct.task.MiniTask
__all__ = ['MiniTask', 'MiniTaskManager']

class MiniTask():
    __module__ = __name__
    done = 0
    cont = 1

    def __init__(self, callback):
        self.__call__ = callback


class MiniTaskManager():
    __module__ = __name__

    def __init__(self):
        self.taskList = []
        self.running = 0

    def add(self, task, name):
        task.name = name
        self.taskList.append(task)

    def remove(self, task):
        try:
            self.taskList.remove(task)
        except ValueError:
            pass

    def __executeTask(self, task):
        return task(task)

    def step(self):
        i = 0
        while i < len(self.taskList):
            task = self.taskList[i]
            ret = task(task)
            if ret == task.cont:
                pass
            else:
                try:
                    self.taskList.remove(task)
                except ValueError:
                    pass

                continue
            i += 1

    def run(self):
        self.running = 1
        while self.running:
            self.step()

    def stop(self):
        self.running = 0
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\task\MiniTask.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:54 Pacific Daylight Time
