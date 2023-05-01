# File: AdvPlayer.py
# Ciel Morrill

"""
defines AdvPlayer class, which holds player data.
"""

from AdvObject import AdvObject

class AdvPlayer:

    def __init__(self, defense = 0, armor = None, weapon = None, hunger = 100, health = 100, morality = 0):
        # class constructors
        self._defense = int(defense) # int
        self._armor = armor # AdvObj
        self._weapon = weapon # AdvObj
        self._hunger = int(hunger) # int
        self._maxhunger = int(hunger) # int
        self._health = int(health) # int
        self._maxhealth = int(health) # int
        self._morality = int(morality) # int
        self._inventory = [] # list
        self._flag = False # flag that determines if complex game is running

    # getter methods start here
    def get_defense(self):
        return int(self._defense)

    def get_armor(self):
        return self._armor

    def get_weapon(self):
        return self._weapon
    
    def get_hunger(self):
        return int(self._hunger)
    
    def get_maxhunger(self):
        return int(self._maxhunger)
    
    def get_health(self):
        return int(self._health)

    def get_maxhealth(self):
        return int(self._maxhealth)
    
    def get_morality(self):
        return int(self._morality)
    
    def get_inventory(self):
        # returns a copy of inventory
        return self._inventory.copy()

    def get_damage(self):
        if self._weapon == None or self._weapon == "None":
            return -5
        else:
            return int(self._weapon.get_damage())

    def get_flag(self):
        return self._flag

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
    
    def set_hunger(self, val):
        self._hunger = val
        return int(self._hunger)
    
    def set_health(self, val):
        self._health = val
        return int(self._health)
    
    def set_morality(self, val):
        self._morality = val
        return int(self._morality)
    
    def set_flag(self, bool):
        self._flag = bool
        return self._flag
    
    # adjustment methods start here
    def adjust_defense(self, value):
        self._defense += int(value)
        return int(self._defense)

    def adjust_hunger(self, value):
        self._hunger += int(value)
        return int(self._hunger)

    def adjust_maxhunger(self, value):
        self._maxhunger += int(value)
        return int(self._maxhunger)

    def adjust_health(self, value):
        self._health += int(value)
        return int(self._health)

    def adjust_maxhealth(self, value):
        self._maxhealth += int(value)
        return int(self._maxhealth)

    def adjust_morality(self, value):
        self._morality += int(value)
        return int(self._morality)

    # assorted methods start here
    def add_object(self, object):
        # add AdvObj to inventory
        object.set_location("PLAYER")
        self._inventory.append(object)
        return self._inventory

    def remove_weapon(self):
        # removes weapon
        self._weapon = None
        return self._weapon

    def remove_object(self, object):
    # removes object from inventory (obj list)
        self._inventory.remove(object)
        return self._inventory
    
    def contains_object(self, object):
    # checks if inventory contains object (in list)
        if object in self._inventory:
            return True
        return False
