#!/usr/bin/env python

'''
Holds the target site HTML and audit information, divides and distributes it to
the functions, and reassembles the final site.
'''

import constants


class Orchestrator:
    '''
    The Orchestrator class is the main coordinator of AWE. It is in charge of
    maintaining the true copies of the target page HTML as well as the parsed
    Lighthouse Audit results.

    It manages the segmentation then distribution of these files to the
    concerned accessibility functions.

    Finally, it reassembles function outputs into the accessible version of the
    target site.

    Parameters:

    Attributes:
    '''
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        return self.arg


def main():
    print(constants.AWE_FUNCTIONS[0])


if __name__ == '__main__':
    main()
