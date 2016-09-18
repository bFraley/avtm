# tapebox - An abstract virtual tape-based machine.
# Copyright by Brett Fraley 2016
# machine.py

import sys

from lib import lex_namespace, lookup_by_name, try_lookup
from core import Core

class Machine:
    def __init__(self, tapesize):
        self.SRC = []               # Source program file
        self.LOOKUP = []            # Initial lookup table instance
        self.CORE = Core()          # Initial machine Core instance
        self.TAPE = self.CORE.TAPE  # Initial Tape instance
        self.TAPE.SIZE = tapesize   # Tape size is number of frames on tape.
        self.TAPE.lookup = self.LOOKUP
        self.RUN = True             # Machine run state

        # Initialize each TAPE.FRAME value at zero.
        for frame in range(self.TAPE.SIZE):
            self.TAPE.FRAMES.append(0);

            
#----------------------------------------------------------------------
# Runtime
    
    # Machine.run initializes a tape and program runtime.
    # It either loads a program from file, or starts a repl instance.

    def run(self):

        # A program source file was provided.
        if len(sys.argv) > 1:
            self.SRC.append(self.load_tape_file())
            self.program_execute(self.SRC[0][sys.argv[1]])

        # No source file provided, run repl interpretter.
        else:
            while self.RUN:

                # Get repl input, assign PROMPT information.
                # User input gets assigned to the 'command' variable.

                self.SRC.append(input('frame ' + str(self.TAPE.FP) + ' :'))
                command = self.SRC[len(self.SRC)-1]
                
                # Exit on input of 'q'

                if command is 'q':
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

        while i < line_length:
                
            # INC increment tape ( + )

            if line[i] is self.CORE.instructions[0]:
                self.CORE.call_INC()

            # DEC decrement tape ( - )

            elif line[i] is self.CORE.instructions[1]:
                self.CORE.call_DEC()            

            # WRITE to current frame ( .w )            

            elif line[i] == self.CORE.instructions[2]:
                if line_length > 1:
                    self.CORE.call_WRITE(line)
                else:
                    print('WARNING: Missing a value to write after ( .w )')
 
            # READ a frame's value ( .r )  
            # Read from current Frame Pointer, or specified index
            # Usage: .r [blank] or .r [index] or .r [namespace]

            elif line[i] == self.CORE.instructions[3]:
                if line_length > 1:
                    arg = line[i+1]
                    self.CORE.call_READ(arg)

                # No specific read argument was provided, so read the current frame.
                else:
                    value = self.TAPE.FRAMES[self.TAPE.FP]
                    print(value)

            # SEGMENT instruction ( .s )
            # Create a new named segment, or un-named segment.
            # Usage: .s .n [mysegment], or just the ( .s ) command.
 
            elif line[i] == '.s':

                # Increment number of segments counter.
                self.TAPE.NS += 1
                
                if line_length > 1:

                    # Is there a .n name command present?
                    if line[i+1] is '.n':

                        # Peeked ahead of (i) in command, skip ahead on next loop.
                        skip += 1

                        # If there is a name for the segment supplied, append the
                        # {segment name: frame index of segment's first frame}
                        # to  LOOKUP and the name to NAMES
                        
                        if line_length  > 2:
                            
                            # Peek ahead again, skip on next loop.
                            skip += 1

                            name = line[i+2]
                            self.TAPE.NAMES.append(name)
                            self.LOOKUP.append({name:self.TAPE.FP})

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

            elif line[i] == '.n':
                if line_length > 1:
                    tryname = line[i+1]

                    # Is this namespace already defined?
                
                    if try_lookup(tryname, self.TAPE.NAMES):
                        print('ERROR: Cannot assign this name. Already in use')
                
                    # Is the input a valid name?
    
                    if lex_namespace(tryname):
                        self.TAPE.NAMES.append(tryname)
                        self.LOOKUP.append({tryname:self.TAPE.FP})

                else:
                    print('Expected name after ( .n ) is missing')


            elif line[i] == '.d':
                print('Delete')
            elif line[i] == '.m':
                print('Merge')
            elif line[i] == '.c':
                print('Cut')
            elif line[i] == '.p':
                print('Paste')

            # Print tape report on INSPECT command.

            elif line[i] == '.i':
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