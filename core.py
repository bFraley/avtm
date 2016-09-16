# tapebox - An abstract virtual tape-based machine.
# Copyright by Brett Fraley 2016
# core.py

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

   # def call_READ(self):

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