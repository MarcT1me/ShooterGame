""" Engine time counter
Total time management file for all engine functions
uses the time module

DESCRIPTION OF VARIABLES
delta - Время между 2-мя итерациями цикла App
start - Временная отметка с запуска программы (import)

global_time - Список счётчиков
 """
from pygame.time import Clock as pg_Clock
from pygame.time import get_ticks as pg_get_ticks
from pygame.time import wait as pg_wait
from pygame.event import Event, post
from numpy import uint8
# standard
from time import time as uix_time
# Engine
from Engine.scripts.app_data import AttributesKeeper, DoubleArray
from Engine.data.constants import EMPTY


class clock:
    def __init__(self):
        self.__pg_cl = pg_Clock()
        
        self.start: float = uix_time()
        self.delta: float = 0
        
        self.roster = AttributesKeeper(default=0)
    
    def get_fps(self) -> float:
        return self.__pg_cl.get_fps()
    
    def get_time(self) -> int:
        return self.__pg_cl.get_time()

    @staticmethod
    def wait(*args, **kwargs):
        pg_wait(*args, **kwargs)
    
    @staticmethod
    def get_ticks() -> int:
        return pg_get_ticks()
    
    def tick(self, fps: float):
        self._expectation()
        self.delta = self.__pg_cl.tick(fps)
    
    def timer(self, name: str, cooldown: float) -> None:
        """ A timer is a function that decides whether a time cycle is suitable for performing some kind of action
        tied to waiting for time """
        current_time = uix_time()
        if current_time - self.roster[name] >= cooldown:
            self.roster[name] = current_time
            return True
        return False
    
    __increment = uint8(256)
    
    def _expectation(self):
        current_time = uix_time()
        for name, double in vars(self.roster).items():
            if not name.startswith('__') and name.startswith('wait_'):
                if double.second <= current_time:
                    # redefining basic values
                    double.second = EMPTY
                    double.first.used = True
                    # setting the actual end time
                    double.first.end = current_time
                    post(double.first)  # push event in event list
                
    def stop_expect(self, event: Event):
        try:
            self.roster.__delattr__(event.name)
        except AttributeError:
            event.used = True
    
    def expect(self, event: Event, _seconds: float):
        # find name
        key = f'wait_{self.__increment}'
        # create Event
        event.name = key
        event.used = False
        # calculate time params
        current_time = uix_time()
        end = current_time+_seconds
        # set time params
        event.start = current_time
        event.end = end
        event.delay = _seconds
        # push event data in roster
        self.roster[key] = DoubleArray(first=event, second=end)
        self.__increment  = uint8(self.__increment + 1)
