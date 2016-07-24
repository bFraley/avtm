# tapebox.py - An abstract virtual tape-based machine.
# Copyright by Brett Fraley 2016

import sys

class Tape:
    def __init__(self):
        self.QUE = []                # Instruction Call Que
        self.IP = 0                  # Instruction Pointer
        self.IC = 0                  # Instruction Counter
        self.ID = 1                  # Instruction Direction
        self.IZ = 0                  # Instruction Size
        self.NS = 1                  # Number of Segments
        self.SP = 1                  # Segment Pointer
        self.FP = 0                  # Frame Pointer
        self.FRAMES = []             # Frame Values
        self.NAMES = []              # Frame and Segment Names
        self.SCOPE = []              # Frame Scope (frame view range)

    def __str__(self):
        tape_report = ''

        for item in self.QUE:
            tape_report += str(item)

        tape_report += 'Instruction Pointer: ' + str(self.IP) + '\n'
        tape_report += 'Instruction Counter: ' + str(self.IC) + '\n'
        tape_report += 'Instruction Direction:'+ str(self.ID) + '\n'
        tape_report += 'Instruction Size: '    + str(self.IZ) + '\n'
        tape_report += 'Number of Segments: '  + str(self.NS) + '\n'
        tape_report += 'Segment Pointer: '     + str(self.SP) + '\n'
        tape_report += 'Frame Pointer: '       + str(self.FP) + '\n'
         
        tape_report += '\nFrames: '
        for item in self.FRAMES:
            tape_report += ' | ' + str(item)
        
        tape_report += '\nNames: '
        for item in self.NAMES:
            tape_report += ' | ' + str(item)

        tape_report += '\nScope: '
        for item in self.SCOPE:
            tape_report += ' | ' + str(item)

        return tape_report

class Machine:
    def __init__(self, cap):
        self.CAP = cap              # Capacity length of tape
        self.AUTO = '*'             # Specify to auto an instruction
        self.INC = '+'              # Increment tape
        self.DEC = '-'              # Decrement tape
        self.WRITE = '.w'           # Write tape frame 
        self.READ = '.r'            # Read tape frame
        self.SEGMENT = '.s'         # Segment a tape into a region
        self.NAME = '.n'            # Name a tape segment region
        self.DELETE = '.d'          # Delete a tape segment region
        self.MERGE = '.a'           # Merge (or join) two segment regions
        self.CUT = '.c'             # Cut tape segment region into two
        self.PASTE = '.p'           # Paste (or write) into a segment region
        self.SRC = []               # Source program file
        self.TAPE = Tape()          # Initial tape instance
        self.LOOKUP = []            # Initial lookup table instance
        self.SWITCH = 0             # Switch for switching tapes
        self.RUN = True             # Machine run state

        # IMPORTANT! Initialize each TAPE.FRAME value at zero.

        for frame in range(cap):
            self.TAPE.FRAMES.append(0);
            

    # Load a source file from argv

    def loadfile(self):
        # Only accepts a single file for now.
        file = open(sys.argv[1])
        src = file.read()
        lines = src.split('\n')
        file.close()

        return {sys.argv[1]: lines}
    
    # Machine.run initializes a tape and program runtime.
    # It either loads a program from file, or starts a repl instance.
    def run(self):

        # A program source file was provided.
        if len(sys.argv) > 1:
            self.SRC.append(self.loadfile())
            self.program_execute(self.SRC[0][sys.argv[1]])

        # No source file provided, run repl interpretter.
        else:
            while self.RUN:
                self.SRC.append(input('][ '))
                command = self.SRC[len(self.SRC)-1]

                if command == 'q':
                    print('exiting...')
                    exit(0)
                else:
                    self.program_step(command)
                    print(self.TAPE.FP)  


    # Interpretter implementation.

    def program_step(self, line):
        
        line = line.split(' ')

        for i in range(len(line)):
                
            if line[i] == self.INC:
                # self.TAPE.move(1)
                if self.TAPE.FP == self.CAP:
                    print('ERROR: Frame Pointer reached Tape Capacity')
                else:
                    self.TAPE.FP += 1

            elif line[i] == self.DEC:
                if self.TAPE.FP == 0:
                    print('ERROR: Frame Pointer at 0, cannot Decrement!')
                else:
                    self.TAPE.FP -= 1

            # Write to current Frame Pointer ( .w value )

            elif line[i] == self.WRITE:
                self.TAPE.FRAMES[self.TAPE.FP] = line[i+1]
 
            # Read from current Frame Pointer
            # Usage: .r [blank] or .r [index]
            elif line[i] == self.READ:
                if len(line) > 1:

                    frameindex = int(line[i+1])

                    if frameindex == len(self.TAPE.FRAMES):
                        print('ERROR: Read above frame index range')
                        exit(0)

                    elif frameindex < 0:
                        print('ERROR: Read below frame index range')
                        exit(0)

                    else:
                        print(self.TAPE.FRAMES[int(line[i+1])])
                else:
                    print(self.TAPE.FRAMES[self.TAPE.FP])
            
            elif line[i] == '.i':
                print(self.TAPE)

            elif line[i] == self.SEGMENT:
                print('Segment')
            elif line[i] == self.NAME:
                print('Name')
            elif line[i] == self.DELETE:
                print('Delete')
            elif line[i] == self.MERGE:
                print('Merge')
            elif line[i] == self.CUT:
                print('Cut')
            elif line[i] == self.PASTE:
                print('Paste')

            # Increment instruction counter
            self.TAPE.IC += 1
                
    def program_execute(self, program):
        for line in program:
            self.program_step(line)

# Initialize and run the machine.
M = Machine(200)
M.run()
