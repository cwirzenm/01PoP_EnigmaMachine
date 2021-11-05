from enigma import *
import copy
import enchant

alphabet = [chr(i) for i in range(65, 91)]
dictionary = enchant.Dict("en_UK")
originalMappings = {
    'A': {
        'A': 'E',
        'B': 'J',
        'C': 'M',
        'D': 'Z',
        'E': 'A',
        'F': 'L',
        'G': 'Y',
        'H': 'X',
        'I': 'V',
        'J': 'B',
        'K': 'W',
        'L': 'F',
        'M': 'C',
        'N': 'R',
        'O': 'Q',
        'P': 'U',
        'Q': 'O',
        'R': 'N',
        'S': 'T',
        'T': 'S',
        'U': 'P',
        'V': 'I',
        'W': 'K',
        'X': 'H',
        'Y': 'G',
        'Z': 'D'
    },
    'B': {
        'A': 'Y',
        'B': 'R',
        'C': 'U',
        'D': 'H',
        'E': 'Q',
        'F': 'S',
        'G': 'L',
        'H': 'D',
        'I': 'P',
        'J': 'X',
        'K': 'N',
        'L': 'G',
        'M': 'O',
        'N': 'K',
        'O': 'M',
        'P': 'I',
        'Q': 'E',
        'R': 'B',
        'S': 'F',
        'T': 'Z',
        'U': 'C',
        'V': 'W',
        'W': 'V',
        'X': 'J',
        'Y': 'A',
        'Z': 'T'
    },
    'C': {
        'A': 'F',
        'B': 'V',
        'C': 'P',
        'D': 'J',
        'E': 'I',
        'F': 'A',
        'G': 'O',
        'H': 'Y',
        'I': 'E',
        'J': 'D',
        'K': 'R',
        'L': 'Z',
        'M': 'X',
        'N': 'W',
        'O': 'G',
        'P': 'C',
        'Q': 'T',
        'R': 'K',
        'S': 'U',
        'T': 'Q',
        'U': 'S',
        'V': 'B',
        'W': 'N',
        'X': 'M',
        'Y': 'H',
        'Z': 'L'
    }
}
x = 0

# loop through different reflectors and all the combinations
for reflector in ['A', 'B', 'C']:
    i1 = 0
    for key1 in alphabet:
        i1 += 1
        i2 = i1
        for key2 in alphabet[i1:]:
            i2 += 1
            i3 = i2
            for key3 in alphabet[i2:]:
                i3 += 1
                for key4 in alphabet[i3:]:
                    customMapping = copy.deepcopy(originalMappings[reflector])
                    customMapping[key1], customMapping[key2] = \
                        customMapping[key2], customMapping[key1]
                    customMapping[customMapping[key1]], customMapping[customMapping[key2]] = \
                        customMapping[customMapping[key2]], customMapping[customMapping[key1]]
                    customMapping[key3], customMapping[key4] = \
                        customMapping[key4], customMapping[key3]
                    customMapping[customMapping[key3]], customMapping[customMapping[key4]] = \
                        customMapping[customMapping[key4]], customMapping[customMapping[key3]]

                    enigma = Machine()

                    # creating the connections on the plugboard
                    enigma.addConnection("UG")
                    enigma.addConnection("IE")
                    enigma.addConnection("PO")
                    enigma.addConnection("NX")
                    enigma.addConnection("WT")

                    # initiating rotors from right to left
                    enigma.initRotor("IV", 7, 'L')
                    enigma.initRotor("II", 18, 'J')
                    enigma.initRotor("V", 6, 'A')

                    # initiating a reflector
                    enigma.initCustomReflector(customMapping)

                    message = enigma.encode("HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX")

                    """
                    The average word length in English, according to different papers, may vary between 4.5 and 5.1 
                     letters per word. In the solution below, we are looking for the occurrences of 6 or more 
                     letter words. Once the word has been detected, it will be displayed as a clue for a final 
                     user verification. The reason we are not doing this for 4 or 5 letter words is that there is a 
                     significantly higher chance of letters randomly aligning to create a word recognisable by a 
                     dictionary. 6 letter words are not uncommon and they are hard enough to be generated randomly to
                     make it easy for verification
                    """
                    for i in range(len(message) - 6):
                        ptr1 = 0
                        for ptr2 in range(6 + i, len(message)):
                            if dictionary.check(message[ptr1:ptr2]):
                                print(f"Detected word '{message[ptr1:ptr2]}'")
                                print(f"The encoded message might say '{message}'")
                                print(f"'{reflector}' is the base reflector and the altered wiring is: "
                                      f"'{key1}-{customMapping[key1]}', "
                                      f"'{key2}-{customMapping[key2]}', "
                                      f"'{key3}-{customMapping[key3]}', "
                                      f"'{key4}-{customMapping[key4]}'.", end='\n\n')
                            ptr1 += 1

                    x += 1
                    if x % 1000 == 0:
                        # [(26*25*24*23)/4!]*3 = 44850
                        print(f"{round(x/44850*100, 2)}% done.")
                    enigma.reset()

print(x)
