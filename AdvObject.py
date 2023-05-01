# File: AdvObject.py
# Ciel Morrill

"""models an object in Adventure."""

class AdvObject:

    def __init__(self, name, description, location, consumable = "temp", moveable = True, itemtype = "temp", damage = 0):
        # creates AdvObject according to constructors
        self._name = name # str
        self._description = description # str
        self._initloc = location # str
        self._location = location # str

        # complex AdvObject constructors
        self._consumable = consumable # str, dictates level of consumability
        self._moveable = moveable # bool
        self._itemtype = itemtype # str (consumable, weapon, armor, item)
        self._damage = damage # int

    def __str__(self):
        # returns str version of obj
        return str(self)

    def set_location(self, location):
        # sets location of object
        self._location = location
        return self._location

    def get_name(self):
        # returns name of object
        return self._name

    def get_description(self):
        # returns description of object
        return self._description

    def get_initial_location(self):
        # returns initial location of object
        return self._initloc

    def get_location(self):
        # returns location of object
        return self._location
    
    # more getter methods
    def get_consumability_val(self):
        return self._consumable
    
    def is_moveable(self):
        return self._moveable

    def get_itemtype(self):
        return self._itemtype
    
    def get_damage(self):
        return int(self._damage)

def read_object(f):
    # reads object from file and returns it as AdvObject
    name = f.readline().rstrip()             # reads object name
    if name == "":                           
        return None

    desc = f.readline().rstrip()                            # reads object description

    loc = f.readline().rstrip()                             # reads object location

    ph = f.readline().rstrip()                              # placeholder to hold blank line in between objects

    return AdvObject(name, desc, loc)  # return completed object

def read_complex_object(f):
    # reads upgraded object from file and returns it as AdvObject
    name = f.readline().rstrip()             # reads object name
    if name == "":                           
        return None

    desc = f.readline().rstrip()                            # reads object description

    loc = f.readline().rstrip()                             # reads object location

    consum = f.readline().strip()                           # reads object consumability value

    moveable = f.readline().strip()                         # reads object moveability bool

    itype = f.readline().strip()                             # reads object type

    dam = f.readline().strip()                              # reads object damage

    ph = f.readline().strip()                              # placeholder to hold blank line in between objects

    return AdvObject(name, desc, loc, consum, moveable, itype, dam)  # return completed object