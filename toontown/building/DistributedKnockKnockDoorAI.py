from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedAnimatedPropAI import DistributedAnimatedPropAI
from toontown.dna.DNASpawnerAI import *
from toontown.dna.DNAFlatDoor import DNAFlatDoor
import re

class DistributedKnockKnockDoorAI(DistributedAnimatedPropAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedKnockKnockDoorAI")

# DNA spawn code:
buildingPattern = re.compile('tb([0-9]+):')
@dnaSpawn(DNAFlatDoor)
def spawn(air, zone, element):
    # Get door's parent building:
    building = element.parent.parent

    # Parse building name to figure out index number:
    match = buildingPattern.match(building.name)

    if not match:
        # No match! Can't spawn a door...
        return

    index = int(match.group(1))

    door = DistributedKnockKnockDoorAI(air)
    door.setPropId(index)
    door.generateWithRequired(zone)
