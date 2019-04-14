import os


def makefileifneed(filename):

    if filename not in os.listdir('.'):
        return open(filename, 'w+')

    return open(filename, 'r+')
