from glm import *


def increment_creator():
    value = 0
    while True:
        yield value
        value += 1
        