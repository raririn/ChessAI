import chess
import time
from random import choice as randChoice
from random import random as rand
from operator import attrgetter
from operator import methodcaller
import matplotlib.pyplot as plt
from evaluation import *

def whichPlayer(x):
    if x:
        return 'White'
    else:
        return 'Black'