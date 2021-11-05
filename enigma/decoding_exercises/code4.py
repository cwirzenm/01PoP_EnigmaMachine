from enigma import *
import copy

plugs = ['D', 'E', 'K', 'L', 'M', 'O', 'Q', 'T', 'U', 'X', 'Y', 'Z']

for conn1 in plugs:
    plugsNoPlug1 = copy.deepcopy(plugs)
    plugsNoPlug1.remove(conn1)
    for conn2 in plugsNoPlug1:

        lead1 = f"A{conn1}"
        lead2 = f"I{conn2}"
        enigma = Machine()

        # creating the connections on the plugboard
        enigma.addConnection("WP")
        enigma.addConnection("RJ")
        enigma.addConnection("VF")
        enigma.addConnection("HN")
        enigma.addConnection("CG")
        enigma.addConnection("BS")
        enigma.addConnection(lead1)
        enigma.addConnection(lead2)

        # initiating rotors from right to left
        enigma.initRotor("IV", 10, 'U')
        enigma.initRotor("III", 12, 'W')
        enigma.initRotor("V", 24, 'S')

        # initiating a reflector
        enigma.initReflector('A')

        message = enigma.encode("SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW")

        if "TUTOR" in message:
            print(f"The encoded message might say {message}")
            print(f"The missing plugboard connections are: {lead1}, {lead2}.", end='\n\n')

        enigma.reset()
