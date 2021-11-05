from enigma import *
import enchant

decodedMessages = {}

for reflector_setting in ["A", "B", "C"]:
    enigma = Machine()

    # creating the connections on the plugboard
    enigma.addConnection("KI")
    enigma.addConnection("XN")
    enigma.addConnection("FL")

    # initiating rotors from right to left
    enigma.initRotor("V", 14, 'M')
    enigma.initRotor("Gamma", 2, 'J')
    enigma.initRotor("Beta", 4, 'M')

    # initiating a reflector
    enigma.initReflector(reflector_setting)

    decodedMessages[reflector_setting] = enigma.encode("DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ")

    enigma.reset()

dictionary = enchant.Dict("en_UK")
for setting in decodedMessages:
    for char in range(3, len(decodedMessages[setting])):
        if dictionary.check(decodedMessages[setting][:char]):
            print(f"Detected word '{decodedMessages[setting][:char]}'")
            print(f"The encoded message might say {decodedMessages[setting]}")
            print(f"The reflector setting for this message is: {setting}.", end='\n\n')
