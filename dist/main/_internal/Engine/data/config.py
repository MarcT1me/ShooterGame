""" Engine settings and configs
"""
from pygame import DOUBLEBUF
from loguru import logger
# default
import os
from inspect import stack
from collections.abc import Mapping
# engine
from Engine.data.constants import ZERO, EMPTY, NO
from Engine.scripts.app_data import AttributesKeeper


class MainData:
    """ Main engine constants """
    PRE_INIT: bool = True
    IS_RELEASE: bool = False
    SCENE_USE_TB: bool = True
    # string
    APPLICATION_name = "SomeName"
    APPLICATION_version = "SomeVersion"
    ENGINE_name = "Engine"


class Core(AttributesKeeper): pass


Core = AttributesKeeper.__new__(Core, EMPTY)


class Screen(AttributesKeeper):
    """ Screen settings """
    # default
    DEFAULT_WIN_SIZE: tuple[int, int] = 1280, 720
    DEFAULT_WIN_TITLE: str = MainData.APPLICATION_name + ' | node window'
    DEFAULT_WIN_MONITOR: int = EMPTY
    DEFAULT_WIN_VSYNC: bool = ZERO
    DEFAULT_WIN_FLAGS: bool = DOUBLEBUF
    # main window
    size: tuple[int, int] = DEFAULT_WIN_SIZE
    monitor: int = DEFAULT_WIN_MONITOR
    title: str = 'My Engine Game'
    vsync: bool = DEFAULT_WIN_VSYNC
    flags: int = DEFAULT_WIN_FLAGS
    fps: int = ZERO
    full: bool = NO
    game_settings: dict = {}


class File:
    """ File and path data """
    config_name: str = 'config'
    config_ext: str = 'json'
    config_local_dir: bool = True
    
    data: dict[str, dict] = {}
    # paths
    __ENGINE_DATA__: str = os.path.dirname(os.path.abspath(__file__)).removesuffix(r'\PyInstaller\loader')
    APPLICATION_path: str = os.path.dirname(os.path.abspath(stack()[-1].filename)).removesuffix(
        r'\PyInstaller\loader'
    ).removesuffix(
        rf"\{MainData.ENGINE_name}\messages"
    )
    APPDATA_LOCAL_path: str = rf'{os.path.expanduser("~")}\AppData\Local'
    data_path: str = lambda: File.APPLICATION_path if File.config_local_dir else File.APPDATA_LOCAL_path
    # names
    DATA_dir: str = 'ShooterGameData'
    SHADER_dir: str = r'shaders'
    TEXTURE_dir: str = r'textures'
    # ico settings
    APPLICATION_ICO_dir: str = f'{MainData.ENGINE_name}/data'
    APPLICATION_ICO_name: str = 'ico.ico'
    
    @staticmethod
    def change_data(changes: dict | Mapping, *, _data: dict = None) -> data:
        """ Change data in dict dict arg changes """
        for key, value in changes.items():
            File.data[key].update(value)
        return File.data
    
    """ Working with config.* file """
    
    @staticmethod
    def set_default_data(
            set_default_core=lambda: File.data.setdefault('Core', {})
    ):
        _ = File.data.setdefault('Screen', {})
        _ = File.data['Screen'].setdefault('fps', Screen.fps)
        _ = File.data['Screen'].setdefault('size', Screen.size)
        _ = File.data['Screen'].setdefault('vsync', Screen.vsync)
        _ = File.data['Screen'].setdefault('full', Screen.full)
        _ = File.data['Screen'].setdefault('monitor', Screen.monitor)
        
        _ = File.data['Screen'].setdefault('game_settings', Screen.game_settings)
        set_default_core()
    
    @staticmethod
    def _load(_load_function) -> data:
        file_path = rf"{File.data_path()}\{File.DATA_dir}\{File.config_name}.{File.config_ext}"
        try:
            with open(file_path, mode='r') as file:
                logger.debug(f'load from file: {File.config_name}.{File.config_ext}')
                return _load_function(file)
        except FileNotFoundError:
            File.set_default_data()
            # create dir
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            # create file
            if not os.path.exists(file_path):
                f = open(file_path, 'w')
                exec(f"""from {File.config_ext} import dump; dump(File.data, f)""")
                f.close()
            logger.debug(f'file not fount -> create: {File.config_name}.{File.config_ext}')
            return File.data
    
    @staticmethod
    def _dump(_dump_function) -> None:
        with open(rf"{File.data_path()}\{File.DATA_dir}\{File.config_name}.{File.config_ext}", mode='w') as file:
            _dump_function(File.data, file)
        logger.debug(f'dump data in file: {File.config_name}.{File.config_ext}')
    
    @classmethod
    def reed_data(cls) -> None:
        """ Apply data from file onto dict """
        
        if len(File.data) is ZERO:
            exec(f"""from {File.config_ext} import load; File.data = File._load(load)""")
        
        for key, value in File.data.items():
            exec(f"""{key}.update(value)""")
    
    @staticmethod
    def save_data() -> None:
        """ Write CONFIG files """
        
        if len(File.data) is ZERO:
            File.reed_data()
        
        exec(f"""from {File.config_ext} import dump; File._dump(dump)""")
    
    """ Working with *.engconf """
    _set_repl = {
        '<ignore message>': "# ENGDATA_IGNORED\n",
        '<main>':           {
            "def*ENGDATA_IGNORE(*f*)*:*", 'from*Engine.data.config*import*',
            "class MainData*:*", "MainData*:*type*",
            "    *:*str*", "    *:*int*", "    *:*list*", "    *:*float*", "    *:*bool*", '    *:*type*'
        },
        'settings':         {
            "class File*:*", "File*:*type*",
            "class Core*:*", "Core*:*type*",
        },
        'graphic':          {
            "class Screen*:*", "Screen*:*type*",
        },
    }  # references list
    
    @staticmethod
    def load_engine_config(name: str = 'settings') -> None:
        from fnmatch import fnmatch
        # reading
        with open(rf'{File.__ENGINE_DATA__}\{name}.engconf', 'r') as config_file:
            lines_data = config_file.readlines()
        # passing through lines and changing by keys
        for line_index in range(len(lines_data)):
            # if the current line is ignored, quickly skip the line
            if lines_data[line_index] == File._set_repl['<ignore message>']:
                continue
            # if the next line is ignored, mark it as ignored and skip the current line
            elif fnmatch(lines_data[line_index], "*@*ENGDATA_IGNORE*"):
                lines_data[line_index] = File._set_repl['<ignore message>']
                lines_data[line_index + 1] = File._set_repl['<ignore message>']
                continue
            else:
                # in other cases, we first look for a reference in <main>
                for line_reference in File._set_repl['<main>']:
                    if fnmatch(lines_data[line_index], line_reference):
                        lines_data[line_index] = File._set_repl['<ignore message>']
                        break
                else:
                    if name in File._set_repl.keys():
                        # if you haven't found a reference among the main ones and the name is on the list, go through it
                        for line_reference in File._set_repl[name]:
                            if fnmatch(lines_data[line_index], line_reference):
                                lines_data[line_index] = File._set_repl['<ignore message>']
                                break
        data = ''.join(lines_data)
        logger.debug(f'parce {name} eng-config complete')
        exec(data)
