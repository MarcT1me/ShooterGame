""" Engine CONSTANTS
"""
class __EngineEmptyClass:
    def __init__(self, val, des: str): self.__eq, self.__des = val, des
    def __str__(self): return self.__des[0].upper() + self.__des[1:].lower() + 'Type'
    def __repr__(self): return self.__str__()
    def __eq__(self, other): return other in {self.__eq, self.__des, self.__str__()}
    def __ne__(self, other): return other not in {self.__eq, self.__des, self.__str__()}
    def __lt__(self, other): return False
    def __le__(self, other): return False
    def __gt__(self, other): return False
    def __ge__(self, other): return False
    
__copy_arr = {
    # configs
    ('', 'graphics.engconf'),
    ('', 'settings.engconf'),
    # images
    ('', 'ico.ico'),
    ('messages', 'debug_err.png'),
    ('messages', 'err_background.png'),
    # shaders
    ('shaders/default', 'main.vert'),
    ('shaders/default', 'main.frag'),
    # docs
    ('../../', '.gitignore'),
    ('../../', 'README.md'),
    ('../../', 'requirements.txt'),
    ('../../', 'LICENSE'),
    ('../../', 'main.pyw'),
}
_set_repl = {
    '<ignore message>': "# ENGDATA_IGNORED\n",
    '<main>': {
        "def*ENGDATA_IGNORE(*f*)*:*", 'from*Engine.data.config*import*',
        "class MainData*:*", "MainData*:*type*",
        "    *:*str*", "    *:*int*", "    *:*list*", "    *:*float*", "    *:*bool*", '    *:*type*'
    },
    'settings': {
        "class File*:*", "File*:*type*",
        "class Core*:*", "Core*:*type*",
    },
    'graphic': {
        "class Screen*:*", "Screen*:*type*",
    },
}

# types
EMPTY = __EngineEmptyClass(None, 'EMPTY')
NULL = __EngineEmptyClass(0, 'NULL')
SUCCESS = __EngineEmptyClass(2, 'SUCCESS')
ZERO = 0
INF = 10 ** 9.2
NO = False
YES = True
# flags
VERTEX_SHADER = 2
FRAGMENT_SHADER = 4
GEOMETRY_SHADER = 8
COMPUTE_SHADER = 16
