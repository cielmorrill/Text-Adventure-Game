# File: AdvGame.py
# Ciel Morrill

"""
defines AdvGame class, which holds backbone of game.
"""

from AdvRoom import AdvRoom, read_room
from AdvObject import AdvObject, read_object, read_complex_object
from AdvCreature import AdvCreature, read_creature
from AdvPlayer import AdvPlayer
import os.path
import random

class AdvGame:

    def __init__(self, datafile):
        # reads game data from the files according to prefix
        self._datafile = datafile
        file_exists = False                # checks if the file exists

        self._roomdict = {}                # reads in dictionary of room {name: AdvRoom}
        file_exists = os.path.exists(datafile + "Rooms.txt")
        if file_exists:
            with open(datafile + "Rooms.txt") as f:
                finished = False
                while not finished:
                    room = read_room(f)
                    if room is None:
                        finished = True
                    else:
                        name = room.get_name()
                        if len(self._roomdict) == 0:
                            self._roomdict["START"] = room
                        self._roomdict[name] = room
        else:
            print("Rooms file does not exist!")

        if self._datafile == "Crowther" or self._datafile == "Small" or self._datafile == "Tiny":
            self._objdict = {}               # reads in dictionary of objects {name: AdvObject}
            file_exists = os.path.exists(datafile + "Objects.txt")
            if file_exists:
                with open(datafile + "Objects.txt") as f:
                    finished = False
                    while not finished:
                        obj = read_object(f)
                        if obj is None:
                            finished = True
                        else:
                            name = obj.get_name()
                            self._objdict[name] = obj
        else:
            self._objdict = {}               # reads in dictionary of complex objects {name: AdvObject}
            file_exists = os.path.exists(datafile + "Objects.txt")
            if file_exists:
                with open(datafile + "Objects.txt") as f:
                    finished = False
                    while not finished:
                        obj = read_complex_object(f)
                        if obj is None:
                            finished = True
                        else:
                            name = obj.get_name()
                            self._objdict[name] = obj

        if not self._datafile == "Crowther" or not self._datafile == "Small" or not self._datafile == "Tiny":
            self._creaturedict = {}               # reads in dictionary of objects {name: AdvObject}
            file_exists = os.path.exists(datafile + "Creatures.txt")
            if file_exists:
                with open(datafile + "Creatures.txt") as f:
                    finished = False
                    while not finished:
                        creature = read_creature(f)
                        if creature is None:
                            finished = True
                        else:
                            name = creature.get_name()
                            self._creaturedict[name] = creature
        
        self._syndict = {}               # reads in dictionary of synonyms {synonym: command}
        file_exists = os.path.exists(datafile + "Synonyms.txt")
        if file_exists:
            with open(datafile + "Synonyms.txt") as f:
                finished = False
                while not finished:
                    line = f.readline()
                    if line is None or line.find("=") == -1:
                        finished = True
                    else:
                        index = line.find("=")
                        synonym = line[:index]
                        define = line[index + 1:]
                        self._syndict[synonym] = define

    def get_room(self, name):
        # returns AdvRoom object according to name
        return self._roomdict[name]

    def run(self):
        # runs the adventure game
        player = AdvPlayer()

        if self._datafile == "Crowther" or self._datafile == "Small" or self._datafile == "Tiny":
            help_text = [
                "Welcome to Adventure!",
                "",
                "This describes the help text for Crowther's game.",
                "If playing a different adventure, change the data file prefix in",
                "Adventure.py and check back.",
                "",
                "Somewhere nearby is Colossal Cave, where some have found fortunes in",
                "treasure and gold, though it is rumored that others who enter are never",
                "seen again.  Magic is said to work in the cave.  I will be your eyes",
                "and hands.  Direct me with natural English commands; I don't understand",
                "all of the English language, but I do a pretty good job.",
                "",
                "It's important to remember that cave passages turn a lot, and that",
                "leaving a room to the north does not guarantee entering the next from",
                "the south, although it often works out that way.  You'd best make",
                "yourself a map as you go along.",
                "",
                "Much of my vocabulary describes places and is used to move you there.",
                "To move, try words like IN, OUT, EAST, WEST, NORTH, SOUTH, UP, or DOWN.",
                "I also know about a number of objects hidden within the cave which you",
                "can TAKE or DROP.  To see what objects you're carrying, say INVENTORY.",
                "To reprint the detailed description of where you are, say LOOK.  If you",
                "want to end your adventure, say QUIT.",
                "",
            ]
            actions = ["QUIT", "HELP", "LOOK", "TAKE", "DROP", "INVENTORY", "ACTIONS"]
        else:
            help_text = [
                "Welcome to the new and improved Adventure!",
                "",
                "This world differs considerably from the area surrounding Colossal Cave.",
                "There are many creatures you will encounter, both friend and foe - ",
                "whether you face them in battle or attempt to make peace is in your hands.",
                "",
                "Will you fight? Will you flee? Or will you forge a new path?",
                "",
                "Ensure that your health stays high and your appetite sated, lest your",
                "journey come to an untimely end. Reinforcing your defenses and staying",
                "well-equipped will help with this endeavor. You may find cooking pots",
                "come in handy.",
                "",
                "Enter ACTIONS to view common commands. Keep in mind that some possibilities",
                "may remain undisplayed."
                "",
                "Know this: your actions have consequences.",
                "",
            ]
            actions = ["ACTIONS", "STATS", "HELP", "LOOK", "QUIT", "INVENTORY", "TAKE", "DROP", "CONSUME", "EQUIP", "ENCOUNTER"]
            encounter_actions = ["FLEE", "ATTACK", "WAIT", "STEAL", "CONSUME", "INSPECT", "INVENTORY", "HELP"]
            secret_actions = ["DIE", "CRY", "COWER", "QUIT"]
            player.set_flag(True)


        # organizes all objects according to location (either to rooms or inventory)
        for name in self._objdict:  
            if self._objdict[name].get_initial_location() in self._roomdict:
                self._roomdict[self._objdict[name].get_initial_location()].add_object(self._objdict[name])
            elif self._objdict[name].get_initial_location() == "PLAYER":
                player.add_object(self._objdict[name])

        # organizes all creatures according to location and gives them their items
        # cdict doesn't initialize unless program name is not crowther/small/tiny
        for name in self._creaturedict:
            if self._creaturedict[name].get_initloc() in self._roomdict:
                self._roomdict[self._creaturedict[name].get_initloc()].add_creature(self._creaturedict[name])
            if self._creaturedict[name].get_armor() is not None and self._creaturedict[name].get_armor() in self._objdict:
                # if armor is not none, adds item to inventory and changes armor to point to AdvObj rather than name
                self._creaturedict[name].add_object(self._objdict[self._creaturedict[name].get_armor()])
                self._creaturedict[name].set_armor(self._objdict[self._creaturedict[name].get_armor()])
            if self._creaturedict[name].get_weapon() is not None and self._creaturedict[name].get_weapon() in self._objdict:
                # if weapon is not none, adds item to inventory and changes weapon to point to AdvObj rather than name
                self._creaturedict[name].add_object(self._objdict[self._creaturedict[name].get_weapon()])
                self._creaturedict[name].set_weapon(self._objdict[self._creaturedict[name].get_weapon()])
            for item in self._objdict:
                if self._objdict[item].get_location() == str(self._creaturedict[name].get_id()):
                    self._creaturedict[name].add_object(self._objdict[item])

        # encounter flag
        encounter_flag = False

        current = "START"
        while current != "EXIT": # game is now running

            # prints description of room according to visitation status
            room = self._roomdict[current]
            if encounter_flag == False:
                if not room.has_been_visited():
                    for line in room.get_long_description():
                        print(line)
                    room.set_visited(True)
                else:
                    print(room.get_short_description())
                print("There is", *room.get_room_obj_desc(), "here.")

            # prints creature status and determines if encounter needs to be forced
            if room.get_creatures() != [] and encounter_flag == False:
                for creature in room.get_creatures():
                    print("There is a", creature.get_name(), "in this room.")
                    if creature.get_aggression() > 0 and creature.get_encountered() == False:
                        encounter_flag = True
                        creature.set_encountered(True)
                        print(creature.get_name(), "has forced an ENCOUNTER!")
                        print("Some possible actions are:", *encounter_actions)
                        

            # computes hunger event
            if player.get_flag():
                if player.get_hunger() < player.get_hunger() // 3:
                    print("You are getting hungry...")
                elif player.get_hunger() < 0:
                    print("You are taking damage from hunger!")
                    player.adjust_health(-5)
                    if player.get_health() < 0:
                        print("You have succumbed to hunger...")
                        skipR = True
                        response = "QUIT"

            if player.get_health() < 0:
                print("You have succumbed to your injuries...")
                current = "EXIT"
                break

            # checks to make sure the room isn't forced, and allows response input accordingly
            skipR = False
            for x in room.get_passages():
                if x[0] == "FORCED":
                    response = "FORCED"
                    room.set_visited(False)
                    skipR = True
            
            if skipR == False:
                response = input("> ").strip().upper() # PLAYER input

            # searches for synoynms in response
            # current issue: if it finds a synonym anywhere in response, it replaces it; needs to have select commands
            """
            for x in self._syndict:
                if x in response:
                    index = response.find(x)
                    rindex = response.rfind(x)
                    left = response[:index]
                    right = response[rindex:]
                    response = left + self._syndict[x] + right
                    response.strip()
                    print("index was", index, "rindex was", rindex, "left:", left, "right:", right)
                    print(response)
            """

            # if statement decides action based on response
            if response in secret_actions:
                # ["DIE", "CRY", "COWER"]
                if response == "QUIT":
                    # quits game
                    current = "EXIT"
                    break
            # checks if an encounter is taking place
            elif encounter_flag and (response in encounter_actions or "STEAL" in response or "CONSUME" in response):
                creature.set_encountered(True)
                print("Some possible actions are:", *encounter_actions)
                # ["FLEE", "ATTACK", "WAIT", "STEAL", "CONSUME", "INSPECT", "INVENTORY", "HELP"]

                # gives some basic information about creature
                for creature in room.get_creatures():
                    if creature.get_name() == "DRAGON" and player.contains_object(self._objdict["SHIFTING_CRYSTAL"]):
                        creature.set_aggression(0)
                        print("The DRAGON is entranced by your SHIFTING_CRYSTAL...")
                    print("You are in an ENCOUNTER with", creature.get_name(), "- it has", creature.get_health(), "hp.")
                    if creature.get_aggression() < -50:
                        print(creature.get_name(), "seems extraordinarily unbothered by your presence.")
                    elif creature.get_aggression() < -10:
                        print(creature.get_name(), "is busy with things that don't include you.")
                    elif creature.get_aggression() == 0:
                        print(creature.get_name(), "is regarding you carefully.")
                    elif creature.get_aggression() < 10:
                        print(creature.get_name(), "is aggressive!")
                    else:
                        print(creature.get_name(), "is filled with a rage that cannot be calmed by ordinary means...")

                    if response == "FLEE":
                        # attempts to end encounter
                        if player.get_damage() > creature.get_damage():
                            encounter_flag = False
                            print("You have successfully fled!")
                        elif creature.get_aggression() < -50:
                            encounter_flag = False
                            print("You have successfully fled!")
                        elif creature.get_aggression() < -10:
                            encounter_flag = False
                            print("You have successfully fled!")
                        elif creature.get_aggression() == 0:
                            encounter_flag = False
                            print("You have successfully fled!")
                        elif creature.get_aggression() < 10:
                            chance = random.randint(0, 100)
                            success = 60
                            if chance > success:
                                encounter_flag = False
                                print("You have successfully fled!")
                            else:
                                print("Your attempts to flee were unsuccessful...")
                                creature.do_something(player)
                        else:
                            chance = random.randint(0, 100)
                            success = 90
                            if chance > success:
                                encounter_flag = False
                                print("You have successfully fled!")
                            else:
                                print("Your attempts to flee were unsuccessful...")
                                creature.do_something(player)
                    elif response == "ATTACK":
                        # deals damage to creature
                        print(creature.get_name(), "has taken", abs(player.get_damage()), "damage at your hands.")

                        if creature.get_aggression() < -50:
                            print(creature.get_name(), "seems rather hurt (emotionally).")
                            player.adjust_morality(-15)
                        elif creature.get_aggression() < -10:
                            print(creature.get_name(), "doesn't seem keen on fighting back.")
                            player.adjust_morality(-10)
                        elif creature.get_aggression() == 0:
                            print(creature.get_name(), "no longer appears passive...")
                            player.adjust_morality(-5)
                        elif creature.get_aggression() < 10:
                            print(creature.get_name(), "looks angry.")
                            player.adjust_morality(-3)
                        else:
                            print(creature.get_name(), "is vengeful!!")
                            player.adjust_morality(-3)

                        creature.adjust_health(player.get_damage())
                        creature.adjust_aggression(2)
                        creature.adjust_aggression(player.get_damage() // 5)
                        if creature.get_health() < 0:
                            print(creature.get_name(), "has been killed.")
                            for x in creature.get_inventory():
                                room.add_object(x)
                            encounter_flag = False
                            creature.set_location("DEAD")
                            room.remove_creature(creature)
                            
                    elif response == "WAIT":
                        # basically inaction on part of player
                        if creature.get_aggression() < 1:
                            print(creature.get_name(), "appears bored.")
                            print("ENCOUNTER has ended!")
                            encounter_flag = False
                        elif creature.get_aggression() < 50:
                            print(creature.get_name(), "is not appeased...")
                            creature.do_something(player)
                        else:
                            print(creature.get_name(), "appears to have become more enraged!!")
                            creature.adjust_aggression(5)
                            creature.do_something(player)
                    elif "STEAL" in response:
                        # attempt to steal item
                        # check if item location is creature
                        # extra hard to steal weapon and armor
                        if len(response) > 5:
                            response = response[5:].strip()
                        else:
                            print("STEAL requires a specified item.")

                        if response in self._objdict and self._objdict[response].get_location() == creature.get_id():
                            chance = random.randint(0, 100)
                            success = 50
                            if creature.get_aggression() < -50:
                                success = 10
                                print(creature.get_name(), "doesn't seem to care either way.")
                                if chance > success:
                                    print(response, "was added to inventory!")
                                    player.add_object(self._objdict[response])
                                    creature.remove_object(self._objdict[response])
                                else:
                                    print("Your attempt was unsuccessful.")
                            elif creature.get_aggression() < -10:
                                success = 25
                                if chance > success:
                                    print(creature.get_name(), "seems a little miffed.")
                                    print(response, "was added to inventory!")
                                    player.add_object(self._objdict[response])
                                    creature.remove_object(self._objdict[response])
                                else:
                                    print("Your attempt was unsuccessful.")
                                    print(creature.get_name(), "looks rather amused.")
                                    creature.adjust_aggression(-2)
                            elif creature.get_aggression() == 0:
                                success = 50
                                if chance > success:
                                    print(response, "was added to inventory!")
                                    print(creature.get_name(), "looks upset!")
                                    creature.adjust_aggression(2)
                                    player.add_object(self._objdict[response])
                                    creature.remove_object(self._objdict[response])
                                else:
                                    print("Your attempt was unsuccessful.")
                                    print(creature.get_name(), "is not pleased with you.")
                            elif creature.get_aggression() < 10:
                                success = 60
                                if chance > success:
                                    print(response, "was added to inventory!")
                                    print(creature.get_name(), "looks like it wants to hurt you.")
                                    player.add_object(self._objdict[response])
                                    creature.remove_object(self._objdict[response])
                                    creature.adjust_aggression(2)
                                else:
                                    print("Your attempt was unsuccessful.")
                                    print("However,", creature.get_name(), "is still visibly upset.")
                                    creature.adjust_aggression(1)
                            else:
                                success = 90
                                if chance > success:
                                    print(response, "was added to inventory!")
                                    print(creature.get_name(), "seems surprised.")
                                    print("The surprise has increased its rage!!")
                                    player.add_object(self._objdict[response])
                                    creature.remove_object(self._objdict[response])
                                    creature.adjust_aggression(5)
                                else:
                                    print("Your attempt was unsuccessful.")
                                    print("Your failure has made", creature.get_name(), "angrier!!")
                                    creature.adjust_aggression(2)
                        else:
                            print("None found.")
                        creature.do_something(player)
                    elif "CONSUME" in response:
                        # consume item
                        if len(response) > 7:
                            response = response[7:].strip()
                        else:
                            print("CONSUME requires a specified item.")

                        ate_flag = False

                        if response in self._objdict and player.contains_object(self._objdict[response]):
                            consum = self._objdict[response].get_consumability_val()
                            if consum == "extra_not_consumable":
                                # can't be consumed
                                print(response, "cannot be consumed!!")
                            elif consum == "not_consumable":
                                # deals damage to player
                                player.adjust_health(self._objdict[response].get_damage())
                                player.remove_object(self._objdict[response])
                                print(response, "consumed!")
                                print("You took", abs(self._objdict[response].get_damage()), "damage!")
                                ate_flag = True
                            elif consum == "heal":
                                # heals player... if the item isn't malicious
                                player.adjust_health(self._objdict[response].get_damage())
                                player.remove_object(self._objdict[response])
                                print(response, "consumed!")
                                print("You healed", self._objdict[response].get_damage(), "hp!")
                                ate_flag = True
                            elif consum == "full_heal":
                                # sets player health to full
                                player.adjust_health(player.get_maxhealth())
                                player.remove_object(self._objdict[response])
                                print(response, "consumed!")
                                print("You are now at full health!")
                                ate_flag = True
                            elif consum == "extra_heal":
                                # increases player health permanently
                                player.adjust_maxhealth(self._objdict[response].get_damage())
                                player.adjust_health(player.get_maxhealth())
                                player.remove_object(self._objdict[response])
                                print(response, "consumed!")
                                print("Your max health has been increased!")
                                ate_flag = True
                            elif consum == "feed":
                                # decreases hunger
                                player.adjust_hunger(self._objdict[response].get_damage())
                                player.remove_object(self._objdict[response])
                                print(response, "consumed!")
                                print("Your hunger has been alleviated for the time being.")
                                ate_flag = True
                            elif consum == "full":
                                # replenishes hunger stat
                                player.adjust_hunger(player.get_maxhunger())
                                player.remove_object(self._objdict[response])
                                print(response, "consumed!")
                                print("You are fully satiated!")
                                ate_flag = True
                            elif consum == "extra_full":
                                # increases max hunger stat
                                player.adjust_maxhunger(self._objdict[response].get_damage())
                                player.adjust_hunger(player.get_maxhunger())
                                player.remove_object(self._objdict[response])
                                print(response, "consumed!")
                                print("Your max hunger has been increased!")
                                ate_flag = True
                            elif consum == "feed_heal":
                                # affects both hunger and health
                                player.adjust_hunger(self._objdict[response].get_damage())
                                player.adjust_health(self._objdict[response].get_damage())
                                player.remove_object(self._objdict[response])
                                print(response, "consumed!")
                                print("Your hunger has been alleviated, and you healed", self._objdict[response].get_damage(), "hp!")
                                ate_flag = True
                            elif consum == "full_heal_full":
                                # sets both health and hunger to full
                                player.adjust_hunger(player.get_maxhunger())
                                player.adjust_health(player.get_maxhealth())
                                player.remove_object(self._objdict[response])
                                print(response, "consumed!")
                                print("Your health and hunger have been restored to full!")
                                ate_flag = True
                            elif consum == "feed_dmg":
                                # helps hunger but deals damage
                                player.adjust_hunger(abs(self._objdict[response].get_damage()))
                                player.adjust_health(self._objdict[response].get_damage())
                                player.remove_object(self._objdict[response])
                                print(response, "consumed!")
                                print("You have alleviated your hunger... but took", abs(self._objdict[response].get_damage()), "damage!")
                                ate_flag = True
                            elif consum == "heal_hunger":
                                # heals but increases hunger
                                player.adjust_hunger(self._objdict[response].get_damage())
                                player.adjust_health(abs(self._objdict[response].get_damage()))
                                player.remove_object(self._objdict[response])
                                print(response, "consumed!")
                                print("You healed", abs(self._objdict[response].get_damage()), "hp... but your hunger has grown.")
                                ate_flag = True
                        else:
                            print("None found to be consumed.")

                        # if you killed yourself doing this
                        if player.get_health() < 0:
                            print("Your actions have led to your own demise!!")
                            print(creature.get_name(), "looks mildly alarmed.")
                            current = "EXIT"
                            break

                        if ate_flag:
                            if self._objdict[response].get_itemtype() == "weapon":
                                # special response if you crunched a weapon
                                if creature.get_aggression() < -50:
                                    print(creature.get_name(), "looks weirded out.")
                                    print(creature.get_name(), "chooses to walk away...")
                                    encounter_flag = False
                                    break
                                elif creature.get_aggression() < -10:
                                    print(creature.get_name(), "looks weirded out.")
                                    print(creature.get_name(), "is not making eye contact...")
                                    creature.adjust_aggression(-10)
                                elif creature.get_aggression() == 0:
                                    print(creature.get_name(), "regards you with... respect?")
                                    print("It seems somewhat at peace.")
                                    creature.adjust_aggression(-5)
                                elif creature.get_aggression() < 10:
                                    print(creature.get_name(), "appears confused.")
                                    print("However, it does seem somewhat appeased?")
                                    creature.adjust_aggression(-5)
                                else:
                                    print(creature.get_name(), "appears confused.")
                                    print("Your actions have filled it with rage!!")
                                    creature.adjust_aggression(10)
                            creature.do_something(player)
                    elif response == "INSPECT":
                        # report creature damage and all items
                        temp = []
                        if creature.get_inventory() != []:
                            for obj in creature.get_inventory():
                                temp.append(obj.get_name())
                                temp.append("and")
                        else:
                            temp.append("nothing and")
                        print(creature.get_name(), "is holding", *temp, "can deal", abs(creature.get_damage()), "damage per hit.")
                    elif response == "INVENTORY":
                    # returns list of items in inventory
                        inventory = player.get_inventory()
                        if len(inventory) == 0:
                            print("No items in inventory.")
                        elif len(player.get_inventory()) == 1:
                            print("Inventory contains", inventory[0].get_name() + ".")
                        else:
                            temp = []
                            for i in range(len(inventory)):
                                if i < len(inventory) - 1:
                                    temp.append(inventory[i].get_name())
                                    temp.append("and")
                                else:
                                    temp.append(inventory[i].get_name())
                            print("Inventory contains", *temp, ".")
                    elif response == "HELP":
                        help = [
                            "You are in a creature ENCOUNTER!",
                            "",
                            "Different creatures have different responses to your actions.",
                            ""
                        ]
                        for l in help:
                            print(l)

            # checks if response is an action verb and acts accordingly
            elif encounter_flag == False and response in actions or "TAKE" in response or "DROP" in response or "STATS" in response or "CONSUME" in response or "ENCOUNTER" in response or "EQUIP" in response:
                # ["ACTIONS", "STATS", "HELP", "LOOK", "QUIT", "INVENTORY", "TAKE", "DROP", "CONSUME", "ENCOUNTER"]
                if response == "QUIT":
                    # quits game
                    current = "EXIT"
                    break
                elif response == "HELP":
                    # returns help text
                    for l in help_text:
                        print(l)
                elif response == "LOOK":
                    # returns long description of room
                    for line in room.get_long_description():
                        print(line)
                    print("There is", *room.get_room_obj_desc(), "here.")
                elif "TAKE" in response:
                    # cuts 'take' off response to isolate item
                    # checks that the obj is in dict and that location matches room
                    # sets location to player, adds to inventory, and removes from room
                    if len(response) > 4:
                        response = response[4:].strip()
                    else:
                        print("TAKE requires a specified item.")

                    if response in self._objdict and self._objdict[response].get_location() == room.get_name():
                        if self._objdict[response].get_name() == "SHIFTING_CRYSTAL":
                            if player.contains_object(self.objdict["HEAVY_DUTY_GLOVES"]):
                                player.add_object(self._objdict[response])
                                room.remove_object(self._objdict[response])
                                print("Your HEAVY_DUTY_GLOVES allow you to pick up the crystal.")
                                print(response, "taken!")
                            else:
                                print("It burns your hand... You can't touch it.")
                        player.add_object(self._objdict[response])
                        room.remove_object(self._objdict[response])
                        print(response, "taken!")
                    elif response == "ALL":
                        for obj in room.get_contents():
                            player.add_object(self._objdict[obj.get_name()])
                            room.remove_object(self._objdict[obj.get_name()])
                        print("All items in room taken!")
                    else:
                        print("None found.")
                elif "DROP" in response:
                    # cuts 'drop' off response to isolate item
                    # checks that the obj is in dict and that location matches player
                    # sets location to room and removes from inventory
                    if len(response) > 4:
                        response = response[4:].strip()
                    else:
                        print("DROP requires a specified item.")

                    if response in self._objdict and self._objdict[response].get_location() == "PLAYER":
                        self._objdict[response].set_location(room.get_name())
                        player.remove_object(self._objdict[response])
                        room.add_object(self._objdict[response])
                        print(response, "dropped!")
                    elif response == "ALL":
                        for obj in player.get_inventory():
                            player.remove_object(self._objdict[obj.get_name()])
                            room.add_object(self._objdict[obj.get_name()])
                        print("All items in inventory dropped!")
                    else:
                        print("None found.")
                elif response == "INVENTORY":
                    # returns list of items in inventory
                    inventory = player.get_inventory()
                    if len(inventory) == 0:
                        print("No items in inventory.")
                    elif len(player.get_inventory()) == 1:
                        print("Inventory contains", inventory[0].get_name() + ".")
                    else:
                        temp = []
                        for i in range(len(inventory)):
                            if i < len(inventory) - 1:
                                temp.append(inventory[i].get_name())
                                temp.append("and")
                            else:
                                temp.append(inventory[i].get_name())
                        print("Inventory contains", *temp, ".")
                elif response == "ACTIONS":
                    # prints list of some common actions
                    print("Some possible actions are:", *actions)
                elif "STATS" in response:
                    # prints player stats if no item specified; otherwise, prints item stats
                    if len(response) > 5:
                        response = response[5:].strip()
                    else:
                        print("Attack:", player.get_damage(), "Hunger:", player.get_hunger(), "Health:", player.get_health())
                    
                    if response in self._objdict and self._objdict[response].get_location() == "PLAYER":
                        print("Item type:", self._objdict[response].get_itemtype(), "Consumability:", self._objdict[response].get_consumability_val(), "Damage:", self._objdict[response].get_damage())
                elif "CONSUME" in response:
                    # checks for item in inventory and responds according to consumability value
                    if len(response) > 7:
                        response = response[7:].strip()
                    else:
                        print("CONSUME requires a specified item.")

                    if response in self._objdict and player.contains_object(self._objdict[response]):
                        consum = self._objdict[response].get_consumability_val()
                        if consum == "extra_not_consumable":
                            # can't be consumed
                            print(response, "cannot be consumed!!")
                        elif consum == "not_consumable":
                            # deals damage to player
                            player.adjust_health(self._objdict[response].get_damage())
                            player.remove_object(self._objdict[response])
                            print(response, "consumed!")
                            print("You took", abs(self._objdict[response].get_damage()), "damage!")
                        elif consum == "heal":
                            # heals player... if the item isn't malicious
                            player.adjust_health(self._objdict[response].get_damage())
                            player.remove_object(self._objdict[response])
                            print(response, "consumed!")
                            print("You healed", self._objdict[response].get_damage(), "hp!")
                        elif consum == "full_heal":
                            # sets player health to full
                            player.adjust_health(player.get_maxhealth())
                            player.remove_object(self._objdict[response])
                            print(response, "consumed!")
                            print("You are now at full health!")
                        elif consum == "extra_heal":
                            # increases player health permanently
                            player.adjust_maxhealth(self._objdict[response].get_damage())
                            player.adjust_health(player.get_maxhealth())
                            player.remove_object(self._objdict[response])
                            print(response, "consumed!")
                            print("Your max health has been increased!")
                        elif consum == "feed":
                            # decreases hunger
                            player.adjust_hunger(self._objdict[response].get_damage())
                            player.remove_object(self._objdict[response])
                            print(response, "consumed!")
                            print("Your hunger has been alleviated for the time being.")
                        elif consum == "full":
                            # replenishes hunger stat
                            player.adjust_hunger(player.get_maxhunger())
                            player.remove_object(self._objdict[response])
                            print(response, "consumed!")
                            print("You are fully satiated!")
                        elif consum == "extra_full":
                            # increases max hunger stat
                            player.adjust_maxhunger(self._objdict[response].get_damage())
                            player.adjust_hunger(player.get_maxhunger())
                            player.remove_object(self._objdict[response])
                            print(response, "consumed!")
                            print("Your max hunger has been increased!")
                        elif consum == "feed_heal":
                            # affects both hunger and health
                            player.adjust_hunger(self._objdict[response].get_damage())
                            player.adjust_health(self._objdict[response].get_damage())
                            player.remove_object(self._objdict[response])
                            print(response, "consumed!")
                            print("Your hunger has been alleviated, and you healed", self._objdict[response].get_damage(), "hp!")
                        elif consum == "full_heal_full":
                            # sets both health and hunger to full
                            player.adjust_hunger(player.get_maxhunger())
                            player.adjust_health(player.get_maxhealth())
                            player.remove_object(self._objdict[response])
                            print(response, "consumed!")
                            print("Your health and hunger have been restored to full!")
                        elif consum == "feed_dmg":
                            # helps hunger but deals damage
                            player.adjust_hunger(abs(self._objdict[response].get_damage()))
                            player.adjust_health(self._objdict[response].get_damage())
                            player.remove_object(self._objdict[response])
                            print(response, "consumed!")
                            print("You have alleviated your hunger... but took", abs(self._objdict[response].get_damage()), "damage!")
                        elif consum == "heal_hunger":
                            # heals but increases hunger
                            player.adjust_hunger(self._objdict[response].get_damage())
                            player.adjust_health(abs(self._objdict[response].get_damage()))
                            player.remove_object(self._objdict[response])
                            print(response, "consumed!")
                            print("You healed", abs(self._objdict[response].get_damage()), "hp... but your hunger has grown.")
                    else:
                        print("None found to be consumed.")
                    
                    if player.get_health() > player.get_maxhealth():
                        player.set_health(player.get_maxhealth())
                    if player.get_hunger() > player.get_maxhunger():
                        player.set_hunger(player.get_maxhunger())

                    if player.get_health() < 0:
                            print("Your actions have led to your own demise!!")
                            current = "EXIT"
                            break

                    if self._objdict[response] == player.get_weapon():
                        player.remove_weapon
                    # have to do this for armor too if i have time
                elif "ENCOUNTER" in response:
                    # allows encounter with creature under valid conditions
                    if len(response) > 9:
                        response = response[9:].strip()
                    else:
                        print("ENCOUNTER requires a specified creature - and creature must be in the same room.")

                    if response in self._creaturedict and self._creaturedict[response].get_location() == room.get_name():
                        encounter_flag = True
                        self._creaturedict[response].set_encountered(True)
                        print("You have started an encounter!")
                        print("Some possible actions are:", *encounter_actions)
                    else:
                        print("None found.")
                elif "EQUIP" in response:
                    # allows weapon to be equipped to player
                    # cuts 'drop' off response to isolate item
                    # checks that the obj is in dict and that location matches player
                    # sets location to room and removes from inventory
                    if len(response) > 5:
                        response = response[5:].strip()
                    else:
                        print("EQUIP requires a specified item.")

                    if response in self._objdict and player.contains_object(self._objdict[response]):
                        player.set_weapon(self._objdict[response])
                        print(response, "equipped!")
                    else:
                        print("None found.")



            else: # if nothing else, adjust room or ask for re-entry of response
                passagelist = room.get_passages() # list of tuples (direction, room name, key)

                next_room = None

                # iterate through passage tuples - key passages take priority; if no rooms accessible, None assigned
                for tup in passagelist:
                    if response == tup[0]:
                    # checks for key room; breaks loop if key room matches
                        if tup[2] is not None:
                            flag = False
                            for item in player.get_inventory():
                                if item.get_name() == tup[2]:
                                    flag = True
                            if flag == True:
                                next_room = tup[1]
                                break
                        elif tup[2] is None:
                            next_room = tup[1]

                if next_room is None:
                    print("Action is not possible.")
                else:
                    if player.get_flag():
                        player.adjust_hunger(-1)
                    current = next_room
