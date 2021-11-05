from enigmaErrors import *

alphabet = [chr(i) for i in range(65, 91)]


class _Plug:
    __plug = None
    _isWired = False

    def __init__(self, letter):
        self.__plug = letter

    def __str__(self):
        return f"{self.__plug}"

    def resetPlug(self):
        self.__plug = None
        self._isWired = False


class _PlugLead:
    __plugIn = None
    __plugOut = None

    def __init__(self, mapping):
        self.__plugIn = mapping[0]
        self.__plugOut = mapping[1]

    def _encodePlugLead(self):
        return self.__plugOut

    def __str__(self):
        return f"{self.__plugIn}{self.__plugOut}"

    def resetPlugLead(self):
        self.__plugIn = None
        self.__plugOut = None


class _PlugBoard:
    __plugLeadMappingCeil = 20
    __plugs = {}
    __plugLeadMapping = {}

    def __init__(self):
        for letter in alphabet:
            self.__plugs[letter] = _Plug(letter)

    def _encodePlugBoard(self, input_char):
        return self.__plugLeadMapping[input_char]._encodePlugLead() \
            if self.__plugs[input_char]._isWired else input_char

    def addConnection(self, connection):
        # Check if the input is a str, has two letters and if plugBoard isn't full
        if isinstance(connection, str) and len(connection) == 2 and \
                len(self.__plugLeadMapping) < _PlugBoard.__plugLeadMappingCeil:

            # Check if the inputs are letters
            if (65 <= ord(connection[0]) < 92 or 97 <= ord(connection[0]) < 123) and \
                    (65 <= ord(connection[1]) < 92 or 97 <= ord(connection[1]) < 123):

                # Check for invalid connections, e.g. AA, BB, CC, etc.
                if not connection[0] is connection[1]:

                    # Check if the plugs aren't already wired up
                    if not (self.__plugs[connection[0]]._isWired or self.__plugs[connection[1]]._isWired):

                        connection = connection.upper()
                        self.__plugLeadMapping[connection[0]] = _PlugLead(connection)
                        self.__plugs[connection[0]]._isWired = True
                        self.__plugLeadMapping[connection[1]] = _PlugLead(connection[::-1])
                        self.__plugs[connection[1]]._isWired = True

                    else:
                        raise PlugIsWiredError(f"Cannot connect a plug that is already wired.")
                else:
                    raise PlugError(f"Cannot connect a plug to itself!")
            else:
                raise ParameterNotCharError(f"Parameter {connection} cannot be converted to char.")
        else:
            if not isinstance(connection, str):
                raise ParameterTypeError(f"Input is a {type(connection)} instead being of <class 'str'>.")
            elif len(self.__plugLeadMapping) >= _PlugBoard.__plugLeadMappingCeil:
                raise PlugBoardFullError(f"PlugBoard is full")
            elif len(connection) != 2:
                raise ParameterOutOfBoundsError(f"Input is of length {len(connection)} instead of being of length '2'.")
            else:
                raise NotImplementedError("Unknown Error.")

    def resetPlugBoard(self):
        for plug in list(self.__plugs):
            self.__plugs[plug].resetPlug()
            self.__plugs.pop(plug)
        self.__plugs = {}
        for plug in list(self.__plugLeadMapping):
            self.__plugLeadMapping[plug].resetPlugLead()
            self.__plugLeadMapping.pop(plug)
        self.__plugLeadMapping = {}


