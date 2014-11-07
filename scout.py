'''
Written by Jay Butera

Allows scouts in the FRC robotics competition to efficiently record
match data using the keyboard instead of navigating through a UI or
spreadsheet with a mouse. Designed for those command line pioneers
with a hatred for mice.

This program assumes a scouting process consisting of a red and blue
flash drive (representing the colored teams respectively). This program
is considered efficient as the drives are passed around just long enough
to let the program write the file to the drive at the end of the match
without having to manually copy the file (eliminating the post processing
step).

When a match is finished, the data is written to a file on the plugged
in flash drive if present, and to a team named file in the same directory
if the specified drive is not present.


_________________________________________________________________________

The MIT License (MIT)

Copyright (c) <year> <copyright holders>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

But secretly I don't really care
_________________________________________________________________________

'''

import os
import collections

class Score(object):
    match = 0
    team = 0
    notes = ''

    # Points data structure contains all point types in 2013 match.
    # This structure should be modified to account for the current competition.
    points = collections.OrderedDict([
            ('AF',0),
            ('AH',0),
            ('AHM',0),
            ('AL',0),
            ('ALM',0),
            ('HF',0),
            ('HFM',0),
            ('HM',0),
            ('HMM',0),
            ('HB',0),
            ('HBM',0),
            ('L',0),
            ('LM',0),
            ('T',0)
    ])

    def allf(self):
        '''
        Returns a composition of all recorded information
        into one list data type.
        '''
        f = [self.match, self.team]
        [f.append(i) for i in self.points.values()]
        f.append(p.notes)
        return f

    def writeFile(self, filepath = ''):
        '''
        Writes the compiled list data type of match information
        to the file.
        '''
        f = open(''.join(filepath + p.team + '.txt'), 'w+')
        f.write('''MATCH # : %s
TEAM #  : %s
AUTO FORWARD DRIVE : %d
AUTO HIGH MADE     : %d
AUTO HIGH MISSED   : %d
AUTO LOW MADE      : %d
AUTO LOW MISSED    : %d
HIGH FRONT MADE    : %d
HIGH FRONT MISSED  : %d
HIGH MID MADE      : %d
HIGH MID MISSED    : %d
HIGH BACK MADE     : %d
HIGH BACK MISSED   : %d
LOW MADE           : %d
LOW MISSED         : %d
TRUSS              : %d
NOTES :  %s''' % tuple(p.allf())
        )
        return f.close()

    def isPluggedIn(self, fpath):
        '''
        Checks if the specified flash drive is currently
        plugged into the computer and mounted for data
        writing.
        '''
        return os.path.exists(fpath)

##################
#                #
#     /) /)      #
#    ( . .)      #
#    c(")(")     #
#                #
#  Le main code  #
##################

s = '' # Contains user command
#Important that ending "/" exists

# Blue flash drive filepath (modify to appropriate name)
blue_path = '/Volumes/BLU TEAM/'
# Red flash drive filepath (modify to appropriate name)
red_path = '/Volumes/RED TEAM/'

# Initialize the record object to store recorded data
p = Score()

# Acquire user specified information on match number and team name
p.match = raw_input('> [MATCH]: ')
p.team = raw_input('> [TEAM]: ')

print '     COMMANDS: ' + ' '.join(p.points.keys())

while s != 'exit':
    s = raw_input('> ')

    if s in p.points.keys():
        p.points[s] += 1

    # Decrement preprend command
    elif s[0] == '-' and s[1:] in p.points.keys():
        p.points[s[1:]] -= 1

    # Exit without saving command
    elif s == 'exit':
        break

    # Exit and write file command
    elif s == 'done':
        # Print the recorded information for confirmation
        print p.allf()[:-1]
        p.notes = raw_input('> [NOTES]: ')

        # First check for the blue flash drive, then red
        if p.isPluggedIn(blue_path):
            p.writeFile(blue_path)
            print 'Saved to BLU TEAM'
        elif p.isPluggedIn(red_path):
            p.writeFile(red_path)
            print 'Saved to RED TEAM'
        # If neither exist, write to current directory
        else:
            p.writeFile()
        break

    # Print a list of the commands and program user information command
    elif s == 'help':
        print '''
                            -----PyScout-----


    - AUTONOMOUS MODE COMMANDS
AF ..... Auto forward drive
AH ..... Auto high goal
AL ..... Auto low goal

    - DRIVER CONTROL MODE COMMANDS
HF ..... High goal front
HM ..... High goal middle
HB ..... High goal back


    TIPS
- Append the letter 'M' to a command to indicate a missed shot.

- Prepend the character '-' to a command to subtract a point in the given
  field.

- Type 'done' to save a file after recording is finished.

- Type 'exit' to quit the session without saving.
  '''

    # Overwrite team name command
    elif s.split()[0] == 'TEAM':
        p.team = s.split()[1]

    # Overwrite match name command
    elif s.split()[0] == 'MATCH':
        p.match = s.split()[1]

    # Invalid command
    else:
        print 'Invalid command'
