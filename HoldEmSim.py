#!/usr/bin/env python

import itertools
import time
import random
import os
from collections import defaultdict
from collections import Counter
import warnings


def isstraightflush(cards):
    return isflush(cards) and isstraight(cards)

def isfourofakind(cards):
    cardnums = [card[:-1] for card in cards]
    c = Counter(cardnums)
    highest = c.most_common(1)[0]
    if(highest[1] == 4):
        return True
    else:
        return False
#determines if there is a full house, will throw an error of deck is messed up (like for 5ok)
def isfullhouse(cards):
    cardnums = [card[:-1] for card in cards]
    c = Counter(cardnums)
    #print("C is infullhouse",c)
    highest = c.most_common(2)[0]
    try:
        second  = c.most_common(2)[1]l
    except:
        warnings.warning("Got Five of a Kind or Something")
    if (highest[1] == 3 and second[1] == 2):
        return True
    else:
        return False

def isflush(cards):
    scount = "".join(cards).count("S")
    hcount = "".join(cards).count("H")
    ccount = "".join(cards).count("C")
    dcount = "".join(cards).count("D")

    if (scount == 5) or (hcount == 5) or (ccount == 5) or (dcount == 5):
        return True
    else:
        return False

def isstraight(cards):
    cardtype = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    value    = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    highstraight = [1, 10, 11, 12, 13]
    combo = dict(zip(cardtype, value))

    #toss the suit, we don't care for straights
    handvalues = []
    cardnums = [card[:-1] for card in cards]
    for card in cardnums:
        handvalues.append(combo[card])

    #sort the values
    handvalues = sorted(handvalues)
    #print(handvalues)

    minv = min(handvalues)
    maxv = max(handvalues)
    #remember, range is stupid in python 3
    rangeofhand = list(range(min(handvalues), max(handvalues)+1))

    #check special high Ace straight
    if(handvalues == highstraight):
        #print("max straight")
        return True
    #will otherwise be a straight if the list is values incremented by one
    elif(handvalues == rangeofhand):
        #print("Non max straight")
        return True
    else:
        #not a straight
        return False

def isthreeofakind(cards):
    cardnums = [card[:-1] for card in cards]
    c = Counter(cardnums)
    highest = c.most_common(2)[0]
    second  = c.most_common(2)[1]
    if (highest[1] == 3 and second[1] == 1):
        return True
    else:
        return False

def istwopair(cards):
    cardnums = [card[:-1] for card in cards]
    c = Counter(cardnums)
    highest = c.most_common(2)[0]
    second  = c.most_common(2)[1]
    if (highest[1] == 2 and second[1] == 2):
        return True
    else:
        return False

def isonepair(cards):
    cardnums = [card[:-1] for card in cards]
    c = Counter(cardnums)
    highest = c.most_common(2)[0]
    second  = c.most_common(2)[1]
    if (highest[1] == 2 and second[1] == 1):
        return True
    else:
        return False
    return

def highcardvalue(cards):
    cardnums = [card[:-1] for card in cards]
    #print("card nums",cardnums)

    cardtype = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    value    = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    combo = dict(zip(cardtype, value))
    return sorted([combo[card] for card in cardnums])[::-1]

def bestsf(setsofcards):

    cardtype = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    value    = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    highstraight = [1, 10, 11, 12, 13]
    combo = dict(zip(cardtype, value))
    potential = []
    max = 0

    for cards in setsofcards:
        cardvals = sorted([combo[card[:-1]] for card in cards])
        if (cardvals == highstraight):
            return cards
        else:
            if(cardvals[-1] > max):
                max = cardvals[-1]
                potential = cards
        #print(cardvals)
    return sorted(potential)

def bestfok(setsofcards):
    cardtype = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    value    = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    combo = dict(zip(cardtype, value))
    potential = []
    maxhighest = 0
    maxoffcard = 0

    for cards in setsofcards:
        cardnums = [card[:-1] for card in cards]
        c = Counter(cardnums)
        highest = combo[c.most_common(2)[0][0]]  #this is the card type of the 4ok
        offcard = combo[c.most_common(2)[1][0]]  #this is the card type of the lonewolf
        if highest > maxhighest:
            potential = cards
            maxhighest = highest
            #print("Highest", potential)
        elif offcard > maxoffcard:
            potential = cards
            maxoffcard = offcard
            #print("Off", potential)
    return sorted(potential)