class _Reflector:
    __mapping = None
    __customMap = None

    # hardcoded mappings
    __mappings = {
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

    def __init__(self, mapping):
        self.__mapping = mapping

    def __str__(self):
        return f"{self.__mapping}"

    def _encodeReflector(self, input_char):
        if self.__mapping is not "Custom":
            return self.__mappings[self.__mapping][input_char]  # lookup the map and return the value
        else:
            return self.__customMap[input_char]

    def _initCustomReflector(self, mapping):
        self.__mapping = 'Custom'
        self.__customMap = mapping

    def resetReflector(self):
        self.__mapping = None
        self.__customMap = None


class Rotor:
    __mapping = None
    __setting = None
    __position = None
    __offset = 0

    # hardcoded mappings and notches
    __mappings = {
        'Beta': {
            'A': 'L',
            'B': 'E',
            'C': 'Y',
            'D': 'J',
            'E': 'V',
            'F': 'C',
            'G': 'N',
            'H': 'I',
            'I': 'X',
            'J': 'W',
            'K': 'P',
            'L': 'B',
            'M': 'Q',
            'N': 'M',
            'O': 'D',
            'P': 'R',
            'Q': 'T',
            'R': 'A',
            'S': 'K',
            'T': 'Z',
            'U': 'G',
            'V': 'F',
            'W': 'U',
            'X': 'H',
            'Y': 'O',
            'Z': 'S'
        },
        'Gamma': {
            'A': 'F',
            'B': 'S',
            'C': 'O',
            'D': 'K',
            'E': 'A',
            'F': 'N',
            'G': 'U',
            'H': 'E',
            'I': 'R',
            'J': 'H',
            'K': 'M',
            'L': 'B',
            'M': 'T',
            'N': 'I',
            'O': 'Y',
            'P': 'C',
            'Q': 'W',
            'R': 'L',
            'S': 'Q',
            'T': 'P',
            'U': 'Z',
            'V': 'X',
            'W': 'V',
            'X': 'G',
            'Y': 'J',
            'Z': 'D'
        },
        'I': {
            'A': 'E',
            'B': 'K',
            'C': 'M',
            'D': 'F',
            'E': 'L',
            'F': 'G',
            'G': 'D',
            'H': 'Q',
            'I': 'V',
            'J': 'Z',
            'K': 'N',
            'L': 'T',
            'M': 'O',
            'N': 'W',
            'O': 'Y',
            'P': 'H',
            'Q': 'X',
            'R': 'U',
            'S': 'S',
            'T': 'P',
            'U': 'A',
            'V': 'I',
            'W': 'B',
            'X': 'R',
            'Y': 'C',
            'Z': 'J'
        },
        'II': {
            'A': 'A',
            'B': 'J',
            'C': 'D',
            'D': 'K',
            'E': 'S',
            'F': 'I',
            'G': 'R',
            'H': 'U',
            'I': 'X',
            'J': 'B',
            'K': 'L',
            'L': 'H',
            'M': 'W',
            'N': 'T',
            'O': 'M',
            'P': 'C',
            'Q': 'Q',
            'R': 'G',
            'S': 'Z',
            'T': 'N',
            'U': 'P',
            'V': 'Y',
            'W': 'F',
            'X': 'V',
            'Y': 'O',
            'Z': 'E'
        },
        'III': {
            'A': 'B',
            'B': 'D',
            'C': 'F',
            'D': 'H',
            'E': 'J',
            'F': 'L',
            'G': 'C',
            'H': 'P',
            'I': 'R',
            'J': 'T',
            'K': 'X',
            'L': 'V',
            'M': 'Z',
            'N': 'N',
            'O': 'Y',
            'P': 'E',
            'Q': 'I',
            'R': 'W',
            'S': 'G',
            'T': 'A',
            'U': 'K',
            'V': 'M',
            'W': 'U',
            'X': 'S',
            'Y': 'Q',
            'Z': 'O'
        },
        'IV': {
            'A': 'E',
            'B': 'S',
            'C': 'O',
            'D': 'V',
            'E': 'P',
            'F': 'Z',
            'G': 'J',
            'H': 'A',
            'I': 'Y',
            'J': 'Q',
            'K': 'U',
            'L': 'I',
            'M': 'R',
            'N': 'H',
            'O': 'X',
            'P': 'L',
            'Q': 'N',
            'R': 'F',
            'S': 'T',
            'T': 'G',
            'U': 'K',
            'V': 'D',
            'W': 'C',
            'X': 'M',
            'Y': 'W',
            'Z': 'B'
        },
        'V': {
            'A': 'V',
            'B': 'Z',
            'C': 'B',
            'D': 'R',
            'E': 'G',
            'F': 'I',
            'G': 'T',
            'H': 'Y',
            'I': 'U',
            'J': 'P',
            'K': 'S',
            'L': 'D',
            'M': 'N',
            'N': 'H',
            'O': 'L',
            'P': 'X',
            'Q': 'A',
            'R': 'W',
            'S': 'M',
            'T': 'J',
            'U': 'Q',
            'V': 'O',
            'W': 'F',
            'X': 'E',
            'Y': 'C',
            'Z': 'K'
        }
    }
    __notches = {
        'Beta': None,
        'Gamma': None,
        'I': 'Q',
        'II': 'E',
        'III': 'V',
        'IV': 'J',
        'V': 'Z'
    }

    def __init__(self, mapping, setting, position):
        self.__mapping = mapping
        self.__setting = setting
        self.__position = position
        self.__offset = alphabet.index(position) + 1 - setting

    def __str__(self):
        return f"{self.__mapping} {self.__setting} {self.__position}"

    def __calculateOffset(self, input_char):
        convertChar = alphabet[(alphabet.index(input_char) - self.__offset) % 26]
        # print(f"{input_char} converts to {convertChar} at offset {self.__offset}")
        return convertChar

    def _rotate(self):
        self.__position = alphabet[alphabet.index(self.__position) + 1] if not self.__position == 'Z' else 'A'
        self.__offset += 1

    def _isSetToNotch(self):
        return self.__position == self.__notches[self.__mapping]

    def encodeRotor(self, input_char):
        receivedChar = alphabet[(alphabet.index(input_char) + self.__offset) % 26]
        # print(f"{input_char} converts to {receivedChar} at offset {self.__offset}."
        #       f"{self} rotor in - "
        #       f"Received signal: {receivedChar}, "
        #       f"Connects to: {self.__mappings[self.__mapping][receivedChar]}")
        return self.__calculateOffset(self.__mappings[self.__mapping][receivedChar])

    def encodeRotor_rev(self, input_char):
        receivedChar = alphabet[(alphabet.index(input_char) + self.__offset) % 26]
        # print(f"{input_char} converts to {receivedChar} at offset {self.__offset}")
        for key in self.__mappings[self.__mapping].keys():
            if self.__mappings[self.__mapping][key] == receivedChar:
                # print(f"{self} rotor out - "
                #       f"Received signal: {receivedChar}, "
                #       f"Connects to: {alphabet[(alphabet.index(key) - self.__offset) % 26]}")
                return self.__calculateOffset(alphabet[alphabet.index(key)])

    def resetRotor(self):
        self.__mapping = None
        self.__setting = None
        self.__position = None
        self.__offset = 0


class _RotorBoard:
    __rotorCounter = 0
    __rotors = []
    __reflector = None
    __isReflectorCustom = False
    __validIDs = {'rotors': ['Beta', 'Gamma', 'I', 'II', 'III', 'IV', 'V'],
                  'reflectors': ['A', 'B', 'C']}

    def __init__(self):
        pass

    def _encodeRotorBoard(self, input_char):
        # rotation mechanics
        if self.__rotors[1]._isSetToNotch():
            self.__rotors[1]._rotate()
            self.__rotors[2]._rotate()
        elif self.__rotors[0]._isSetToNotch():
            self.__rotors[1]._rotate()
        self.__rotors[0]._rotate()  # right-most rotation

        # print(f"{input_char} signal comes in")
        # rotor encoding
        output_char = input_char
        for rotor in self.__rotors:
            output_char = rotor.encodeRotor(output_char)

        # reflector encoding
        # print(f"{self.__reflector} reflector - "
        #       f"Received signal: {output_char}, "
        #       f"Connects to: {self.__reflector._encodeReflector(output_char)}")
        output_char = self.__reflector._encodeReflector(output_char)

        # reversed rotor encoding
        for rotor in self.__rotors[::-1]:
            output_char = rotor.encodeRotor_rev(output_char)

        # print(f"{output_char} signal comes out")
        return output_char

    def initRotor(self, rotor_id, rotor_setting, rotor_position):
        # check if you can fit more rotors
        if self.__rotorCounter >= 4:
            raise ObjectOverflowError(f"You can't fit more than four rotors inside the machine.")

        # validate the rotor ID
        if rotor_id not in self.__validIDs['rotors']:
            raise InvalidObjectIDError(f"Rotor ID invalid.")

        # validate the rotor setting
        if not (isinstance(rotor_setting, int) or 1 <= rotor_setting <= 26):
            raise ValueError(f"Rotor setting must be represented by an integer between 1 and 26.")

        # validate the rotor position
        if rotor_position.upper() not in alphabet or len(rotor_position) != 1:
            raise ParameterNotCharError(f"Rotor setting must be represented by a single letter.")

        # initiate the rotor
        self.__rotorCounter += 1
        self.__rotors.append(Rotor(rotor_id, rotor_setting, rotor_position.upper()))

    def initReflector(self, reflector_id):
        # check if the reflector is not initiated
        if self.__reflector is not None:
            raise ObjectOverflowError(f"You can't fit more than one reflector inside the machine.")

        # validate the reflector ID
        if reflector_id.upper() not in self.__validIDs['reflectors']:
            raise InvalidObjectIDError(f"Reflector ID invalid.")

        # initiate the reflector
        self.__reflector = _Reflector(reflector_id.upper())
        self.__isReflectorCustom = False

    def initCustomReflector(self, mapping):
        # check if the reflector is not initiated
        if self.__reflector is not None:
            raise ObjectOverflowError(f"You can't fit more than one reflector inside the machine.")

        self.__isReflectorCustom = True
        self.__reflector = _Reflector("Custom")
        self.__reflector._initCustomReflector(mapping)

    def resetRotorBoard(self):
        self.__reflector.resetReflector()
        self.__reflector = None
        self.__rotorCounter = 0
        self.__isReflectorCustom = False
        for rotor in self.__rotors[::-1]:
            rotor.resetRotor()
            self.__rotors.pop()
        self.__rotors = []


class Machine(_PlugBoard, _RotorBoard):
    def __init__(self):
        super().__init__()

    def encode(self, input_string):
        encodedMessage = []
        for char in input_string:
            if (65 <= ord(char) < 92 or 97 <= ord(char) < 123) and \
                    (65 <= ord(char) < 92 or 97 <= ord(char) < 123):

                # todo check if the machine has all needed components

                char = Machine._encodePlugBoard(self, char.upper())  # plugboard encoding

                char = Machine._encodeRotorBoard(self, char)  # rotorboard encoding

                char = Machine._encodePlugBoard(self, char)  # plugboard encoding

                encodedMessage.append(char)
            else:
                raise ParameterNotCharError(f"Parameter {char} cannot be encoded")
        return ''.join(encodedMessage)

    def reset(self):
        Machine.resetRotorBoard(self)
        Machine.resetPlugBoard(self)


if __name__ == "__main__":
    # initiating a machine class
    enigma = Machine()

    # creating the connections on the plugboard
    enigma.addConnection("AB")
    enigma.addConnection("CD")
    enigma.addConnection("EF")
    enigma.addConnection("GH")
    enigma.addConnection("IJ")
    enigma.addConnection("KL")
    enigma.addConnection("MN")
    enigma.addConnection("OP")
    enigma.addConnection("RS")
    enigma.addConnection("TU")

    # initiating rotors from right to left
    enigma.initRotor("III", 15, 'F')
    enigma.initRotor("IV", 18, 'H')
    enigma.initRotor("V", 3, 'C')
    enigma.initRotor("I", 24, 'Z')

    # initiating a reflector
    enigma.initReflector("C")

    print(enigma.encode("XVDRUCPOJWDTGWTETXMELPGMAHWBPWYCKJMYMMFSUIYDICTCMEBGDVIAQZLXOANXNNKKMDNWEPMMKOLDTXHITJLMGZW"))

    enigma.reset()

    enigma = Machine()

    enigma.initRotor("III", 1, 'A')
    enigma.initRotor("II", 1, 'A')
    enigma.initRotor("I", 1, 'A')
    enigma.initReflector("B")

    print(enigma.encode("A") == "B")
