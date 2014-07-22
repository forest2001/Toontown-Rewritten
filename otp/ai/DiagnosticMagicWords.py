from MagicWordGlobal import *
from direct.showbase.GarbageReport import GarbageLogger
from direct.showbase.ContainerReport import ContainerReport
from direct.directnotify.DirectNotifyGlobal import *
import gc

category = CATEGORY_SYSADMIN if game.process == 'server' else CATEGORY_DEBUG

notify = directNotify.newCategory('DiagnosticMagicWords')

def aiPrefix(func):
    """Prefixes `func`'s name with 'ai' if this is an AI server."""
    if game.process == 'server':
        func.func_name = 'ai' + func.func_name
    return func

@magicWord(category=category)
@aiPrefix
def garbage(arg=''):
    """Reports the total garbage use for this process."""

    flags = arg.split()

    GarbageLogger('~garbage', fullReport=('full' in flags), threaded=True,
                  safeMode=('safe' in flags), delOnly=('delonly' in flags))

    return 'Garbage report is now being written to log...'

@magicWord(category=category)
@aiPrefix
def heap():
    """Counts the number of objects in Python's object memory."""

    return '%d active objects (%d garbage)' % (len(gc.get_objects()),
                                               len(gc.garbage))


@magicWord(category=category, types=[int])
@aiPrefix
def objects(minimum=30):
    """Write the objects down to log."""

    cls_counts = {}

    objs = gc.get_objects()
    for obj in objs:
        cls = getattr(obj, '__class__', None) or type(obj)

        cls_counts[cls] = cls_counts.get(cls, 0) + 1

    classes = cls_counts.keys()
    classes.sort(key=lambda x: cls_counts[x], reverse=True)

    notify.info('=== OBJECT TYPES REPORT: ===')
    for cls in classes:
        if cls_counts[cls] < minimum: continue # Not notable enough...
        notify.info('%s: %s' % (repr(cls), cls_counts[cls]))
    notify.info('============================')

    return 'Wrote object types to log.'

@magicWord(category=category, types=[int])
@aiPrefix
def containers(limit=30):
    """Write the container report to log."""

    ContainerReport('~containers', log=True, limit=limit, threaded=True)

    return 'Writing container report to log...'
