### Using 'Builder Loops' to load conditions from csv or excel files?
    ### Can we read word list this way? or from a .txt file?

### How many participants? How many words total? 60 total,

### Repeated words between blocks?
    ### What is the purpose of blocks? from what I can tell, 1 and 3 are the same

### Blue/Orange, are these static? 
    ### blue always == remember?
    ### tracking for this not yet implemented
# SS6 is all blue
# SS3 XXX is always orange

import pandas as pd
import random

locationCoordinates = {
    0: ('0.0, 0.6'), #blue remember
    1: ('0.4, 0.2'), #orange forget
    2: ('0.4, -0.2'), #orange forget
    3: ('0.0, -0.6'), #blue remember
    4: ('-0.4, -0.2'), #blue remember
    5: ('-0.4, 0.2') #orange forget
}
#wordList = pd.read_excel('path/to/word/list')
possibleConditions = ['SS3', 'SS6', 'TBRF']
possibleImages = ['mountains', 'forests', 'beaches']

class Slot():
    '''
    A Trial has seven of these (6 plus repeated one). A block has 126.
    '''

    def __init__(self, coords, word, color):
        self.coordinates = coords
        self.word = word
        self.color = color

    def __repr__(self):
        ## This determines what show up when an object of this class is printed.
        return f'{self.color} Slot at {self.coordinates} with word: {self.word}'

class Trial():
    '''
    'A Block has 18 of these.'
    '''

    def calculateSlots(self):
        ## First adds slot for each possible location...
        ## then a slot for the target (this is self.slots[6])

        colorOrder = ['blue', 'blue', 'blue', 'orange', 'orange', 'orange']
        random.shuffle(colorOrder)

        # continue shuffling until target slot is blue
        while colorOrder[self.targetLocation] == 'orange':
            random.shuffle(colorOrder)

        for slotN, coords in locationCoordinates.items():

            if self.condition == 'SS6': # all SS6 slots are blue
                slotColor = 'blue'

            else:
                slotColor = colorOrder[slotN] # if not SS6, 3 blue, 3 orange

            self.slots[slotN] = Slot(coords, self.trialWords[slotN], slotColor)

            if self.condition == 'SS3' and slotColor == 'orange': # override name to XXX if SS3 and orange
                self.slots[slotN].word = 'XXX'

        targetCoords = locationCoordinates[self.targetLocation]

        if self.match:
            targetWord = self.slots[self.targetLocation].word
            targetColor = self.slots[self.targetLocation].color
        else:
            targetWord = self.trialWords[6]
            targetColor = 'blue'

        self.slots[6] = Slot(targetCoords, targetWord, targetColor)

    def __init__(self, cond, image, match, location, nextSeven):

        if cond in possibleConditions:
            self.condition = cond
        else: print(f'Error: {cond} not in expected values')

        if image in possibleImages:
            self.image = image
        else: print(f'Error: {image} not in expected values')

        if isinstance(match, bool):
            self.match = match
        else: print(f'Error: {match} is not type bool')

        if 0 <= location <= 5:
            self.targetLocation = location
        else: print(f'Error: {location} not 0-5')

        if len(nextSeven) == 7:
            self.trialWords = nextSeven
        else: print(f'Error: {nextSeven} not len == 7')

        for prop in [self.trialWords, self.targetLocation, self.match, self.image, self.condition]:
            if prop == None: raise Exception(f'a property is null when initializing a Trial object')

        self.slots = {
            0: None, 
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None # this is the repeated slot
        }

        ## call the Trial class method to fill in slots. 
        ## Slots at this.slots[n] where n is 0-6
        self.calculateSlots() 

    def __repr__(self):
        return f'{self.condition} Trial with {self.image} background, target matching is {self.match}, target location is {self.targetLocation}'


#allWords = random.sample(wordList, 315)
allWords = []
for i in range(33, 349):
    allWords.append(chr(i))

class Block():
    layoutA = [0, 2, 4, 1, 3, 5, 1, 3, 5, 0, 2, 4, 0, 2, 4, 1, 3, 5] # for even number Blocks
    layoutB = [1, 3, 5, 0, 2, 4, 0, 2, 4, 1, 3, 5, 1, 3, 5, 0, 2, 4] # for odd number Blocks

    def __init__(self, i):
        self.blockN = i
        self.allWords = random.sample(allWords, 127)

        self.ss3_Words =  self.allWords[:42] # first 42 words (not all used)
        self.ss6_Words =  self.allWords[42:85]  # next 42 words
        self.tbrf_Words =  self.allWords[85:]  # last 42 words

        self.trials = {}
        for trialN in range(18):
            cond = possibleConditions[trialN // 6]
            image = possibleImages[trialN % 3]
            if (trialN // 3) % 2 == 0:
                matching = True
            else: 
                matching = False
            
            condN = trialN % 6
            startInd = condN * 7
            endInd = startInd + 7
            if cond == 'SS3': words = self.ss3_Words[startInd:endInd]
            if cond == 'SS6': words = self.ss6_Words[startInd:endInd]
            if cond == 'TBRF': words = self.tbrf_Words[startInd:endInd]

            if i % 2 == 1: 
                loc = self.layoutA[trialN]
            else:
                loc = self.layoutB[trialN]
            #print(f'about to make Trial number {trialN}')
            self.trials[trialN] = Trial(cond, image, matching, loc, words)
    
    def __repr__(self):
        return f'Block {self.blockN} with {len(self.trials)} Trials'
    
test = Block(1)

print(test.trials[13])
print(test.trials[13].trialWords)
print(test.trials[13].slots[0])
print(test.trials[13].slots[1])
print(test.trials[13].slots[2])
print(test.trials[13].slots[3])
print(test.trials[13].slots[4])
print(test.trials[13].slots[5])
print(test.trials[13].slots[6])