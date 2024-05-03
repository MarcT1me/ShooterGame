""" Engine CONSTANTS
"""
from typing import BinaryIO
class __EngineEmptyClass:
    def __init__(self, val, des: str):
        self.__eq = val
        self.__des = des
    def __str__(self):
        return self.__des[0].upper() + self.__des[1:].lower() + 'Type'
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return self.__eq is other
    def __ne__(self, other):
        return self.__eq is not other
    def __lt__(self, other): return False
    def __le__(self, other): return False
    def __gt__(self, other): return False
    def __ge__(self, other): return False

# types
NULL = __EngineEmptyClass(0, 'NULL')
EMPTY = __EngineEmptyClass(None, 'EMPTY')
BINARY = __EngineEmptyClass(BinaryIO, 'BINARY')
ZERO = 0
INF = 10**9.2
NO = False
YES = True
# flags
VERTEX_SHADER = 2
FRAGMENT_SHADER = 4
GEOMETRY_SHADER = 8
COMPUTE_SHADER = 16
