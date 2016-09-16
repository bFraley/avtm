# tapebox - An abstract virtual tape-based machine.
# Copyright by Brett Fraley 2016
# tape.py

class Tape:
    def __init__(self):
        self.LC = 0                  # Line Counter
        self.IC = 0                  # Instruction Counter
        self.NS = 0                  # Number of Segments
        self.SP = 0                  # Segment Pointer
        self.FP = 0                  # Frame Pointer
        self.SIZE = 0                # Tape Capacity
        self.FRAMES = []             # Frame Values
        self.NAMES = []              # Frame and Segment Names
        self.SCOPE = []              # Frame Scope (frame view range)

    def __str__(self):
   
        tape_report = '\nNumber of Segments: ' +  str(self.NS) + \
           '\nSegment Pointer: ' +  str(self.SP) + \
               '\nFrame Pointer: ' + str(self.FP)
        
        tape_report += '\nNames: '
        for item in self.NAMES:
            tape_report += ' | ' + str(item)

        tape_report += '\nScope: '
        for item in self.SCOPE:
            tape_report += ' | ' + str(item)

        tape_report +=  '\nFrames:'
        for item in self.FRAMES:
            tape_report += ' | ' + str(item)
    
        tape_report += '\n'          
        return tape_report