def bestfh(setsofcards):

    cardtype = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    value    = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    combo = dict(zip(cardtype, value))
    potential = []
    maxhighest = 0
    maxoffcard = 0

    for cards in setsofcards:
        cardnums = [card[:-1] for card in cards]
        c = Counter(cardnums)
        #print("here is C",c)
        highest = combo[c.most_common(2)[0][0]]  #this is the card type of the 3ok
        offcard = combo[c.most_common(2)[1][0]]  #this is the card type of the pair
        if highest > maxhighest:
            potential = cards
            maxhighest = highest
            #print("Highest", potential)
            break
        elif offcard > maxoffcard:
            potential = cards
            maxoffcard = offcard
            #print("Second", potential)
    return sorted(potential)


def bestfl(setsofcards):
    cardtype = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    value    = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    combo = dict(zip(cardtype, value))
    scards = []

    currentmax = [0, 0, 0, 0, 0]
    maxcards   = [0, 0, 0, 0, 0]

    for cards in setsofcards:
        currentsort = (sorted([combo[card[:-1]] for card in cards])[::-1])
        compare = [currentsort[i] - currentmax[i] for i in range(5)]
        for i in range(5):
            if compare[i] > 0:
                currentmax = currentsort
                maxcards   = cards
                #print("Assigning CM as", currentmax)
                break
        #print("Compare is ", compare)
    return sorted(maxcards)

#determine best straight from cards that are all straight hands
#Only works for one player currently
def bestst(setsofcards):
    cardtype = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    value    = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    highstraight = [1, 10, 11, 12, 13][::-1] #going to reverse it this time for easier sorting comparisons
    combo = dict(zip(cardtype, value))

    currentmax = [0, 0 ,0, 0, 0]
    maxcards = []

    for cards in setsofcards:
        currentsort = (sorted([combo[card[:-1]] for card in cards]))[::-1]
        if (currentsort == highstraight):
            return sorted(cards)
        else:
            compare = [currentsort[i] - currentmax[i] for i in range(5)]
            for i in range(5):
                if compare[i] > 0:
                    currentmax = currentsort
                    maxcards = cards
    return sorted(maxcards)

#Get best three of a kind hand out of multiple tok hands
def besttok(setsofcards):
    cardtype = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    value    = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    combo = dict(zip(cardtype, value))

    currentmax = [0, 0, 0]
    maxcards = []

    for cards in setsofcards:
        cardnums = [card[:-1] for card in cards]
        c = Counter(cardnums)
        highest = combo[c.most_common(3)[0][0]]
        offone  = max(combo[c.most_common(3)[1][0]], combo[c.most_common(3)[2][0]])
        offtwo  = min(combo[c.most_common(3)[1][0]], combo[c.most_common(3)[2][0]])
        if highest > currentmax[0]:
            currentmax = [highest, offone, offtwo]
            maxcards = cards
            #print("Assigning based on 3ok", sorted(maxcards))
        elif offone > currentmax[1]:
            currentmax = [highest, offone, offtwo]
            maxcards = cards
            #print("Assigning based on higher off", sorted(maxcards))
        elif offtwo > currentmax[2]:
            currentmax = [highest, offone, offtwo]
            maxcards = cards
            #print("Assigning based on lower off", sorted(maxcards))
    return sorted(maxcards)

#Get best two-pair hand out of multiple two-pair hands
def besttp(setsofcards):
    cardtype = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    value    = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    combo = dict(zip(cardtype, value))

    currentmax = [0, 0, 0]
    maxcards = []

    for cards in setsofcards:
        cardnums = [card[:-1] for card in cards]
        c = Counter(cardnums)
        #We know there are two pair, so we want to grab the max for the high
        #and the min for the low
        highpair = max(combo[c.most_common(2)[0][0]], combo[c.most_common(2)[1][0]])
        lowpair  = min(combo[c.most_common(2)[0][0]], combo[c.most_common(2)[1][0]])
        offcard  = combo[c.most_common(3)[2][0]]
        if highpair > currentmax[0]:
            currentmax = [highpair, lowpair, offcard]
            maxcards = cards
            continue
            #print("Assigning based on highpair", sorted(maxcards))
        elif lowpair > currentmax[1]:
            currentmax = [highpair, lowpair, offcard]
            maxcards = cards
            continue
            #print("Assigning based on lowpair", sorted(maxcards))
        elif offcard > currentmax[2]:
            currentmax = [highpair, lowpair, offcard]
            maxcards = cards
            #print("Assigning based on off", sorted(maxcards))
    return sorted(maxcards)

