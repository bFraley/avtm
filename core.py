# tapebox - An abstract virtual tape-based machine.
# Copyright by Brett Fraley 2016
# core.py

from lib import lex_namespace, lookup_by_name, try_lookup
from tape import Tape

class Core():
    def __init__(self):
        self.instructions = ['+','-','.w','.r','.n','.s','.d','.m','.c','.p']
        self.opchars = ['+','-','*','/']
        self.TAPE = Tape()

    def call_open_file(self, filename, mode, label_name):
         filestream = open(filename, mode)
         contents = filestream.read()
         filestream.close()
         return contents

    def call_INC(self):
        if self.TAPE.FP == self.TAPE.SIZE:
            print('ERROR: Frame Pointer reached Tape Capacity')
        else:
            self.TAPE.FP += 1

    def call_DEC(self):
        if self.TAPE.FP == 0:
            print('ERROR: Frame Pointer at 0, cannot Decrement!')
        else:
            self.TAPE.FP -= 1
   
    def call_WRITE(self, line):
        value = ' '.join(line[1:])
        self.TAPE.FRAMES[self.TAPE.FP] = value

    def call_READ(self, read_argument):
        
        # Read a frame's value via frame index number.
        if read_argument.isdigit():
            read_argument = int(read_argument)
        
            if read_argument >= len(self.TAPE.FRAMES):
                print('ERROR: Read above frame index range')
                exit(0)

            elif read_argument < 0:
                print('ERROR: Read below frame index range')
                exit(0)

            else:
                value = self.TAPE.FRAMES[read_argument]
                print(value)
                return value

        # Read a frame's value via namespace identifier.
        elif lex_namespace(read_argument):
            print(read_argument)
             
            if try_lookup(read_argument, self.TAPE.NAMES):
                frameindex = lookup_by_name(read_argument, self.TAPE.lookup)
                value = self.TAPE.FRAMES[frameindex]
                print(value)
                return value
            else:
                print('Cannot read name from tape, unrecognized name')

   # def call_DELETE(self):

   # def call_MERGE(self):

   # def call_CUT(self):

   # def call_PASTE(self):


    def add(self, left, right):
        return left + right

    def sub(self, left, right):
        return left - right

    def mul(self, left, right):
        return left * right

    def div(self, left, right):
        return left / right

    def mod(self, left, right):
        return left % right

    def exp(self, expression):
        return expression