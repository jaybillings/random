#!/usr/bin/env python
'''Rabbit simulation v0.1'''
import random
import uuid
import sys

class Rabbit:
    '''a generic rabbit'''
    name = None
    age = 0
    sex = None
    generation = 0
    stats = {
        "fortitude": 0,
        "agility": 0,
        "foraging": 0,
        "aggression": 0
    }
    parents = {
        "dad": None,
        "mom": None
    }

    def __init__(self, dad=None, mom=None, name=None sex=None, age=None):
        '''the init function'''
        random.seed()
        # Set name
        if name:
            self.name = name
        else:
            self.name = str(uuid.uuid4())

        # Set sex
        if sex:
            self.sex = sex
        else:
            sex = random.randint(0, 1)
            if sex == 0:
                self.sex = "male"
            else:
                self.sex = "female"

        # Set age
        if age:
            self.age = age

        # Set stats
        if dad and mom:
            # inheriting stats from the parent
            # random range defined by max and min of parent stats
            fort = [dad.stats["fortitude"], mom.stats["fortitude"]]
            fort.sort()

            agil = [dad.stats["agility"], mom.stats["agility"]]
            agil.sort()

            forag = [dad.stats["foraging"], mom.stats["foraging"]]
            forag.sort()

            agg = [dad.stats["aggression"], mom.stats["aggression"]]
            agg.sort()

            self.stats = {"fortitude": random.randint(fort[0], fort[1]),
                          "agility": random.randint(agil[0], agil[1]),
                          "foraging": random.randint(forag[0], forag[1]),
                          "aggression": random.randint(agg[0], agg[1])}
            self.generation += 1
        else:
            # If user-generated, pick stats entirely randomly
            self.stats = {"fortitude": random.randint(1, 10),
                          "agility": random.randint(1, 10),
                          "foraging": random.randint(1, 10),
                           "aggression": random.randint(1, 10)}

        # Set parents, if applicable
        if dad and mom:
            self.parents = {"dad": dad.name,
                            "mom": mom.name}

    def display(self):
        '''Displays stats about the rabbit'''
        print "Name: " + self.name
        print "Sex: " + self.sex
        print "Generation: " + self.generation
        print "Fortitude  : " + str(self.stats["fortitude"])
        print "Agility    : " + str(self.stats["agility"])
        print "Foraging   : " + str(self.stats["foraging"])
        print "Aggression : " + str(self.stats["aggression"])
    
    def display_lineage(self):
        numeral = "th"
        if self.generation == 1:
            prefix = "st"
        elif self.generation == 2:
            prefix = "nd"
        elif self.generation == 3:
            prefix = "rd"
        print self.name + " is a " + self.generation + prefix + "rabbit."
        print "Its parents are " + self.dad + " and " + self.mom + "."

def test():
        mom = Rabbit(sex='female')
        dad = Rabbit(sex='male')
        mom.display()
        dad.display()
        child = Rabbit(dad=dad, mom=mom)
        child.display()

def option_screen():
    '''Print the option screen and collect the choice'''
    choice = -1
    while int(choice) < 0 or int(choice) > 4:
        print "Here's what you can do:"
        print "1) List rabbits"
        print "2) Create rabbit"
        print "3) Breed rabbits"
        print "4) Exit"
        choice = raw_input("What would you like to do? ")
        print choice
    return choice

def run():
    '''Run the freaking program'''
    rabbits = []

    print "Welcome to RabbitSim!"
    choice = int(option_screen())

    while choice:
        if choice == 1:
            # List rabbits
            if not rabbits:
                print "You have no rabbits."
            else:
                print "Here are your rabbits:"
                for bun in rabbits:
                    bun.display()
        elif choice == 2:
            # Create a new rabbit and display it
            rab = Rabbit()
            print "Here is your new rabbit: "
            rab.display()
            rabbits.append(rab)
        elif choice == 3:
            # Breed two rabbits
            dad = None
            mom = None
            dad_name = raw_input("Who is the father? ")
            mom_name = raw_input("Who is the mother? ")
            for bun in rabbits:
                if bun.name == dad_name and bun.sex == "male":
                    dad = bun
                if bun.name == mom_name and bun.sex == "female":
                    mom = bun
            if not mom or not dad:
                print "Those are not valid parents."
            else:
                rab = Rabbit(dad, mom)
                print "Here is your new rabbit: "
                rab.display()
                rabbits.append(rab)
        elif choice == 4:
            print 'Goodbye!'
            sys.exit(0)
        choice = int(option_screen())

if __name__ == "__main__":
    run()