#Return the best one-pair hand out of multiple one-pair hands
def bestop(setsofcards):
    cardtype = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    value    = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    combo = dict(zip(cardtype, value))

    currentmaxoff = [0, 0, 0]
    maxpair = 0
    maxcards = []

    for cards in setsofcards:
        cardnums = [card[:-1] for card in cards]
        c = Counter(cardnums)

        #most commmon will be one pair
        pair = combo[c.most_common(1)[0][0]]
        #the remaining cards will be the non-pair values
        remaining = sorted([combo[val] for val in cardnums if combo[val] != pair])[::-1]
        #print("remaining", remaining)
        if pair > maxpair:
            maxpair = pair
            currentmaxoff = remaining
            maxcards = cards
        #    print("Assigning based on pair", sorted(maxcards))
            continue

        elif remaining[0] > currentmaxoff[0]:
            currentmaxoff = remaining
            maxcards = cards
        #    print("Assigning based on first off ", sorted(maxcards))
            continue

        elif remaining[1] > currentmaxoff[1]:
            currentmaxoff = remaining
            maxcards = cards
        #    print("Assigning based on second off", sorted(maxcards))
            continue

        elif remaining[2] > currentmaxoff[2]:
            currentmaxoff = remaining
            maxcards = cards
            #print("Assigning based on third off", sorted(maxcards))
    return sorted(maxcards)

#function returns the best high-card hand out of multiple hc hands
def besthc(setsofcards):
    #ace is only high
    cardtype = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    value    = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    max = [0, 0, 0, 0, 0]
    maxcards = []
    combo = dict(zip(cardtype, value))
    for cards in setsofcards:
        cardvals = sorted([combo[card[:-1]] for card in cards])[::-1] #sorted in max
        for i, val in enumerate(cardvals):
            if val > max[i]:
                max = cardvals
                maxcards = cards
                #print("Assigning, i", i, cardvals)
                break
    return sorted(maxcards)

#This function returns the category of best hand, along with the best possible hand
#It's arguments are the players hole cards and the community cards
def determinebesthand(pcards, ccards):
    playercards = pcards + ccards
    possiblehands = list(itertools.combinations(playercards, 5))
    sfhands  = []
    fokhands = []
    fhhands  = []
    flhands  = []
    sthands  = []
    tokhands = []
    tphands  = []
    ophands  = []
    hchands  = []

    sf  = False
    fok = False
    fh  = False
    fl  = False
    st  = False
    tok = False
    tp  = False
    op  = False
    hc  = False

    #sorting the hands for the best possible ones
    for hand in possiblehands:

        if isstraightflush(hand):
            sfhands.append(hand)
            sf = True
            #print("SF", hand)
        elif isfourofakind(hand):
            fokhands.append(hand)
            fok = True
            #print("4ok", hand)
        elif isfullhouse(hand):
            fhhands.append(hand)
            fh = True
            #print("FH", hand)
        elif isflush(hand):
            flhands.append(hand)
            fl = True
            #print("FL", hand)
        elif isstraight(hand):
            sthands.append(hand)
            st = True
            #print("ST", hand)
        elif isthreeofakind(hand):
            tokhands.append(hand)
            tok = True
            #print("3k", hand)
        elif istwopair(hand):
            tphands.append(hand)
            tp = True
            #print("2P", hand)
        elif isonepair(hand):
            ophands.append(hand)
            op = True
            #print("OP", hand)
        else:
            hchands.append(hand)
            #print("HC", hand)

    #now return the best possible category of handvalues, with the best hand
    if sf:
        return ["Straight-flush", bestsf(sfhands)]
    elif fok:
        return ["Four-of-a-kind", bestfok(fokhands)]
    elif fh:
        return ["Full-house", bestfh(fhhands)]
    elif fl:
        return ["Flush", bestfl(flhands)]
    elif st:
        return ["Straight", bestst(sthands)]
    elif tok:
        return ["Three-of-a-kind", besttok(tokhands)]
    elif tp:
        return ["Two-pair", besttp(tphands)]
    elif op:
        return ["One-pair", bestop(ophands)]
    else:
        return ["High-card", besthc(hchands)]

