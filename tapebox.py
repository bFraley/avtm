# tapebox.py - An abstract virtual tape-based machine.
# Copyright by Brett Fraley 2016

import sys

#----------------------------------------------------------------------
# Class definitions

class Tape:
    def __init__(self):
        self.QUE = []                # Instruction Call Que
        self.IP = 0                  # Instruction Pointer
        self.IC = 0                  # Instruction Counter
        self.ID = 1                  # Instruction Direction
        self.IZ = 0                  # Instruction Size
        self.NS = 0                  # Number of Segments
        self.SP = 0                  # Segment Pointer
        self.FP = 0                  # Frame Pointer
        self.FRAMES = []             # Frame Values
        self.NAMES = []              # Frame and Segment Names
        self.SCOPE = []              # Frame Scope (frame view range)

    def __str__(self):
        tape_report = ''

        for item in self.QUE:
            tape_report += str(item)

        tape_report += 'Instruction Pointer: '    + str(self.IP) + '\n'
        tape_report += 'Instruction Counter: '    + str(self.IC) + '\n'
        tape_report += 'Instruction Direction: '  + str(self.ID) + '\n'
        tape_report += 'Instruction Size: '       + str(self.IZ) + '\n'
        tape_report += 'Number of Segments: '     + str(self.NS) + '\n'
        tape_report += 'Segment Pointer: '        + str(self.SP) + '\n'
        tape_report += 'Frame Pointer: '          + str(self.FP) + '\n'
         
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
        self.MERGE = '.m'           # Merge (or join) two segment regions
        self.CUT = '.c'             # Cut tape segment region into two
        self.PASTE = '.p'           # Paste (or write) into a segment region
        self.INSPECT = '.i'         # Inspect (report) the machine's state
        self.CORE = Core()          # Core implementation of machine instructions
        self.SRC = []               # Source program file
        self.TAPE = Tape()          # Initial tape instance
        self.LOOKUP = []            # Initial lookup table instance
        self.PROMPT = 'frame '      # Prompt text provides frame and segment info
        self.RUN = True             # Machine run state

        # IMPORTANT! Initialize each TAPE.FRAME value at zero.

        for frame in range(cap):
            self.TAPE.FRAMES.append(0);

#----------------------------------------------------------------------            
# Utility Functions

    # Load a source file from argv

    def loadfile(self):
        # Only accepts a single file for now.
        file = open(sys.argv[1])
        src = file.read()
        lines = src.split('\n')
        file.close()

        return {sys.argv[1]: lines}

    # Check if word is Alphanumeric, and can't start with a digit.
    def lex_namespace(self, word):
        if word.isalnum():
            if word[0].isdigit():
                print('NAME ERROR: name begins with digit')
                exit(0)
            else:
                return True
        else:
            return False

#----------------------------------------------------------------------
# Runtime
    
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

                # Get repl input, assign PROMPT information.
                # User input gets assigned to the 'command' variable.

                self.SRC.append(input(self.PROMPT + str(self.TAPE.FP) + ' :'))
                command = self.SRC[len(self.SRC)-1]
                
                # Exit on input of 'q'

                if command == 'q':
                    print('exiting...')
                    exit(0)
                
                # Call program_step, provides 'command' as argument.
                
                else:
                    self.program_step(command)

#----------------------------------------------------------------------
# Interpretter implementation

    def program_step(self, line):
        i = 0
        
        # Amount to skip ahead (i) in line
        skip = 0 

        line = line.split(' ')
        line_length = len(line)

        while i < len(line):
                
            # INC increment tape ( + )

            if line[i] == self.INC:

                if self.TAPE.FP == self.CAP:
                    print('ERROR: Frame Pointer reached Tape Capacity')
                else:
                    self.TAPE.FP += 1
            
            # DEC decrement tape ( - )

            elif line[i] == self.DEC:
                if self.TAPE.FP == 0:
                    print('ERROR: Frame Pointer at 0, cannot Decrement!')
                else:
                    self.TAPE.FP -= 1

            # WRITE to current Frame Pointer ( .w value )
            # NOTE: Anything after .w on the same line is
            # written to the current frame. Need to look ahead of
            # the write value for a pipe delimiter which allows for 
            # additional instructions to be on the same line as a ( .w )            

            elif line[i] == self.WRITE:
                if line_length > 1:
                    value = ' '.join(line[1:])
                    self.TAPE.FRAMES[self.TAPE.FP] = value
                else:
                    print('WARNING: Missing a value to write after ( .w )')
 
            # READ a frame's value ( .r )  
            # Read from current Frame Pointer, or specified index
            # Usage: .r [blank] or .r [index]

            elif line[i] == self.READ:
                if line_length > 1:

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
            
            # SEGMENT instruction ( .s )
            # Create a new named segment, or un-named segment.
            # Usage: .s .n [mysegment], or just the ( .s ) command.
 
            elif line[i] == self.SEGMENT:

                # Increment number of segments counter.
                self.TAPE.NS += 1
                
                if line_length > 1:

                    # Is there a .n name command present?
                    if line[i+1] == self.NAME:

                        # Peeked ahead of (i) in command, skip ahead on next loop.
                        skip += 1

                        # If there is a name for the segment supplied, append the
                        # {segment name: frame index of segment's first frame}
                        # to TAPE.NAMES and LOOKUP
                        
                        if line_length  > 2:
                            
                            # Peek ahead again, skip on next loop.
                            skip += 1

                            self.TAPE.NAMES.append({ line[i+2]: self.TAPE.FP })
                            self.LOOKUP.append(self.TAPE.NAMES[-1])

                        # Error if no name was provided after the .n command.
                        else:
                            print('ERROR: Segment (.s .n name) missing name')

                # A name command to name the new segment wasn't given.
                # Add unnamed segment to LOOKUP, start segment at Frame Pointer.
                else:
                    self.LOOKUP.append({ "(S)":(self.TAPE.NS, self.TAPE.FP) })

                print(self.LOOKUP[-1])     

                
            # NAME instruction ( .n )
            # Name a frame location
            elif line[i] == self.NAME:
                if line_length > 1:
                    tryname = line[i+1]

                    # Is this namespace already defined?
                    # Is the input a valid name?
                    
                    #if self.TAPE.NAMES[tryname]:TRY ME
                    #    print('ERROR: Cannot assign this name. Already in use')
                    
                    if self.lex_namespace(line[i+1]):
                        self.TAPE.NAMES.append({ line[i+1]:self.TAPE.FP })
                        self.LOOKUP.append(self.TAPE.NAMES[-1])
                else:
                    print('Expected name after ( .n ) is missing')


            elif line[i] == self.DELETE:
                print('Delete')
            elif line[i] == self.MERGE:
                print('Merge')
            elif line[i] == self.CUT:
                print('Cut')
            elif line[i] == self.PASTE:
                print('Paste')

            # Print tape report on INSPECT command.

            elif line[i] == self.INSPECT:
                print(self.TAPE)

            # Increment instruction counter.
            self.TAPE.IC += 1

            # Skip (i) ahead for next loop.
            i += 1 + skip
    
    # Program execute is called on program source files
    # and feeds each line of code to program_step.

    def program_execute(self, program):
        for line in program:
            self.program_step(line)

#--------------------------------------------------------------------
# Core 

class Core():
    def __init__(self):
        self.opchars = ['+','-','*','/']

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

#----------------------------------------------------------------------
# For development purposes.
# A machine and tape runtime start up when this file is loaded or imported.

# Initialize and run the machine.
M = Machine(200)
M.run()

