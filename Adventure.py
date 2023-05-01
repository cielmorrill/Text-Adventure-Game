# File: Adventure.py
# Ciel Morrill

"""this file runs the Adventure game."""

# DATA_FILE_PREFIX options:
#
#    "Tiny"      a four-room Adventure with no objects or synonyms
#    "Small"     a 12-room Adventure that tests all features
#    "Crowther"  full 77-room Adventure game
#    "Ciel"      custom Adventure game with new features

from AdvGame import AdvGame

# constants

DATA_FILE_PREFIX = "Ciel"

# main program

def adventure():
    game = AdvGame(DATA_FILE_PREFIX)
    game.run()

# start-up code

if __name__ == "__main__":
    adventure()

"""
ASSORTED ADDITIONAL IMPLEMENTATIONS:
(but not even close to all)

Player class
- inventory, defense, armor, weapon, hunger, max hunger, health, max health, morality, flag

Creature class
-name, ID, inventory, defense, armor, weapon, health, aggression, initloc

AdvObject constructors: 
consumable (str val)
moveable (bool)
itemtype (consumable, weapon, item)
damage (int)

many commands, including
ACTIONS
STATS (x)
TAKE/DROP ALL
CONSUME (x)

hunger/starvation system
creatures

creatures find the action of eating weapons rather odd.

ACTIONS IN DETAIL:
TAKE (x): adds the specified item to inventory, or all
DROP (x): removes the specified item from inventory, or all
INVENTORY: displays a list of items in inventory
ACTIONS: displays a list of some basic actions
STATS (x): if no item specified, returns player stats; otherwise returns information about the item
CONSUME (x): adjusts stats based on consumability value of item
- extra_not_consumable (can't eat or progression impossible)
- not_consumable (damage according to weapon damage)
- heal (abs of damage stat)
- full_heal (maxes health)
- extra_heal (permanently increases health)
-  feed (abs of damage for hunger stat)
-  full (fills all hunger)
- extra_full (increase max hunger stat)
- feed_heal (heals and adjusts hunger)
- full_heal_full (fully fills and heals)
- feed_dmg (alleviates hunger but deals damage)
- heal_hunger (heals but increases hunger)
LOOK: displays a more detailed description of room
HELP: displays help text
QUIT: exits game

ENCOUNTER ACTIONS:
["FLEE", "ATTACK", "WAIT", "STEAL", "CONSUME", "HELP"]

do_something() event for creature
"""