#function returns the winning player or players if a tie
#input is a hash table with keys the player number, and the values are a tuple
#of hand-type, the best cards
def determinewinningplayer(besthandinfo):
    #for pnum, result in besthandinfo.items():
    #    handtype, cards, num = result
    #    print(pnum, handtype, cards, num)

    handtypes = [x[0] for x in besthandinfo.values()]
    bestcardsofallplayers = [x[1] for x in besthandinfo.values()]
    bestoverall = []
    winningplayers = []


    if "Straight-flush" in handtypes:
        bestoverall = bestsf([x[1] for x in besthandinfo.values() if x[0] == "Straight-flush"])
        cardnums = sorted([card[:-1] for card in bestoverall])
        #print("Cardnums",cardnums,"bestoverall",bestoverall)
        #no way for hands of different suits to matter, so just grab the highest hand's players based on cardnums
        ###HEY PICK UP HERE / NEED TO CHECK CARD FACE VALUES ARE EQUAL, not sure about x[1][:-1]
        for x in besthandinfo.values():
            xhandnums = x[1]
            xhandnums = sorted([x[:-1] for x in xhandnums])
            if(cardnums == xhandnums and x[0] == "Straight-flush"):
                winningplayers.append(x[2])
        #winningplayers = [x[2] for x in besthandinfo.values() if cardnums == x[1][:-1] and x[0] == "Straight-flush"]


    elif "Four-of-a-kind" in handtypes:
        bestoverall = bestfok([x[1] for x in besthandinfo.values() if x[0] == "Four-of-a-kind"])
        #suits don't matter, so just need to match numbers (4A and KC is same as 4A and KS)
        cardnums = sorted([card[:-1] for card in bestoverall])
        #print("Cardnums",cardnums,"bestoverall",bestoverall)
        for x in besthandinfo.values():
            xhandnums = x[1]
            xhandnums = sorted([x[:-1] for x in xhandnums])
            if(cardnums == xhandnums and x[0] == "Four-of-a-kind"):
                winningplayers.append(x[2])

    elif "Full-house" in handtypes:
        bestoverall = bestfh([x[1] for x in besthandinfo.values() if x[0] == "Full-house"])
        #suits don't matter, so just need to match numbers
        cardnums = sorted([card[:-1] for card in bestoverall])
        #print("Cardnums",cardnums,"bestoverall",bestoverall)
        for x in besthandinfo.values():
            xhandnums = x[1]
            xhandnums = sorted([x[:-1] for x in xhandnums])
            if(cardnums == xhandnums and x[0] == "Full-house"):
                winningplayers.append(x[2])

    elif "Flush" in handtypes:
        bestoverall = bestfl([x[1] for x in besthandinfo.values() if x[0] == "Flush"])
        #suits don't matter--there's no preferred suit, so just need to match numbers
        #likely won't have to ignore suits in hold'em, but maybe for Omaha?
        cardnums = sorted([card[:-1] for card in bestoverall])
        #print("Cardnums",cardnums,"bestoverall",bestoverall)
        for x in besthandinfo.values():
            xhandnums = x[1]
            xhandnums = sorted([x[:-1] for x in xhandnums])
            if(cardnums == xhandnums and x[0] == "Flush"):
                winningplayers.append(x[2])

    elif "Straight" in handtypes:
        bestoverall = bestst([x[1] for x in besthandinfo.values() if x[0] == "Straight"])
        #suits don't matter, so just need to match numbers
        cardnums = sorted([card[:-1] for card in bestoverall])
        #print("Cardnums",cardnums,"bestoverall",bestoverall)
        for x in besthandinfo.values():
            xhandnums = x[1]
            xhandnums = sorted([x[:-1] for x in xhandnums])
            if(cardnums == xhandnums and x[0] == "Straight"):
                winningplayers.append(x[2])

    elif "Three-of-a-kind" in handtypes:
        bestoverall = besttok([x[1] for x in besthandinfo.values() if x[0] == "Three-of-a-kind"])
        #suits don't matter, so just need to match numbers
        cardnums = sorted([card[:-1] for card in bestoverall])
        #print("Cardnums",cardnums,"bestoverall",bestoverall)
        for x in besthandinfo.values():
            xhandnums = x[1]
            xhandnums = sorted([x[:-1] for x in xhandnums])
            if(cardnums == xhandnums and x[0] == "Three-of-a-kind"):
                winningplayers.append(x[2])

    elif "Two-pair" in handtypes:
        bestoverall = besttp([x[1] for x in besthandinfo.values() if x[0] == "Two-pair"])
        #suits don't matter, so just need to match numbers
        cardnums = sorted([card[:-1] for card in bestoverall])
        #print("Cardnums",cardnums,"bestoverall",bestoverall)
        for x in besthandinfo.values():
            xhandnums = x[1]
            xhandnums = sorted([x[:-1] for x in xhandnums])
            if(cardnums == xhandnums and x[0] == "Two-pair"):
                winningplayers.append(x[2])

    elif "One-pair" in handtypes:
        bestoverall = bestop([x[1] for x in besthandinfo.values() if x[0] == "One-pair"])
        #suits don't matter, so just need to match numbers
        cardnums = sorted([card[:-1] for card in bestoverall])
        #print("Cardnums",cardnums,"bestoverall",bestoverall)
        for x in besthandinfo.values():
            xhandnums = x[1]
            xhandnums = sorted([x[:-1] for x in xhandnums])
            if(cardnums == xhandnums and x[0] == "One-pair"):
                winningplayers.append(x[2])

    elif "High-card" in handtypes:
        bestoverall = besthc([x[1] for x in besthandinfo.values() if x[0] == "High-card"])
        #suits don't matter, so just need to match numbers
        cardnums = sorted([card[:-1] for card in bestoverall])
        #print("Cardnums",cardnums,"bestoverall",bestoverall)
        for x in besthandinfo.values():
            xhandnums = x[1]
            xhandnums = sorted([x[:-1] for x in xhandnums])
            if(cardnums == xhandnums and x[0] == "High-card"):
                winningplayers.append(x[2])

    return sorted(bestoverall), sorted(winningplayers)

