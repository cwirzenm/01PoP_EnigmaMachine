from enigma import *

alphabet = [chr(i) for i in range(65, 91)]
decodedMessages = {}

for position1_setting in alphabet:
    for position2_setting in alphabet:
        for position3_setting in alphabet:
            settings = [position1_setting, position2_setting, position3_setting]
            enigma = Machine()

            # creating the connections on the plugboard
            enigma.addConnection("VH")
            enigma.addConnection("PT")
            enigma.addConnection("ZG")
            enigma.addConnection("BJ")
            enigma.addConnection("EY")
            enigma.addConnection("FS")

            # initiating rotors from right to left
            enigma.initRotor("III", 10, position3_setting)
            enigma.initRotor("I", 2, position2_setting)
            enigma.initRotor("Beta", 23, position1_setting)

            # initiating a reflector
            enigma.initReflector("B")

            decodedMessages[str(settings)] = enigma.encode("CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH")

            enigma.reset()

for setting in decodedMessages:
    if "UNIVERSITY" in decodedMessages[setting]:
        print(f"Detected word 'UNIVERSITY'.")
        print(f"The encoded message might say {decodedMessages[setting]}.")
        print(f"The starting positions of this message are: {setting}.", end='\n\n')
