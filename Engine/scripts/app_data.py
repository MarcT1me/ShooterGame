""" App data classes
"""
# default
from dataclasses import dataclass, field
from copy import deepcopy
# engine
import Engine


@dataclass(init=True)
class WinData:
    """ data for every engine window """
    # size
    size: tuple[int, int] = field(init=True, default_factory=lambda: Engine.config.Screen.DEFAULT_WIN_SIZE[0])
    # other window variables
    monitor: int | None = field(init=True, default_factory=lambda: Engine.config.Screen.DEFAULT_WIN_MONITOR)
    title: str = field(init=True, default_factory=lambda: Engine.config.Screen.DEFAULT_WIN_TITLE)
    opacity: float = field(init=True, default_factory=lambda: 1.0)
    vsync: bool = field(init=True, default_factory=lambda: Engine.config.Screen.DEFAULT_WIN_VSYNC)
    flags: int = field(init=True, default_factory=lambda: Engine.config.Screen.DEFAULT_WIN_FLAGS)
    """ constant variables """
    # position
    posX: int | None = field(init=True, default_factory=lambda: None)   # CONSTANTS
    posY: int | None = field(init=True, default_factory=lambda: None)   # CONSTANTS
    # OpenGL configs
    view_x: int = field(init=True, default_factory=lambda: 0)           # CONSTANTS
    view_y: int = field(init=True, default_factory=lambda: 0)           # CONSTANTS
    near: float = field(init=True, default_factory=lambda: 0.01)        # CONSTANTS
    fara: float = field(init=True, default_factory=lambda: 300.0)       # CONSTANTS
    
    def extern(self, changes: dict):
        """ extern ths win_data and return new """
        new_data = deepcopy(self)
        for var, value in changes.items():
            var = var.split('/')[-1]  # getting a name in the patch
            if var not in 'posX,posy,view_x,view_y,near,fara':  # exclude constants
                exec(f"""new_data.{var}, Engine.config.Screen.{var} = value, value""")  # applying changes to the name
        return new_data  # return new data


class AttributesKeeper:
    """ A class that should store attributes and replace the dictionary """
    
    def __new__(cls, default=Engine.EMPTY):
        instance = super().__new__(cls)
        instance._default = default
        return instance
    
    def __getitem__(self, item):
        exec(f'self._res = self.{item}')
        return self._res
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
    
    def __getattr__(self, item):
        setattr(self, item, self._default)
        return self._default
    
    @classmethod
    def update(cls, changes: dict) -> None:
        for key, value in changes.items():
            exec(f'cls.{key} = value')


class SafetyDict(dict):
    """  """
    
    def __init__(self, default=Engine.EMPTY, default_key=Engine.ZERO):
        self._default = default
        self._default_key = default_key
        super().__init__()
    
    def __repr__(self):
        return f'<NamedArray: default={self._default}, default_key={self._default_key}> \t{super().__repr__()}'
    
    def __getattr__(self, item):
        try:
            return self[self._default_key]
        except KeyError:
            self[item] = self._default
            return self._default


class DoubleArray:
    def __init__(self, first=Engine.EMPTY, second=Engine.EMPTY):
        self.first, self.second = first, second
    
    def __repr__(self):
        return f'<first={self.first}, second={self.second}>'
    
    def get(self):
        return self.first, self.second
    
    def clear(self, default=Engine.EMPTY):
        self.first, self.second = default, default
    
    def pop(self):
        if self.second is not None:
            r = self.second
            self.second = Engine.EMPTY
        else:
            r = self.first
            self.first = Engine.EMPTY
        return r
