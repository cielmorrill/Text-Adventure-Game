# File: AdvRoom.py
# Ciel Morrill

"""models a single room in Adventure."""

# Constants

MARKER = "-----"

from AdvObject import AdvObject
from AdvCreature import AdvCreature

class AdvRoom:

    def __init__(self, name, shortdesc, longdesc, passages, visited = False):
        # creates an AdvRoom object with constructors
        self._name = name # str
        self._shortdesc = shortdesc # str
        self._longdesc = longdesc # multi-line str
        self._passages = passages # list of tuples
        self._visited = visited # visited flag (bool)
        self._objects = [] # list
        self._creatures = [] # list

    def get_name(self):
        # returns room name
        return self._name

    def get_short_description(self):
        # returns a one-line room description
        return self._shortdesc

    def get_long_description(self):
        # returns a (potentially) multi-line description of room
        return self._longdesc

    def get_passages(self):
        # returns a copy of passages (list of tuples)
        return self._passages.copy()

    def set_visited(self, bool):
        # sets the status of visited flag
        self._visited = bool
        return self._visited

    def has_been_visited(self):
        # returns value of visited flag
        return self._visited

    def add_object(self, object):
        # adds object to room (obj list)
        object.set_location(self._name)
        self._objects.append(object)
        return self._objects

    def add_creature(self, creature):
        # adds creature to room (c list)
        creature.set_location(self._name)
        self._creatures.append(creature)
        return self._creatures
    
    def remove_object(self, object):
        # removes object from room (obj list)
        self._objects.remove(object)
        return self._objects

    def remove_creature(self, creature):
        # removes creature from room (c list)
        self._creatures.remove(creature)
        return self._creatures

    def contains_object(self, object):
        # checks if room contains object (in list)
        if object in self._objects:
            return True
        return False

    def contains_creature(self, creature):
        # checks if room contains creature (in list)
        if creature in self._creatures:
            return True
        return False
    
    def get_contents(self):
        # returns a copy of list of objects in room
        return self._objects.copy()

    def get_creatures(self):
        # returns a copy of list of creatures in room
        return self._creatures.copy()
    
    def get_room_obj_desc(self):
        # returns a list of all object descriptions in room
        objdesc = [ ]
        if len(self._objects) == 0:
                objdesc.append("not an object")
        elif len(self._objects) == 1:
            objdesc.append(self._objects[0].get_description())
        else:
            for index in range(len(self._objects)):
                if index < len(self._objects) - 1:
                    objdesc.append(self._objects[index].get_description())
                    objdesc.append("and")
                else:
                    objdesc.append(self._objects[index].get_description())
        return objdesc

def read_room(f):
    # reads room from file and returns it as an AdvRoom object

    name = f.readline().rstrip()             # reads room name
    if name == "":                           
        return None

    shortdesc = f.readline().rstrip()                             # reads short description

    longdesc = [ ]                               # reads long description
    finished = False
    while not finished:
        line = f.readline().rstrip()
        if line == MARKER:
            finished = True
        else:
            longdesc.append(line)

    passages = [ ]                       # reads passages into list of tuples (direction, room name, key)
    finished = False
    while not finished:
        line = f.readline().rstrip()
        if line == "":
            finished = True
        else:
            colon = line.find(":")
            if colon == -1:
                raise ValueError("Missing colon in " + line)
            direction = line[:colon].strip().upper()
            slash = line.find("/")
            if slash == -1:
                location = line[colon + 1:].strip()
                key = None
            else:
                location = line[colon + 1: slash].strip()
                key = line[slash + 1:].strip()
            tup = (direction, location, key)
            passages.append(tup)
    
    return AdvRoom(name, shortdesc, longdesc, passages)  # returns completed object