def fiboseq(n):
    output = []
    output.append(0)
    if n == 1:
        return output
    a, b = 0, 1
    for i in range(n-1):
        a, b = b, a+b
        output.append(a)
    return output

def playahand(cards, numplayers):

    #file io
    f = open("log.txt", "a")

    #players is a dictionary with the player's hole cards
    players = defaultdict(list)

    #shuffle
    random.shuffle(cards)

    #deal first card
    for i in range(numplayers):
        card = cards.pop()
        #print ("Card ",card, len(cards))
        players[i].append(card)

    #deal second card
    for i in range(numplayers):
        card = cards.pop()
        #print ("Card ",card, len(cards))
        players[i].append(card)

    #Player's hole cards
    for i in range(numplayers):
        f.write("Player " + str(i) + str(players[i]) + "\n")

    #Flop
    community = [cards.pop(), cards.pop(), cards.pop()]
    f.write("flop: " +  str(community) + "\n")

    #Deal the turn
    community.append(cards.pop())
    f.write('turn: ' + str(community) + "\n")

    #Deal the river
    community.append(cards.pop())
    f.write('river: ' + str(community) + "\n")

    BestHandForPlayer = {}

    for i in range(numplayers):
        #handtype, besthand = determinebesthand(players[i], community)
        BestHandForPlayer[i] = determinebesthand(players[i], community) + [i]

    for key in BestHandForPlayer:
        f.write(str(BestHandForPlayer[key]) + "\n")

    f.close()

    return determinewinningplayer(BestHandForPlayer)


#Builds the deck
values  = "A23456789"
lvalues = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suits = "SCDH"

numplayers = 10
wincount = defaultdict(int)
ties = 0

if os.path.exists("log.txt"):
     os.remove("log.txt")
else:
    print("Log not created")

for i in range(5000):
    #This can't be the most efficient way of doing this, but popping the list screwed me

    cards = ["".join(card) for card in itertools.product(lvalues, suits)]
    winninghand, winningplayers = playahand(cards, numplayers)
    f = open("log.txt", "a")
    f.write(str(i) + " Winning players and hand "+str(winningplayers)+str(winninghand)+"\n")
    f.close()
    if len(winningplayers) > 1:
        ties += len(winningplayers) - 1
    for players in winningplayers:
        wincount[players] += 1
    print(i, winningplayers, winninghand)

totalwins = 0
for players in sorted(wincount):
    print("Player", players+1, " wins: ", wincount[players])
    totalwins += wincount[players]

print("Ties:", ties, "\nTotalwins:", totalwins, "\nTotalwins - ties:", totalwins - ties)

#print("Length:", len(cards))
#print(cards)

#startinghands = list(itertools.combinations(cards, 2))
#acehands = [aces for aces in startinghands if ("A" in aces[0]) and ("A" in aces[1])]

#print ("Ace hands", acehands)
#print ("Probability of getting pocket aces", len(acehands)/len(startinghands) * 100.0)
