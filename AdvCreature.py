# File: AdvCreature.py
# Ciel Morrill

"""
defines AdvCreature class, which holds creature data.
"""

from AdvObject import AdvObject
import AdvPlayer

class AdvCreature:

    def __init__(self, name, id, defense, armor, weapon, health, aggression, initloc):
        # class constructors
        self._name = name # str
        self._id = id # str (000)
        self._defense = int(defense) # int
        self._armor = armor # AdvObj
        self._weapon = weapon # AdvObj
        self._health = int(health) # int
        self._aggression = int(aggression) # int
        self._initloc = initloc # str
        self._location = initloc # str
        self._inventory = [] # list
        self._encountered = False # bool

    # getter methods start here
    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_defense(self):
        return int(self._defense)

    def get_armor(self):
        return self._armor

    def get_weapon(self):
        return self._weapon
    
    def get_health(self):
        return int(self._health)
    
    def get_aggression(self):
        return int(self._aggression)

    def get_initloc(self):
        return self._initloc

    def get_location(self):
        return self._location
    
    def get_encountered(self):
        return self._encountered
    
    def get_damage(self):
        if self._weapon == None or self._weapon == "None":
            return -5
        else:
            return int(self._weapon.get_damage())
    
    def get_inventory(self):
        # returns a copy of inventory
        return self._inventory.copy()

    # setter methods start here
    def set_defense(self, val):
        self._defense = val
        return int(self._defense)

    def set_armor(self, obj):
        self._armor = obj
        return self._armor

    def set_weapon(self, obj):
        self._weapon = obj
        return self._weapon
    
    def set_health(self, val):
        self._health = val
        return int(self._health)
    
    def set_aggression(self, val):
        self._aggression = val
        return int(self._aggression)

    def set_location(self, loc):
        self._location = loc
        return self._location

    def set_encountered(self, bool):
        self._encountered = bool
        return self._encountered
    
    # adjustment methods start here
    def adjust_defense(self, value):
        self._defense += int(value)
        return int(self._defense)

    def adjust_health(self, value):
        self._health += int(value)
        return int(self._health)

    def adjust_aggression(self, value):
        self._aggression += int(value)
        return int(self._aggression)

    # assorted methods start here
    def add_object(self, object):
        # add AdvObj to inventory
        object.set_location(self._id)
        self._inventory.append(object)
        return self._inventory

    def remove_object(self, object):
        # removes object from inventory (obj list)
        if self._weapon != None and self._weapon != "None":
            if object == self._weapon.get_name():
                self._weapon = None
        if self._armor != None and self._armor != "None":
            if object == self._armor.get_name():
                self._armor = None
        self._inventory.remove(object)
        return self._inventory
    
    def contains_object(self, object):
        # checks if inventory contains object (in list)
        if object in self._inventory:
            return True
        return False

    def do_something(self, player):
        # determines creature action in encounter
        if self._aggression > 0:
            player.adjust_health(self.get_damage())
            print("You took", self.get_damage(), "damage!")


def read_creature(f):
    # reads creature from file and returns it as AdvCreature
    # name, id, defense, armor, weapon, health, aggression, initloc
    name = f.readline().rstrip()             # reads creature name
    if name == "":                           
        return None

    id = f.readline().strip()                         

    defense = f.readline().strip()                          

    armor = f.readline().strip()                           

    weapon = f.readline().strip()                        

    health = f.readline().strip()                             

    agg = f.readline().strip()        

    initloc = f.readline().strip()                       

    ph = f.readline().strip()                              # placeholder to hold blank line in between objects

    return AdvCreature(name, id, defense, armor, weapon, health, agg, initloc)  # return completed creature