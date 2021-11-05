from enigma import *
import copy

ring_settings = [2, 4, 6, 8, 20, 22, 24, 26]
rotors = ["II", "IV", "Beta", "Gamma"]
reflectors = ["A", "B", "C"]

for rotor1 in rotors:
    rotorsNoRotor1 = copy.deepcopy(rotors)
    rotorsNoRotor1.remove(rotor1)
    for rotor2 in rotorsNoRotor1:
        rotorsNoRotor2 = copy.deepcopy(rotorsNoRotor1)
        rotorsNoRotor2.remove(rotor2)
        for rotor3 in rotorsNoRotor2:
            for reflector in reflectors:
                for ring1 in ring_settings:
                    for ring2 in ring_settings:
                        for ring3 in ring_settings:

                            settings = str([rotor1, rotor2, rotor3, reflector, ring1, ring2, ring3])
                            enigma = Machine()

                            # creating the connections on the plugboard
                            enigma.addConnection("FH")
                            enigma.addConnection("TS")
                            enigma.addConnection("BE")
                            enigma.addConnection("UQ")
                            enigma.addConnection("KD")
                            enigma.addConnection("AL")

                            # initiating rotors from right to left
                            enigma.initRotor(rotor3, ring3, 'Y')
                            enigma.initRotor(rotor2, ring2, 'M')
                            enigma.initRotor(rotor1, ring1, 'E')

                            # initiating a reflector
                            enigma.initReflector(reflector)

                            message = enigma.encode("ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY")

                            if "THOUSANDS" in message:
                                print(f"Detected word 'THOUSANDS'.")
                                print(f"The encoded message might say {message}.")
                                print(f"The starting positions of this message are: {settings}.", end='\n\n')

                            enigma.reset()
