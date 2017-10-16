import cfg
import random
from Person import Person
from Person import personFromString

currentViewers = [] # each person represented as Persoonclass
saveCounter = 0
gHublist = [] # each person represented as ["name", #points]

# neatline = (type, username, channel, [message])

with open('log.txt', 'a') as f:
    f.write("Ayy")


def handle(neatline):

    # constant string handling
    if neatline == "?":
        return "?"
    elif neatline == "DISTRIBUTE":
        print("gHublist")
        for person in gHublist:
            print(person)
        print("currentViewers")
        for person in currentViewers:
            print(person)
        for viewer in currentViewers:
            viewer.addPoints(10)
        cfg.SAVE += 1
        if cfg.SAVE == 1:
            cfg.SAVE = 0
            with open('ghublist.txt', 'w') as f:
                for viewer in currentViewers:
                    f.write(str(viewer))
            # TODO: Import viewerlist from file
        return "Success"
    elif neatline == "PING":
        return "PING"

    # simple string handling
    [messageType, username, channel] = neatline[:3]
    if messageType == "MESSAGE":
        with open('log.txt', 'a') as f:
            f.write("MESSAGE = " + username + ": " + neatline[3] + " "+ channel + "\n")
        return "Success"
    elif messageType == "JOIN":
        foundperson = findperson(username, currentViewers)
        if foundperson == "notFound":
            foundperson = findperson(username, gHublist)
            if foundperson == "notFound":
                newPerson = Person(username, channel)
                currentViewers.append(newPerson)
                gHublist.append(newPerson)
                # TODO: adopt save to join multiple persons with same name
            else:
                currentViewers.append(foundperson)
        else:
            foundperson.channel = channel
        return "Success"
    elif neatline[0] == "PART":

        try:
            foundperson = findperson(username, currentViewers)
            currentViewers.remove(foundperson)
            return "Success"
        except:
            return "Err: Player " + username + " not found!"
    #the problem
    elif messageType == "COMMAND":
        with open('log.txt', 'a') as f:
            f.write("COMMAND = " + username + ": " + neatline[3] + " "+ channel + "\n")
        neatCommand = neatline[3].split(' ')
        if neatCommand[0] == "gamble":
            return gamble(neatCommand, username, channel)

        return "Success"
        # TODO: check command in a list of commands, then return appropriate text
        # TODO: bonus, bonusall (game specific commands), points, bet/poll (outputs to text), give, duel, giveaway, lief (nonary, unary), nietlief, about, ranking, commands, speurtocht(maybe real)
        # TODO: questions, gamble tracking
        # TODO: Moderation


    #error catching
    else:
        print("Err: Command + " + neatline + " not recognized")
        return "Err: Command + " + neatline + " not recognized"


def findperson(value, list):
    for person in list:
        if value == person.name:
            return person
    return "notFound"

def gamble(neatCommand, username, channel):
    try:
        value = int(neatCommand[1])
    except:
        return ["MSG: Wel een getal invullen grapjas", channel]
    person = findperson(username, currentViewers)
    if person == "notFound":
        return ["MSG: Even geduld, je kan zo pas gamblen!", channel]
    elif person.points < value:
        return ["MSG: Je hebt maar " + str(person.points) + " GHubbies!", channel]
    else:
        roll = random.randint(1,100)
        if roll < 66:
            person.points -= value
            return ["MSG: Helaas, je rolde " + str(roll) + "! Je hebt nog " + str(person.points) + " GHubbies!", channel]
        elif roll == 100:
            person.points += 2*value
            return ["MSG: Wow, 100! Je hebt nu " + str(person.points) + " GHubbies!", channel]
        else:
            person.points += value
            return ["MSG: Gefeliciteerd, je rolde " + str(roll) + "! Je hebt nu " + str(person.points) + " GHubbies!", channel]