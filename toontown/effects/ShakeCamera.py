import random
from otp.ai.MagicWordGlobal import *

class ShakeCamera:
    def __init__(self, intensity, duration=0.5, rate=30.0):
        self.intensity = intensity
        self.duration = duration
        self.rate = rate

        self.elapsed = 0.0

    def start(self):
        taskMgr.add(self.__task, 'shakeCamera')

    def __task(self, task):
        random_x = random.random()*2 - 1
        random_z = random.random()*2 - 1

        lifecycle = self.elapsed / self.duration
        if lifecycle > 1.0:
            base.cam.setPos(0, 0, 0)
            return task.done

        displacement = (1-lifecycle) * self.intensity

        base.cam.setPos(random_x * displacement, 0, random_z * displacement)

        task.delayTime = 1.0/self.rate
        self.elapsed += 1.0/self.rate
        return task.again

@magicWord(category=CATEGORY_GRAPHICAL, types=[float])
def shakeCamera(intensity):
    """Momentarily shake the camera, as if something heavy went bump nearby."""
    sc = ShakeCamera(intensity)
    sc.start()
